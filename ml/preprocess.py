"""Shared preprocessing for training and inference."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd

from feature_config import CATEGORICAL_FEATURES, FEATURE_COLUMNS, NUMERIC_FEATURES


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive age/employment years and ratio features from raw application fields."""
    out = df.copy()

    if "AGE_YEARS" not in out.columns:
        if "DAYS_BIRTH" in out.columns:
            out["AGE_YEARS"] = (-out["DAYS_BIRTH"] / 365.25).clip(lower=18, upper=100)
        else:
            out["AGE_YEARS"] = out.get("age_years", 35)

    if "EMPLOYMENT_YEARS" not in out.columns:
        if "DAYS_EMPLOYED" in out.columns:
            days = out["DAYS_EMPLOYED"].replace(365243, np.nan)
            out["EMPLOYMENT_YEARS"] = (-days / 365.25).clip(lower=0, upper=60)
        else:
            out["EMPLOYMENT_YEARS"] = out.get("employment_years", 0)

    income = out["AMT_INCOME_TOTAL"].replace(0, np.nan)
    out["CREDIT_INCOME_RATIO"] = out["AMT_CREDIT"] / income
    out["ANNUITY_INCOME_RATIO"] = out["AMT_ANNUITY"] / income
    goods = out["AMT_GOODS_PRICE"].replace(0, np.nan)
    out["CREDIT_GOODS_RATIO"] = out["AMT_CREDIT"] / goods

    # If no car, car age should be missing
    if "FLAG_OWN_CAR" in out.columns:
        out.loc[out["FLAG_OWN_CAR"] == "N", "OWN_CAR_AGE"] = np.nan

    for col in CATEGORICAL_FEATURES:
        if col in out.columns:
            out[col] = out[col].astype("string").fillna("Missing").astype(str)

    return out


def build_training_frame(raw: pd.DataFrame) -> pd.DataFrame:
    engineered = engineer_features(raw)
    return engineered[["TARGET"] + FEATURE_COLUMNS].copy()


class FeaturePreprocessor:
    """Median impute numerics + categorical codes for LightGBM."""

    def __init__(self) -> None:
        self.numeric_medians: dict[str, float] = {}
        self.category_maps: dict[str, dict[str, int]] = {}
        self.feature_columns = list(FEATURE_COLUMNS)

    def fit(self, df: pd.DataFrame) -> FeaturePreprocessor:
        for col in NUMERIC_FEATURES:
            median = float(pd.to_numeric(df[col], errors="coerce").median())
            if np.isnan(median):
                median = 0.0
            self.numeric_medians[col] = median

        for col in CATEGORICAL_FEATURES:
            values = sorted(df[col].astype(str).fillna("Missing").unique().tolist())
            if "Missing" not in values:
                values.append("Missing")
            self.category_maps[col] = {v: i for i, v in enumerate(values)}
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        out = pd.DataFrame(index=df.index)
        for col in NUMERIC_FEATURES:
            series = pd.to_numeric(df[col], errors="coerce")
            out[col] = series.fillna(self.numeric_medians[col])

        for col in CATEGORICAL_FEATURES:
            mapping = self.category_maps[col]
            unknown = mapping.get("Missing", 0)
            out[col] = (
                df[col]
                .astype(str)
                .fillna("Missing")
                .map(mapping)
                .fillna(unknown)
                .astype(int)
            )
        return out[self.feature_columns]

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return self.fit(df).transform(df)

    def to_dict(self) -> dict[str, Any]:
        return {
            "numeric_medians": self.numeric_medians,
            "category_maps": self.category_maps,
            "feature_columns": self.feature_columns,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FeaturePreprocessor:
        obj = cls()
        obj.numeric_medians = data["numeric_medians"]
        obj.category_maps = data["category_maps"]
        obj.feature_columns = data["feature_columns"]
        return obj


def application_dict_to_frame(payload: dict[str, Any]) -> pd.DataFrame:
    """Convert API / form payload into a one-row raw DataFrame."""
    age_years = float(payload["age_years"])
    employment_years = float(payload["employment_years"])
    row = {
        "NAME_CONTRACT_TYPE": payload["name_contract_type"],
        "CODE_GENDER": payload["code_gender"],
        "FLAG_OWN_CAR": payload["flag_own_car"],
        "FLAG_OWN_REALTY": payload["flag_own_realty"],
        "CNT_CHILDREN": payload["cnt_children"],
        "AMT_INCOME_TOTAL": payload["amt_income_total"],
        "AMT_CREDIT": payload["amt_credit"],
        "AMT_ANNUITY": payload["amt_annuity"],
        "AMT_GOODS_PRICE": payload.get("amt_goods_price") or payload["amt_credit"],
        "NAME_TYPE_SUITE": payload.get("name_type_suite") or "Unaccompanied",
        "NAME_INCOME_TYPE": payload["name_income_type"],
        "NAME_EDUCATION_TYPE": payload["name_education_type"],
        "NAME_FAMILY_STATUS": payload["name_family_status"],
        "NAME_HOUSING_TYPE": payload["name_housing_type"],
        "DAYS_BIRTH": int(-round(age_years * 365.25)),
        "DAYS_EMPLOYED": int(-round(employment_years * 365.25))
        if employment_years > 0
        else 365243,
        "OWN_CAR_AGE": payload.get("own_car_age"),
        "OCCUPATION_TYPE": payload.get("occupation_type") or "Missing",
        "CNT_FAM_MEMBERS": payload["cnt_fam_members"],
        "ORGANIZATION_TYPE": payload["organization_type"],
        "REGION_RATING_CLIENT": payload["region_rating_client"],
        "FLAG_EMAIL": int(payload["flag_email"]),
        "FLAG_PHONE": int(payload["flag_phone"]),
        "FLAG_WORK_PHONE": int(payload["flag_work_phone"]),
        "WEEKDAY_APPR_PROCESS_START": payload.get("weekday_appr_process_start")
        or "MONDAY",
        "AGE_YEARS": age_years,
        "EMPLOYMENT_YEARS": employment_years,
    }
    return engineer_features(pd.DataFrame([row]))
