/** M-43: Theme toggle component with persistence */

import * as React from "react";
import { Sun, Moon, Monitor } from "lucide-react";
import { useThemeStore } from "@/stores/themeStore";
import { Button } from "./Button";

type Theme = "light" | "dark" | "system";

const themeIcons: Record<Theme, React.ReactNode> = {
  light: <Sun className="h-5 w-5" />,
  dark: <Moon className="h-5 w-5" />,
  system: <Monitor className="h-5 w-5" />,
};

const themeLabels: Record<Theme, string> = {
  light: "Light mode",
  dark: "Dark mode",
  system: "System preference",
};

interface ThemeToggleProps {
  variant?: "icon" | "dropdown" | "segmented";
  className?: string;
}

export function ThemeToggle({ variant = "icon", className }: ThemeToggleProps) {
  const { theme, setTheme, toggleTheme } = useThemeStore();

  if (variant === "segmented") {
    return (
      <div className={`flex rounded-lg border border-stone-200 bg-white p-1 ${className}`}>
        {(["light", "dark", "system"] as Theme[]).map((t) => (
          <button
            key={t}
            onClick={() => setTheme(t)}
            className={`flex items-center gap-2 rounded-md px-3 py-1.5 text-sm transition-colors ${
              theme === t
                ? "bg-stone-800 text-white"
                : "text-stone-600 hover:bg-stone-100"
            }`}
            aria-label={themeLabels[t]}
            aria-pressed={theme === t}
          >
            {themeIcons[t]}
            <span className="capitalize">{t}</span>
          </button>
        ))}
      </div>
    );
  }

  if (variant === "dropdown") {
    const [isOpen, setIsOpen] = React.useState(false);
    const ref = React.useRef<HTMLDivElement>(null);

    React.useEffect(() => {
      const handleClickOutside = (event: MouseEvent) => {
        if (ref.current && !ref.current.contains(event.target as Node)) {
          setIsOpen(false);
        }
      };
      document.addEventListener("mousedown", handleClickOutside);
      return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
      <div ref={ref} className={`relative ${className}`}>
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsOpen(!isOpen)}
          aria-haspopup="menu"
          aria-expanded={isOpen}
        >
          {themeIcons[theme]}
          <span className="sr-only">{themeLabels[theme]}</span>
        </Button>
        {isOpen && (
          <div className="absolute right-0 top-full z-50 mt-1 w-40 rounded-lg border border-stone-200 bg-white py-1 shadow-lg">
            {(["light", "dark", "system"] as Theme[]).map((t) => (
              <button
                key={t}
                onClick={() => {
                  setTheme(t);
                  setIsOpen(false);
                }}
                className={`flex w-full items-center gap-2 px-4 py-2 text-left text-sm transition-colors hover:bg-stone-100 ${
                  theme === t ? "font-medium text-stone-900" : "text-stone-600"
                }`}
              >
                {themeIcons[t]}
                <span className="capitalize">{t}</span>
              </button>
            ))}
          </div>
        )}
      </div>
    );
  }

  // Icon variant (default)
  return (
    <Button
      variant="ghost"
      size="sm"
      onClick={toggleTheme}
      className={className}
      aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
    >
      {themeIcons[theme === "light" ? "dark" : "light"]}
    </Button>
  );
}
