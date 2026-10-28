import { i18n } from "@/i18n";
import { ApiError } from "./client";

/** The text for a failed call, in the current language. */
export function errorText(error: unknown): string {
  // A newer backend can send a code this page has no text for yet
  const code =
    error instanceof ApiError && i18n.exists(`errors.${error.code}`)
      ? error.code
      : "INTERNAL";
  return i18n.t(`errors.${code}`);
}
