import { Link } from "react-router-dom";
import { useI18n } from "../i18n/I18nProvider";

export function HomePage() {
  const { t } = useI18n();

  return (
    <main className="page home-page">
      <section className="hero-panel">
        <p className="brand">{t.brand}</p>
        <h1>{t.home.title}</h1>
        <p className="lede">{t.home.lede}</p>
        <div className="cta-row">
          <Link className="btn btn-primary" to="/apply">
            {t.home.start}
          </Link>
          <a className="btn btn-ghost" href="#how">
            {t.home.how}
          </a>
          <Link className="btn btn-ghost" to="/privacy">
            {t.privacy.navLink}
          </Link>
        </div>
        <p className="disclaimer">{t.home.disclaimer}</p>
      </section>

      <section id="how" className="how-section">
        <h2>{t.home.stepsTitle}</h2>
        <ol className="steps">
          <li>
            <strong>{t.home.step1Title}</strong>
            <span>{t.home.step1Desc}</span>
          </li>
          <li>
            <strong>{t.home.step2Title}</strong>
            <span>{t.home.step2Desc}</span>
          </li>
          <li>
            <strong>{t.home.step3Title}</strong>
            <span>{t.home.step3Desc}</span>
          </li>
        </ol>
      </section>
    </main>
  );
}
