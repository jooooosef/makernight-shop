import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";
import { api } from "@/api/client";
import { errorText } from "@/api/errorText";
import { LanguageSwitch } from "@/components/LanguageSwitch";

export default function App() {
  const { t } = useTranslation();
  const status = useQuery({
    queryKey: ["status"],
    queryFn: async () => (await api.GET("/api/v1/status")).data,
    meta: { showsOwnError: true },
  });

  return (
    <div className="flex min-h-svh flex-col">
      <header className="flex justify-end p-4">
        <LanguageSwitch />
      </header>
      <main className="flex flex-1 flex-col items-center justify-center gap-2">
        <h1 className="text-2xl font-semibold">Maker night shop</h1>
        <p className="text-muted-foreground">{t("start.welcome")}</p>
        {status.isError ? (
          <p className="text-destructive text-sm">{errorText(status.error)}</p>
        ) : (
          <p className="text-muted-foreground text-sm">
            {status.data
              ? t(`start.status.${status.data.status}`)
              : t("start.checking")}
          </p>
        )}
      </main>
    </div>
  );
}
