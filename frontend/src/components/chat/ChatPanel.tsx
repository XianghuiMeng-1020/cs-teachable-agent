import { useState, useRef, useEffect, useCallback } from "react";
import { useTranslation } from "react-i18next";
import { useQueryClient, useQuery } from "@tanstack/react-query";
import { motion, AnimatePresence } from "framer-motion";
import { Send, AlertCircle, CheckCircle, BarChart3, BookOpen, Lightbulb, Sparkles, Bot, ChevronDown } from "lucide-react";
import { teachStream, getMessages, analyzeTeaching, getProactiveCheckin } from "@/api/client";
import { Button } from "@/components/ui/Button";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { TeachingHelper, type TeachingHelperResult } from "./TeachingHelper";
import { ModeIndicator } from "./ModeIndicator";
import { formatRelative } from "@/lib/utils";
import { useTypingCadence } from "@/components/assessment/AntiCheatShell";
import { emitTelemetry } from "@/lib/telemetry";

export interface ChatMessage {
  role: "student" | "ta" | "thinking";
  content: string;
  timestamp?: string;
  metadata?: {
    interpreted_units?: string[];
    quality_score?: number;
    failed?: boolean;
    lastInput?: string;
    streaming?: boolean;
    proactive?: boolean;
  };
}

interface ChatPanelProps {
  taId: number | null;
  problemContext?: { problem_id: string; problem_type: string } | undefined;
  lineRef?: string | null;
  onLineRefUsed?: () => void;
}

const MAX_INPUT_LENGTH = 2000;
const MIN_QUALITY_INPUT_LENGTH = 15;
const QUALITY_CHECK_DEBOUNCE_MS = 400;
const MIN_INPUT_ROWS = 2;
const MAX_INPUT_ROWS = 8;

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

// Auto-resize textarea hook
function useAutoResizeTextarea(minRows: number, maxRows: number) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [rows, setRows] = useState(minRows);

  const adjustHeight = useCallback((value: string) => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Reset to measure
    textarea.rows = minRows;

    // Calculate new rows based on scroll height
    const lineHeight = parseInt(getComputedStyle(textarea).lineHeight, 10) || 20;
    const padding = parseInt(getComputedStyle(textarea).paddingTop, 10) +
                   parseInt(getComputedStyle(textarea).paddingBottom, 10);
    const contentHeight = textarea.scrollHeight - padding;
    const newRows = Math.min(
      maxRows,
      Math.max(minRows, Math.ceil(contentHeight / lineHeight))
    );

    setRows(newRows);
  }, [minRows, maxRows]);

  return { textareaRef, rows, adjustHeight };
}

