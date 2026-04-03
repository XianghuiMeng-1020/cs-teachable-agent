import { useState, useRef, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useQueryClient, useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Send, MessageCircle, AlertCircle, CheckCircle, BarChart3, BookOpen, Lightbulb, Sparkles, Bot, ChevronDown } from "lucide-react";
import { teach, teachStream, getMessages, analyzeTeaching } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { TeachingHelper, type TeachingHelperResult } from "./TeachingHelper";
import { ModeIndicator } from "./ModeIndicator";
import { formatRelative } from "@/lib/utils";
import { useTypingCadence } from "@/components/assessment/AntiCheatShell";
import { emitTelemetry } from "@/lib/telemetry";

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
  problemContext?: { problem_id: string; problem_type: string } | undefined;
  lineRef?: string | null;
  onLineRefUsed?: () => void;
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

// Enhanced Quality indicator component
function QualityIndicator({ 
  length, 
  maxLength, 
  qualityResult 
}: { 
  length: number; 
  maxLength: number; 
  qualityResult: TeachingHelperResult | null;
}) {
  const { t } = useTranslation();
  const isNearLimit = length > maxLength * 0.9;
  const isOverLimit = length > maxLength;
  
  if (isOverLimit) {
    return (
      <div className="flex items-center gap-1.5 text-xs text-rose-600 font-medium">
        <AlertCircle className="w-3.5 h-3.5" />
        <span>{length}/{maxLength}</span>
      </div>
    );
  }
  
  if (qualityResult) {
    const isGood = qualityResult.pattern === "good";
    return (
      <div className={`flex items-center gap-1.5 text-xs font-medium ${isGood ? 'text-emerald-600' : 'text-amber-600'}`}>
        {isGood ? <CheckCircle className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
        <span>
          {isGood
            ? t("chat.qualityGood", { defaultValue: "Quality: Good" })
            : t("chat.qualityNeedsImprovement", { defaultValue: "Quality: Needs improvement" })}
        </span>
      </div>
    );
  }
  
  return (
    <div className={`flex items-center gap-1.5 text-xs font-medium ${isNearLimit ? 'text-amber-600' : 'text-stone-400'}`}>
      <BarChart3 className="w-3.5 h-3.5" />
      <span>{length}/{maxLength}</span>
    </div>
  );
}

// Empty state with guided steps
function EmptyStateGuide({ onStart }: { onStart: () => void }) {
  const { t } = useTranslation();
  const steps = [
    { 
      icon: BookOpen, 
      title: "Read the Problem", 
      desc: "Understand what the code should do",
      color: "bg-blue-50 text-blue-600 border-blue-200"
    },
    { 
      icon: Lightbulb, 
      title: "Explain the Concept", 
      desc: "Teach the AI agent the logic step by step",
      color: "bg-amber-50 text-amber-600 border-amber-200"
    },
    { 
      icon: Sparkles, 
      title: "Watch it Learn", 
      desc: "See the agent apply your teaching to solve it",
      color: "bg-emerald-50 text-emerald-600 border-emerald-200"
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full px-6 py-8 text-center">
      <motion.div 
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="w-16 h-16 bg-gradient-to-br from-brand-100 to-brand-200 rounded-2xl flex items-center justify-center mb-4 shadow-lg"
      >
        <Bot className="w-8 h-8 text-brand-600" />
      </motion.div>
      
      <motion.h3 
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="text-lg font-bold text-stone-800 mb-1"
      >
        Teach Your AI Agent
      </motion.h3>
      
      <motion.p 
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.15 }}
        className="text-sm text-stone-500 mb-6 max-w-[240px]"
      >
        Guide your agent to understand programming by explaining concepts clearly
      </motion.p>
      
      {/* Step cards */}
      <motion.div 
        initial={{ y: 20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="w-full max-w-[280px] space-y-2"
      >
        {steps.map((step, i) => (
          <div 
            key={i} 
            className={`flex items-center gap-3 p-2.5 rounded-xl border ${step.color} transition-transform hover:scale-[1.02] cursor-default`}
          >
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center bg-white/60`}>
              <step.icon className="w-4 h-4" />
            </div>
            <div className="text-left">
              <p className="text-xs font-semibold">{step.title}</p>
              <p className="text-[10px] opacity-80">{step.desc}</p>
            </div>
          </div>
        ))}
      </motion.div>
      
      <motion.button
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.35 }}
        onClick={onStart}
        className="mt-6 flex items-center gap-2 text-xs font-medium text-brand-600 hover:text-brand-700 transition-colors"
      >
        Start by typing below
        <motion.div
          animate={{ y: [0, 4, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
        >
          <ChevronDown className="w-4 h-4" />
        </motion.div>
      </motion.button>
    </div>
  );
}

export function ChatPanel({ taId, problemContext, lineRef, onLineRefUsed }: ChatPanelProps) {
  const { t } = useTranslation();
  const queryClient = useQueryClient();
  const [input, setInput] = useState("");
  const [localMessages, setLocalMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [teachingHelperResult, setTeachingHelperResult] = useState<TeachingHelperResult | null>(null);
  const [isCheckingQuality, setIsCheckingQuality] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);
  const lastCheckRef = useRef<string>("");
  const sendTimestampRef = useRef<number>(0);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Anti-cheat: detect rapid paste-like typing
  const onTypingInput = useTypingCadence(25, 400);

  // Anti-cheat: track response time for abnormally fast answers
  const trackResponseTime = useCallback((startMs: number) => {
    const elapsed = Date.now() - startMs;
    if (elapsed < 3000 && input.length > 50) {
      emitTelemetry("typing_anomaly", { responseTimeMs: elapsed, inputLength: input.length, type: "rapid_response" });
    }
  }, [input.length]);

  // Auto-insert line reference from problem panel
  useEffect(() => {
    if (lineRef && !loading) {
      setInput((prev) => {
        const prefix = prev.trim() ? prev.trim() + "\n" : "";
        return prefix + lineRef + " ";
      });
      onLineRefUsed?.();
      inputRef.current?.focus();
    }
  }, [lineRef, loading, onLineRefUsed]);

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
    
    if (text === lastCheckRef.current && teachingHelperResult) return;
    
    setIsCheckingQuality(true);
    try {
      const result = await analyzeTeaching(taId, text.trim());
      setTeachingHelperResult(result);
      lastCheckRef.current = text;
    } catch {
      // Silently fail
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
      if (Math.abs(newValue.length - (lastCheckRef.current?.length ?? 0)) > 10) {
        debouncedQualityCheck(newValue);
      }
    }
  };

  const handleSend = async () => {
    if (!taId || !input.trim()) return;
    const text = input.trim();
    trackResponseTime(sendTimestampRef.current);
    sendTimestampRef.current = Date.now();
    setInput("");
    setTeachingHelperResult(null);
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
        problemId: problemContext?.problem_id,
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
      if (res.code_modification) {
        window.dispatchEvent(new CustomEvent("ta-code-modification", {
          detail: { modification: res.code_modification },
        }));
      }
      if (taId != null) {
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "state"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "misconceptions"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "history"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "messages"] });
        queryClient.invalidateQueries({ queryKey: ["ta", taId, "problems"] });
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
  const hasMessages = messages.length > 0 || loading;

  return (
    <div className="flex h-full flex-col bg-white">
      {/* Enhanced Header */}
      <div className="flex items-center justify-between border-b border-stone-200 px-4 py-3">
        <div className="flex items-center gap-3">
          {/* AI Agent avatar */}
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-100 to-brand-200 flex items-center justify-center shadow-sm">
            <Bot className="w-5 h-5 text-brand-600" />
          </div>
          <div>
            <p className="text-sm font-semibold text-stone-800">AI Agent</p>
            <div className="flex items-center gap-1.5 text-xs text-stone-500">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
              Ready to learn
            </div>
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <ModeIndicator taMessageCount={taMessageCount} compact />
          {taMessageCount > 0 && (
            <span className="text-xs text-stone-400 bg-stone-100 px-2 py-0.5 rounded-full">
              {taMessageCount} messages
            </span>
          )}
        </div>
      </div>

      {/* Messages area with empty state */}
      <div className="flex-1 overflow-y-auto custom-scrollbar">
        <AnimatePresence mode="wait">
          {!hasMessages ? (
            <motion.div
              key="empty"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="h-full"
            >
              <EmptyStateGuide onStart={() => inputRef.current?.focus()} />
            </motion.div>
          ) : (
            <motion.div
              key="messages"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="px-4 py-4 space-y-4"
            >
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
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Enhanced Input area */}
      <div className="border-t border-stone-200 p-4 bg-stone-50/50">
        <AnimatePresence>
          {teachingHelperResult && (
            <motion.div 
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="mb-3"
            >
              <TeachingHelper
                result={teachingHelperResult}
                onDismiss={() => { setTeachingHelperResult(null); }}
              />
            </motion.div>
          )}
        </AnimatePresence>
        
        <div className="flex gap-3">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              placeholder={t("chat.inputPlaceholder", {
                defaultValue: "Explain the concept to teach your AI agent...",
              })}
              value={input}
              onChange={handleInputChange}
              onInput={onTypingInput}
              onKeyDown={handleKeyDown}
              data-allow-clipboard="true"
              className="w-full min-h-[52px] max-h-40 resize-y rounded-xl border border-stone-300 bg-white px-4 py-3 text-sm placeholder:text-stone-400 focus:border-brand-500 focus:ring-2 focus:ring-brand-500/20 focus:outline-none disabled:bg-stone-100 disabled:text-stone-500 transition-all shadow-sm"
              disabled={!taId || loading}
              rows={2}
              maxLength={MAX_INPUT_LENGTH}
            />
            <div className="absolute bottom-2 right-3">
              <QualityIndicator 
                length={input.length} 
                maxLength={MAX_INPUT_LENGTH} 
                qualityResult={teachingHelperResult}
              />
            </div>
            {/* Shift+Enter hint */}
            <div className="absolute -bottom-5 right-0 text-[10px] text-stone-400">
              Shift+Enter for new line
            </div>
          </div>
          
          <Button
            variant="outline"
            onClick={handleCheckQuality}
            disabled={!taId || loading || !input.trim() || isCheckingQuality}
            loading={isCheckingQuality}
            className="shrink-0 h-[52px] px-4"
            title={t("chat.checkTeachingQualityTitle", { defaultValue: "Check teaching quality" })}
          >
            {t("chat.check", { defaultValue: "Check" })}
          </Button>
          
          <Button
            icon={Send}
            onClick={handleSend}
            disabled={!taId || !input.trim() || loading || input.length > MAX_INPUT_LENGTH}
            title={t("chat.sendMessageTitle", { defaultValue: "Send message" })}
            className="shrink-0 h-[52px] px-5 bg-brand-600 hover:bg-brand-700 text-white"
          >
            {t("chat.send", { defaultValue: "Send" })}
          </Button>
        </div>
      </div>
    </div>
  );
}
