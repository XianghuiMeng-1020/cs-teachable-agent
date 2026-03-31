export function TypingIndicator() {
  return (
    <div className="flex gap-2">
      <div className="h-8 w-8 shrink-0 rounded-full bg-accent-500" aria-hidden />
      <div className="rounded-2xl rounded-bl-md bg-stone-100 px-4 py-3">
        <div className="flex gap-1">
          <span className="h-2 w-2 rounded-full bg-stone-400 animate-pulse-dot" style={{ animationDelay: "0s" }} />
          <span className="h-2 w-2 rounded-full bg-stone-400 animate-pulse-dot" style={{ animationDelay: "0.2s" }} />
          <span className="h-2 w-2 rounded-full bg-stone-400 animate-pulse-dot" style={{ animationDelay: "0.4s" }} />
        </div>
      </div>
    </div>
  );
}
