from __future__ import annotations

from typing import Any

from app.i18n.messages import t


def build_feedback(
    payload: dict[str, Any],
    *,
    approved: bool,
    default_probability: float,
    risk_level: str,
    max_approved_amount: float | None,
    lang: str = "en",
) -> dict[str, Any]:
    income = float(payload["amt_income_total"])
    credit = float(payload["amt_credit"])
    annuity = float(payload["amt_annuity"])
    age = float(payload["age_years"])
    emp = float(payload["employment_years"])
    credit_income = credit / income if income else 999
    annuity_income = annuity / income if income else 999

    positives: list[str] = []
    concerns: list[str] = []
    suggestions: list[str] = []

    if credit_income <= 3.5:
        positives.append(t("credit_ok", lang))
    elif credit_income <= 5.5:
        concerns.append(t("credit_high", lang))
    else:
        concerns.append(t("credit_very_high", lang))

    if annuity_income <= 0.25:
        positives.append(t("annuity_ok", lang))
    elif annuity_income <= 0.4:
        concerns.append(t("annuity_high", lang))
    else:
        concerns.append(t("annuity_very_high", lang))

    if emp >= 3:
        positives.append(t("emp_stable", lang))
    elif emp >= 1:
        concerns.append(t("emp_short", lang))
    else:
        concerns.append(t("emp_weak", lang))

    if payload.get("flag_own_realty") == "Y":
        positives.append(t("own_realty", lang))
    if payload.get("flag_own_car") == "Y":
        positives.append(t("own_car", lang))

    edu = payload.get("name_education_type", "")
    if "Higher" in edu or "Academic" in edu:
        positives.append(t("edu_strong", lang))

    if age < 23:
        concerns.append(t("age_young", lang))
    elif age > 60:
        concerns.append(t("age_old", lang))
    else:
        positives.append(t("age_ok", lang))

    income_type = payload.get("name_income_type", "")
    if income_type in {"Unemployed", "Maternity leave", "Student"}:
        concerns.append(t("income_unstable", lang, income_type=income_type))
    elif income_type in {"Working", "Commercial associate", "State servant"}:
        positives.append(t("income_stable", lang))

    if credit_income > 4:
        suggestions.append(t("sug_lower_amount", lang))
    if annuity_income > 0.3:
        suggestions.append(t("sug_longer_term", lang))
    if emp < 2:
        suggestions.append(t("sug_employment", lang))
    if payload.get("flag_own_realty") != "Y" and payload.get("flag_own_car") != "Y":
        suggestions.append(t("sug_assets", lang))
    if not suggestions:
        suggestions.append(t("sug_keep", lang))

    positives = positives[:4] or [t("default_positive", lang)]
    concerns = concerns[:4] or [t("default_concern", lang)]
    suggestions = suggestions[:4]

    prob = f"{default_probability:.1%}"
    if approved:
        summary = t(
            "summary_approved",
            lang,
            risk_level=risk_level,
            prob=prob,
        )
        if max_approved_amount is not None:
            summary += t(
                "summary_amount",
                lang,
                amount=f"{max_approved_amount:,.0f}",
            )
    else:
        summary = t(
            "summary_declined",
            lang,
            risk_level=risk_level,
            prob=prob,
        )

    return {
        "summary": summary,
        "positives": positives,
        "concerns": concerns,
        "suggestions": suggestions,
    }
