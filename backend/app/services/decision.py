from __future__ import annotations

from typing import Any

from app.services.ml_runtime import ml_runtime


def find_max_approved_amount(
    payload: dict[str, Any],
    *,
    threshold: float,
    requested_amount: float,
    income: float,
) -> float | None:
    """Binary-search the largest credit amount with P(default) < threshold."""
    hard_cap = min(income * 8.0, 2_000_000.0, requested_amount * 1.5)
    hard_cap = max(hard_cap, min(requested_amount, income * 2.0))
    low = min(20_000.0, hard_cap)
    high = hard_cap

    # Quick reject if even a tiny loan fails
    if ml_runtime.predict_proba(payload, credit_amount=low) >= threshold:
        return None

    best = low
    for _ in range(24):
        mid = (low + high) / 2.0
        proba = ml_runtime.predict_proba(payload, credit_amount=mid)
        if proba < threshold:
            best = mid
            low = mid
        else:
            high = mid

    return round(best / 1000.0) * 1000.0


def evaluate_application(payload: dict[str, Any]) -> dict[str, Any]:
    ml_runtime.ensure_loaded()
    requested = float(payload["amt_credit"])
    income = float(payload["amt_income_total"])
    threshold = ml_runtime.approval_threshold

    default_probability = ml_runtime.predict_proba(payload, credit_amount=requested)
    risk_level = ml_runtime.risk_level(default_probability)
    approved = default_probability < threshold

    max_approved_amount = None
    if approved:
        max_approved_amount = find_max_approved_amount(
            payload,
            threshold=threshold,
            requested_amount=requested,
            income=income,
        )
        if max_approved_amount is None:
            # Extremely rare edge case: requested passes but search fails
            max_approved_amount = round(requested / 1000.0) * 1000.0
        else:
            # Ensure at least the requested amount when approved
            max_approved_amount = max(max_approved_amount, round(requested / 1000.0) * 1000.0)

    return {
        "approved": approved,
        "default_probability": round(default_probability, 6),
        "risk_level": risk_level,
        "requested_amount": requested,
        "max_approved_amount": max_approved_amount,
        "model_version": ml_runtime.model_version,
        "threshold": threshold,
    }
