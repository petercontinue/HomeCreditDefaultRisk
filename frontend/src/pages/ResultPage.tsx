import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { fetchPrediction, type PredictionResult } from "../api/client";
import { useI18n } from "../i18n/I18nProvider";

export function ResultPage() {
  const { id } = useParams();
  const { t, locale, formatMoney, formatDateTime } = useI18n();
  const [data, setData] = useState<PredictionResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const cached = sessionStorage.getItem("lastPrediction");
    if (cached) {
      try {
        const parsed = JSON.parse(cached) as PredictionResult;
        if (parsed.application_id === id) {
          setData(parsed);
          return;
        }
      } catch {
        /* ignore */
      }
    }
    if (!id) return;
    fetchPrediction(id, locale)
      .then(setData)
      .catch((err: Error) => setError(err.message));
  }, [id, locale]);

  if (error) {
    return (
      <main className="page">
        <p className="form-error">{error}</p>
        <Link to="/apply" className="btn btn-primary">
          {t.result.reassess}
        </Link>
      </main>
    );
  }

  if (!data) {
    return (
      <main className="page">
        <p className="muted">{t.result.loading}</p>
      </main>
    );
  }

  const pct = Math.min(100, Math.round(data.default_probability * 1000) / 10);
  const createdAt = formatDateTime(data.created_at);

  return (
    <main className="page result-page">
      <header className="page-header">
        <p className="brand-sm">{t.brand}</p>
        <h1>{t.result.title}</h1>
      </header>

      <section className={`verdict ${data.approved ? "pass" : "fail"}`}>
        <p className="verdict-label">
          {data.approved ? t.result.approve : t.result.decline}
        </p>
        <p className="verdict-summary">{data.feedback.summary}</p>
        <div className="metrics">
          <div>
            <span className="metric-label">{t.result.riskLevel}</span>
            <strong>{data.risk_level}</strong>
          </div>
          <div>
            <span className="metric-label">{t.result.defaultProb}</span>
            <strong>{pct}%</strong>
          </div>
          <div>
            <span className="metric-label">{t.result.requestedAmount}</span>
            <strong>{formatMoney(data.requested_amount)}</strong>
          </div>
          <div>
            <span className="metric-label">{t.result.maxAmount}</span>
            <strong>{data.approved ? formatMoney(data.max_approved_amount) : "—"}</strong>
          </div>
        </div>
        <div className="risk-bar" aria-hidden>
          <div className="risk-bar-fill" style={{ width: `${Math.min(100, pct * 2)}%` }} />
        </div>
      </section>

      <section className="feedback-grid">
        <div>
          <h2>{t.result.positives}</h2>
          <ul>
            {data.feedback.positives.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div>
          <h2>{t.result.concerns}</h2>
          <ul>
            {data.feedback.concerns.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
        <div className="full">
          <h2>{t.result.suggestions}</h2>
          <ul>
            {data.feedback.suggestions.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </section>

      <p className="muted meta-line">
        {t.result.applicationId}: {data.application_id} · {t.result.model} {data.model_version}
        {createdAt ? ` · ${createdAt}` : ""}
      </p>

      <div className="cta-row">
        <Link className="btn btn-primary" to="/apply">
          {t.result.assessAgain}
        </Link>
        <Link className="btn btn-ghost" to="/">
          {t.result.backHome}
        </Link>
      </div>
    </main>
  );
}
