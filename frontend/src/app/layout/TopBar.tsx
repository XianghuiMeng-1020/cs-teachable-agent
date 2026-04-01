import * as React from "react";
import * as Select from "@radix-ui/react-select";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import * as Dialog from "@radix-ui/react-dialog";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "sonner";
import { ChevronDown, User, LogOut, Menu, Plus, X } from "lucide-react";
import { useTranslation } from "react-i18next";
import { useAuthStore } from "@/stores/authStore";
import { useAppStore } from "@/stores/appStore";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { LanguageSwitcher } from "@/components/ui/LanguageSwitcher";
import { createTA } from "@/api/client";
import { cn } from "@/lib/utils";
import type { TAInstance } from "@/lib/types";

interface TopBarProps {
  pageName: string;
  taList?: TAInstance[];
  onMenuClick?: () => void;
}

export function TopBar({ pageName, taList = [], onMenuClick }: TopBarProps) {
  const { t } = useTranslation();
  const domains = React.useMemo(
    () =>
      [
        { id: "python" as const, label: t("onboarding.pythonLabel"), desc: t("onboarding.pythonDesc") },
        { id: "database" as const, label: t("onboarding.sqlLabel"), desc: t("onboarding.sqlDesc") },
        { id: "ai_literacy" as const, label: t("onboarding.aiLabel"), desc: t("onboarding.aiDesc") },
      ] as const,
    [t]
  );
  const { user, logout } = useAuthStore();
  const { currentTaId, setCurrentTaId } = useAppStore();
  const queryClient = useQueryClient();
  const [newTADialogOpen, setNewTADialogOpen] = React.useState(false);
  const [newTADomain, setNewTADomain] = React.useState<"python" | "database" | "ai_literacy">("python");
  const currentTa = taList.find((t) => t.id === currentTaId) ?? taList[0];

  const createTAMutation = useMutation({
    mutationFn: (domain_id: string) => createTA(domain_id),
    onSuccess: (created) => {
      queryClient.invalidateQueries({ queryKey: ["ta", "list"] });
      setCurrentTaId(created.id);
      setNewTADialogOpen(false);
    },
    onError: (err: Error) => {
      toast.error(err?.message ?? t("topbar.failedCreateTA"));
    },
  });

  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-stone-200/80 bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="rounded-lg p-2 text-stone-500 hover:bg-stone-100 lg:hidden"
          aria-label="Open menu"
        >
          <Menu className="h-5 w-5" />
        </button>
        <h1 className="text-sm font-semibold text-stone-800">{pageName}</h1>
      </div>

      <div className="flex items-center gap-2">
        {/* New TA Dialog */}
        <Dialog.Root open={newTADialogOpen} onOpenChange={setNewTADialogOpen}>
          <Dialog.Trigger asChild>
            <button
              type="button"
              className="flex h-8 items-center gap-1.5 rounded-lg border border-stone-200 bg-white px-2.5 text-xs font-medium text-stone-600 transition-colors hover:bg-stone-50"
            >
              <Plus className="h-3.5 w-3.5" />
              <span className="hidden sm:inline">{t("topbar.newTA")}</span>
            </button>
          </Dialog.Trigger>
          <Dialog.Portal>
            <Dialog.Overlay className="fixed inset-0 z-50 bg-black/30 backdrop-blur-sm" />
            <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-sm -translate-x-1/2 -translate-y-1/2 rounded-xl border border-stone-200 bg-white p-6 shadow-elevated animate-scale-in">
              <div className="flex items-center justify-between">
                <Dialog.Title className="font-serif text-lg font-semibold text-stone-900">
                  {t("topbar.createTA")}
                </Dialog.Title>
                <Dialog.Close className="rounded-lg p-1 text-stone-400 hover:bg-stone-100 hover:text-stone-600">
                  <X className="h-4 w-4" />
                </Dialog.Close>
              </div>
              <Dialog.Description className="mt-1 text-sm text-stone-500">
                {t("onboarding.chooseDomainDesc")}
              </Dialog.Description>
              <div className="mt-5 flex flex-col gap-2">
                {domains.map((d) => (
                  <label
                    key={d.id}
                    className={cn(
                      "flex cursor-pointer items-center gap-3 rounded-lg border-2 p-3 transition-all",
                      newTADomain === d.id
                        ? "border-brand-600 bg-brand-50"
                        : "border-stone-200 hover:border-stone-300"
                    )}
                  >
                    <input
                      type="radio"
                      name="domain"
                      value={d.id}
                      checked={newTADomain === d.id}
                      onChange={() => setNewTADomain(d.id)}
                      className="sr-only"
                    />
                    <div>
                      <div className={cn("text-sm font-semibold", newTADomain === d.id ? "text-brand-900" : "text-stone-700")}>
                        {d.label}
                      </div>
                      <div className="text-xs text-stone-500">{d.desc}</div>
                    </div>
                  </label>
                ))}
              </div>
              <div className="mt-6 flex justify-end gap-2">
                <Button variant="secondary" size="sm" onClick={() => setNewTADialogOpen(false)}>
                  {t("common.cancel")}
                </Button>
                <Button
                  size="sm"
                  loading={createTAMutation.isPending}
                  onClick={() => createTAMutation.mutate(newTADomain)}
                >
                  {t("onboarding.createMyTA")}
                </Button>
              </div>
            </Dialog.Content>
          </Dialog.Portal>
        </Dialog.Root>

        {/* TA Selector */}
        {taList.length > 0 && (
          <Select.Root
            value={currentTaId != null ? String(currentTaId) : ""}
            onValueChange={(v) => setCurrentTaId(Number(v))}
          >
            <Select.Trigger
              className={cn(
                "flex h-8 min-w-[120px] items-center justify-between gap-1.5 rounded-lg border border-stone-200 bg-white px-2.5 text-xs font-medium text-stone-700",
                "hover:bg-stone-50 focus:outline-none focus:ring-2 focus:ring-brand-600/20"
              )}
            >
              <span>
                {t("topbar.taLabel", { id: currentTa?.id ?? currentTaId })}
                <span className="ml-1 text-stone-400">
                  {currentTa?.domain_id ?? "python"}
                </span>
              </span>
              <ChevronDown className="h-3.5 w-3.5 text-stone-400" />
            </Select.Trigger>
            <Select.Portal>
              <Select.Content
                className="z-50 max-h-[280px] overflow-auto rounded-lg border border-stone-200 bg-white py-1 shadow-elevated"
                position="popper"
                sideOffset={4}
              >
                {taList.map((ta) => (
                  <Select.Item
                    key={ta.id}
                    value={String(ta.id)}
                    className="cursor-pointer px-3 py-2 text-sm outline-none hover:bg-stone-50 data-[highlighted]:bg-stone-50"
                  >
                    {t("topbar.taLabel", { id: ta.id })}
                    <span className="ml-1.5 text-stone-400">{ta.domain_id}</span>
                  </Select.Item>
                ))}
              </Select.Content>
            </Select.Portal>
          </Select.Root>
        )}

        {/* Language switcher */}
        <LanguageSwitcher />

        {/* User menu */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button
              type="button"
              className="rounded-full outline-none ring-2 ring-transparent transition-all focus:ring-brand-600/30"
            >
              <Avatar fallback={user?.username} size="sm" />
            </button>
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="z-50 min-w-[180px] rounded-xl border border-stone-200 bg-white py-1.5 shadow-elevated"
              sideOffset={8}
              align="end"
            >
              <div className="border-b border-stone-100 px-3 pb-2 pt-1">
                <p className="text-sm font-semibold text-stone-900">{user?.username}</p>
                <p className="text-xs text-stone-400 capitalize">{user?.role}</p>
              </div>
              <DropdownMenu.Item
                className="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm text-stone-600 outline-none hover:bg-stone-50"
                onSelect={(e) => e.preventDefault()}
              >
                <User className="h-4 w-4" />
                {t("common.profile")}
              </DropdownMenu.Item>
              <DropdownMenu.Separator className="my-1 h-px bg-stone-100" />
              <DropdownMenu.Item
                className="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm text-stone-600 outline-none hover:bg-stone-50"
                onSelect={() => logout()}
              >
                <LogOut className="h-4 w-4" />
                {t("common.signOut")}
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}
