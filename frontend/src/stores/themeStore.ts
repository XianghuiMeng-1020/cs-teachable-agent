import { create } from "zustand";
import { persist } from "zustand/middleware";

export type ThemeMode = "light" | "dark" | "system";
export type FontSize = "small" | "normal" | "large" | "xlarge";
export type MonoFont = "jetbrains" | "fira" | "sf";

interface ThemeState {
  // Theme
  theme: ThemeMode;
  resolvedTheme: "light" | "dark";
  setTheme: (theme: ThemeMode) => void;
  toggleTheme: () => void;

  // Font settings
  fontSize: FontSize;
  setFontSize: (size: FontSize) => void;
  monoFont: MonoFont;
  setMonoFont: (font: MonoFont) => void;

  // Accessibility
  reducedMotion: boolean;
  setReducedMotion: (value: boolean) => void;
  highContrast: boolean;
  setHighContrast: (value: boolean) => void;
}

function getSystemTheme(): "light" | "dark" {
  if (typeof window === "undefined") return "light";
  return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: "system",
      resolvedTheme: "light",
      setTheme: (theme) => {
        const resolved = theme === "system" ? getSystemTheme() : theme;
        set({ theme, resolvedTheme: resolved });
        document.documentElement.classList.toggle("dark", resolved === "dark");
      },
      toggleTheme: () => {
        const current = get().resolvedTheme;
        const next = current === "light" ? "dark" : "light";
        set({ theme: next, resolvedTheme: next });
        document.documentElement.classList.toggle("dark", next === "dark");
      },

      fontSize: "normal",
      setFontSize: (fontSize) => {
        set({ fontSize });
        const sizes = { small: "14px", normal: "16px", large: "18px", xlarge: "20px" };
        document.documentElement.style.fontSize = sizes[fontSize];
      },
      monoFont: "jetbrains",
      setMonoFont: (monoFont) => set({ monoFont }),

      reducedMotion: false,
      setReducedMotion: (reducedMotion) => {
        set({ reducedMotion });
        document.documentElement.classList.toggle("reduce-motion", reducedMotion);
      },
      highContrast: false,
      setHighContrast: (highContrast) => {
        set({ highContrast });
        document.documentElement.classList.toggle("high-contrast", highContrast);
      },
    }),
    {
      name: "cs-ta-theme",
      onRehydrateStorage: () => (state) => {
        if (state) {
          // Apply stored theme on rehydration
          const resolved = state.theme === "system" ? getSystemTheme() : state.theme;
          document.documentElement.classList.toggle("dark", resolved === "dark");
          document.documentElement.classList.toggle("reduce-motion", state.reducedMotion);
          document.documentElement.classList.toggle("high-contrast", state.highContrast);
          const sizes = { small: "14px", normal: "16px", large: "18px", xlarge: "20px" };
          document.documentElement.style.fontSize = sizes[state.fontSize];
        }
      },
    }
  )
);

// Listen for system theme changes
if (typeof window !== "undefined") {
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaQuery.addEventListener("change", (e) => {
    const state = useThemeStore.getState();
    if (state.theme === "system") {
      const resolved = e.matches ? "dark" : "light";
      useThemeStore.setState({ resolvedTheme: resolved });
      document.documentElement.classList.toggle("dark", resolved === "dark");
    }
  });
}
