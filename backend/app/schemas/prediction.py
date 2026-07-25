from __future__ import annotations

from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.i18n.messages import normalize_lang, t


class ApplicationInput(BaseModel):
    name_contract_type: Literal["Cash loans", "Revolving loans"]
    code_gender: Literal["F", "M"]
    flag_own_car: Literal["N", "Y"]
    flag_own_realty: Literal["N", "Y"]
    cnt_children: int = Field(ge=0, le=20)
    amt_income_total: float = Field(gt=0, le=10_000_000)
    amt_credit: float = Field(gt=0, le=20_000_000)
    amt_annuity: float = Field(gt=0, le=5_000_000)
    amt_goods_price: float | None = Field(default=None, gt=0, le=20_000_000)
    name_type_suite: str = "Unaccompanied"
    name_income_type: str
    name_education_type: str
    name_family_status: str
    name_housing_type: str
    age_years: float = Field(ge=18, le=100)
    employment_years: float = Field(ge=0, le=60)
    own_car_age: float | None = Field(default=None, ge=0, le=80)
    occupation_type: str | None = None
    cnt_fam_members: float = Field(ge=1, le=30)
    organization_type: str
    region_rating_client: int = Field(ge=1, le=3)
    flag_email: bool = False
    flag_phone: bool = False
    flag_work_phone: bool = False
    weekday_appr_process_start: str | None = None
    lang: str = "en"

    @model_validator(mode="after")
    def validate_relationships(self) -> ApplicationInput:
        self.lang = normalize_lang(self.lang)
        lang = self.lang
        if self.cnt_fam_members < self.cnt_children + 1:
            raise ValueError(t("err_family_members", lang))
        if self.flag_own_car == "Y" and self.own_car_age is None:
            self.own_car_age = 5.0
        if self.flag_own_car == "N":
            self.own_car_age = None
        if self.amt_goods_price is None:
            self.amt_goods_price = self.amt_credit
        if self.employment_years > self.age_years - 15:
            raise ValueError(t("err_employment_age", lang))
        return self


class FeedbackOut(BaseModel):
    summary: str
    positives: list[str]
    concerns: list[str]
    suggestions: list[str]


class PredictionOut(BaseModel):
    application_id: UUID
    approved: bool
    default_probability: float
    risk_level: str
    requested_amount: float
    max_approved_amount: float | None
    feedback: FeedbackOut
    model_version: str
    created_at: datetime | None = None


class FormOptionsOut(BaseModel):
    options: dict[str, list]
    model_version: str
    approval_threshold: float