// Enhanced Quality indicator component with dark mode support
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
      <div className="flex items-center gap-1.5 text-xs text-rose-600 dark:text-rose-400 font-medium">
        <AlertCircle className="w-3.5 h-3.5" />
        <span>{length}/{maxLength}</span>
      </div>
    );
  }

  if (qualityResult) {
    const isGood = qualityResult.pattern === "good";
    return (
      <div className={`flex items-center gap-1.5 text-xs font-medium ${isGood ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'}`}>
        {isGood ? <CheckCircle className="w-3.5 h-3.5" /> : <AlertCircle className="w-3.5 h-3.5" />}
        <span>
          {isGood
            ? t("chat.qualityGood", { defaultValue: "质量: 良好" })
            : t("chat.qualityNeedsImprovement", { defaultValue: "质量: 需改进" })}
        </span>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-1.5 text-xs font-medium ${isNearLimit ? 'text-amber-600 dark:text-amber-400' : 'text-stone-400 dark:text-stone-500'}`}>
      <BarChart3 className="w-3.5 h-3.5" />
      <span>{length}/{maxLength}</span>
    </div>
  );
}

// Enhanced keyboard shortcut hint with icons
function KeyboardHint() {
  return (
    <div className="flex items-center gap-2 text-[10px] text-stone-400 dark:text-stone-500 mt-1.5">
      <span className="flex items-center gap-1">
        <kbd className="px-1.5 py-0.5 rounded bg-stone-100 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 font-mono text-[9px]">
          Enter
        </kbd>
        <span>发送</span>
      </span>
      <span className="text-stone-300 dark:text-stone-600">|</span>
      <span className="flex items-center gap-1">
        <kbd className="px-1.5 py-0.5 rounded bg-stone-100 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 font-mono text-[9px]">
          Shift
        </kbd>
        <kbd className="px-1.5 py-0.5 rounded bg-stone-100 dark:bg-stone-800 border border-stone-200 dark:border-stone-700 font-mono text-[9px]">
          Enter
        </kbd>
        <span>换行</span>
      </span>
    </div>
  );
}

// Empty state with guided steps - enhanced with dark mode
function EmptyStateGuide({ onStart }: { onStart: () => void }) {
  const { t } = useTranslation();
  const steps = [
    {
      icon: BookOpen,
      title: t("chat.step1", { defaultValue: "阅读问题" }),
      desc: t("chat.step1Desc", { defaultValue: "理解代码应该做什么" }),
      color: "bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800"
    },
    {
      icon: Lightbulb,
      title: t("chat.step2", { defaultValue: "解释概念" }),
      desc: t("chat.step2Desc", { defaultValue: "一步步教AI代理逻辑" }),
      color: "bg-amber-50 dark:bg-amber-900/30 text-amber-600 dark:text-amber-400 border-amber-200 dark:border-amber-800"
    },
    {
      icon: Sparkles,
      title: t("chat.step3", { defaultValue: "观察学习" }),
      desc: t("chat.step3Desc", { defaultValue: "看代理如何应用你的教学" }),
      color: "bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800"
    },
  ];

  return (
    <div className="flex flex-col items-center justify-center h-full px-6 py-8 text-center">
      <motion.div
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ duration: 0.4 }}
        className="w-16 h-16 bg-gradient-to-br from-brand-100 to-brand-200 dark:from-brand-900/50 dark:to-brand-800/30 rounded-2xl flex items-center justify-center mb-4 shadow-lg"
      >
        <Bot className="w-8 h-8 text-brand-600 dark:text-brand-400" />
      </motion.div>

      <motion.h3
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="text-lg font-bold text-stone-800 dark:text-stone-200 mb-1"
      >
        {t("chat.emptyTitle", { defaultValue: "教你的AI代理" })}
      </motion.h3>

      <motion.p
        initial={{ y: 10, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ delay: 0.15 }}
        className="text-sm text-stone-500 dark:text-stone-400 mb-6 max-w-[240px]"
      >
        {t("chat.emptyDesc", { defaultValue: "通过清晰地解释概念来引导你的代理理解编程" })}
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
            <div className={`w-8 h-8 rounded-lg flex items-center justify-center bg-white/60 dark:bg-black/20`}>
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
        className="mt-6 flex items-center gap-2 text-xs font-medium text-brand-600 dark:text-brand-400 hover:text-brand-700 dark:hover:text-brand-300 transition-colors tap-target"
      >
        {t("chat.startTyping", { defaultValue: "在下方开始输入" })}
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
  const lastActivityRef = useRef<number>(Date.now());
  const lastProactiveAtRef = useRef<number>(0);
  const { textareaRef: inputRef, rows, adjustHeight } = useAutoResizeTextarea(MIN_INPUT_ROWS, MAX_INPUT_ROWS);

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
      // Adjust height after auto-insert
      setTimeout(() => adjustHeight(inputRef.current?.value || ""), 0);
    }
  }, [lineRef, loading, onLineRefUsed, inputRef, adjustHeight]);

  const { data: messagesData } = useQuery({
    queryKey: ["ta", taId, "messages"],
    queryFn: () => getMessages(taId!),
    enabled: !!taId,
  });

  // Auto quality check with optimized debounce (400ms)
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

  useEffect(() => {
    if (!taId) return;
    const timer = setInterval(async () => {
      if (loading) return;
      if (input.trim()) return;
      if (messages.length === 0) return;
      const now = Date.now();
      if (now - lastActivityRef.current < 60000) return;
      if (now - lastProactiveAtRef.current < 120000) return;
      try {
        const res = await getProactiveCheckin(taId);
        if (!res.message) return;
        setLocalMessages((m) => [
          ...m,
          {
            role: "ta",
            content: res.message,
            timestamp: formatRelative(new Date().toISOString()),
            metadata: { proactive: true },
          },
        ]);
        lastProactiveAtRef.current = Date.now();
      } catch {
        // ignore proactive checkin errors
      }
    }, 15000);
    return () => clearInterval(timer);
  }, [taId, loading, input, messages.length]);

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
      lastActivityRef.current = Date.now();
      adjustHeight(newValue);
      if (Math.abs(newValue.length - (lastCheckRef.current?.length ?? 0)) > 10) {
        debouncedQualityCheck(newValue);
      }
    }
  };

  const handleSend = async () => {
    if (!taId || !input.trim()) return;
    const text = input.trim();
    lastActivityRef.current = Date.now();
    trackResponseTime(sendTimestampRef.current);
    sendTimestampRef.current = Date.now();
    setInput("");
    setTeachingHelperResult(null);
    adjustHeight(""); // Reset height
    const now = new Date().toISOString();
    setLocalMessages((m) => [
      ...m,
      { role: "student", content: text, timestamp: formatRelative(now) },
    ]);
    setLoading(true);
    const streamedContent = { current: "" };
    const thinkingRef = { current: "" };
    setLocalMessages((m) => [
      ...m,
      {
        role: "thinking",
        content: "🤔 TA is thinking...",
        timestamp: formatRelative(new Date().toISOString()),
      },
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
            // Find the TA streaming message (skip thinking message)
            const taIdx = next.findIndex((m, i) => i > 0 && m.role === "ta" && m.metadata?.streaming);
            if (taIdx !== -1) {
              next[taIdx] = { ...next[taIdx], content: streamedContent.current };
            }
            return next;
          });
        },
        onThinking: (thinkingText) => {
          thinkingRef.current = thinkingText;
          setLocalMessages((prev) => {
            const next = [...prev];
            const thinkingIdx = next.findIndex((m) => m.role === "thinking");
            if (thinkingIdx !== -1) {
              next[thinkingIdx] = { ...next[thinkingIdx], content: thinkingText };
            }
            return next;
          });
        },
      });
      lastActivityRef.current = Date.now();
      setLocalMessages((m) => {
        const next = [...m];
        // Remove thinking message and update TA message
        const filtered = next.filter((msg) => msg.role !== "thinking");
        const taIdx = filtered.findIndex((m) => m.role === "ta" && m.metadata?.streaming);
        if (taIdx !== -1) {
          filtered[taIdx] = {
            ...filtered[taIdx],
            content: res.ta_response ?? filtered[taIdx].content,
            metadata: { interpreted_units: res.interpreted_units },
          };
        }
        return filtered;
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
        // Remove thinking message and update TA message
        const filtered = next.filter((msg) => msg.role !== "thinking");
        const taIdx = filtered.findIndex((m) => m.role === "ta" && m.metadata?.streaming);
        if (taIdx !== -1) {
          filtered[taIdx] = { ...filtered[taIdx], content: errMsg, metadata: { failed: true, lastInput: text } };
          return filtered;
        }
        return [...filtered, { role: "ta" as const, content: errMsg, timestamp: formatRelative(new Date().toISOString()), metadata: { failed: true, lastInput: text } }];
      });
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    // Support both Ctrl+Enter and plain Enter for sending
    if ((e.key === "Enter" && !e.shiftKey && !e.isComposing) ||
        (e.key === "Enter" && (e.metaKey || e.ctrlKey))) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleRetry = (lastInput: string) => {
    if (!taId || !lastInput.trim()) return;
    setLocalMessages((m) => m.slice(0, -2));
    setLoading(true);
    lastActivityRef.current = Date.now();
    const studentMsg: ChatMessage = {
      role: "student",
      content: lastInput,
      timestamp: formatRelative(new Date().toISOString()),
    };
    const streamedContent = { current: "" };
    setLocalMessages((m) => [
      ...m,
      studentMsg,
      {
        role: "ta",
        content: "",
        timestamp: formatRelative(new Date().toISOString()),
        metadata: { streaming: true },
      },
    ]);
    teachStream(taId, lastInput, {
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
    })
      .then((res) => {
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
        setLocalMessages((m) => [...m, taMsg]);
      })
      .finally(() => setLoading(false));
  };

  const taMessageCount = messages.filter((m) => m.role === "ta").length;
  const hasMessages = messages.length > 0 || loading;

  return (
    <div className="flex h-full flex-col bg-white dark:bg-surfaceDark-card transition-colors duration-300">
      {/* Enhanced Header with dark mode */}
      <div className="flex items-center justify-between border-b border-stone-200 dark:border-stone-700 px-4 py-3">
        <div className="flex items-center gap-3">
          {/* AI Agent avatar */}
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-100 to-brand-200 dark:from-brand-900/50 dark:to-brand-800/30 flex items-center justify-center shadow-sm">
            <Bot className="w-5 h-5 text-brand-600 dark:text-brand-400" />
          </div>
          <div>
            <p className="text-sm font-semibold text-stone-800 dark:text-stone-200">AI Agent</p>
            <div className="flex items-center gap-1.5 text-xs text-stone-500 dark:text-stone-400">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              {t("chat.readyToLearn", { defaultValue: "准备好学习" })}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <ModeIndicator taMessageCount={taMessageCount} compact />
          {taMessageCount > 0 && (
            <span className="text-xs text-stone-400 dark:text-stone-500 bg-stone-100 dark:bg-stone-800 px-2 py-0.5 rounded-full">
              {taMessageCount} {t("chat.messages", { defaultValue: "条消息" })}
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
                  key={`${msg.role}-${msg.timestamp ?? "no-ts"}-${msg.content.slice(0, 24)}-${i}`}
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

      {/* Enhanced Input area with auto-resize and dark mode */}
      <div className="border-t border-stone-200 dark:border-stone-700 p-4 bg-stone-50/50 dark:bg-stone-900/50">
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

        <div className="flex gap-3 items-end">
          <div className="flex-1 relative">
            <textarea
              ref={inputRef}
              placeholder={t("chat.inputPlaceholder", {
                defaultValue: "解释概念来教你的AI代理...",
              })}
              value={input}
              onChange={handleInputChange}
              onInput={onTypingInput}
              onKeyDown={handleKeyDown}
              data-allow-clipboard="true"
              className="w-full resize-none rounded-xl border border-stone-300 dark:border-stone-600 bg-white dark:bg-surfaceDark-card px-4 py-3 text-sm text-ink dark:text-inkDark placeholder:text-stone-400 dark:placeholder:text-stone-500 focus:border-brand-500 dark:focus:border-brand-400 focus:ring-2 focus:ring-brand-500/20 dark:focus:ring-brand-400/20 focus:outline-none disabled:bg-stone-100 dark:disabled:bg-stone-800 disabled:text-stone-500 dark:disabled:text-stone-600 transition-all shadow-sm dark:shadow-none"
              disabled={!taId || loading}
              rows={rows}
              maxLength={MAX_INPUT_LENGTH}
              aria-label={t("chat.inputAriaLabel", { defaultValue: "输入教学说明" })}
              aria-describedby="input-hint"
            />
            <div className="absolute bottom-2 right-3">
              <QualityIndicator
                length={input.length}
                maxLength={MAX_INPUT_LENGTH}
                qualityResult={teachingHelperResult}
              />
            </div>
            {/* Enhanced keyboard hint */}
            <div id="input-hint">
              <KeyboardHint />
            </div>
          </div>

          <Button
            variant="outline"
            onClick={handleCheckQuality}
            disabled={!taId || loading || !input.trim() || isCheckingQuality}
            loading={isCheckingQuality}
            className="shrink-0 h-[52px] px-4 tap-target"
            title={t("chat.checkTeachingQualityTitle", { defaultValue: "检查教学质量" })}
            aria-label={t("chat.checkTeachingQualityTitle", { defaultValue: "检查教学质量" })}
          >
            {t("chat.check", { defaultValue: "检查" })}
          </Button>

          <Button
            icon={Send}
            onClick={handleSend}
            disabled={!taId || !input.trim() || loading || input.length > MAX_INPUT_LENGTH}
            title={t("chat.sendMessageTitle", { defaultValue: "发送消息" })}
            className="shrink-0 h-[52px] px-5 bg-brand-600 hover:bg-brand-700 text-white tap-target"
            aria-label={t("chat.sendMessageTitle", { defaultValue: "发送消息" })}
          >
            {t("chat.send", { defaultValue: "发送" })}
          </Button>
        </div>
      </div>
    </div>
  );
}
