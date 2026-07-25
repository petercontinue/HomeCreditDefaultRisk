"""Train LightGBM default-risk model and export artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import lightgbm as lgb
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from feature_config import (  # noqa: E402
    CATEGORICAL_FEATURES,
    DEFAULT_APPROVAL_THRESHOLD,
    MODEL_VERSION,
    RAW_COLUMNS,
)
from preprocess import FeaturePreprocessor, build_training_frame  # noqa: E402

DATASET = ROOT / "dataset" / "application_train.csv"
ARTIFACTS = Path(__file__).resolve().parent / "artifacts"


def pick_threshold(y_true: np.ndarray, y_prob: np.ndarray) -> dict:
    """Pick approval threshold targeting ~70% pass rate on validation."""
    target_approval_rate = 0.70
    thr = float(np.quantile(y_prob, target_approval_rate))
    thr = float(np.clip(thr, 0.05, 0.25))
    approved = y_prob < thr
    # Among rejected applicants, what share are actual defaults (precision of reject)
    rejected = ~approved
    reject_precision = (
        float(y_true[rejected].mean()) if rejected.any() else 0.0
    )
    # Among actual defaults, what share are rejected (recall of reject)
    reject_recall = (
        float(((y_true == 1) & rejected).sum() / max(1, (y_true == 1).sum()))
    )
    return {
        "threshold": thr,
        "target_approval_rate": target_approval_rate,
        "actual_approval_rate": float(approved.mean()),
        "reject_default_rate": reject_precision,
        "default_catch_rate": reject_recall,
        "fallback_threshold": DEFAULT_APPROVAL_THRESHOLD,
    }


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    print(f"Loading {DATASET} ...")
    raw = pd.read_csv(DATASET, usecols=RAW_COLUMNS)
    # Drop invalid gender codes from training
    raw = raw[raw["CODE_GENDER"].isin(["F", "M"])].copy()

    frame = build_training_frame(raw)
    y = frame["TARGET"].astype(int).values
    X_raw = frame.drop(columns=["TARGET"])

    X_train_raw, X_valid_raw, y_train, y_valid = train_test_split(
        X_raw,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    preprocessor = FeaturePreprocessor()
    X_train = preprocessor.fit_transform(X_train_raw)
    X_valid = preprocessor.transform(X_valid_raw)

    cat_indices = [X_train.columns.get_loc(c) for c in CATEGORICAL_FEATURES]

    train_set = lgb.Dataset(
        X_train,
        label=y_train,
        categorical_feature=cat_indices,
        free_raw_data=False,
    )
    valid_set = lgb.Dataset(
        X_valid,
        label=y_valid,
        reference=train_set,
        categorical_feature=cat_indices,
        free_raw_data=False,
    )

    params = {
        "objective": "binary",
        "metric": "auc",
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 48,
        "max_depth": 7,
        "min_child_samples": 80,
        "feature_fraction": 0.8,
        "bagging_fraction": 0.8,
        "bagging_freq": 1,
        "lambda_l1": 0.1,
        "lambda_l2": 0.1,
        # Keep probabilities closer to real default rates for product thresholds.
        "scale_pos_weight": float((y_train == 0).sum() / max(1, (y_train == 1).sum()) * 0.35),
        "verbosity": -1,
        "seed": 42,
    }

    print("Training LightGBM ...")
    model = lgb.train(
        params,
        train_set,
        num_boost_round=800,
        valid_sets=[train_set, valid_set],
        valid_names=["train", "valid"],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=50),
        ],
    )

    valid_prob = model.predict(X_valid, num_iteration=model.best_iteration)
    train_prob = model.predict(X_train, num_iteration=model.best_iteration)
    valid_auc = float(roc_auc_score(y_valid, valid_prob))
    train_auc = float(roc_auc_score(y_train, train_prob))
    threshold_info = pick_threshold(y_valid, valid_prob)

    # Approval uses low default probability; threshold is on P(default)
    approval_threshold = float(threshold_info["threshold"])

    metrics = {
        "model_version": MODEL_VERSION,
        "train_rows": int(len(X_train)),
        "valid_rows": int(len(X_valid)),
        "train_auc": train_auc,
        "valid_auc": valid_auc,
        "best_iteration": int(model.best_iteration or 0),
        "approval_threshold": approval_threshold,
        "threshold_tuning": threshold_info,
        "positive_rate": float(y.mean()),
    }

    model_path = ARTIFACTS / "model.txt"
    prep_path = ARTIFACTS / "preprocessor.joblib"
    metrics_path = ARTIFACTS / "metrics.json"
    meta_path = ARTIFACTS / "feature_meta.json"

    model.save_model(str(model_path))
    joblib.dump(preprocessor, prep_path)

    low_cut = round(approval_threshold * 0.45, 4)
    feature_meta = {
        "model_version": MODEL_VERSION,
        "feature_columns": preprocessor.feature_columns,
        "categorical_features": CATEGORICAL_FEATURES,
        "approval_threshold": approval_threshold,
        "risk_levels": {
            "Low": [0.0, low_cut],
            "Medium": [low_cut, approval_threshold],
            "High": [approval_threshold, 1.01],
        },
    }

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    meta_path.write_text(json.dumps(feature_meta, indent=2), encoding="utf-8")

    print(json.dumps(metrics, indent=2))
    print(f"Saved artifacts to {ARTIFACTS}")


if __name__ == "__main__":
    main()
