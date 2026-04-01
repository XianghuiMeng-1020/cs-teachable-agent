import * as React from "react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { Globe } from "lucide-react";
import { useTranslation } from "react-i18next";
import { cn } from "@/lib/utils";

const LANGUAGES = [
  { code: "en", label: "English", flag: "EN" },
  { code: "zh-CN", label: "简体中文", flag: "简" },
  { code: "zh-TW", label: "繁體中文", flag: "繁" },
] as const;

interface LanguageSwitcherProps {
  variant?: "topbar" | "landing";
  className?: string;
}

export function LanguageSwitcher({ variant = "topbar", className }: LanguageSwitcherProps) {
  const { i18n } = useTranslation();
  const currentLang = LANGUAGES.find((l) => l.code === i18n.language) ?? LANGUAGES[0];

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <button
          type="button"
          className={cn(
            "flex items-center gap-1.5 rounded-lg border px-2.5 text-xs font-medium transition-colors focus:outline-none",
            variant === "topbar"
              ? "h-8 border-stone-200 bg-white text-stone-600 hover:bg-stone-50"
              : "h-9 border-white/20 bg-white/10 text-white/90 hover:bg-white/20 backdrop-blur-sm",
            className
          )}
        >
          <Globe className="h-3.5 w-3.5" />
          <span>{currentLang.flag}</span>
        </button>
      </DropdownMenu.Trigger>
      <DropdownMenu.Portal>
        <DropdownMenu.Content
          className="z-[100] min-w-[160px] rounded-xl border border-stone-200 bg-white py-1.5 shadow-elevated"
          sideOffset={6}
          align="end"
        >
          {LANGUAGES.map((lang) => (
            <DropdownMenu.Item
              key={lang.code}
              className={cn(
                "flex cursor-pointer items-center gap-3 px-3 py-2 text-sm outline-none hover:bg-stone-50",
                i18n.language === lang.code ? "text-brand-700 font-semibold" : "text-stone-600"
              )}
              onSelect={() => i18n.changeLanguage(lang.code)}
            >
              <span className="flex h-6 w-6 items-center justify-center rounded bg-stone-100 text-xs font-bold text-stone-700">
                {lang.flag}
              </span>
              {lang.label}
            </DropdownMenu.Item>
          ))}
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
