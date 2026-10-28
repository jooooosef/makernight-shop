import type { ErrorCode } from "@/api/client";
import type { components } from "@/api/schema";

type StatusValue = components["schemas"]["StatusEnum"];

// For the codes a team can't act on. They only reach a team through a defect of ours.
const UNEXPECTED = "Something went wrong. Please try again.";

export const en = {
  start: {
    welcome: "Welcome to the shop.",
    checking: "Checking the server…",
    status: {
      ok: "The server is running.",
    } satisfies Record<StatusValue, string>,
  },
  crash: {
    title: "Something went wrong.",
    hint: "Please reload the page.",
    reload: "Reload page",
  },
  errors: {
    INVALID_INPUT: "Please check your input.",
    NOT_LOGGED_IN: "Please log in first.",
    FORBIDDEN: "You aren't allowed to do this.",
    NOT_FOUND: UNEXPECTED,
    METHOD_NOT_ALLOWED: UNEXPECTED,
    INTERNAL: UNEXPECTED,
    NETWORK_ERROR:
      "The server can't be reached. Check your connection and try again.",
  } satisfies Record<ErrorCode, string>,
};

/** The shape every language's texts must have, so a missing text fails the type check. */
export type Translations = typeof en;
