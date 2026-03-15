import { useState, useRef, useEffect, useCallback } from "react";
import { useQueryClient, useQuery } from "@tanstack/react-query";
import { Send, MessageCircle, AlertCircle, CheckCircle, BarChart3 } from "lucide-react";
import { teach, teachStream, getMessages, analyzeTeaching } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { EmptyState } from "@/components/ui/EmptyState";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { TeachingHelper, type TeachingHelperResult } from "./TeachingHelper";
import { ModeIndicator } from "./ModeIndicator";
import { formatRelative } from "@/lib/utils";

export interface ChatMessage {
  role: "student" | "ta";
  content: string;
  timestamp?: string;
  metadata?: {
    interpreted_units?: string[];
    quality_score?: number;
    failed?: boolean;
    lastInput?: string;
    streaming?: boolean;
  };
}

interface ChatPanelProps {
  taId: number | null;
}

const MAX_INPUT_LENGTH = 2000;
const MIN_QUALITY_INPUT_LENGTH = 20;
const QUALITY_CHECK_DEBOUNCE_MS = 800;

// Simple debounce hook
function useDebouncedCallback<T extends (...args: Parameters<T>) => ReturnType<T>>(
  callback: T,
  delay: number
) {
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  
  return useCallback((...args: Parameters<T>) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    timeoutRef.current = setTimeout(() => {
      callback(...args);
    }, delay);
  }, [callback, delay]);
}

// Quality indicator component
function QualityIndicator({ 
  length, 
  maxLength, 
  qualityResult 
}: { 
  length: number; 
  maxLength: number; 
  qualityResult: TeachingHelperResult | null;
}) {
  const isNearLimit = length > maxLength * 0.9;
  const isOverLimit = length > maxLength;
  
  if (isOverLimit) {
    return (
      <div className="flex items-center gap-1 text-xs text-rose-600">
        <AlertCircle className="w-3 h-3" />
        <span>{length}/{maxLength}</span>
      </div>
    );
  }
  
  if (qualityResult) {
    const isGood = qualityResult.pattern === "good";
    return (
      <div className={`flex items-center gap-1 text-xs ${isGood ? 'text-emerald-600' : 'text-amber-600'}`}>
        {isGood ? <CheckCircle className="w-3 h-3" /> : <AlertCircle className="w-3 h-3" />}
        <span>{isGood ? 'Quality: Good' : 'Quality: Needs improvement'}</span>
      </div>
    );
  }
  
  return (
    <div className={`flex items-center gap-1 text-xs ${isNearLimit ? 'text-amber-600' : 'text-slate-400'}`}>
      <BarChart3 className="w-3 h-3" />
      <span>{length}/{maxLength}</span>
    </div>
  );
}

