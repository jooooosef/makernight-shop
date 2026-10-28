import { fireEvent, render, screen } from "@testing-library/react";
import { expect, test } from "vitest";
import App from "@/App";

test("switches to German and remembers it on the device", async () => {
  render(<App />);
  expect(screen.getByText("Welcome to the shop.")).toBeInTheDocument();

  fireEvent.click(screen.getByRole("button", { name: "Deutsch" }));

  expect(await screen.findByText("Willkommen im Shop.")).toBeInTheDocument();
  expect(document.documentElement.lang).toBe("de");
  expect(localStorage.getItem("language")).toBe("de");
});
