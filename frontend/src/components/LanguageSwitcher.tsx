import { LOCALES } from "../i18n/types";
import { useI18n } from "../i18n/I18nProvider";

export function LanguageSwitcher() {
  const { locale, setLocale, t } = useI18n();

  return (
    <div className="lang-switcher" aria-label={t.common.language}>
      <label className="lang-switcher-label" htmlFor="lang-select">
        {t.common.language}
      </label>
      <select
        id="lang-select"
        className="lang-select"
        value={locale}
        onChange={(e) => setLocale(e.target.value as typeof locale)}
      >
        {LOCALES.map((item) => (
          <option key={item.code} value={item.code}>
            {item.label}
          </option>
        ))}
      </select>
    </div>
  );
}
