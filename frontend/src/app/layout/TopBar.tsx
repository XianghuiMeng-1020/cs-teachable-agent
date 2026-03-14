import * as React from "react";
import * as Select from "@radix-ui/react-select";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import { ChevronDown, Bell, User, LogOut, Menu } from "lucide-react";
import { useAuthStore } from "@/stores/authStore";
import { useAppStore } from "@/stores/appStore";
import { Avatar } from "@/components/ui/Avatar";
import { cn } from "@/lib/utils";
import type { TAInstance } from "@/lib/types";

interface TopBarProps {
  pageName: string;
  taList?: TAInstance[];
  onMenuClick?: () => void;
}

export function TopBar({ pageName, taList = [], onMenuClick }: TopBarProps) {
  const { user, logout } = useAuthStore();
  const { currentTaId, setCurrentTaId } = useAppStore();
  const currentTa = taList.find((t) => t.id === currentTaId) ?? taList[0];

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
