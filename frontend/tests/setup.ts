import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";
import { i18n } from "@/i18n";

// Testing Library only cleans up on its own when afterEach is a global, and
// Vitest globals are off.
afterEach(async () => {
  cleanup();
  // Each test starts in English, with nothing remembered on the device
  await i18n.changeLanguage("en");
  localStorage.clear();
});
