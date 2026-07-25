from __future__ import annotations

from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.i18n.messages import normalize_lang, t
from app.models.loan_application import LoanApplication
from app.schemas.prediction import (
    ApplicationInput,
    FeedbackOut,
    FormOptionsOut,
    PredictionOut,
)
from app.services.decision import evaluate_application
from app.services.feedback import build_feedback
from app.services.ml_runtime import ml_runtime

router = APIRouter(prefix="/api")


def resolve_lang(
    body_lang: str | None = None,
    x_lang: str | None = None,
    accept_language: str | None = None,
) -> str:
    if body_lang:
        return normalize_lang(body_lang)
    if x_lang:
        return normalize_lang(x_lang)
    if accept_language:
        primary = accept_language.split(",")[0].strip()
        return normalize_lang(primary)
    return "en"


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/meta/form-options", response_model=FormOptionsOut)
def form_options() -> FormOptionsOut:
    ml_runtime.ensure_loaded()
    return FormOptionsOut(
        options=ml_runtime.form_options,
        model_version=ml_runtime.model_version,
        approval_threshold=ml_runtime.approval_threshold,
    )


@router.get("/meta/languages")
def languages() -> dict:
    return {
        "languages": [
            {"code": "en", "label": "English"},
            {"code": "zh-CN", "label": "简体中文"},
            {"code": "zh-TW", "label": "繁體中文"},
            {"code": "ja", "label": "日本語"},
            {"code": "ko", "label": "한국어"},
        ]
    }


@router.post("/predict", response_model=PredictionOut)
def predict(
    body: ApplicationInput,
    request: Request,
    db: Session = Depends(get_db),
    x_lang: str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
) -> PredictionOut:
    ml_runtime.ensure_loaded()
    lang = resolve_lang(body.lang, x_lang, accept_language)
    payload = body.model_dump()
    payload.pop("lang", None)

    result = evaluate_application(payload)
    feedback = build_feedback(
        payload,
        approved=result["approved"],
        default_probability=result["default_probability"],
        risk_level=result["risk_level"],
        max_approved_amount=result["max_approved_amount"],
        lang=lang,
    )

    row = LoanApplication(
        input_json={**payload, "lang": lang},
        requested_amount=result["requested_amount"],
        default_probability=result["default_probability"],
        approved=result["approved"],
        risk_level=result["risk_level"],
        max_approved_amount=result["max_approved_amount"],
        feedback_json=feedback,
        model_version=result["model_version"],
        client_meta=request.headers.get("user-agent"),
    )
    db.add(row)
    db.commit()
    db.refresh(row)

    return PredictionOut(
        application_id=row.id,
        approved=row.approved,
        default_probability=row.default_probability,
        risk_level=row.risk_level,
        requested_amount=row.requested_amount,
        max_approved_amount=row.max_approved_amount,
        feedback=FeedbackOut(**feedback),
        model_version=row.model_version,
        created_at=row.created_at,
    )


@router.get("/predictions/{application_id}", response_model=PredictionOut)
def get_prediction(
    application_id: UUID,
    db: Session = Depends(get_db),
    x_lang: str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
) -> PredictionOut:
    row = db.get(LoanApplication, application_id)
    if row is None:
        lang = resolve_lang(None, x_lang, accept_language)
        raise HTTPException(status_code=404, detail=t("err_not_found", lang))
    return PredictionOut(
        application_id=row.id,
        approved=row.approved,
        default_probability=row.default_probability,
        risk_level=row.risk_level,
        requested_amount=row.requested_amount,
        max_approved_amount=row.max_approved_amount,
        feedback=FeedbackOut(**row.feedback_json),
        model_version=row.model_version,
        created_at=row.created_at,
    )
