/** TA state: user, ta list, current TA id, refresh. */

import { useState, useEffect, useCallback } from "react";
import { me, listTA, createTA } from "../api/client";

export interface TAItem {
  id: number;
  domain_id: string;
  name?: string;
}

export function useTA() {
  const [user, setUser] = useState<{ id: number; username: string } | null>(null);
  const [taList, setTaList] = useState<TAItem[]>([]);
  const [currentTaId, setCurrentTaId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    try {
      setError(null);
      const u = await me();
      setUser(u);
      const list = await listTA();
      setTaList(list);
      setCurrentTaId((prev) => {
        if (list.length === 0) return prev;
        if (!prev || !list.some((t) => t.id === prev)) return list[0].id;
        return prev;
      });
      if (list.length === 0) {
        const created = await createTA();
        setTaList([created]);
        setCurrentTaId(created.id);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, []);

  return {
    user,
    taList,
    currentTaId,
    setCurrentTaId,
    refresh,
    loading,
    error,
  };
}
