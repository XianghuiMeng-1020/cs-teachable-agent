import { useState, useRef, useEffect } from "react";
import { useQueryClient, useQuery } from "@tanstack/react-query";
import { Send, MessageCircle } from "lucide-react";
import { teach, getMessages } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { EmptyState } from "@/components/ui/EmptyState";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { formatRelative } from "@/lib/utils";

export interface ChatMessage {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
  metadata?: { interpreted_units?: string[]; quality_score?: number };
}

interface ChatPanelProps {
  taId: number | null;
}

export function ChatPanel({ taId }: ChatPanelProps) {
  const queryClient = useQueryClient();
  const [input, setInput] = useState("");
  const [localMessages, setLocalMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const { data: messagesData } = useQuery({
    queryKey: ["ta", taId, "messages"],
    queryFn: () => getMessages(taId!),
    enabled: !!taId,
  });

  const persistedMessages: ChatMessage[] =
    messagesData?.messages?.map((m) => ({
      role: m.role,
      content: m.content,
      timestamp: m.timestamp,
    })) ?? [];
  const messages =
    loading && localMessages.length > 0
      ? localMessages
      : persistedMessages.length > 0
        ? persistedMessages
        : localMessages;

  useEffect(() => {
    if (messagesData?.messages?.length && !loading) setLocalMessages([]);
  }, [messagesData?.messages?.length, loading]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const handleSend = async () => {
    if (!taId || !input.trim()) return;
    const text = input.trim();
    setInput("");
    const now = new Date().toISOString();
    setLocalMessages((m) => [
      ...m,
      { role: "student", content: text, timestamp: formatRelative(now) },
    ]);
    setLoading(true);
    try {
      const res = await teach(taId, text);
      setLocalMessages((m) => [
        ...m,
        {
          role: "ta",
          content: res.ta_response ?? "OK.",
          timestamp: formatRelative(new Date().toISOString()),
          metadata: {
            interpreted_units: res.interpreted_units,
            quality_score: res.quality_score,
          },
        },
      ]);
      if (taId != null) {
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "state"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "misconceptions"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "history"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "messages"] });
      }
    } catch (err) {
      setLocalMessages((m) => [
        ...m,
        {
          role: "ta",
          content: "Error: " + (err instanceof Error ? err.message : "Failed"),
          timestamp: formatRelative(new Date().toISOString()),
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-3 overflow-y-auto px-4 py-3">
        {messages.length === 0 && !loading && (
          <EmptyState
            icon={MessageCircle}
            title="Start teaching"
            description="Start teaching your TA by explaining a concept (e.g. variables, print, or conditionals)."
          />
        )}
        {messages.map((msg, i) => (
          <MessageBubble
            key={i}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
            metadata={msg.metadata}
          />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
      <div className="border-t border-slate-200 p-3">
        <div className="flex gap-2">
          <Input
            placeholder="Type to teach..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            className="flex-1"
            disabled={!taId || loading}
          />
          <Button
            icon={Send}
            onClick={handleSend}
            disabled={!taId || !input.trim() || loading}
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}
