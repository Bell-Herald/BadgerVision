import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { QueryParamProvider } from "use-query-params";
import { WindowHistoryAdapter } from "use-query-params/adapters/window";
import {
  MantineProvider,
  createTheme,
  MantineColorsTuple,
} from "@mantine/core";
import "@mantine/core/styles.css";

const badgerColor: MantineColorsTuple = [
  "#ffe9eb",
  "#fed1d2",
  "#fb9fa2",
  "#f86a6f",
  "#f74044",
  "#f62729",
  "#f71a1b",
  "#dc0f0f",
  "#c4050c",
  "#ac0006",
];

const theme = createTheme({
  colors: {
    badger: badgerColor,
  },
  primaryColor: "badger",
  primaryShade: 4,
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryParamProvider adapter={WindowHistoryAdapter}>
      <MantineProvider theme={theme}>
        <App />
      </MantineProvider>
    </QueryParamProvider>
  </StrictMode>
);
