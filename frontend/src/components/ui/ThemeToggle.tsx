import { useState } from "react";
import { Sun, Moon, Monitor, Check, Type, Eye, VolumeX } from "lucide-react";
import { useThemeStore, type ThemeMode, type FontSize } from "@/stores/themeStore";
import { Button } from "./Button";

const themeOptions: { value: ThemeMode; label: string; icon: typeof Sun }[] = [
  { value: "light", label: "Light", icon: Sun },
  { value: "dark", label: "Dark", icon: Moon },
  { value: "system", label: "System", icon: Monitor },
];

const fontSizeOptions: { value: FontSize; label: string; size: string }[] = [
  { value: "small", label: "Small", size: "14px" },
  { value: "normal", label: "Normal", size: "16px" },
  { value: "large", label: "Large", size: "18px" },
  { value: "xlarge", label: "Extra Large", size: "20px" },
];

export function ThemeToggle({ variant = "dropdown" }: { variant?: "dropdown" | "button" }) {
  const {
    theme,
    resolvedTheme,
    setTheme,
    toggleTheme,
    fontSize,
    setFontSize,
    reducedMotion,
    setReducedMotion,
    highContrast,
    setHighContrast,
  } = useThemeStore();

  const [showMenu, setShowMenu] = useState(false);
  const currentIcon = resolvedTheme === "dark" ? Moon : Sun;

  if (variant === "button") {
    return (
      <Button
        variant="ghost"
        size="sm"
        onClick={toggleTheme}
        className="tap-target"
        aria-label={resolvedTheme === "dark" ? "切换到浅色模式" : "切换到深色模式"}
      >
        <currentIcon className="w-5 h-5" />
      </Button>
    );
  }

  return (
    <div className="relative">
      <Button
        variant="ghost"
        size="sm"
        onClick={() => setShowMenu(!showMenu)}
        className="gap-2 tap-target"
        aria-label="打开主题设置"
        aria-expanded={showMenu}
      >
        <currentIcon className="w-4 h-4" />
        <span className="hidden sm:inline text-sm">主题</span>
      </Button>

      {showMenu && (
        <>
          <div
            className="fixed inset-0 z-40"
            onClick={() => setShowMenu(false)}
          />
          <div className="absolute right-0 top-full mt-2 w-56 bg-white dark:bg-surfaceDark-card rounded-xl border border-stone-200 dark:border-stone-700 shadow-elevated dark:shadow-elevated-dark z-50 py-2 animate-fade-in-up">
            {/* Theme Mode */}
            <div className="px-3 py-2">
              <p className="text-xs font-semibold text-stone-500 dark:text-stone-400 mb-2 uppercase tracking-wider">
                外观
              </p>
              <div className="space-y-1">
                {themeOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => {
                      setTheme(option.value);
                      setShowMenu(false);
                    }}
                    className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
                      theme === option.value
                        ? "bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300"
                        : "hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300"
                    }`}
                  >
                    <option.icon className="w-4 h-4" />
                    <span>{option.label}</span>
                    {theme === option.value && <Check className="w-4 h-4 ml-auto" />}
                  </button>
                ))}
              </div>
            </div>

            <div className="border-t border-stone-200 dark:border-stone-700 my-2" />

            {/* Font Size */}
            <div className="px-3 py-2">
              <p className="text-xs font-semibold text-stone-500 dark:text-stone-400 mb-2 uppercase tracking-wider">
                字体大小
              </p>
              <div className="space-y-1">
                {fontSizeOptions.map((option) => (
                  <button
                    key={option.value}
                    onClick={() => {
                      setFontSize(option.value);
                    }}
                    className={`w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                      fontSize === option.value
                        ? "bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300"
                        : "hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300"
                    }`}
                  >
                    <Type className="w-4 h-4" style={{ fontSize: option.size }} />
                    <span>{option.label}</span>
                    {fontSize === option.value && <Check className="w-4 h-4 ml-auto" />}
                  </button>
                ))}
              </div>
            </div>

            <div className="border-t border-stone-200 dark:border-stone-700 my-2" />

            {/* Accessibility Options */}
            <div className="px-3 py-2 space-y-1">
              <button
                onClick={() => setReducedMotion(!reducedMotion)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
                  reducedMotion
                    ? "bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300"
                    : "hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300"
                }`}
              >
                <VolumeX className="w-4 h-4" />
                <span>减少动画</span>
                {reducedMotion && <Check className="w-4 h-4 ml-auto" />}
              </button>

              <button
                onClick={() => setHighContrast(!highContrast)}
                className={`w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors ${
                  highContrast
                    ? "bg-brand-50 dark:bg-brand-900/30 text-brand-700 dark:text-brand-300"
                    : "hover:bg-stone-100 dark:hover:bg-stone-800 text-stone-700 dark:text-stone-300"
                }`}
              >
                <Eye className="w-4 h-4" />
                <span>高对比度</span>
                {highContrast && <Check className="w-4 h-4 ml-auto" />}
              </button>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
