import { Link } from "react-router-dom";
import { useI18n } from "../i18n/I18nProvider";
import { LanguageSwitcher } from "./LanguageSwitcher";

export function AppHeader() {
  const { t } = useI18n();

  return (
    <header className="app-header">
      <div className="app-header-left">
        <Link to="/" className="app-header-brand">
          {t.brand}
        </Link>
        <Link to="/privacy" className="app-header-link">
          {t.privacy.navLink}
        </Link>
      </div>
      <LanguageSwitcher />
    </header>
  );
}
