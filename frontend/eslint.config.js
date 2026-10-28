import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";
import prettier from "eslint-config-prettier";

const useApiClient =
  "Call the server through `api` from src/api/client.ts, which turns every failure into an ApiError.";

export default tseslint.config(
  { ignores: ["dist", "src/api/schema.d.ts"] },
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,
      ...tseslint.configs.recommendedTypeChecked,
      reactHooks.configs.flat["recommended-latest"],
      prettier,
    ],
    languageOptions: {
      globals: globals.browser,
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },
    rules: {
      "no-restricted-globals": [
        "error",
        { name: "fetch", message: useApiClient },
      ],
      "no-restricted-properties": [
        "error",
        { object: "window", property: "fetch", message: useApiClient },
        { object: "globalThis", property: "fetch", message: useApiClient },
      ],
    },
  },
);
