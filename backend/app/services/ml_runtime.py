from __future__ import annotations

import json
import sys
from typing import Any

import joblib
import lightgbm as lgb

from app.config import PROJECT_ROOT, get_settings

ML_DIR = PROJECT_ROOT / "ml"
if str(ML_DIR) not in sys.path:
    sys.path.insert(0, str(ML_DIR))

from feature_config import FORM_OPTIONS, MODEL_VERSION  # noqa: E402
from preprocess import FeaturePreprocessor, application_dict_to_frame  # noqa: E402


class MLRuntime:
    def __init__(self) -> None:
        self.model: lgb.Booster | None = None
        self.preprocessor: FeaturePreprocessor | None = None
        self.approval_threshold: float = 0.15
        self.model_version: str = MODEL_VERSION
        self.risk_levels: dict[str, list[float]] = {
            "Low": [0.0, 0.08],
            "Medium": [0.08, 0.15],
            "High": [0.15, 1.01],
        }
        self.form_options = FORM_OPTIONS
        self._loaded = False

    def load(self) -> None:
        settings = get_settings()
        model_dir = settings.model_dir_path
        model_path = model_dir / "model.txt"
        prep_path = model_dir / "preprocessor.joblib"
        meta_path = model_dir / "feature_meta.json"

        if not model_path.exists() or not prep_path.exists():
            raise FileNotFoundError(
                f"Model artifacts not found in {model_dir}. "
                "Run: python ml/train.py"
            )

        self.model = lgb.Booster(model_file=str(model_path))
        self.preprocessor = joblib.load(prep_path)

        if meta_path.exists():
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            self.model_version = meta.get("model_version", MODEL_VERSION)
            self.approval_threshold = float(
                meta.get("approval_threshold", self.approval_threshold)
            )
            self.risk_levels = meta.get("risk_levels", self.risk_levels)

        if settings.approval_threshold is not None:
            self.approval_threshold = float(settings.approval_threshold)

        self._loaded = True

    def ensure_loaded(self) -> None:
        if not self._loaded:
            self.load()

    def predict_proba(self, payload: dict[str, Any], credit_amount: float | None = None) -> float:
        self.ensure_loaded()
        assert self.model is not None and self.preprocessor is not None

        data = dict(payload)
        if credit_amount is not None:
            data["amt_credit"] = credit_amount
            # Keep annuity / credit ratio stable while searching amounts
            base_credit = float(payload["amt_credit"])
            base_annuity = float(payload["amt_annuity"])
            if base_credit > 0:
                data["amt_annuity"] = base_annuity * (credit_amount / base_credit)
            goods = payload.get("amt_goods_price") or base_credit
            data["amt_goods_price"] = float(goods) * (credit_amount / base_credit)

        # Normalize bool flags to 0/1 for preprocessor path
        data["flag_email"] = int(bool(data.get("flag_email")))
        data["flag_phone"] = int(bool(data.get("flag_phone")))
        data["flag_work_phone"] = int(bool(data.get("flag_work_phone")))

        frame = application_dict_to_frame(data)
        features = self.preprocessor.transform(frame)
        proba = float(self.model.predict(features)[0])
        return proba

    def risk_level(self, proba: float) -> str:
        for name, (lo, hi) in self.risk_levels.items():
            if lo <= proba < hi:
                return name
        return "High"


ml_runtime = MLRuntime()
