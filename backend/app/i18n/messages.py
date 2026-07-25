from __future__ import annotations

from typing import Any

SUPPORTED_LANGS = ("en", "zh-CN", "zh-TW", "ja", "ko")
DEFAULT_LANG = "en"


def normalize_lang(lang: str | None) -> str:
    if not lang:
        return DEFAULT_LANG
    raw = lang.strip()
    if raw in SUPPORTED_LANGS:
        return raw
    lower = raw.lower()
    if lower.startswith("zh-tw") or lower.startswith("zh-hk"):
        return "zh-TW"
    if lower.startswith("zh"):
        return "zh-CN"
    if lower.startswith("ja"):
        return "ja"
    if lower.startswith("ko"):
        return "ko"
    if lower.startswith("en"):
        return "en"
    return DEFAULT_LANG


MESSAGES: dict[str, dict[str, str]] = {
    "credit_ok": {
        "en": "Requested amount is reasonable relative to income",
        "zh-CN": "申请金额与收入比例较为合理",
        "zh-TW": "申請金額與收入比例較為合理",
        "ja": "希望金額は収入に対して妥当です",
        "ko": "신청 금액이 소득 대비 합리적입니다",
    },
    "credit_high": {
        "en": "Requested amount is somewhat high relative to income",
        "zh-CN": "申请金额相对收入偏高",
        "zh-TW": "申請金額相對收入偏高",
        "ja": "希望金額は収入に対してやや高めです",
        "ko": "신청 금액이 소득 대비 다소 높습니다",
    },
    "credit_very_high": {
        "en": "Requested amount is significantly above income capacity",
        "zh-CN": "申请金额显著高于收入承受能力",
        "zh-TW": "申請金額顯著高於收入承受能力",
        "ja": "希望金額は収入負担能力を大きく超えています",
        "ko": "신청 금액이 소득 감당 수준을 크게 초과합니다",
    },
    "annuity_ok": {
        "en": "Payment burden is within an acceptable range",
        "zh-CN": "月供负担在可接受范围内",
        "zh-TW": "月付負擔在可接受範圍內",
        "ja": "返済負担は許容範囲内です",
        "ko": "상환 부담이 허용 범위 내입니다",
    },
    "annuity_high": {
        "en": "Annuity / payment takes a high share of income",
        "zh-CN": "年金/月供占收入比例偏高",
        "zh-TW": "年金/月付占收入比例偏高",
        "ja": "年賦／返済が収入に占める割合が高めです",
        "ko": "연금/상환액이 소득에서 차지하는 비중이 높습니다",
    },
    "annuity_very_high": {
        "en": "Repayment burden is heavy and may hurt approval odds",
        "zh-CN": "还款负担过重，可能影响审批",
        "zh-TW": "還款負擔過重，可能影響審批",
        "ja": "返済負担が重く、承認に不利になる可能性があります",
        "ko": "상환 부담이 과중하여 승인에 불리할 수 있습니다",
    },
    "emp_stable": {
        "en": "Employment tenure looks relatively stable",
        "zh-CN": "工作年限较为稳定",
        "zh-TW": "工作年限較為穩定",
        "ja": "勤続年数は比較的安定しています",
        "ko": "근속 연수가 비교적 안정적입니다",
    },
    "emp_short": {
        "en": "Employment tenure is relatively short",
        "zh-CN": "工作年限偏短",
        "zh-TW": "工作年限偏短",
        "ja": "勤続年数が短めです",
        "ko": "근속 연수가 다소 짧습니다",
    },
    "emp_weak": {
        "en": "Employment stability is limited",
        "zh-CN": "就业稳定性不足",
        "zh-TW": "就業穩定性不足",
        "ja": "就業の安定性が十分ではありません",
        "ko": "고용 안정성이 부족합니다",
    },
    "own_realty": {
        "en": "Home ownership is a positive asset signal",
        "zh-CN": "拥有房产，资产状况加分",
        "zh-TW": "擁有房產，資產狀況加分",
        "ja": "不動産所有はプラスの資産シグナルです",
        "ko": "부동산 보유는 긍정적 자산 신호입니다",
    },
    "own_car": {
        "en": "Car ownership is a positive asset signal",
        "zh-CN": "拥有车辆，资产状况加分",
        "zh-TW": "擁有車輛，資產狀況加分",
        "ja": "車所有はプラスの資産シグナルです",
        "ko": "차량 보유는 긍정적 자산 신호입니다",
    },
    "edu_strong": {
        "en": "Education background is comparatively strong",
        "zh-CN": "教育背景较好",
        "zh-TW": "教育背景較好",
        "ja": "学歴背景は比較的良好です",
        "ko": "학력 배경이 비교적 우수합니다",
    },
    "age_young": {
        "en": "Applicant is young; credit history may be limited",
        "zh-CN": "年龄偏年轻，信用积累可能不足",
        "zh-TW": "年齡偏年輕，信用累積可能不足",
        "ja": "年齢が若く、信用実績が限られる可能性があります",
        "ko": "연령이 어려 신용 이력이 제한될 수 있습니다",
    },
    "age_old": {
        "en": "Applicant age is higher; loan term fit should be considered",
        "zh-CN": "年龄偏高，需关注还款周期匹配度",
        "zh-TW": "年齡偏高，需關注還款週期匹配度",
        "ja": "年齢が高めのため、返済期間の適合に注意が必要です",
        "ko": "연령이 높아 상환 기간 적합성을 고려해야 합니다",
    },
    "age_ok": {
        "en": "Age falls in a relatively comfortable application range",
        "zh-CN": "年龄处于较稳妥的申请区间",
        "zh-TW": "年齡處於較穩妥的申請區間",
        "ja": "年齢は比較的妥当な申請レンジです",
        "ko": "연령이 비교적 안정적인 신청 구간에 있습니다",
    },
    "income_unstable": {
        "en": "Income type “{income_type}” suggests weaker stability",
        "zh-CN": "收入类型为「{income_type}」，稳定性偏弱",
        "zh-TW": "收入類型為「{income_type}」，穩定性偏弱",
        "ja": "収入タイプ「{income_type}」は安定性が弱めです",
        "ko": "소득 유형 “{income_type}”은 안정성이 약합니다",
    },
    "income_stable": {
        "en": "Income source type looks comparatively stable",
        "zh-CN": "收入来源类型较稳定",
        "zh-TW": "收入來源類型較穩定",
        "ja": "収入源タイプは比較的安定しています",
        "ko": "소득원 유형이 비교적 안정적입니다",
    },
    "sug_lower_amount": {
        "en": "Consider lowering the requested amount or increasing verifiable income",
        "zh-CN": "可适当降低申请金额，或提高可核实收入",
        "zh-TW": "可適當降低申請金額，或提高可核實收入",
        "ja": "希望金額を下げるか、確認可能な収入を増やすことを検討してください",
        "ko": "신청 금액을 낮추거나 검증 가능한 소득을 늘리는 것을 고려하세요",
    },
    "sug_longer_term": {
        "en": "Consider a longer term to reduce payment pressure",
        "zh-CN": "可考虑拉长贷款期限以降低月供压力",
        "zh-TW": "可考慮拉長貸款期限以降低月付壓力",
        "ja": "返済圧力を下げるため、期間延長を検討してください",
        "ko": "상환 부담을 줄이려면 대출 기간 연장을 고려하세요",
    },
    "sug_employment": {
        "en": "Stronger proof of stable employment can improve the assessment",
        "zh-CN": "补充更稳定的在职证明有助于改善评估",
        "zh-TW": "補充更穩定的在職證明有助於改善評估",
        "ja": "安定した在職証明を補うと評価改善につながります",
        "ko": "더 안정적인 재직 증빙이 평가 개선에 도움이 됩니다",
    },
    "sug_assets": {
        "en": "Other liquid assets or a co-applicant may improve approval odds",
        "zh-CN": "如有其他可变现资产或共同申请人，可提升通过概率",
        "zh-TW": "如有其他可變現資產或共同申請人，可提升通過機率",
        "ja": "換金可能な資産や共同申請人があれば承認率が上がる可能性があります",
        "ko": "기타 유동 자산이나 공동 신청인이 있으면 승인 확률이 높아질 수 있습니다",
    },
    "sug_keep": {
        "en": "Keep stable income and prudent debt to maintain a healthy assessment",
        "zh-CN": "保持稳定收入与合理负债，有助于维持良好评估结果",
        "zh-TW": "保持穩定收入與合理負債，有助於維持良好評估結果",
        "ja": "安定収入と健全な負債を維持すると良い評価につながります",
        "ko": "안정적 소득과 합리적 부채를 유지하면 좋은 평가에 도움이 됩니다",
    },
    "default_positive": {
        "en": "Application details are complete; risk assessment finished",
        "zh-CN": "综合资料完整，已完成风险评估",
        "zh-TW": "綜合資料完整，已完成風險評估",
        "ja": "申請情報は揃っており、リスク評価が完了しました",
        "ko": "신청 정보가 완비되어 위험 평가가 완료되었습니다",
    },
    "default_concern": {
        "en": "No major risk flags identified",
        "zh-CN": "未发现突出风险点",
        "zh-TW": "未發現突出風險點",
        "ja": "大きなリスク指標は見つかりませんでした",
        "ko": "두드러진 위험 신호는 확인되지 않았습니다",
    },
    "summary_approved": {
        "en": "Approved (risk level: {risk_level}, default probability about {prob}).",
        "zh-CN": "评估通过（风险等级：{risk_level}，违约概率约 {prob}）。",
        "zh-TW": "評估通過（風險等級：{risk_level}，違約機率約 {prob}）。",
        "ja": "承認（リスク水準：{risk_level}、デフォルト確率 約 {prob}）。",
        "ko": "승인（위험 등급: {risk_level}, 부도 확률 약 {prob}）。",
    },
    "summary_amount": {
        "en": " Suggested maximum loan amount is about {amount}.",
        "zh-CN": "建议最大可贷金额约 {amount}。",
        "zh-TW": "建議最大可貸金額約 {amount}。",
        "ja": " 推奨最大融資額は約 {amount} です。",
        "ko": " 권장 최대 대출 금액은 약 {amount}입니다.",
    },
    "summary_declined": {
        "en": "Declined (risk level: {risk_level}, default probability about {prob}). Adjust the application using the suggestions below and try again.",
        "zh-CN": "评估未通过（风险等级：{risk_level}，违约概率约 {prob}）。建议根据下方提示调整申请条件后重试。",
        "zh-TW": "評估未通過（風險等級：{risk_level}，違約機率約 {prob}）。建議根據下方提示調整申請條件後重試。",
        "ja": "否認（リスク水準：{risk_level}、デフォルト確率 約 {prob}）。以下の提案を参考に条件を調整して再申請してください。",
        "ko": "거절（위험 등급: {risk_level}, 부도 확률 약 {prob}）. 아래 제안을 참고해 조건을 조정한 뒤 다시 시도하세요.",
    },
    "err_family_members": {
        "en": "Family members cannot be fewer than children + 1",
        "zh-CN": "家庭人数不能少于子女数+1",
        "zh-TW": "家庭人數不能少於子女數+1",
        "ja": "家族人数は子供の人数+1より少なくできません",
        "ko": "가족 수는 자녀 수+1보다 적을 수 없습니다",
    },
    "err_employment_age": {
        "en": "Years employed is unreasonable relative to age",
        "zh-CN": "工作年限相对于年龄不合理",
        "zh-TW": "工作年限相對於年齡不合理",
        "ja": "勤続年数が年齢に対して不自然です",
        "ko": "근속 연수가 나이 대비 비합리적입니다",
    },
    "err_not_found": {
        "en": "Application not found",
        "zh-CN": "申请记录不存在",
        "zh-TW": "申請記錄不存在",
        "ja": "申請が見つかりません",
        "ko": "신청을 찾을 수 없습니다",
    },
    "err_consent_required": {
        "en": "You must accept the Privacy Notice before submitting.",
        "zh-CN": "提交前必须勾选同意隐私说明。",
        "zh-TW": "提交前必須勾選同意隱私說明。",
        "ja": "送信前にプライバシー通知への同意が必要です。",
        "ko": "제출 전에 개인정보 안내에 동의해야 합니다.",
    },
    "err_privacy_version": {
        "en": "Privacy Notice version is missing or outdated. Please review the latest notice.",
        "zh-CN": "隐私说明版本缺失或已过期，请阅读最新说明后再提交。",
        "zh-TW": "隱私說明版本缺失或已過期，請閱讀最新說明後再提交。",
        "ja": "プライバシー通知のバージョンが未指定または古いです。最新版を確認してください。",
        "ko": "개인정보 안내 버전이 없거나 오래되었습니다. 최신 안내를 확인하세요.",
    },
}


def t(key: str, lang: str, **kwargs: Any) -> str:
    lang = normalize_lang(lang)
    template = MESSAGES.get(key, {}).get(lang) or MESSAGES.get(key, {}).get(DEFAULT_LANG) or key
    return template.format(**kwargs) if kwargs else template
