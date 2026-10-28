import { QueryClientProvider, type QueryClient } from "@tanstack/react-query";
import App from "./App";
import { AppErrorBoundary } from "./components/AppErrorBoundary";
import { Toaster } from "./components/ui/sonner";

/** Everything around the app, the same in the browser and in the tests. */
export function Root({ queryClient }: { queryClient: QueryClient }) {
  return (
    <>
      <AppErrorBoundary>
        <QueryClientProvider client={queryClient}>
          <App />
        </QueryClientProvider>
      </AppErrorBoundary>
      {/* The page has no dark mode yet, so the toasts don't follow the system's */}
      <Toaster position="top-right" theme="light" richColors closeButton />
    </>
  );
}
