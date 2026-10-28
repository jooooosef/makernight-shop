import { useTranslation } from "react-i18next";
import { LanguageSwitch } from "@/components/LanguageSwitch";

export default function App() {
  const { t } = useTranslation();

  return (
    <div className="flex min-h-svh flex-col">
      <header className="flex justify-end p-4">
        <LanguageSwitch />
      </header>
      <main className="flex flex-1 flex-col items-center justify-center gap-2">
        <h1 className="text-2xl font-semibold">Maker night shop</h1>
        <p className="text-muted-foreground">{t("start.welcome")}</p>
      </main>
    </div>
  );
}
