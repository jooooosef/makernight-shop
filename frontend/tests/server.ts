import { http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import type { components } from "@/api/schema";

type Status = components["schemas"]["Status"];

/** The made-up server of every test. A test replaces a handler with `server.use()`. */
export const server = setupServer(
  http.get("/api/v1/status", () =>
    HttpResponse.json({ status: "ok" } satisfies Status),
  ),
);
