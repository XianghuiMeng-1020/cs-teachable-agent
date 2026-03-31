import { useState, useEffect, useRef } from "react";
import { getAdminConfig } from "@/api/admin";

interface AntiCaptureOverlayProps {
  children: React.ReactNode;
}

const DEFAULT_FPS = 40;

/**
 * Anti-capture overlay that creates visual interference patterns
 * imperceptible to human vision but causing banding/moiré artifacts
 * on phone cameras (typically 30fps or 60fps).
 *
 * Settings are fetched from the admin config API — students see
 * no controls at all; only teachers can adjust Hz via the Proctoring page.
 */
export function AntiCaptureOverlay({ children }: AntiCaptureOverlayProps) {
  const [fps, setFps] = useState(DEFAULT_FPS);
  const [enabled, setEnabled] = useState(true);
  const [phase, setPhase] = useState(0);
  const rafRef = useRef<number>(0);
  const lastRef = useRef(0);

  useEffect(() => {
    let cancelled = false;
    getAdminConfig()
      .then((cfg) => {
        if (cancelled) return;
        if (typeof cfg.anti_capture_hz === "number") setFps(cfg.anti_capture_hz);
        if (typeof cfg.anti_capture_enabled === "boolean") setEnabled(cfg.anti_capture_enabled);
      })
      .catch(() => {});
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!enabled) return;
    const interval = 1000 / fps;

    const tick = (now: number) => {
      if (now - lastRef.current >= interval) {
        lastRef.current = now;
        setPhase((p) => (p + 1) % 4);
      }
      rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(rafRef.current);
  }, [enabled, fps]);

  if (!enabled) return <>{children}</>;

  const patterns = [
    "repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(180,180,180,0.04) 3px, rgba(180,180,180,0.04) 4px)",
    "repeating-linear-gradient(90deg, transparent, transparent 3px, rgba(160,160,160,0.05) 3px, rgba(160,160,160,0.05) 4px)",
    "repeating-linear-gradient(45deg, transparent, transparent 4px, rgba(170,170,170,0.04) 4px, rgba(170,170,170,0.04) 5px)",
    "repeating-linear-gradient(135deg, transparent, transparent 4px, rgba(150,150,150,0.05) 4px, rgba(150,150,150,0.05) 5px)",
  ];

  return (
    <div className="relative">
      {children}

      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-[9999]"
        style={{
          background: patterns[phase],
          mixBlendMode: "multiply",
          willChange: "background",
        }}
      />

      <div
        aria-hidden
        className="pointer-events-none fixed inset-0 z-[9999]"
        style={{
          background: patterns[(phase + 2) % 4],
          mixBlendMode: "difference",
          opacity: 0.03,
          willChange: "background",
        }}
      />
    </div>
  );
}
