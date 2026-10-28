import { MutationCache, QueryCache, QueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { errorText } from "./errorText";

/** What a call can say about itself, as `meta` on its query or mutation. */
interface CallMeta extends Record<string, unknown> {
  /** The page shows the call's error itself, so no toast appears for it. */
  showsOwnError?: boolean;
}

declare module "@tanstack/react-query" {
  interface Register {
    queryMeta: CallMeta;
    mutationMeta: CallMeta;
  }
}

function showError(error: unknown, meta: CallMeta | undefined): void {
  if (meta?.showsOwnError) {
    return;
  }
  const text = errorText(error);
  // The same text replaces its earlier toast, so a call that keeps failing shows one toast
  toast.error(text, { id: text });
}

/**
 * Every failed call shows its error text in a toast. Retries are off, because polling
 * queries try again anyway. A call that needs them sets its own `retry`.
 */
export function createQueryClient(): QueryClient {
  return new QueryClient({
    queryCache: new QueryCache({
      onError: (error, query) => showError(error, query.meta),
    }),
    mutationCache: new MutationCache({
      onError: (error, _variables, _onMutateResult, mutation) =>
        showError(error, mutation.meta),
    }),
    defaultOptions: { queries: { retry: false } },
  });
}
