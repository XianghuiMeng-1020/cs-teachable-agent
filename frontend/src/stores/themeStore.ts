/** M-43: Theme store with persistence */

import { create } from "zustand";
import { persist } from "zustand/middleware";

type Theme = "light" | "dark" | "system";

interface ThemeState {
  theme: Theme;
  resolvedTheme: "light" | "dark";
  setTheme: (theme: Theme) => void;
  toggleTheme: () => void;
}

const STORAGE_KEY = "cs-ta-theme";

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: "system",
      resolvedTheme: getSystemTheme(),
      setTheme: (theme) => {
        const resolved = theme === "system" ? getSystemTheme() : theme;
        set({ theme, resolvedTheme: resolved });
        document.documentElement.classList.toggle("dark", resolved === "dark");
      },
      toggleTheme: () => {
        const { resolvedTheme } = get();
        const newTheme = resolvedTheme === "light" ? "dark" : "light";
        set({ theme: newTheme, resolvedTheme: newTheme });
        document.documentElement.classList.toggle("dark", newTheme === "dark");
      },
    }),
    {
      name: STORAGE_KEY,
      partialize: (s) => ({ theme: s.theme }),
      onRehydrateStorage: () => (state) => {
        if (state) {
          const resolved =
            state.theme === "system" ? getSystemTheme() : state.theme;
          document.documentElement.classList.toggle("dark", resolved === "dark");
        }
      },
    }
  )
);
