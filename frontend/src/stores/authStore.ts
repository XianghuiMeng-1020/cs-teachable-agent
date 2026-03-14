import { create } from "zustand";
import { persist } from "zustand/middleware";
import * as api from "@/api/client";
import type { User } from "@/lib/types";

interface AuthState {
  token: string | null;
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, role: string) => Promise<void>;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const PERSIST_KEY = "cs-ta-auth";

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      login: async (username, password) => {
        await api.login(username, password);
        const user = await api.me();
        set({ user, token: api.getToken() });
      },
      register: async (username, password, role) => {
        await api.register(username, password, role);
        await api.login(username, password);
        const user = await api.me();
        set({ user, token: api.getToken() });
      },
      logout: () => {
        api.setToken(null);
        set({ token: null, user: null });
      },
      refreshUser: async () => {
        try {
          const user = await api.me();
          set({ user });
        } catch {
          set({ token: null, user: null });
        }
      },
    }),
    {
      name: PERSIST_KEY,
      partialize: (s) => ({ token: s.token, user: s.user }),
      onRehydrateStorage: () => (state) => {
        if (state?.token) api.setToken(state.token);
      },
    }
  )
);
