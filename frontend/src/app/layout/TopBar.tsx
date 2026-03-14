import * as React from "react";
import * as Select from "@radix-ui/react-select";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import * as Dialog from "@radix-ui/react-dialog";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { ChevronDown, Bell, User, LogOut, Menu, Plus } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { useAppStore } from "@/stores/appStore";
import { Avatar } from "@/components/ui/Avatar";
import { Button } from "@/components/ui/Button";
import { createTA } from "@/api/client";
import { cn } from "@/lib/utils";
import type { TAInstance } from "@/lib/types";

const DOMAINS = [
  { id: "python", label: "Python" },
  { id: "database", label: "Database (SQL)" },
  { id: "ai_literacy", label: "AI Literacy" },
] as const;

interface TopBarProps {
  pageName: string;
  taList?: TAInstance[];
  onMenuClick?: () => void;
}

export function TopBar({ pageName, taList = [], onMenuClick }: TopBarProps) {
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
  });

  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
      <div className="flex items-center gap-3">
        <button
          type="button"
          onClick={onMenuClick}
          className="rounded-lg p-2 text-slate-600 hover:bg-slate-100 lg:hidden"
          aria-label="Open menu"
        >
          <Menu className="h-5 w-5" />
        </button>
        <p className="text-sm text-slate-500">{pageName}</p>
      </div>
      <div className="flex items-center gap-4">
        <Dialog.Root open={newTADialogOpen} onOpenChange={setNewTADialogOpen}>
          <Dialog.Trigger asChild>
            <button
              type="button"
              className="rounded-lg p-2 text-slate-600 hover:bg-slate-100"
              aria-label="New TA"
            >
              <Plus className="h-5 w-5" />
            </button>
          </Dialog.Trigger>
          <Dialog.Portal>
            <Dialog.Overlay className="fixed inset-0 z-50 bg-black/40" />
            <Dialog.Content className="fixed left-1/2 top-1/2 z-50 w-full max-w-sm -translate-x-1/2 -translate-y-1/2 rounded-xl border border-slate-200 bg-white p-6 shadow-card">
              <Dialog.Title className="text-lg font-semibold text-slate-900">New Teachable Agent</Dialog.Title>
              <Dialog.Description className="mt-1 text-sm text-slate-500">Choose a domain for this TA.</Dialog.Description>
              <div className="mt-4 flex flex-col gap-2">
                {DOMAINS.map((d) => (
                  <label key={d.id} className="flex cursor-pointer items-center gap-2 rounded-lg border border-slate-200 p-3 hover:bg-slate-50">
                    <input
                      type="radio"
                      name="domain"
                      value={d.id}
                      checked={newTADomain === d.id}
                      onChange={() => setNewTADomain(d.id)}
                      className="h-4 w-4"
                    />
                    <span className="text-sm font-medium text-slate-800">{d.label}</span>
                  </label>
                ))}
              </div>
              <div className="mt-6 flex justify-end gap-2">
                <Button variant="secondary" onClick={() => setNewTADialogOpen(false)}>Cancel</Button>
                <Button
                  loading={createTAMutation.isPending}
                  onClick={() => createTAMutation.mutate(newTADomain)}
                >
                  Create TA
                </Button>
              </div>
            </Dialog.Content>
          </Dialog.Portal>
        </Dialog.Root>
        {taList.length > 0 && (
          <Select.Root
            value={currentTaId != null ? String(currentTaId) : ""}
            onValueChange={(v) => setCurrentTaId(Number(v))}
          >
            <Select.Trigger
              className={cn(
                "flex h-9 min-w-[140px] items-center justify-between gap-2 rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm text-slate-700",
                "hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-brand-500/20"
              )}
            >
              <span>
                TA #{currentTa?.id ?? currentTaId} ({currentTa?.domain_id ?? "python"})
              </span>
              <ChevronDown className="h-4 w-4 text-slate-400" />
            </Select.Trigger>
            <Select.Portal>
              <Select.Content
                className="z-50 max-h-[280px] overflow-auto rounded-lg border border-slate-200 bg-white py-1 shadow-card"
                position="popper"
                sideOffset={4}
              >
                {taList.map((ta) => (
                  <Select.Item
                    key={ta.id}
                    value={String(ta.id)}
                    className="cursor-pointer px-3 py-2 text-sm outline-none hover:bg-slate-100 data-[highlighted]:bg-slate-100"
                  >
                    TA #{ta.id} ({ta.domain_id})
                  </Select.Item>
                ))}
              </Select.Content>
            </Select.Portal>
          </Select.Root>
        )}
        <button
          type="button"
          className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
          aria-label="Notifications"
        >
          <Bell className="h-5 w-5" />
        </button>
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button
              type="button"
              className="rounded-full outline-none ring-2 ring-transparent focus:ring-brand-500/30"
            >
              <Avatar fallback={user?.username} size="sm" />
            </button>
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="z-50 min-w-[160px] rounded-lg border border-slate-200 bg-white py-1 shadow-card"
              sideOffset={8}
              align="end"
            >
              <DropdownMenu.Item
                className="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50"
                onSelect={(e) => e.preventDefault()}
                asChild
              >
                <span>
                  <User className="h-4 w-4" />
                  Profile
                </span>
              </DropdownMenu.Item>
              <DropdownMenu.Separator className="my-1 h-px bg-slate-100" />
              <DropdownMenu.Item
                className="flex cursor-pointer items-center gap-2 px-3 py-2 text-sm text-slate-700 outline-none hover:bg-slate-50"
                onSelect={() => logout()}
              >
                <LogOut className="h-4 w-4" />
                Logout
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}
