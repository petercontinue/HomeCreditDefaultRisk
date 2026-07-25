import { Link } from "react-router-dom";
import { useI18n } from "../i18n/I18nProvider";
import { PRIVACY_NOTICE_VERSION } from "../i18n/types";

export function PrivacyPage() {
  const { t } = useI18n();

  return (
    <main className="page privacy-page">
      <header className="page-header">
        <p className="brand-sm">{t.brand}</p>
        <h1>{t.privacy.title}</h1>
        <p className="muted">
          {t.privacy.lastUpdated} · {t.privacy.versionLabel} {PRIVACY_NOTICE_VERSION}
        </p>
      </header>

      <article className="privacy-article">
        <p className="privacy-intro">{t.privacy.intro}</p>
        {t.privacy.sections.map((section) => (
          <section key={section.heading} className="privacy-section">
            <h2>{section.heading}</h2>
            <p>{section.body}</p>
          </section>
        ))}
      </article>

      <div className="cta-row">
        <Link className="btn btn-primary" to="/apply">
          {t.home.start}
        </Link>
        <Link className="btn btn-ghost" to="/">
          {t.privacy.back}
        </Link>
      </div>
    </main>
  );
}
