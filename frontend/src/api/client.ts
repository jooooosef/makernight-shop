import createClient, { type Middleware } from "openapi-fetch";
import type { components, paths } from "./schema";

type ErrorBody = components["schemas"]["ErrorBody"];

/** The code of a call that got no response at all, such as when the server is down. */
export const NETWORK_ERROR = "NETWORK_ERROR";

/** Every code a failed call can have: the server's, plus the one for no response. */
export type ErrorCode = ErrorBody["code"] | typeof NETWORK_ERROR;

/** Thrown for every failed API call. Components branch on `code`, never on the HTTP status. */
export class ApiError extends Error {
  readonly code: ErrorCode;
  readonly details: ErrorBody["details"];

  constructor(
    code: ErrorCode,
    message: string,
    details: ErrorBody["details"] = null,
    options?: ErrorOptions,
  ) {
    super(message, options);
    this.name = "ApiError";
    this.code = code;
    this.details = details;
  }
}

function isErrorBody(body: unknown): body is ErrorBody {
  return (
    typeof body === "object" &&
    body !== null &&
    "code" in body &&
    typeof body.code === "string" &&
    "message" in body &&
    typeof body.message === "string"
  );
}

// What a proxy in front of the server answers when the server is down or too slow
const GATEWAY_ERRORS = [502, 503, 504];

async function toApiError(response: Response): Promise<ApiError> {
  const body: unknown = await response.json().catch(() => null);
  if (isErrorBody(body)) {
    return new ApiError(body.code, body.message, body.details);
  }
  if (GATEWAY_ERRORS.includes(response.status)) {
    return new ApiError(
      NETWORK_ERROR,
      `The server did not respond (HTTP ${response.status}).`,
    );
  }
  // Not the server's error body, such as a page of a broken proxy
  return new ApiError("INTERNAL", `HTTP ${response.status}`);
}

const throwApiError: Middleware = {
  async onResponse({ response }) {
    if (!response.ok) {
      throw await toApiError(response);
    }
  },
  // Runs when `fetch` itself fails, so there is no response. The returned error is thrown.
  onError({ error, request }) {
    // A call the page cancelled itself isn't a failure, so its error passes through
    if (request.signal.aborted) {
      return undefined;
    }
    return new ApiError(NETWORK_ERROR, "The server did not respond.", null, {
      cause: error,
    });
  },
};

/** The only way the page calls the server. */
export const api = createClient<paths>({
  // Absolute, because Node's `fetch` in the tests rejects relative URLs
  baseUrl: window.location.origin,
});
api.use(throwApiError);
