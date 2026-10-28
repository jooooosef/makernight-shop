import type { ReactNode } from "react";
import { ErrorBoundary } from "react-error-boundary";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/button";

function CrashPage() {
  const { t } = useTranslation();

  return (
    <main className="flex min-h-svh flex-col items-center justify-center gap-6">
      <div className="flex flex-col items-center gap-2">
        <h1 className="text-2xl font-semibold">{t("crash.title")}</h1>
        <p className="text-muted-foreground">{t("crash.hint")}</p>
      </div>
      <Button size="lg" onClick={() => window.location.reload()}>
        {t("crash.reload")}
      </Button>
    </main>
  );
}

/** Shows a reload page instead of a white screen when a component crashes while drawing. */
export function AppErrorBoundary({ children }: { children: ReactNode }) {
  return <ErrorBoundary fallback={<CrashPage />}>{children}</ErrorBoundary>;
}
