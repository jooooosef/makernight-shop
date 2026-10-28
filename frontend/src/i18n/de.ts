import type { Translations } from "./en";

const UNEXPECTED = "Etwas ist schiefgelaufen. Bitte versuche es noch einmal.";

export const de: Translations = {
  start: {
    welcome: "Willkommen im Shop.",
    checking: "Server wird geprüft…",
    status: {
      ok: "Der Server läuft.",
    },
  },
  crash: {
    title: "Etwas ist schiefgelaufen.",
    hint: "Bitte lade die Seite neu.",
    reload: "Seite neu laden",
  },
  errors: {
    INVALID_INPUT: "Bitte prüfe deine Eingabe.",
    NOT_LOGGED_IN: "Bitte melde dich zuerst an.",
    FORBIDDEN: "Das darfst du nicht.",
    NOT_FOUND: UNEXPECTED,
    METHOD_NOT_ALLOWED: UNEXPECTED,
    INTERNAL: UNEXPECTED,
    NETWORK_ERROR:
      "Der Server ist nicht erreichbar. Prüfe deine Verbindung und versuche es noch einmal.",
  },
};
