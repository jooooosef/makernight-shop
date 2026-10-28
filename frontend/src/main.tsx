import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import "./i18n";
import { createQueryClient } from "./api/queryClient.ts";
import { Root } from "./Root.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Root queryClient={createQueryClient()} />
  </StrictMode>,
);
