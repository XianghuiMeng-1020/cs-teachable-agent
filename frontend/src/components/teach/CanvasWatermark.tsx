import { useEffect, useRef } from "react";

interface CanvasWatermarkProps {
  userId: number;
  username?: string;
  className?: string;
}

export function CanvasWatermark({ userId, username, className = "" }: CanvasWatermarkProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas || userId <= 0) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const text = `${username || "U"}#${userId}`;
    const w = canvas.parentElement?.offsetWidth ?? 600;
    const h = canvas.parentElement?.offsetHeight ?? 400;
    canvas.width = w;
    canvas.height = h;
    ctx.clearRect(0, 0, w, h);
    ctx.font = "12px sans-serif";
    ctx.fillStyle = "rgba(0,0,0,0.015)";
    ctx.textAlign = "center";

    const gap = 120;
    for (let y = 20; y < h; y += gap) {
      for (let x = 30; x < w; x += gap * 1.5) {
        ctx.save();
        ctx.translate(x, y);
        ctx.rotate(-0.35);
        ctx.fillText(text, 0, 0);
        ctx.restore();
      }
    }
  }, [userId, username]);

  return (
    <canvas
      ref={canvasRef}
      className={`absolute inset-0 pointer-events-none z-10 ${className}`}
      style={{ mixBlendMode: "multiply" }}
    />
  );
}