export function ChatPanel({ taId }: ChatPanelProps) {
  const queryClient = useQueryClient();
  const [input, setInput] = useState("");
  const [localMessages, setLocalMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [teachingHelperResult, setTeachingHelperResult] = useState<TeachingHelperResult | null>(null);
  const [pendingInput, setPendingInput] = useState<string | null>(null);
  const [isCheckingQuality, setIsCheckingQuality] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const lastCheckRef = useRef<string>("");

  const { data: messagesData } = useQuery({
    queryKey: ["ta", taId, "messages"],
    queryFn: () => getMessages(taId!),
    enabled: !!taId,
  });

  // Auto quality check with debounce
  const performQualityCheck = useCallback(async (text: string) => {
    if (!taId || text.length < MIN_QUALITY_INPUT_LENGTH) {
      setTeachingHelperResult(null);
      return;
    }
    
    // Don't check if we already checked this text
    if (text === lastCheckRef.current && teachingHelperResult) return;
    
    setIsCheckingQuality(true);
    try {
      const result = await analyzeTeaching(taId, text.trim());
      setTeachingHelperResult(result);
      lastCheckRef.current = text;
    } catch {
      // Silently fail - quality check is optional
    } finally {
      setIsCheckingQuality(false);
    }
  }, [taId, teachingHelperResult]);

  const debouncedQualityCheck = useDebouncedCallback(performQualityCheck, QUALITY_CHECK_DEBOUNCE_MS);

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

  const handleCheckQuality = async () => {
    if (!taId || !input.trim()) return;
    setIsCheckingQuality(true);
    try {
      const result = await analyzeTeaching(taId, input.trim());
      setTeachingHelperResult(result);
      lastCheckRef.current = input.trim();
    } catch {
      setTeachingHelperResult(null);
    } finally {
      setIsCheckingQuality(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const newValue = e.target.value;
    if (newValue.length <= MAX_INPUT_LENGTH) {
      setInput(newValue);
      // Clear quality result if input changed significantly
      if (Math.abs(newValue.length - (lastCheckRef.current?.length ?? 0)) > 10) {
        debouncedQualityCheck(newValue);
      }
    }
  };

  const handleSend = async () => {
    if (!taId || !input.trim()) return;
    const text = input.trim();
    setInput("");
    setTeachingHelperResult(null);
    setPendingInput(null);
    const now = new Date().toISOString();
    setLocalMessages((m) => [
      ...m,
      { role: "student", content: text, timestamp: formatRelative(now) },
    ]);
    setLoading(true);
    const streamedContent = { current: "" };
    setLocalMessages((m) => [
      ...m,
      {
        role: "ta",
        content: "",
        timestamp: formatRelative(new Date().toISOString()),
        metadata: { streaming: true },
      },
    ]);
    try {
      const res = await teachStream(taId, text, {
        onChunk: (chunk) => {
          streamedContent.current += chunk;
          setLocalMessages((prev) => {
            const next = [...prev];
            const last = next[next.length - 1];
            if (last?.role === "ta" && last.metadata?.streaming) {
              next[next.length - 1] = { ...last, content: streamedContent.current };
            }
            return next;
          });
        },
      });
      setLocalMessages((m) => {
        const next = [...m];
        const last = next[next.length - 1];
        if (last?.role === "ta" && last.metadata?.streaming) {
          next[next.length - 1] = {
            ...last,
            content: res.ta_response ?? last.content,
            metadata: { interpreted_units: res.interpreted_units },
          };
        }
        return next;
      });
      if (taId != null) {
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "state"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "misconceptions"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "history"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "messages"] });
      }
    } catch (err) {
      const errMsg = "Error: " + (err instanceof Error ? err.message : "Failed");
      setLocalMessages((m) => {
        const next = [...m];
        const last = next[next.length - 1];
        if (last?.role === "ta" && last.metadata?.streaming) {
          next[next.length - 1] = { ...last, content: errMsg, metadata: { failed: true, lastInput: text } };
          return next;
        }
        return [...next, { role: "ta" as const, content: errMsg, timestamp: formatRelative(new Date().toISOString()), metadata: { failed: true, lastInput: text } }];
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleRetry = (lastInput: string) => {
    if (!taId || !lastInput.trim()) return;
    setLocalMessages((m) => m.slice(0, -2));
    setLoading(true);
    const studentMsg: ChatMessage = {
      role: "student",
      content: lastInput,
      timestamp: formatRelative(new Date().toISOString()),
    };
    teach(taId, lastInput)
      .then((res) => {
        const taMsg: ChatMessage = {
          role: "ta",
          content: res.ta_response ?? "OK.",
          timestamp: formatRelative(new Date().toISOString()),
          metadata: { interpreted_units: res.interpreted_units, quality_score: res.quality_score },
        };
        setLocalMessages((m) => [...m, studentMsg, taMsg]);
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "state"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "misconceptions"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "history"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "messages"] });
      })
      .catch((err) => {
        const taMsg: ChatMessage = {
          role: "ta",
          content: "Error: " + (err instanceof Error ? err.message : "Failed"),
          timestamp: formatRelative(new Date().toISOString()),
          metadata: { failed: true, lastInput },
        };
        setLocalMessages((m) => [...m, studentMsg, taMsg]);
      })
      .finally(() => setLoading(false));
  };

  const taMessageCount = messages.filter((m) => m.role === "ta").length;

  return (
    <div className="flex h-full flex-col">
      <div className="flex flex-wrap items-center justify-end gap-2 border-b border-slate-200 px-3 py-2 dark:border-slate-700">
        <ModeIndicator taMessageCount={taMessageCount} compact />
      </div>
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
            onRetry={
              msg.metadata?.failed && msg.metadata?.lastInput
                ? () => handleRetry(msg.metadata!.lastInput!)
                : undefined
            }
          />
        ))}
        {loading && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
      <div className="border-t border-slate-200 p-3">
        {teachingHelperResult && (
          <div className="mb-3">
            <TeachingHelper
              result={teachingHelperResult}
              onDismiss={() => { setTeachingHelperResult(null); setPendingInput(null); }}
            />
          </div>
        )}
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <textarea
              placeholder="Type to teach... (Shift+Enter for new line)"
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              className="w-full min-h-[40px] max-h-32 resize-y rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm placeholder:text-slate-400 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 focus:outline-none disabled:bg-slate-50 disabled:text-slate-500"
              disabled={!taId || loading}
              rows={2}
              maxLength={MAX_INPUT_LENGTH}
            />
            <div className="absolute bottom-1 right-2">
              <QualityIndicator 
                length={input.length} 
                maxLength={MAX_INPUT_LENGTH} 
                qualityResult={teachingHelperResult}
              />
            </div>
          </div>
          <Button
            variant="outline"
            onClick={handleCheckQuality}
            disabled={!taId || loading || !input.trim() || isCheckingQuality}
            loading={isCheckingQuality}
            className="shrink-0"
            title="Check teaching quality"
          >
            Check
          </Button>
          <Button
            icon={Send}
            onClick={handleSend}
            disabled={!taId || !input.trim() || loading || input.length > MAX_INPUT_LENGTH}
            title="Send message"
          >
            Send
          </Button>
        </div>
      </div>
    </div>
  );
}
