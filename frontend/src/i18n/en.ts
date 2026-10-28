export const en = {
  start: {
    welcome: "Welcome to the shop.",
  },
  crash: {
    title: "Something went wrong.",
    hint: "Please reload the page.",
    reload: "Reload page",
  },
};

/** The shape every language's texts must have, so a missing text fails the type check. */
export type Translations = typeof en;
