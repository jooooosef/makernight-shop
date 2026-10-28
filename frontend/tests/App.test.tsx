import { fireEvent, render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import { createQueryClient } from "@/api/queryClient";
import { Root } from "@/Root";

test("shows the server's status, in German after switching and remembers it", async () => {
  render(<Root queryClient={createQueryClient()} />);
  expect(await screen.findByText("The server is running.")).toBeInTheDocument();

  fireEvent.click(screen.getByRole("button", { name: "Deutsch" }));

  expect(await screen.findByText("Der Server läuft.")).toBeInTheDocument();
  expect(document.documentElement.lang).toBe("de");
  expect(localStorage.getItem("language")).toBe("de");
});
