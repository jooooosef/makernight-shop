import i18n from "i18next";
import LanguageDetector from "i18next-browser-languagedetector";
import { initReactI18next } from "react-i18next";
import { de } from "./de";
import { en, type Translations } from "./en";

declare module "i18next" {
  interface CustomTypeOptions {
    resources: { translation: Translations };
  }
}

/** Each language's own name, which is how a switch shows it. */
export const LANGUAGES = { en: "English", de: "Deutsch" } as const;
export type Language = keyof typeof LANGUAGES;

i18n.on("languageChanged", (language) => {
  document.documentElement.lang = language;
});

void i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources: { en: { translation: en }, de: { translation: de } },
    supportedLngs: Object.keys(LANGUAGES),
    // A browser set to "de-AT" gets German
    nonExplicitSupportedLngs: true,
    fallbackLng: "en",
    // The device's choice first, then the browser's languages
    detection: {
      order: ["localStorage", "navigator"],
      caches: ["localStorage"],
      lookupLocalStorage: "language",
    },
    // React escapes the texts already
    interpolation: { escapeValue: false },
    // The texts are bundled, so the first render already has them
    initAsync: false,
  });

export { i18n };
