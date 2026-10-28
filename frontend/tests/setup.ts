import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { toast } from "sonner";
import { afterAll, afterEach } from "vitest";
import { i18n } from "@/i18n";
import { server } from "./server";

// Here and not in beforeAll: the API client takes `fetch` when its module loads, which
// is before any hook runs, and must get the one MSW intercepts.
server.listen({ onUnhandledFrame: "error" });

// Testing Library only cleans up on its own when afterEach is a global, and
// Vitest globals are off.
afterEach(async () => {
  cleanup();
  toast.dismiss();
  server.resetHandlers();
  // Each test starts in English, with nothing remembered on the device
  await i18n.changeLanguage("en");
  localStorage.clear();
});

afterAll(() => {
  server.close();
});
