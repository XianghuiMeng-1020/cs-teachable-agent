import { create } from "zustand";

interface AppState {
  currentTaId: number | null;
  sidebarCollapsed: boolean;
  mobileMenuOpen: boolean;
  setCurrentTaId: (id: number | null) => void;
  toggleSidebar: () => void;
  setMobileMenuOpen: (open: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  currentTaId: null,
  sidebarCollapsed: false,
  mobileMenuOpen: false,
  setCurrentTaId: (id) => set({ currentTaId: id }),
  toggleSidebar: () => set((s) => ({ sidebarCollapsed: !s.sidebarCollapsed })),
  setMobileMenuOpen: (open) => set({ mobileMenuOpen: open }),
}));
