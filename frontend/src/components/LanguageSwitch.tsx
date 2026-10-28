import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";
import { LANGUAGES, type Language } from "@/i18n";

export function LanguageSwitch() {
  const { i18n } = useTranslation();

  return (
    <div className="flex gap-1">
      {(Object.keys(LANGUAGES) as Language[]).map((language) => (
        <Button
          key={language}
          variant={i18n.resolvedLanguage === language ? "secondary" : "ghost"}
          size="sm"
          aria-label={LANGUAGES[language]}
          aria-pressed={i18n.resolvedLanguage === language}
          onClick={() => void i18n.changeLanguage(language)}
        >
          {language.toUpperCase()}
        </Button>
      ))}
    </div>
  );
}
