"use client";

import Link from "next/link";
import {
  ArrowForwardRounded,
  CheckCircleRounded,
  LockOutlined,
  RefreshRounded,
  ReplayRounded
} from "@mui/icons-material";
import {
  Alert,
  alpha,
  Box,
  Button,
  Chip,
  CircularProgress,
  Divider,
  LinearProgress,
  Paper,
  Slider,
  Stack,
  TextField,
  Typography
} from "@mui/material";
import { useEffect, useMemo, useRef, useState, type DragEventHandler, type ReactNode } from "react";
import {
  buildOpenAIHintRequestBody,
  DEFAULT_OPENAI_HINT_MODEL,
  normalizeHintBody,
  normalizeHintTarget,
  normalizeHintTitle,
  parseHintModelOutput,
  type OpenAIResponsesPayload
} from "@/src/hints/openai-hint";
import type {
  StudentGradeResponse,
  StudentHintRequest,
  StudentHintResponse,
  StudentHintType,
  StudentTaskListItem,
  StudentTaskResponse,
  StudentTelemetryEvent,
  StudentTelemetryEventType
} from "@/src/types";

type BlockOption = {
  id: string;
  text: string;
};

type AttemptStatus = {
  attempted: boolean;
  correct: boolean;
};

type DragState = {
  source: "available" | "answer";
  optionId: string;
};

type FocusLossEvent = {
  timestamp: string;
  reason: "window-blur" | "tab-hidden";
};

type HintRating = "helpful" | "unhelpful" | null;

type HintHistoryRecord = StudentHintResponse & {
  reflection: string;
  rating: HintRating;
  escalationNotes: string;
  escalated: boolean;
  createdAt: string;
};

const QUICK_START_STORAGE_KEY = "assessment-studio-quick-start-dismissed";
const DEV_BROWSER_HINTS_ALLOWED = process.env.NODE_ENV !== "production";
const EXTERNAL_HINT_API_BASE_URL = process.env.NEXT_PUBLIC_HINT_API_BASE_URL?.trim() ?? "";
const DEV_BROWSER_HINT_MODEL = DEFAULT_OPENAI_HINT_MODEL;
const HINT_LIMITS: Record<StudentHintType, number> = {
  understand: 1,
  "next-step": 2,
  "check-one-issue": 2
};

export default function HomePage() {
  const [maxAiPassRate, setMaxAiPassRate] = useState<number>(75);
  const [items, setItems] = useState<StudentTaskListItem[]>([]);
  const [selectedKey, setSelectedKey] = useState<string>("");
  const [task, setTask] = useState<StudentTaskResponse | null>(null);
  const [availableOptions, setAvailableOptions] = useState<BlockOption[]>([]);
  const [answerOptions, setAnswerOptions] = useState<BlockOption[]>([]);
  const [dropdownOptions, setDropdownOptions] = useState<Record<string, string[]>>({});
  const [responseValues, setResponseValues] = useState<Record<string, string>>({});
  const [feedback, setFeedback] = useState<StudentGradeResponse | null>(null);
  const [taskListLoading, setTaskListLoading] = useState(true);
  const [taskLoading, setTaskLoading] = useState(false);
  const [grading, setGrading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);
  const [attemptHistory, setAttemptHistory] = useState<Record<string, AttemptStatus>>({});
  const [dragState, setDragState] = useState<DragState | null>(null);
  const [practiceLocked, setPracticeLocked] = useState(false);
  const [focusEvents, setFocusEvents] = useState<FocusLossEvent[]>([]);
  const [showQuickStart, setShowQuickStart] = useState(false);
  const [sessionId] = useState(() => createClientId("session"));
  const [currentAttemptId, setCurrentAttemptId] = useState<string | null>(null);
  const [currentAttemptNumber, setCurrentAttemptNumber] = useState<number>(0);
  const lastFocusEventRef = useRef(0);
  const attemptCountersRef = useRef<Record<string, number>>({});
  const attemptStartedAtRef = useRef<string | null>(null);
  const currentAttemptFocusLossCountRef = useRef(0);
  const prefetchedTaskKeyRef = useRef<string | null>(null);

  const selectedItem = useMemo(
    () => items.find((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey) ?? null,
    [items, selectedKey]
  );

  const progress = useMemo(() => {
    const statuses = Object.values(attemptHistory);
    return {
      attempted: statuses.filter((status) => status.attempted).length,
      correct: statuses.filter((status) => status.correct).length
    };
  }, [attemptHistory]);

  const latestFocusEvent = focusEvents[0] ?? null;

  const currentIndex = useMemo(() => {
    if (!selectedItem) {
      return 0;
    }
    const index = items.findIndex((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey);
    return index >= 0 ? index + 1 : 0;
  }, [items, selectedItem, selectedKey]);

  const attemptedPercent = items.length === 0 ? 0 : (progress.attempted / items.length) * 100;
  const viewingPercent = items.length === 0 ? 0 : (currentIndex / items.length) * 100;
  const readyToSubmit = task
    ? task.itemType === "parsons"
      ? answerOptions.length === task.requiredBlockCount
      : task.itemType === "dropdown"
        ? task.blanks.every((blank) => {
            const selected = responseValues[blank.blankId];
            return typeof selected === "string" && selected.trim().length > 0;
          })
        : task.checkpoints.every((checkpoint) => {
            const selected = responseValues[checkpoint.checkpointId];
            return typeof selected === "string" && selected.trim().length > 0;
          })
    : false;

  const hintProgressSummary = useMemo(() => {
    if (!task) {
      return "";
    }

    if (task.itemType === "parsons") {
      return `${answerOptions.length}/${task.requiredBlockCount} blocks placed`;
    }

    if (task.itemType === "dropdown") {
      const answeredCount = task.blanks.filter((blank) => {
        const selected = responseValues[blank.blankId];
        return typeof selected === "string" && selected.trim().length > 0;
      }).length;
      return `${answeredCount}/${task.requiredBlankCount} blanks answered`;
    }

    const answeredCount = task.checkpoints.filter((checkpoint) => {
      const selected = responseValues[checkpoint.checkpointId];
      return typeof selected === "string" && selected.trim().length > 0;
    }).length;
    return `${answeredCount}/${task.requiredCheckpointCount} checkpoints answered`;
  }, [task, answerOptions.length, responseValues]);

  function buildTelemetryEvent(
    eventType: StudentTelemetryEventType,
    payload: Record<string, unknown>,
    overrides?: Partial<StudentTelemetryEvent>
  ): StudentTelemetryEvent {
    return {
      eventId: createClientId("evt"),
      sessionId,
      attemptId: currentAttemptId,
      attemptNumber: currentAttemptNumber || null,
      queryId: task?.queryId ?? selectedItem?.queryId ?? null,
      taskId: task?.taskId ?? selectedItem?.taskId ?? null,
      itemId: task?.itemId ?? selectedItem?.itemId ?? null,
      itemType: task?.itemType ?? selectedItem?.itemType ?? null,
      eventType,
      eventTime: new Date().toISOString(),
      payload,
      ...overrides
    };
  }

  async function sendTelemetry(events: StudentTelemetryEvent[]) {
    if (events.length === 0) {
      return;
    }

    try {
      await fetch("/api/studio/student/telemetry", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ events }),
        keepalive: true
      });
    } catch {
      // Ignore telemetry failures during practice.
    }
  }

  function emitTelemetry(
    eventType: StudentTelemetryEventType,
    payload: Record<string, unknown>,
    overrides?: Partial<StudentTelemetryEvent>
  ) {
    void sendTelemetry([buildTelemetryEvent(eventType, payload, overrides)]);
  }

  useEffect(() => {
    void loadEligibleItems(maxAiPassRate);
  }, [maxAiPassRate]);

  useEffect(() => {
    try {
      setShowQuickStart(window.localStorage.getItem(QUICK_START_STORAGE_KEY) !== "1");
    } catch {
      setShowQuickStart(true);
    }
  }, []);

  useEffect(() => {
    const startedAt = new Date().toISOString();
    void sendTelemetry([
      {
        eventId: createClientId("evt"),
        sessionId,
        eventType: "session_started",
        eventTime: startedAt,
        payload: {
          maxAiPassRate,
          userAgent: typeof navigator !== "undefined" ? navigator.userAgent : "unknown",
          viewport:
            typeof window !== "undefined"
              ? { width: window.innerWidth, height: window.innerHeight }
              : null
        }
      }
    ]);

    return () => {
      if (typeof navigator !== "undefined" && typeof navigator.sendBeacon === "function") {
        const event = {
          eventId: createClientId("evt"),
          sessionId,
          eventType: "session_ended",
          eventTime: new Date().toISOString(),
          payload: {}
        } satisfies StudentTelemetryEvent;
        const blob = new Blob([JSON.stringify({ events: [event] })], { type: "application/json" });
        navigator.sendBeacon("/api/studio/student/telemetry", blob);
      }
    };
  }, [sessionId]);

  useEffect(() => {
    if (items.length === 0) {
      setSelectedKey("");
      setTask(null);
      setAvailableOptions([]);
      setAnswerOptions([]);
      setDropdownOptions({});
      setResponseValues({});
      return;
    }

    const exists = items.some((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey);
    if (!exists) {
      setSelectedKey(makeKey(items[0].queryId, items[0].taskId, items[0].itemType));
    }
  }, [items, selectedKey]);

  useEffect(() => {
    if (!selectedItem) {
      return;
    }
    const nextKey = makeKey(selectedItem.queryId, selectedItem.taskId, selectedItem.itemType);
    if (prefetchedTaskKeyRef.current === nextKey) {
      prefetchedTaskKeyRef.current = null;
      return;
    }
    void loadTask(selectedItem.queryId, selectedItem.taskId, selectedItem.itemType);
  }, [selectedItem?.queryId, selectedItem?.taskId, selectedItem?.itemType]);

  useEffect(() => {
    function recordFocusLoss(reason: FocusLossEvent["reason"]) {
      const now = Date.now();
      if (now - lastFocusEventRef.current < 500) {
        return;
      }

      lastFocusEventRef.current = now;
      currentAttemptFocusLossCountRef.current += 1;
      setPracticeLocked(true);
      const event = {
        timestamp: new Date().toISOString(),
        reason
      } satisfies FocusLossEvent;
      setFocusEvents((current) => [event, ...current].slice(0, 12));
      emitTelemetry(
        "focus_lost",
        {
          reason,
          focusLossCountInAttempt: currentAttemptFocusLossCountRef.current
        },
        {
          eventTime: event.timestamp
        }
      );
    }

    function handleVisibilityChange() {
      if (document.visibilityState === "hidden") {
        recordFocusLoss("tab-hidden");
      }
    }

    function handleWindowBlur() {
      recordFocusLoss("window-blur");
    }

    window.addEventListener("blur", handleWindowBlur);
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      window.removeEventListener("blur", handleWindowBlur);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [
    currentAttemptId,
    currentAttemptNumber,
    selectedItem?.itemId,
    selectedItem?.itemType,
    selectedItem?.queryId,
    selectedItem?.taskId,
    task?.itemId,
    task?.itemType,
    task?.queryId,
    task?.taskId
  ]);

  function applyLoadedTask(nextTask: StudentTaskResponse) {
    setTask(nextTask);
    emitTelemetry(
      "task_loaded",
      {
        queryId: nextTask.queryId,
        taskId: nextTask.taskId,
        itemType: nextTask.itemType,
        aiPassRate: nextTask.aiPassRate
      },
      {
        queryId: nextTask.queryId,
        taskId: nextTask.taskId,
        itemId: nextTask.itemId,
        itemType: nextTask.itemType
      }
    );
    resetAttempt(nextTask, "task_loaded");
  }

  async function loadEligibleItems(threshold: number, forceRefresh = false) {
    setTaskListLoading(true);
    setErrorMessage(null);

    try {
      const params = new URLSearchParams({
        maxAiPassRate: String(threshold)
      });
      if (forceRefresh) {
        params.set("refresh", "1");
      }

      const response = await fetch(`/api/studio/student/index?${params.toString()}`, {
        cache: "no-store"
      });
      const payload = (await response.json()) as {
        items?: StudentTaskListItem[];
        initialTask?: StudentTaskResponse | null;
        error?: string;
      };
      if (!response.ok) {
        throw new Error(payload.error ?? "Failed to load student tasks.");
      }
      const nextItems = payload.items ?? [];
      setItems(nextItems);
      setStatusMessage(
        `Loaded ${nextItems.length} assessment item${nextItems.length === 1 ? "" : "s"} with AI pass <= ${threshold}%.`
      );

      const selectedStillExists = nextItems.some((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey);
      if (selectedStillExists) {
        if (forceRefresh) {
          const selected = nextItems.find((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey);
          if (selected) {
            void loadTask(selected.queryId, selected.taskId, selected.itemType, true);
          }
        }
        return;
      }

      if (nextItems.length === 0) {
        setSelectedKey("");
        setTask(null);
        setAvailableOptions([]);
        setAnswerOptions([]);
        setDropdownOptions({});
        setResponseValues({});
        setFeedback(null);
        return;
      }

      const initialItem = nextItems[0];
      const initialKey = makeKey(initialItem.queryId, initialItem.taskId, initialItem.itemType);
      setSelectedKey(initialKey);

      if (
        payload.initialTask &&
        makeKey(payload.initialTask.queryId, payload.initialTask.taskId, payload.initialTask.itemType) === initialKey
      ) {
        prefetchedTaskKeyRef.current = initialKey;
        applyLoadedTask(payload.initialTask);
      }
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to load student tasks.");
      setItems([]);
    } finally {
      setTaskListLoading(false);
    }
  }

  async function loadTask(
    queryId: string,
    taskId: string,
    itemType: "parsons" | "dropdown" | "execution-trace",
    forceRefresh = false
  ) {
    setTaskLoading(true);
    setErrorMessage(null);
    setFeedback(null);

    try {
      const params = new URLSearchParams({
        queryId,
        taskId,
        itemType
      });
      if (forceRefresh) {
        params.set("refresh", "1");
      }
      const response = await fetch(
        `/api/studio/student/task?${params.toString()}`,
        { cache: "no-store" }
      );
      const payload = (await response.json()) as StudentTaskResponse & { error?: string };
      if (!response.ok) {
        throw new Error(payload.error ?? "Failed to load assessment item.");
      }
      applyLoadedTask(payload);
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to load assessment item.");
      setTask(null);
      setAvailableOptions([]);
      setAnswerOptions([]);
      setDropdownOptions({});
      setResponseValues({});
    } finally {
      setTaskLoading(false);
    }
  }

  function resetAttempt(nextTask: StudentTaskResponse | null = task, reason: "task_loaded" | "manual_reset" = "manual_reset") {
    if (!nextTask) {
      return;
    }

    const taskKey = makeKey(nextTask.queryId, nextTask.taskId, nextTask.itemType);
    const nextAttemptNumber = (attemptCountersRef.current[taskKey] ?? 0) + 1;
    attemptCountersRef.current[taskKey] = nextAttemptNumber;
    const nextAttemptId = createClientId("attempt");
    const nextStartedAt = new Date().toISOString();

    if (reason === "manual_reset" && currentAttemptId) {
      emitTelemetry("attempt_reset", {
        replacedAttemptId: currentAttemptId,
        nextAttemptNumber
      });
    }

    setCurrentAttemptId(nextAttemptId);
    setCurrentAttemptNumber(nextAttemptNumber);
    attemptStartedAtRef.current = nextStartedAt;
    currentAttemptFocusLossCountRef.current = 0;
    emitTelemetry(
      "attempt_started",
      {
        attemptNumber: nextAttemptNumber,
        reason
      },
      {
        attemptId: nextAttemptId,
        attemptNumber: nextAttemptNumber,
        queryId: nextTask.queryId,
        taskId: nextTask.taskId,
        itemId: nextTask.itemId,
        itemType: nextTask.itemType
      }
    );

    if (nextTask.itemType === "parsons") {
      const options = shuffle(
        nextTask.options.map((text, index) => ({
          id: `${nextTask.queryId}-${nextTask.taskId}-${nextTask.itemType}-option-${index}`,
          text
        }))
      );
      setAvailableOptions(options);
      setAnswerOptions([]);
      setDropdownOptions({});
    } else if (nextTask.itemType === "dropdown") {
      setAvailableOptions([]);
      setAnswerOptions([]);
      setDropdownOptions(
        Object.fromEntries(
          nextTask.blanks.map((blank) => [blank.blankId, shuffle(blank.options)])
        )
      );
    } else {
      setAvailableOptions([]);
      setAnswerOptions([]);
      setDropdownOptions({});
      setResponseValues({});
    }

    setResponseValues({});
    setFeedback(null);
    setDragState(null);
  }

  function removeBlock(optionId: string) {
    const option = answerOptions.find((item) => item.id === optionId);
    if (!option) {
      return;
    }

    setAnswerOptions((current) => current.filter((item) => item.id !== optionId));
    setAvailableOptions((current) => [...current, option]);
    emitTelemetry("block_removed", {
      optionId,
      blockText: option.text
    });
    setFeedback(null);
  }

  function startDrag(source: "available" | "answer", optionId: string) {
    setDragState({ source, optionId });
    setFeedback(null);
  }

  function endDrag() {
    setDragState(null);
  }

  function moveToAnswer(optionId: string, insertAt?: number) {
    if (!task || task.itemType !== "parsons" || answerOptions.length >= task.requiredBlockCount) {
      return;
    }

    const option = availableOptions.find((item) => item.id === optionId);
    if (!option) {
      return;
    }

    const nextIndex = insertAt === undefined ? answerOptions.length : Math.max(0, Math.min(insertAt, answerOptions.length));
    setAvailableOptions((current) => current.filter((item) => item.id !== optionId));
    setAnswerOptions((current) => {
      const next = [...current];
      next.splice(nextIndex, 0, option);
      return next;
    });
    emitTelemetry("block_added", {
      optionId,
      blockText: option.text,
      insertAt: nextIndex
    });
    setFeedback(null);
  }

  function reorderAnswer(optionId: string, insertAt?: number) {
    const sourceIndex = answerOptions.findIndex((item) => item.id === optionId);
    if (sourceIndex < 0) {
      return;
    }

    const rawTargetIndex = insertAt === undefined ? answerOptions.length : insertAt;
    const targetIndex = sourceIndex < rawTargetIndex ? rawTargetIndex - 1 : rawTargetIndex;
    if (targetIndex === sourceIndex) {
      return;
    }

    setAnswerOptions((current) => {
      const next = [...current];
      const currentIndex = next.findIndex((item) => item.id === optionId);
      if (currentIndex < 0) {
        return current;
      }
      const [moved] = next.splice(currentIndex, 1);
      const boundedIndex = Math.max(0, Math.min(targetIndex, next.length));
      next.splice(boundedIndex, 0, moved);
      return next;
    });
    emitTelemetry("block_reordered", {
      optionId,
      fromIndex: sourceIndex,
      toIndex: Math.max(0, targetIndex)
    });
    setFeedback(null);
  }

  function returnToAvailable(optionId: string) {
    const option = answerOptions.find((item) => item.id === optionId);
    if (!option) {
      return;
    }

    setAnswerOptions((current) => current.filter((item) => item.id !== optionId));
    setAvailableOptions((current) => [...current, option]);
    setFeedback(null);
  }

  function dropIntoAnswer(insertAt?: number) {
    if (!dragState) {
      return;
    }

    if (dragState.source === "available") {
      moveToAnswer(dragState.optionId, insertAt);
    } else {
      reorderAnswer(dragState.optionId, insertAt);
    }

    setDragState(null);
  }

  function dropIntoAvailable() {
    if (!dragState) {
      return;
    }

    if (dragState.source === "answer") {
      returnToAvailable(dragState.optionId);
    }

    setDragState(null);
  }

  function shuffleAvailable() {
    setAvailableOptions((current) => shuffle(current));
    emitTelemetry("pool_shuffled", {
      optionCount: availableOptions.length
    });
  }

  async function submitAnswer() {
    if (!task) {
      return;
    }

    setGrading(true);
    setErrorMessage(null);
    emitTelemetry("submit_clicked", {
      readyToSubmit,
      selectedCount:
        task.itemType === "parsons"
          ? answerOptions.length
          : Object.values(responseValues).filter((value) => value.trim().length > 0).length
    });

    try {
      const response = await fetch("/api/studio/student/grade", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          sessionId,
          attemptId: currentAttemptId,
          attemptNumber: currentAttemptNumber,
          startedAt: attemptStartedAtRef.current,
          focusLossCount: currentAttemptFocusLossCountRef.current,
          itemId: task.itemId,
          queryId: task.queryId,
          taskId: task.taskId,
          itemType: task.itemType,
          ...(task.itemType === "parsons"
            ? {
                selectedBlocks: answerOptions.map((option) => option.text)
              }
            : {
                selectedAnswers: responseValues
              })
        })
      });

      const payload = (await response.json()) as StudentGradeResponse & { error?: string };
      if (!response.ok) {
        throw new Error(payload.error ?? "Failed to grade submission.");
      }

      setFeedback(payload);
      emitTelemetry(payload.correct ? "graded_correct" : "graded_incorrect", {
        correctCount: payload.correctCount,
        expectedCount: payload.expectedCount,
        selectedCount: payload.selectedCount
      });
      setAttemptHistory((current) => ({
        ...current,
        [makeKey(task.queryId, task.taskId, task.itemType)]: {
          attempted: true,
          correct: payload.correct
        }
      }));
    } catch (error) {
      setErrorMessage(error instanceof Error ? error.message : "Failed to grade submission.");
    } finally {
      setGrading(false);
    }
  }

  function goToNextTask() {
    if (!selectedItem || items.length === 0) {
      return;
    }

    const index = items.findIndex((item) => makeKey(item.queryId, item.taskId, item.itemType) === selectedKey);
    const nextItem = items[(index + 1) % items.length];
    setSelectedKey(makeKey(nextItem.queryId, nextItem.taskId, nextItem.itemType));
  }

  function handleDropdownSelect(blankId: string, option: string) {
    const previous = responseValues[blankId];
    setResponseValues((current) => ({ ...current, [blankId]: option }));
    emitTelemetry(previous && previous !== option ? "blank_changed" : "blank_selected", {
      blankId,
      previous: previous ?? null,
      next: option
    });
  }

  function handleCheckpointBlur(checkpointId: string, value: string) {
    emitTelemetry("checkpoint_blurred", {
      checkpointId,
      valueLength: value.trim().length,
      value
    });
  }

  function dismissQuickStart() {
    setShowQuickStart(false);
    try {
      window.localStorage.setItem(QUICK_START_STORAGE_KEY, "1");
    } catch {
      // Ignore storage failures in restricted environments.
    }
  }

  return (
    <Box
      className="studio-shell anti-copy-shell"
      onCopy={(event) => {
        if (shouldBypassClipboardLock(event.target)) {
          return;
        }
        event.preventDefault();
      }}
      onCut={(event) => {
        if (shouldBypassClipboardLock(event.target)) {
          return;
        }
        event.preventDefault();
      }}
      onPaste={(event) => {
        if (shouldBypassClipboardLock(event.target)) {
          return;
        }
        event.preventDefault();
      }}
      onContextMenu={(event) => {
        if (shouldBypassClipboardLock(event.target)) {
          return;
        }
        event.preventDefault();
      }}
    >
      <Box sx={{ maxWidth: 1480, mx: "auto", px: { xs: 2, md: 4.5 }, py: { xs: 3, md: 4.5 } }}>
        <Stack spacing={2.75}>
          <PageHeader
            selectedItem={selectedItem}
            maxAiPassRate={maxAiPassRate}
            currentIndex={currentIndex}
            totalItems={items.length}
            attempted={progress.attempted}
            correct={progress.correct}
            viewingValue={viewingPercent}
            onShowQuickStart={() => setShowQuickStart(true)}
          />

          {showQuickStart && <QuickStartPanel onDismiss={dismissQuickStart} />}
          {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

          {items.length === 0 && !taskListLoading ? (
            <Paper sx={{ p: { xs: 3, md: 4 }, borderRadius: 4 }}>
              <Stack spacing={1.25}>
                <Typography variant="h2">No eligible assessment items</Typography>
                <Typography variant="body2" sx={{ color: "text.secondary", maxWidth: 640 }}>
                  Raise the threshold or generate more typed assessments, then refresh.
                </Typography>
              </Stack>
            </Paper>
          ) : (
            <Box
              sx={{
                display: "grid",
                gridTemplateColumns: { xs: "1fr", lg: "248px minmax(0, 1fr)" },
                gap: { xs: 2.5, lg: 3.5 },
                alignItems: "start"
              }}
            >
              <Box component="aside" sx={{ position: { lg: "sticky" }, top: { lg: 24 } }}>
                <Stack spacing={2.2}>
                  <SidebarSection title="Filter">
                    <Stack spacing={1.4}>
                      <Stack direction="row" justifyContent="space-between" alignItems="center">
                        <Typography variant="body2" color="text.secondary">
                          Max AI pass
                        </Typography>
                        <Chip size="small" color="primary" label={`≤ ${maxAiPassRate}%`} />
                      </Stack>
                      <Slider
                        value={maxAiPassRate}
                        onChange={(_, value) => setMaxAiPassRate(value as number)}
                        min={20}
                        max={100}
                        step={5}
                        valueLabelDisplay="off"
                      />
                      <Stack direction="row" spacing={0.5}>
                        <Button
                          size="small"
                          variant="text"
                          startIcon={taskListLoading ? <CircularProgress size={14} color="inherit" /> : <RefreshRounded />}
                          onClick={() => void loadEligibleItems(maxAiPassRate, true)}
                        >
                          Refresh
                        </Button>
                        <Button size="small" variant="text" endIcon={<ArrowForwardRounded />} onClick={goToNextTask} disabled={items.length === 0}>
                          Next task
                        </Button>
                      </Stack>
                      {statusMessage && !errorMessage && (
                        <Typography variant="caption" sx={{ color: "text.secondary" }}>
                          {statusMessage}
                        </Typography>
                      )}
                    </Stack>
                  </SidebarSection>

                  <SidebarSection
                    title="Task list"
                    description={taskListLoading ? "Loading..." : `${items.length} items`}
                  >
                    <Box
                      sx={{
                        border: "1px solid",
                        borderColor: "divider",
                        borderRadius: 3,
                        overflow: "hidden",
                        bgcolor: alpha("#FFFFFF", 0.78)
                      }}
                    >
                      {taskListLoading ? (
                        <Box sx={{ px: 1.25, py: 1.5 }}>
                          <LoadingState message="Loading tasks..." />
                        </Box>
                      ) : (
                        <Stack divider={<Divider flexItem />}>
                          {items.map((item) => {
                            const key = makeKey(item.queryId, item.taskId, item.itemType);
                            const attempt = attemptHistory[key];
                            return (
                              <TaskListEntry
                                key={key}
                                selected={selectedKey === key}
                                taskId={item.taskId}
                                itemType={item.itemType}
                                title={item.title}
                                aiPassRate={item.aiPassRate}
                                attempted={attempt?.attempted ?? false}
                                correct={attempt?.correct ?? false}
                                onClick={() => setSelectedKey(key)}
                              />
                            );
                          })}
                        </Stack>
                      )}
                    </Box>
                  </SidebarSection>

                  <SidebarSection title="Session">
                    <Stack spacing={1.25}>
                      <LinearProgress variant="determinate" value={attemptedPercent} />
                      <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
                        <MetaChip label={`${progress.attempted}/${items.length || 0} attempted`} tone="primary" />
                        <MetaChip label={`${progress.correct} correct`} tone={progress.correct > 0 ? "success" : "default"} />
                        <MetaChip label={`${focusEvents.length} exits`} tone={focusEvents.length > 0 ? "warning" : "default"} />
                      </Stack>
                      {latestFocusEvent ? (
                        <Typography variant="caption" sx={{ color: "text.secondary" }}>
                          Latest exit: {latestFocusEvent.reason === "tab-hidden" ? "tab hidden" : "window blurred"} at{" "}
                          {formatSessionTime(latestFocusEvent.timestamp)}
                        </Typography>
                      ) : null}
                    </Stack>
                  </SidebarSection>
                </Stack>
              </Box>

              <Box sx={{ position: "relative" }}>
                <Paper sx={{ borderRadius: 5, overflow: "hidden" }}>
                  <Stack
                    spacing={0}
                    sx={{
                      filter: practiceLocked ? "blur(10px)" : "none",
                      pointerEvents: practiceLocked ? "none" : "auto",
                      transition: "filter 140ms ease"
                    }}
                  >
                  {taskLoading || !task ? (
                    <Box sx={{ p: { xs: 3.5, md: 4.5 } }}>
                      <LoadingState message="Loading current problem..." />
                    </Box>
                  ) : (
                    <>
                      <ProblemPanel task={task} selectedItem={selectedItem} />

                      <Divider />

                      <Box sx={{ p: { xs: 2.25, md: 3.25 }, bgcolor: alpha("#FCFDFE", 0.84) }}>
                        <HintPanel
                          task={task}
                          progressSummary={hintProgressSummary}
                          feedback={feedback}
                          selectedBlocks={task.itemType === "parsons" ? answerOptions.map((option) => option.text) : []}
                          selectedAnswers={task.itemType === "parsons" ? null : responseValues}
                          attemptNumber={currentAttemptNumber}
                          emitTelemetry={emitTelemetry}
                        />
                      </Box>

                      <Divider />

                      <Box sx={{ p: { xs: 2.25, md: 3.25 } }}>
                        {task.itemType === "parsons" ? (
                          <Box
                            sx={{
                              display: "grid",
                              gridTemplateColumns: { xs: "1fr", xl: "minmax(0, 0.9fr) minmax(400px, 1.12fr)" },
                              gap: { xs: 2.25, xl: 2.75 }
                            }}
                          >
                            <Box>
                              <SectionHeader
                                eyebrow="Step 1"
                                title="Pick valid blocks"
                                description="Tap or drag blocks into the builder."
                                action={
                                  <Button size="small" variant="text" onClick={shuffleAvailable} disabled={availableOptions.length === 0}>
                                    Shuffle
                                  </Button>
                                }
                              />

                              <PoolDropSurface
                                active={dragState?.source === "answer"}
                                onDragOver={(event) => {
                                  event.preventDefault();
                                }}
                                onDrop={(event) => {
                                  event.preventDefault();
                                  dropIntoAvailable();
                                }}
                              >
                                <Stack spacing={1}>
                                  {availableOptions.length === 0 ? (
                                    <Typography variant="body2" color="text.secondary">
                                      All currently selected blocks are in the builder.
                                    </Typography>
                                  ) : (
                                    availableOptions.map((option) => (
                                      <PoolBlock
                                        key={option.id}
                                        text={option.text}
                                        dimmed={dragState?.optionId === option.id}
                                        onPick={() => moveToAnswer(option.id)}
                                        onDragStart={(event) => {
                                          event.dataTransfer.effectAllowed = "move";
                                          startDrag("available", option.id);
                                        }}
                                        onDragEnd={endDrag}
                                      />
                                    ))
                                  )}
                                </Stack>
                              </PoolDropSurface>
                            </Box>

                            <AnswerBuilderPanel
                              task={task}
                              answerOptions={answerOptions}
                              dragState={dragState}
                              grading={grading}
                              readyToSubmit={readyToSubmit}
                              onReset={() => resetAttempt(undefined, "manual_reset")}
                              onSubmit={() => void submitAnswer()}
                              onDropIntoAnswer={dropIntoAnswer}
                              onStartDrag={startDrag}
                              onEndDrag={endDrag}
                              onRemove={removeBlock}
                            />
                          </Box>
                        ) : task.itemType === "dropdown" ? (
                          <Box
                            sx={{
                              display: "grid",
                              gridTemplateColumns: { xs: "1fr", xl: "minmax(0, 0.9fr) minmax(400px, 1.12fr)" },
                              gap: { xs: 2.25, xl: 2.75 }
                            }}
                          >
                            <DropdownTemplatePanel task={task} answers={responseValues} />
                            <DropdownAnswerPanel
                              task={task}
                              optionOrder={dropdownOptions}
                              answers={responseValues}
                              grading={grading}
                              readyToSubmit={readyToSubmit}
                              onSelect={handleDropdownSelect}
                              onReset={() => resetAttempt(undefined, "manual_reset")}
                              onSubmit={() => void submitAnswer()}
                            />
                          </Box>
                        ) : (
                          <Box
                            sx={{
                              display: "grid",
                              gridTemplateColumns: { xs: "1fr", xl: "minmax(0, 0.9fr) minmax(400px, 1.12fr)" },
                              gap: { xs: 2.25, xl: 2.75 }
                            }}
                          >
                            <ExecutionTracePromptPanel task={task} />
                            <ExecutionTraceAnswerPanel
                              task={task}
                              answers={responseValues}
                              grading={grading}
                              readyToSubmit={readyToSubmit}
                              onChange={(checkpointId, value) =>
                                setResponseValues((current) => ({ ...current, [checkpointId]: value }))
                              }
                              onBlur={handleCheckpointBlur}
                              onReset={() => resetAttempt(undefined, "manual_reset")}
                              onSubmit={() => void submitAnswer()}
                            />
                          </Box>
                        )}
                      </Box>
                      <Divider />

                      <Box sx={{ p: { xs: 2.25, md: 3.25 }, bgcolor: alpha("#F8FAFC", 0.72) }}>
                        {feedback ? (
                          <FeedbackCard feedback={feedback} onNext={goToNextTask} />
                        ) : (
                          <Typography variant="body2" sx={{ color: "text.secondary" }}>
                            Submit to get instant feedback.
                          </Typography>
                        )}
                      </Box>
                    </>
                  )}
                  </Stack>
                </Paper>

                {practiceLocked && (
                  <PracticeLockOverlay
                    eventCount={focusEvents.length}
                    latestEvent={latestFocusEvent}
                    onResume={() => {
                      setPracticeLocked(false);
                      emitTelemetry("resume_clicked", {
                        focusLossCountInAttempt: currentAttemptFocusLossCountRef.current
                      });
                    }}
                  />
                )}
              </Box>
            </Box>
          )}
        </Stack>
      </Box>
    </Box>
  );
}

function PageHeader({
  selectedItem,
  maxAiPassRate,
  currentIndex,
  totalItems,
  attempted,
  correct,
  viewingValue,
  onShowQuickStart
}: {
  selectedItem: StudentTaskListItem | null;
  maxAiPassRate: number;
  currentIndex: number;
  totalItems: number;
  attempted: number;
  correct: number;
  viewingValue: number;
  onShowQuickStart: () => void;
}) {
  return (
    <Box
      component="header"
      sx={{
        display: "grid",
        gridTemplateColumns: { xs: "1fr", md: "minmax(0, 1fr) 240px" },
        gap: 2.5,
        alignItems: { xs: "start", md: "end" },
        pb: 2.25,
        borderBottom: "1px solid",
        borderColor: "divider"
      }}
    >
      <Stack spacing={0.85}>
        <Typography variant="overline">Student mode</Typography>
        <Typography variant="h1">Solve one task, then check.</Typography>
        <Typography variant="body2" sx={{ color: "text.secondary", maxWidth: 700 }}>
          Student mode is a focused practice view: pick one low-pass item, answer it in the workspace, then review
          feedback below.
        </Typography>
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <MetaChip label={selectedItem ? `${selectedItem.queryId} · ${selectedItem.taskId}` : "No task selected"} tone="primary" />
          <MetaChip label={`AI pass ≤ ${maxAiPassRate}%`} />
        </Stack>
      </Stack>

      <Box
        sx={{
          alignSelf: { xs: "stretch", md: "end" },
          pl: { md: 2.25 },
          minWidth: 0
        }}
      >
        <Stack spacing={1.15}>
          <Stack direction="row" justifyContent="flex-end" spacing={0.5}>
            <Button size="small" variant="text" onClick={onShowQuickStart}>
              Quick start
            </Button>
            <Button component={Link} href="/metrics" variant="outlined" endIcon={<ArrowForwardRounded fontSize="small" />}>
              Analytics
            </Button>
          </Stack>
          <Stack direction="row" justifyContent="space-between" alignItems="baseline">
            <Typography variant="caption" color="text.secondary">
              Current
            </Typography>
            <Typography variant="h3" sx={{ fontSize: "1rem" }}>
              {currentIndex || 0} / {totalItems || 0}
            </Typography>
          </Stack>
          <LinearProgress variant="determinate" value={viewingValue} />
          <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
            <MetaChip label={`${attempted} attempted`} />
            <MetaChip label={`${correct} correct`} tone={correct > 0 ? "success" : "default"} />
          </Stack>
        </Stack>
      </Box>
    </Box>
  );
}

function QuickStartPanel({ onDismiss }: { onDismiss: () => void }) {
  return (
    <Paper
      sx={{
        p: { xs: 2, md: 2.3 },
        borderRadius: 4.5,
        border: "1px solid",
        borderColor: alpha("#1E6676", 0.14),
        background: `linear-gradient(180deg, ${alpha("#F8FCFD", 0.98)} 0%, ${alpha("#F6F8FB", 0.96)} 100%)`,
        boxShadow: `0 18px 40px ${alpha("#0F172A", 0.06)}`
      }}
    >
      <Stack spacing={1.8}>
        <Stack
          direction={{ xs: "column", sm: "row" }}
          justifyContent="space-between"
          alignItems={{ xs: "flex-start", sm: "center" }}
          spacing={1}
        >
          <Stack spacing={0.35}>
            <Typography variant="overline">Quick start</Typography>
            <Typography variant="h3">Student mode in one glance.</Typography>
          </Stack>
          <Button size="small" variant="text" onClick={onDismiss}>
            Hide
          </Button>
        </Stack>

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", lg: "minmax(260px, 0.92fr) minmax(0, 1.08fr)" },
            gap: 1.25
          }}
        >
          <QuickStartGoalCard />
          <QuickStartPageMap />
        </Box>

        <Box
          sx={{
            display: "grid",
            gridTemplateColumns: { xs: "1fr", md: "repeat(3, minmax(0, 1fr))" },
            gap: 1.25
          }}
        >
          <QuickStartStep step="01" title="Pick" caption="Use the task list on the left.">
            <QuickStartPickerMotion />
          </QuickStartStep>
          <QuickStartStep step="02" title="Solve" caption="Work in the main answer area.">
            <QuickStartBuildMotion />
          </QuickStartStep>
          <QuickStartStep step="03" title="Check" caption="Submit to see feedback below.">
            <QuickStartSubmitMotion />
          </QuickStartStep>
        </Box>
      </Stack>
    </Paper>
  );
}

function QuickStartGoalCard() {
  return (
    <Paper
      sx={{
        p: 1.45,
        borderRadius: 3.5,
        boxShadow: "none",
        bgcolor: alpha("#FFFFFF", 0.88),
        border: "1px solid",
        borderColor: alpha("#D7E1EA", 0.88)
      }}
    >
      <Stack spacing={1.05}>
        <Box>
          <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
            Goal
          </Typography>
          <Typography variant="h4" sx={{ mt: 0.25 }}>
            Solve one practice coding task.
          </Typography>
        </Box>
        <Typography variant="body2" sx={{ color: "text.secondary", maxWidth: 360 }}>
          Pick one low-pass item, answer it, then check the result before moving on.
        </Typography>
        <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
          <MetaChip label="1 task at a time" tone="primary" />
          <MetaChip label="Instant feedback" />
        </Stack>
      </Stack>
    </Paper>
  );
}

function QuickStartPageMap() {
  return (
    <Paper
      sx={{
        p: 1.45,
        borderRadius: 3.5,
        boxShadow: "none",
        bgcolor: alpha("#FFFFFF", 0.88),
        border: "1px solid",
        borderColor: alpha("#D7E1EA", 0.88)
      }}
    >
      <Stack spacing={1.05}>
        <Box>
          <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
            How it works
          </Typography>
          <Typography variant="h4" sx={{ mt: 0.25 }}>
            Follow the page in this order.
          </Typography>
        </Box>

        <Box
          sx={{
            position: "relative",
            display: "grid",
            gridTemplateColumns: "148px minmax(0, 1fr)",
            gridTemplateRows: "1fr auto",
            gap: 0.95,
            minHeight: 128,
            '@keyframes quickStartMapPulse': {
              "0%, 20%, 100%": { opacity: 0, transform: "scale(0.98)" },
              "26%, 44%": { opacity: 1, transform: "scale(1)" }
            },
            '@keyframes quickStartMapPulseMid': {
              "0%, 30%, 100%": { opacity: 0, transform: "scale(0.98)" },
              "38%, 62%": { opacity: 1, transform: "scale(1)" }
            },
            '@keyframes quickStartMapPulseBottom': {
              "0%, 56%, 100%": { opacity: 0, transform: "scale(0.98)" },
              "64%, 88%": { opacity: 1, transform: "scale(1)" }
            }
          }}
        >
          <QuickStartMapRegion
            title="Choose a task"
            caption="Step 1"
            sx={{
              gridColumn: "1 / 2",
              gridRow: "1 / 3"
            }}
            pulseSx={{
              animation: "quickStartMapPulse 3s ease-in-out infinite"
            }}
          />
          <QuickStartMapRegion
            title="Answer here"
            caption="Step 2"
            sx={{
              gridColumn: "2 / 3",
              gridRow: "1 / 2"
            }}
            pulseSx={{
              animation: "quickStartMapPulseMid 3s ease-in-out infinite"
            }}
          />
          <QuickStartMapRegion
            title="Read feedback"
            caption="Step 3"
            sx={{
              gridColumn: "2 / 3",
              gridRow: "2 / 3"
            }}
            pulseSx={{
              animation: "quickStartMapPulseBottom 3s ease-in-out infinite"
            }}
          />
        </Box>

        <Typography variant="body2" sx={{ color: "text.secondary" }}>
          1. Choose a task from the left list. 2. Solve it in the main workspace. 3. Submit and read the feedback below.
        </Typography>
      </Stack>
    </Paper>
  );
}

function QuickStartMapRegion({
  title,
  caption,
  sx,
  pulseSx
}: {
  title: string;
  caption: string;
  sx?: object;
  pulseSx?: object;
}) {
  return (
    <Box
      sx={{
        position: "relative",
        minHeight: 0,
        borderRadius: 2.8,
        border: "1px solid",
        borderColor: alpha("#D5DFE8", 0.92),
        bgcolor: alpha("#F8FAFC", 0.96),
        p: 1,
        overflow: "hidden",
        ...sx
      }}
    >
      <Box
        sx={{
          position: "absolute",
          inset: 0,
          borderRadius: "inherit",
          border: "1px solid",
          borderColor: alpha("#1E6676", 0.28),
          boxShadow: `inset 0 0 0 1px ${alpha("#1E6676", 0.08)}`,
          ...pulseSx
        }}
      />
      <Stack spacing={0.5} sx={{ position: "relative", zIndex: 1, height: "100%", justifyContent: "space-between" }}>
        <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
          {caption}
        </Typography>
        <Typography variant="h4">{title}</Typography>
      </Stack>
    </Box>
  );
}

function QuickStartStep({
  step,
  title,
  caption,
  children
}: {
  step: string;
  title: string;
  caption: string;
  children: ReactNode;
}) {
  return (
    <Paper
      sx={{
        p: 1.35,
        borderRadius: 3.5,
        boxShadow: "none",
        bgcolor: alpha("#FFFFFF", 0.88),
        border: "1px solid",
        borderColor: alpha("#D7E1EA", 0.88),
        minHeight: 172
      }}
    >
      <Stack spacing={1.1}>
        {children}
        <Stack spacing={0.35}>
          <Box
            sx={{
              width: "fit-content",
              px: 0.75,
              py: 0.1,
              borderRadius: 999,
              bgcolor: alpha("#1E6676", 0.08)
            }}
          >
            <Typography variant="caption" sx={{ color: "primary.main", letterSpacing: "0.06em" }}>
              {step}
            </Typography>
          </Box>
          <Typography variant="h4">{title}</Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            {caption}
          </Typography>
        </Stack>
      </Stack>
    </Paper>
  );
}

function QuickStartPickerMotion() {
  return (
    <Box
      sx={{
        position: "relative",
        height: 98,
        borderRadius: 3,
        border: "1px solid",
        borderColor: alpha("#D5DFE8", 0.92),
        bgcolor: alpha("#F8FAFC", 0.96),
        overflow: "hidden",
        p: 1,
        '@keyframes quickStartPickCursor': {
          "0%, 18%": { transform: "translate(0px, 0px)", opacity: 0.36 },
          "40%, 78%": { transform: "translate(0px, 29px)", opacity: 1 },
          "100%": { transform: "translate(0px, 29px)", opacity: 0.7 }
        },
        '@keyframes quickStartPickPulse': {
          "0%, 100%": { boxShadow: `inset 0 0 0 1px ${alpha("#1E6676", 0.12)}` },
          "42%, 72%": { boxShadow: `inset 0 0 0 1px ${alpha("#1E6676", 0.34)}` }
        }
      }}
    >
      <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
        Task list
      </Typography>
      <Box
        sx={{
          position: "absolute",
          left: 10,
          top: 30,
          width: 10,
          height: 10,
          borderRadius: "50%",
          bgcolor: "#1E6676",
          boxShadow: `0 0 0 6px ${alpha("#1E6676", 0.12)}`,
          animation: "quickStartPickCursor 2.5s ease-in-out infinite"
        }}
      />
      <Stack spacing={0.7} sx={{ mt: 0.85, ml: 2.2 }}>
        {[0, 1, 2].map((index) => (
          <Box
            key={index}
            sx={{
              px: 0.8,
              py: 0.65,
              borderRadius: 2.2,
              bgcolor: index === 1 ? alpha("#1E6676", 0.12) : alpha("#FFFFFF", 0.88),
              animation: index === 1 ? "quickStartPickPulse 2.5s ease-in-out infinite" : "none"
            }}
          >
            <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
              <Box sx={{ width: index === 1 ? "58%" : "68%", height: 10, borderRadius: 999, bgcolor: alpha("#17212B", 0.08) }} />
              <Box
                sx={{
                  px: 0.55,
                  py: 0.1,
                  borderRadius: 999,
                  bgcolor: index === 1 ? alpha("#1E6676", 0.18) : alpha("#17212B", 0.06)
                }}
              >
                <Typography variant="caption" sx={{ fontSize: "0.63rem", color: index === 1 ? "primary.main" : "text.secondary" }}>
                  {index === 1 ? "Open" : "Task"}
                </Typography>
              </Box>
            </Stack>
          </Box>
        ))}
      </Stack>
    </Box>
  );
}

function QuickStartBuildMotion() {
  return (
    <Box
      sx={{
        position: "relative",
        height: 98,
        borderRadius: 3,
        border: "1px solid",
        borderColor: alpha("#D5DFE8", 0.92),
        bgcolor: alpha("#F8FAFC", 0.96),
        overflow: "hidden",
        p: 1,
        '@keyframes quickStartBuildMove': {
          "0%, 12%": { transform: "translate(0px, 0px)", opacity: 0 },
          "22%, 56%": { transform: "translate(38px, 0px)", opacity: 1 },
          "70%, 100%": { transform: "translate(82px, 24px)", opacity: 1 }
        }
      }}
    >
      <Stack direction="row" justifyContent="space-between" sx={{ mb: 0.75 }}>
        <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
          Pool
        </Typography>
        <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
          Answer
        </Typography>
      </Stack>
      <Box sx={{ display: "grid", gridTemplateColumns: "1fr auto 1fr", gap: 0.85, alignItems: "center", height: "calc(100% - 22px)" }}>
        <Stack spacing={0.7}>
          {[56, 48, 52].map((width, index) => (
            <Box
              key={width}
              sx={{
                width,
                height: 12,
                borderRadius: 999,
                bgcolor: alpha("#1E6676", index === 0 ? 0.22 : 0.12)
              }}
            />
          ))}
        </Stack>
        <Typography variant="body2" sx={{ color: "primary.main", fontWeight: 700 }}>
          →
        </Typography>
        <Stack spacing={0.7}>
          {[0, 1, 2].map((index) => (
            <Box
              key={index}
              sx={{
                height: 14,
                borderRadius: 999,
                border: "1px dashed",
                borderColor: alpha("#1E6676", index === 1 ? 0.35 : 0.16),
                bgcolor: index === 1 ? alpha("#1E6676", 0.08) : alpha("#FFFFFF", 0.72)
              }}
            />
          ))}
        </Stack>
      </Box>
      <Box
        sx={{
          position: "absolute",
          left: 18,
          top: 34,
          width: 42,
          height: 12,
          borderRadius: 999,
          bgcolor: "#1E6676",
          boxShadow: `0 8px 16px ${alpha("#1E6676", 0.18)}`,
          animation: "quickStartBuildMove 2.6s ease-in-out infinite"
        }}
      />
    </Box>
  );
}

function QuickStartSubmitMotion() {
  return (
    <Box
      sx={{
        position: "relative",
        height: 98,
        borderRadius: 3,
        border: "1px solid",
        borderColor: alpha("#D5DFE8", 0.92),
        bgcolor: alpha("#F8FAFC", 0.96),
        overflow: "hidden",
        p: 1,
        '@keyframes quickStartButtonPulse': {
          "0%, 100%": { transform: "scale(1)", opacity: 0.86 },
          "50%": { transform: "scale(1.03)", opacity: 1 }
        },
        '@keyframes quickStartBadgePop': {
          "0%, 28%": { transform: "scale(0.6)", opacity: 0 },
          "42%, 100%": { transform: "scale(1)", opacity: 1 }
        },
        '@keyframes quickStartCardGlow': {
          "0%, 100%": { borderColor: alpha("#D5DFE8", 0.92) },
          "45%, 78%": { borderColor: alpha("#46705C", 0.34) }
        }
      }}
    >
      <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
        Feedback
      </Typography>
      <Stack
        spacing={1}
        justifyContent="space-between"
        sx={{
          height: "calc(100% - 18px)",
          mt: 0.55,
          p: 0.8,
          borderRadius: 2.6,
          border: "1px solid",
          borderColor: alpha("#D5DFE8", 0.92),
          bgcolor: alpha("#FFFFFF", 0.86),
          animation: "quickStartCardGlow 2.4s ease-in-out infinite"
        }}
      >
        <Box sx={{ width: "78%", height: 10, borderRadius: 999, bgcolor: alpha("#17212B", 0.08) }} />
        <Box
          sx={{
            width: 102,
            height: 30,
            borderRadius: 999,
            bgcolor: "#1E6676",
            animation: "quickStartButtonPulse 2.4s ease-in-out infinite",
            display: "flex",
            alignItems: "center",
            justifyContent: "center"
          }}
        >
          <Typography variant="caption" sx={{ color: "#FFFFFF", fontWeight: 700, letterSpacing: "0.03em" }}>
            SUBMIT
          </Typography>
        </Box>
      </Stack>
      <Box
        sx={{
          position: "absolute",
          top: 38,
          right: 10,
          px: 0.8,
          py: 0.25,
          borderRadius: 999,
          bgcolor: alpha("#46705C", 0.16),
          border: "1px solid",
          borderColor: alpha("#46705C", 0.2),
          animation: "quickStartBadgePop 2.4s ease-in-out infinite"
        }}
      >
        <Typography variant="caption" sx={{ color: "#46705C", fontWeight: 700 }}>
          Correct
        </Typography>
      </Box>
    </Box>
  );
}

function SidebarSection({
  title,
  description,
  children
}: {
  title: string;
  description?: string;
  children: ReactNode;
}) {
  return (
    <Box
      sx={{
        px: 0.25,
        py: 0.1
      }}
    >
      <Stack spacing={1.1}>
        <Box>
          <Typography variant="h4">{title}</Typography>
          {description ? (
            <Typography variant="body2" sx={{ mt: 0.25 }}>
              {description}
            </Typography>
          ) : null}
        </Box>
        {children}
      </Stack>
    </Box>
  );
}

function MetricPair({ label, value }: { label: string; value: string }) {
  return (
    <Stack spacing={0.35}>
      <Typography variant="caption">{label}</Typography>
      <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 600 }}>
        {value}
      </Typography>
    </Stack>
  );
}

function TaskListEntry({
  selected,
  taskId,
  itemType,
  title,
  aiPassRate,
  attempted,
  correct,
  onClick
}: {
  selected: boolean;
  taskId: string;
  itemType: "parsons" | "dropdown" | "execution-trace";
  title: string;
  aiPassRate: number | null;
  attempted: boolean;
  correct: boolean;
  onClick: () => void;
}) {
  return (
    <Box
      onClick={onClick}
      sx={{
        cursor: "pointer",
        px: 1.15,
        py: 1.05,
        bgcolor: selected ? alpha("#1E6676", 0.08) : "transparent",
        borderLeft: "2px solid",
        borderLeftColor: selected ? "primary.main" : "transparent",
        transition: "background-color 140ms ease, border-color 140ms ease",
        '&:hover': {
          bgcolor: selected ? alpha("#1E6676", 0.11) : alpha("#1E6676", 0.045)
        }
      }}
    >
      <Stack spacing={0.45}>
        <Stack direction="row" justifyContent="space-between" spacing={1} alignItems="center">
          <Stack direction="row" spacing={0.75} alignItems="center">
            <Typography variant="body2" sx={{ color: "text.primary", fontWeight: 600 }}>
              {taskId}
            </Typography>
            <MetaChip label={formatItemTypeLabel(itemType)} />
          </Stack>
          {attempted && (
            <Typography variant="caption" sx={{ color: correct ? "success.main" : "warning.main" }}>
              {correct ? "Solved" : "Attempted"}
            </Typography>
          )}
        </Stack>
        <Typography variant="body2" sx={{ color: "text.secondary", fontSize: "0.84rem" }}>
          <Box
            component="span"
            sx={{
              display: "-webkit-box",
              WebkitBoxOrient: "vertical",
              WebkitLineClamp: 2,
              overflow: "hidden"
            }}
          >
            {title}
          </Box>
        </Typography>
        {aiPassRate !== null && (
          <Typography variant="caption" sx={{ color: "text.disabled" }}>
            AI pass {formatPercent(aiPassRate)}
          </Typography>
        )}
      </Stack>
    </Box>
  );
}

function ProblemPanel({ task, selectedItem }: { task: StudentTaskResponse; selectedItem: StudentTaskListItem | null }) {
  const [showFullPrompt, setShowFullPrompt] = useState(false);
  const showPromptToggle = task.prompt.length > 280;

  useEffect(() => {
    setShowFullPrompt(false);
  }, [task.itemId]);

  return (
    <Box sx={{ px: { xs: 2.75, md: 3.25 }, py: { xs: 2.5, md: 3 } }}>
      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", lg: "minmax(0, 1fr) 220px" },
          gap: 2.5,
          alignItems: "start"
        }}
      >
        <Stack spacing={1.4}>
          <Typography variant="overline">Current problem</Typography>
          <Typography variant="h2">{task.title}</Typography>
          <Stack direction="row" spacing={0.9} flexWrap="wrap" useFlexGap>
            {task.theme && <MetaChip label={task.theme} tone="primary" />}
            <MetaChip label={formatItemTypeLabel(task.itemType)} />
            <MetaChip
              label={
                task.itemType === "parsons"
                  ? `${task.requiredBlockCount} blocks`
                  : task.itemType === "dropdown"
                    ? `${task.requiredBlankCount} blanks`
                    : `${task.requiredCheckpointCount} checkpoints`
              }
            />
            {task.concepts.slice(0, 2).map((concept) => (
              <MetaChip key={concept} label={concept} />
            ))}
          </Stack>
          <Paper
            sx={{
              p: 1.35,
              borderRadius: 3.25,
              boxShadow: "none",
              bgcolor: alpha("#F8FAFC", 0.92),
              maxWidth: "76ch"
            }}
          >
            <Stack spacing={0.75}>
              <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                <Typography variant="caption" sx={{ color: "text.secondary", letterSpacing: "0.04em", textTransform: "uppercase" }}>
                  Brief
                </Typography>
                {showPromptToggle ? (
                  <Button size="small" variant="text" onClick={() => setShowFullPrompt((current) => !current)}>
                    {showFullPrompt ? "Collapse" : "Expand"}
                  </Button>
                ) : null}
              </Stack>
              <Typography
                variant="body2"
                sx={{
                  color: "text.secondary",
                  whiteSpace: "pre-line",
                  ...(showPromptToggle && !showFullPrompt
                    ? {
                        display: "-webkit-box",
                        WebkitBoxOrient: "vertical",
                        WebkitLineClamp: 4,
                        overflow: "hidden"
                      }
                    : {})
                }}
              >
                {task.prompt}
              </Typography>
            </Stack>
          </Paper>
        </Stack>

        <Box
          sx={{
            borderLeft: { lg: "1px solid" },
            borderColor: { lg: "divider" },
            pl: { lg: 2.5 }
          }}
        >
          <Stack spacing={1}>
            <MetricPair label="Task" value={selectedItem ? `${selectedItem.queryId} / ${selectedItem.taskId}` : "n/a"} />
            <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
              <MetaChip
                label={`AI ${selectedItem?.aiPassRate !== null && selectedItem?.aiPassRate !== undefined ? formatPercent(selectedItem.aiPassRate) : "n/a"}`}
              />
              <MetaChip
                label={`Students ${
                  selectedItem?.studentPassRate !== null && selectedItem?.studentPassRate !== undefined
                    ? formatPercent(selectedItem.studentPassRate)
                    : "n/a"
                }`}
              />
            </Stack>
          </Stack>
        </Box>
      </Box>
    </Box>
  );
}

function HintPanel({
  task,
  progressSummary,
  feedback,
  selectedBlocks,
  selectedAnswers,
  attemptNumber,
  emitTelemetry
}: {
  task: StudentTaskResponse;
  progressSummary: string;
  feedback: StudentGradeResponse | null;
  selectedBlocks: string[];
  selectedAnswers: Record<string, string> | null;
  attemptNumber: number;
  emitTelemetry: (
    eventType: StudentTelemetryEventType,
    payload: Record<string, unknown>,
    overrides?: Partial<StudentTelemetryEvent>
  ) => void;
}) {
  const [selectedHintType, setSelectedHintType] = useState<StudentHintType | null>(null);
  const [reflectionDraft, setReflectionDraft] = useState("");
  const [hintHistory, setHintHistory] = useState<HintHistoryRecord[]>([]);
  const [remainingByType, setRemainingByType] = useState<Record<StudentHintType, number>>(createHintBudget);
  const [hintLoadingType, setHintLoadingType] = useState<StudentHintType | null>(null);
  const [hintError, setHintError] = useState<string | null>(null);
  const [developerApiKey, setDeveloperApiKey] = useState("");
  const [useDeveloperKey, setUseDeveloperKey] = useState(false);

  useEffect(() => {
    setSelectedHintType(null);
    setReflectionDraft("");
    setHintHistory([]);
    setRemainingByType(createHintBudget());
    setHintLoadingType(null);
    setHintError(null);
  }, [task.itemId]);

  useEffect(() => {
    if (useDeveloperKey && developerApiKey.trim().length === 0) {
      setUseDeveloperKey(false);
    }
  }, [developerApiKey, useDeveloperKey]);

  async function requestHint(hintType: StudentHintType, reflectionOverride?: string) {
    if (remainingByType[hintType] <= 0 || hintLoadingType) {
      return;
    }

    const requestsUsed = HINT_LIMITS[hintType] - remainingByType[hintType];
    const level = Math.min(requestsUsed + 1, 3) as 1 | 2 | 3;
    const reflection = (reflectionOverride ?? reflectionDraft).trim();
    const requestBody: StudentHintRequest = {
      queryId: task.queryId,
      taskId: task.taskId,
      itemType: task.itemType,
      hintType,
      level,
      taskContext: task,
      reflection,
      progressSummary,
      attemptNumber,
      lastFeedback: feedback,
      ...(task.itemType === "parsons"
        ? {
            selectedBlocks
          }
        : {
            selectedAnswers: selectedAnswers ?? {}
          })
    };
    const hintSource =
      useDeveloperKey && developerApiKey.trim().length > 0
        ? "developer-key"
        : EXTERNAL_HINT_API_BASE_URL
          ? "external-backend"
          : "app-backend";

    setHintLoadingType(hintType);
    setHintError(null);
    emitTelemetry("hint_requested", {
      hintType,
      level,
      reflectionLength: reflection.length,
      hasFeedback: Boolean(feedback),
      source: hintSource
    });

    try {
      const payload =
        hintSource === "developer-key"
          ? await requestHintWithDeveloperKey(requestBody, developerApiKey.trim())
          : await requestHintViaBackend(requestBody);

      const nextHint = {
        ...payload,
        reflection,
        rating: null,
        escalationNotes: "",
        escalated: false,
        createdAt: new Date().toISOString()
      } satisfies HintHistoryRecord;

      setHintHistory((current) => [nextHint, ...current]);
      setRemainingByType((current) => ({
        ...current,
        [hintType]: Math.max(0, current[hintType] - 1)
      }));
      setSelectedHintType(hintType);
      setReflectionDraft("");
      emitTelemetry("hint_received", {
        hintId: payload.hintId,
        hintType: payload.hintType,
        level: payload.level,
        model: payload.model,
        targetKind: payload.target?.kind ?? null,
        source: hintSource
      });
    } catch (error) {
      const nextMessage = error instanceof Error ? error.message : "Failed to generate hint.";
      setHintError(nextMessage);
      emitTelemetry("hint_request_failed", {
        hintType,
        level,
        message: nextMessage,
        source: hintSource
      });
    } finally {
      setHintLoadingType(null);
    }
  }

  async function requestStrongerHint(hint: HintHistoryRecord) {
    emitTelemetry("hint_stronger_requested", {
      hintId: hint.hintId,
      hintType: hint.hintType,
      previousLevel: hint.level
    });
    await requestHint(hint.hintType, hint.reflection);
  }

  function rateHint(hintId: string, rating: Exclude<HintRating, null>) {
    const ratedHint = hintHistory.find((hint) => hint.hintId === hintId);
    setHintHistory((current) =>
      current.map((hint) =>
        hint.hintId === hintId
          ? {
              ...hint,
              rating
            }
          : hint
      )
    );
    if (ratedHint) {
      emitTelemetry(rating === "helpful" ? "hint_helpful" : "hint_unhelpful", {
        hintId,
        hintType: ratedHint.hintType,
        level: ratedHint.level
      });
    }
  }

  function updateEscalationNotes(hintId: string, escalationNotes: string) {
    setHintHistory((current) =>
      current.map((hint) =>
        hint.hintId === hintId
          ? {
              ...hint,
              escalationNotes
            }
          : hint
      )
    );
  }

  function markEscalated(hintId: string) {
    setHintHistory((current) =>
      current.map((hint) =>
        hint.hintId === hintId
          ? {
              ...hint,
              escalated: true
            }
          : hint
      )
    );
    const escalatedHint = hintHistory.find((hint) => hint.hintId === hintId);
    if (escalatedHint) {
      emitTelemetry("hint_escalation_saved", {
        hintId,
        hintType: escalatedHint.hintType,
        level: escalatedHint.level,
        noteLength: escalatedHint.escalationNotes.trim().length
      });
    }
  }

  const modeOrder: StudentHintType[] = ["understand", "next-step", "check-one-issue"];
  const hintBusy = hintLoadingType !== null;
  const activeHintSourceLabel =
    useDeveloperKey && developerApiKey.trim().length > 0
      ? "Browser key active"
      : EXTERNAL_HINT_API_BASE_URL
        ? "External API active"
        : "App API active";

  return (
    <Stack spacing={1.45}>
      <Stack spacing={0.65}>
        <Typography variant="overline">Hints</Typography>
        <Typography variant="h3">Need a hint before you submit?</Typography>
        <Typography variant="body2" sx={{ color: "text.secondary", maxWidth: 780 }}>
          Ask for one short AI hint at a time, then rate whether it helped. Stronger hints stay available only if the
          first one was not enough.
        </Typography>
        <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
          <MetaChip label={progressSummary} tone="primary" />
          <MetaChip label={feedback ? "Feedback context available" : "Pre-submit support"} />
          <MetaChip
            label={activeHintSourceLabel}
            tone={useDeveloperKey && developerApiKey.trim().length > 0 ? "warning" : "default"}
          />
        </Stack>
        {hintError ? <Alert severity="warning">{hintError}</Alert> : null}
      </Stack>

      {DEV_BROWSER_HINTS_ALLOWED ? (
        <Paper
          data-allow-clipboard="true"
          sx={{
            p: 1.3,
            borderRadius: 3.5,
            boxShadow: "none",
            border: "1px solid",
            borderColor: alpha("#8D6A34", 0.16),
            bgcolor: alpha("#FFF9EF", 0.82)
          }}
        >
          <Stack spacing={1}>
            <Stack direction={{ xs: "column", md: "row" }} justifyContent="space-between" spacing={1}>
              <Box>
                <Typography variant="h4">Developer only</Typography>
                <Typography variant="body2" sx={{ color: "text.secondary", maxWidth: 760 }}>
                  Local dev only. The key stays in memory for this tab and disappears on refresh. Do not use this mode in
                  public deployments.
                </Typography>
              </Box>
              <MetaChip
                label={useDeveloperKey && developerApiKey.trim().length > 0 ? "Browser direct mode" : "Backend mode"}
                tone={useDeveloperKey && developerApiKey.trim().length > 0 ? "warning" : "default"}
              />
            </Stack>

            <TextField
              size="small"
              type="password"
              label="Temporary OpenAI API key"
              placeholder="sk-..."
              value={developerApiKey}
              onChange={(event) => setDeveloperApiKey(event.target.value)}
              autoComplete="off"
              spellCheck={false}
              disabled={hintBusy}
            />

            <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
              <Button
                variant={useDeveloperKey && developerApiKey.trim().length > 0 ? "contained" : "outlined"}
                color="warning"
                disabled={developerApiKey.trim().length === 0 || hintBusy}
                onClick={() => {
                  setUseDeveloperKey((current) => !current);
                  setHintError(null);
                }}
              >
                {useDeveloperKey && developerApiKey.trim().length > 0 ? "Use backend API instead" : "Use browser key"}
              </Button>
              <Button
                variant="text"
                disabled={(developerApiKey.trim().length === 0 && !useDeveloperKey) || hintBusy}
                onClick={() => {
                  setDeveloperApiKey("");
                  setUseDeveloperKey(false);
                  setHintError(null);
                }}
              >
                Forget key
              </Button>
            </Stack>

            <Typography variant="caption" sx={{ color: "text.secondary" }}>
              Browser-direct requests may still fail because of region policy, CORS, or network restrictions. Model:
              {" "}
              {DEV_BROWSER_HINT_MODEL}
            </Typography>
          </Stack>
        </Paper>
      ) : null}

      <Box
        sx={{
          display: "grid",
          gridTemplateColumns: { xs: "1fr", xl: "minmax(280px, 0.72fr) minmax(0, 1.28fr)" },
          gap: 1.5,
          alignItems: "start"
        }}
      >
        <Paper
          sx={{
            p: 1.3,
            borderRadius: 3.5,
            boxShadow: "none",
            bgcolor: alpha("#FFFFFF", 0.9)
          }}
        >
          <Stack spacing={1.1}>
            <Typography variant="h4">Pick a help mode</Typography>
            <Typography variant="body2" sx={{ color: "text.secondary" }}>
              The panel starts with short nudges, not full solutions.
            </Typography>

            <Stack spacing={0.8}>
              {modeOrder.map((hintType) => {
                const selected = selectedHintType === hintType;
                const remaining = remainingByType[hintType];
                return (
                  <Button
                    key={hintType}
                    variant={selected ? "contained" : "outlined"}
                    color={selected ? "primary" : "inherit"}
                    onClick={() => setSelectedHintType(hintType)}
                    disabled={remaining <= 0 || hintBusy}
                    sx={{
                      justifyContent: "space-between",
                      px: 1.2,
                      py: 1.05
                    }}
                  >
                    <Stack direction="row" justifyContent="space-between" alignItems="center" width="100%" spacing={1}>
                      <Box sx={{ textAlign: "left" }}>
                        <Typography variant="body2" sx={{ fontWeight: 700, color: selected ? "#FFFFFF" : "text.primary" }}>
                          {formatHintTypeLabel(hintType)}
                        </Typography>
                        <Typography
                          variant="caption"
                          sx={{ color: selected ? alpha("#FFFFFF", 0.84) : "text.secondary", display: "block", mt: 0.15 }}
                        >
                          {getHintDescription(hintType)}
                        </Typography>
                      </Box>
                      <Chip
                        size="small"
                        label={`${remaining} left`}
                        color={selected ? "secondary" : "default"}
                        sx={{ bgcolor: selected ? alpha("#FFFFFF", 0.16) : undefined, color: selected ? "#FFFFFF" : undefined }}
                      />
                    </Stack>
                  </Button>
                );
              })}
            </Stack>

            {selectedHintType ? (
              <Paper
                sx={{
                  p: 1.15,
                  borderRadius: 3,
                  boxShadow: "none",
                  border: "1px solid",
                  borderColor: alpha("#1E6676", 0.12),
                  bgcolor: alpha("#F8FCFD", 0.94)
                }}
              >
                <Stack spacing={1}>
                  <Box>
                    <Typography variant="body2" sx={{ fontWeight: 700, color: "text.primary" }}>
                      {formatHintTypeLabel(selectedHintType)}
                    </Typography>
                    <Typography variant="caption" sx={{ color: "text.secondary" }}>
                      Optional: add a short note so the hint can sound more targeted later.
                    </Typography>
                  </Box>
                  <TextField
                    size="small"
                    multiline
                    minRows={3}
                    placeholder={getHintInputPlaceholder(selectedHintType)}
                    value={reflectionDraft}
                    onChange={(event) => setReflectionDraft(event.target.value)}
                    disabled={hintBusy}
                  />
                  <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
                    <Button
                      onClick={() => void requestHint(selectedHintType)}
                      disabled={remainingByType[selectedHintType] <= 0 || hintBusy}
                    >
                      {hintLoadingType === selectedHintType ? "Generating hint..." : "Request hint"}
                    </Button>
                    <Button
                      variant="text"
                      onClick={() => setReflectionDraft("")}
                      disabled={reflectionDraft.trim().length === 0 || hintBusy}
                    >
                      Clear note
                    </Button>
                  </Stack>
                </Stack>
              </Paper>
            ) : null}
          </Stack>
        </Paper>

        <Stack spacing={1}>
          <Typography variant="h4">Hint history</Typography>
          {hintHistory.length === 0 ? (
            <Paper
              sx={{
                p: 1.45,
                borderRadius: 3.5,
                boxShadow: "none",
                border: "1px dashed",
                borderColor: alpha("#1E6676", 0.18),
                bgcolor: alpha("#FFFFFF", 0.76)
              }}
            >
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                No hints yet. Start with one short nudge, then decide whether it was helpful.
              </Typography>
            </Paper>
          ) : (
            hintHistory.map((hint) => (
              <HintHistoryCard
                key={hint.hintId}
                hint={hint}
                remainingCount={remainingByType[hint.hintType]}
                onRate={rateHint}
                onEscalationNotesChange={updateEscalationNotes}
                onEscalate={markEscalated}
                onRequestStronger={() => void requestStrongerHint(hint)}
                disabled={hintBusy}
              />
            ))
          )}
        </Stack>
      </Box>
    </Stack>
  );
}

function HintHistoryCard({
  hint,
  remainingCount,
  onRate,
  onEscalationNotesChange,
  onEscalate,
  onRequestStronger,
  disabled
}: {
  hint: HintHistoryRecord;
  remainingCount: number;
  onRate: (hintId: string, rating: Exclude<HintRating, null>) => void;
  onEscalationNotesChange: (hintId: string, escalationNotes: string) => void;
  onEscalate: (hintId: string) => void;
  onRequestStronger: () => void;
  disabled: boolean;
}) {
  return (
    <Paper
      sx={{
        p: 1.35,
        borderRadius: 3.5,
        boxShadow: "none",
        border: "1px solid",
        borderColor:
          hint.rating === "helpful"
            ? alpha("#46705C", 0.18)
            : hint.rating === "unhelpful"
              ? alpha("#8D6A34", 0.2)
              : alpha("#1E6676", 0.14),
        bgcolor:
          hint.rating === "helpful"
            ? alpha("#EEF5F1", 0.7)
            : hint.rating === "unhelpful"
              ? alpha("#F8F2E7", 0.78)
              : alpha("#FFFFFF", 0.92)
      }}
    >
      <Stack spacing={1.15}>
        <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" spacing={1}>
          <Stack direction="row" spacing={0.75} flexWrap="wrap" useFlexGap>
            <MetaChip label={formatHintTypeLabel(hint.hintType)} tone="primary" />
            <MetaChip label={`Level ${hint.level}`} />
            {hint.target ? <MetaChip label={`Focus: ${hint.target.label}`} /> : null}
            {hint.rating === "helpful" ? (
              <MetaChip label="Helpful" tone="success" />
            ) : hint.rating === "unhelpful" ? (
              <MetaChip label="Needs follow-up" tone="warning" />
            ) : null}
          </Stack>
          <Typography variant="caption" sx={{ color: "text.secondary" }}>
            {formatSessionTime(hint.createdAt)}
          </Typography>
        </Stack>

        <Box>
          <Typography variant="h4">{hint.title}</Typography>
          <Typography variant="body1" sx={{ mt: 0.45 }}>
            {hint.body}
          </Typography>
        </Box>

        {hint.reflection ? (
          <Paper
            sx={{
              p: 1,
              borderRadius: 2.8,
              boxShadow: "none",
              bgcolor: alpha("#F8FAFC", 0.84)
            }}
          >
            <Typography variant="caption" sx={{ color: "text.secondary", display: "block", mb: 0.25 }}>
              Your note
            </Typography>
            <Typography variant="body2" sx={{ color: "text.primary" }}>
              {hint.reflection}
            </Typography>
          </Paper>
        ) : null}

        {hint.rating === null ? (
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
            <Button variant="outlined" color="success" onClick={() => onRate(hint.hintId, "helpful")} disabled={disabled}>
              Helpful
            </Button>
            <Button variant="outlined" color="warning" onClick={() => onRate(hint.hintId, "unhelpful")} disabled={disabled}>
              Not helpful
            </Button>
          </Stack>
        ) : null}

        {hint.rating === "unhelpful" ? (
          <Stack spacing={1}>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
              <Button variant="outlined" onClick={onRequestStronger} disabled={remainingCount <= 0 || disabled}>
                {remainingCount > 0 ? "Try a stronger hint" : "No stronger hints left"}
              </Button>
              <Button variant="text" disabled>
                Ask coach (next step)
              </Button>
            </Stack>

            <TextField
              size="small"
              multiline
              minRows={2}
              placeholder="Why was this hint not enough? This note can be reused for escalation later."
              value={hint.escalationNotes}
              onChange={(event) => onEscalationNotesChange(hint.hintId, event.target.value)}
              disabled={disabled}
            />

            {hint.escalated ? (
              <Typography variant="caption" sx={{ color: "success.main" }}>
                Escalation prototype saved locally. Backend routing can be added next.
              </Typography>
            ) : (
              <Button variant="outlined" onClick={() => onEscalate(hint.hintId)} disabled={disabled}>
                Save escalation note
              </Button>
            )}
          </Stack>
        ) : null}
      </Stack>
    </Paper>
  );
}

function SectionHeader({
  eyebrow,
  title,
  description,
  action
}: {
  eyebrow: string;
  title: string;
  description?: string;
  action?: ReactNode;
}) {
  return (
    <Stack direction={{ xs: "column", sm: "row" }} justifyContent="space-between" alignItems={{ xs: "flex-start", sm: "flex-end" }} spacing={1.25} sx={{ mb: 1.4 }}>
      <Box>
        <Typography variant="caption" sx={{ color: "text.disabled", display: "block", mb: 0.3 }}>
          {eyebrow}
        </Typography>
        <Typography variant="h3" sx={{ mt: 0.1 }}>
          {title}
        </Typography>
        {description ? (
          <Typography variant="body2" sx={{ mt: 0.28, maxWidth: 540 }}>
            {description}
          </Typography>
        ) : null}
      </Box>
      {action}
    </Stack>
  );
}

function PoolDropSurface({
  active,
  children,
  onDragOver,
  onDrop
}: {
  active: boolean;
  children: ReactNode;
  onDragOver: DragEventHandler<HTMLDivElement>;
  onDrop: DragEventHandler<HTMLDivElement>;
}) {
  return (
    <Box
      onDragOver={onDragOver}
      onDrop={onDrop}
      sx={{
        borderRadius: 3,
        border: "1px solid",
        borderColor: active ? "primary.main" : "divider",
        bgcolor: active ? alpha("#1E6676", 0.045) : alpha("#FFFFFF", 0.76),
        p: 0.8,
        transition: "border-color 140ms ease, background-color 140ms ease"
      }}
    >
      {children}
    </Box>
  );
}

function PoolBlock({
  text,
  dimmed,
  onPick,
  onDragStart,
  onDragEnd
}: {
  text: string;
  dimmed: boolean;
  onPick: () => void;
  onDragStart: DragEventHandler<HTMLDivElement>;
  onDragEnd: DragEventHandler<HTMLDivElement>;
}) {
  return (
    <Box
      role="button"
      tabIndex={0}
      draggable
      onClick={onPick}
      onKeyDown={(event) => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          onPick();
        }
      }}
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
      sx={{
        display: "grid",
        gridTemplateColumns: "minmax(0, 1fr) auto",
        gap: 1.15,
        alignItems: "start",
        px: 1.2,
        py: 1,
        borderRadius: 2.5,
        border: "1px solid",
        borderColor: dimmed ? alpha("#E3E8EE", 0.92) : alpha("#CED7E1", 0.7),
        bgcolor: dimmed ? alpha("#F6F8FB", 0.8) : alpha("#FFFFFF", 0.92),
        cursor: "grab",
        opacity: dimmed ? 0.48 : 1,
        transition: "transform 140ms ease, border-color 140ms ease, background-color 140ms ease",
        '&:hover': {
          borderColor: alpha("#1E6676", 0.34),
          bgcolor: alpha("#1E6676", 0.03),
          transform: "translateY(-1px)"
        },
        '&:focus-visible': {
          outline: "2px solid",
          outlineColor: alpha("#1E6676", 0.26),
          outlineOffset: 2
        }
      }}
    >
      <Typography
        component="pre"
        className="code-face"
        sx={{
          m: 0,
          color: "text.primary",
          fontSize: "0.83rem",
          lineHeight: 1.68,
          whiteSpace: "pre-wrap",
          wordBreak: "break-word"
        }}
      >
        {text}
      </Typography>
      <Typography variant="caption" sx={{ color: "text.disabled", whiteSpace: "nowrap", pt: 0.25 }}>
        Add
      </Typography>
    </Box>
  );
}

function AnswerBuilderPanel({
  task,
  answerOptions,
  dragState,
  grading,
  readyToSubmit,
  onReset,
  onSubmit,
  onDropIntoAnswer,
  onStartDrag,
  onEndDrag,
  onRemove
}: {
  task: Extract<StudentTaskResponse, { itemType: "parsons" }>;
  answerOptions: BlockOption[];
  dragState: DragState | null;
  grading: boolean;
  readyToSubmit: boolean;
  onReset: () => void;
  onSubmit: () => void;
  onDropIntoAnswer: (insertAt?: number) => void;
  onStartDrag: (source: "available" | "answer", optionId: string) => void;
  onEndDrag: () => void;
  onRemove: (optionId: string) => void;
}) {
  return (
    <Box
      sx={{
        position: { xl: "sticky" },
        top: { xl: 24 },
        borderRadius: 4,
        border: "1px solid",
        borderColor: alpha("#1E6676", 0.22),
        bgcolor: "background.paper",
        boxShadow: `0 12px 28px ${alpha("#0F172A", 0.05)}`,
        p: { xs: 2.1, md: 2.4 }
      }}
    >
      <Stack spacing={1.6}>
        <SectionHeader
          eyebrow="Step 2"
          title="Build answer"
          description={`Place ${task.requiredBlockCount} blocks in order.`}
        />

        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <MetaChip label={`${answerOptions.length}/${task.requiredBlockCount} selected`} tone="primary" />
          {readyToSubmit && <MetaChip label="Ready to submit" tone="success" />}
        </Stack>

        <AnswerDropArea
          isEmpty={answerOptions.length === 0}
          active={dragState !== null}
          onDragOver={(event) => {
            event.preventDefault();
          }}
          onDrop={(event) => {
            event.preventDefault();
            onDropIntoAnswer();
          }}
        >
          {answerOptions.length === 0 ? (
            <Stack spacing={0.75} sx={{ maxWidth: 360 }}>
              <Typography variant="h3">Drop blocks here</Typography>
              <Typography variant="body2" color="text.secondary">
                Tap or drag from the pool.
              </Typography>
            </Stack>
          ) : (
            <Stack spacing={1}>
              <AnswerInsertionMarker
                visible={dragState !== null}
                onDragOver={(event) => {
                  event.preventDefault();
                }}
                onDrop={(event) => {
                  event.preventDefault();
                  onDropIntoAnswer(0);
                }}
              />
              {answerOptions.map((option, index) => (
                <Stack key={option.id} spacing={1}>
                  <AnswerBlockCard
                    index={index}
                    text={option.text}
                    dimmed={dragState?.optionId === option.id}
                    onDragStart={(event) => {
                      event.dataTransfer.effectAllowed = "move";
                      onStartDrag("answer", option.id);
                    }}
                    onDragEnd={onEndDrag}
                    onRemove={() => onRemove(option.id)}
                  />
                  <AnswerInsertionMarker
                    visible={dragState !== null}
                    onDragOver={(event) => {
                      event.preventDefault();
                    }}
                    onDrop={(event) => {
                      event.preventDefault();
                      onDropIntoAnswer(index + 1);
                    }}
                  />
                </Stack>
              ))}
            </Stack>
          )}
        </AnswerDropArea>

        <Stack spacing={1.1}>
          <Typography variant="body2" sx={{ color: readyToSubmit ? "primary.main" : "text.secondary" }}>
            {readyToSubmit ? "Ready to submit." : `${task.requiredBlockCount} blocks needed.`}
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.1}>
            <Button variant="outlined" startIcon={<ReplayRounded />} onClick={onReset}>
              Reset attempt
            </Button>
            <Button
              variant="contained"
              startIcon={grading ? <CircularProgress size={15} color="inherit" /> : <CheckCircleRounded />}
              onClick={onSubmit}
              disabled={grading}
            >
              Submit answer
            </Button>
          </Stack>
        </Stack>
      </Stack>
    </Box>
  );
}

function DropdownTemplatePanel({
  task,
  answers
}: {
  task: Extract<StudentTaskResponse, { itemType: "dropdown" }>;
  answers: Record<string, string>;
}) {
  const substitutions = Object.fromEntries(
    task.blanks.map((blank) => [blank.placeholder, answers[blank.blankId] ?? ""])
  );

  return (
    <Box>
      <SectionHeader
        eyebrow="Step 1"
        title="Template"
        description="Selections appear inline."
      />
      <Paper sx={{ p: 1.5, borderRadius: 3.5, boxShadow: "none", bgcolor: alpha("#FFFFFF", 0.92) }}>
        <CodeTemplatePreview template={task.promptTemplate} substitutions={substitutions} />
      </Paper>
    </Box>
  );
}

function DropdownAnswerPanel({
  task,
  optionOrder,
  answers,
  grading,
  readyToSubmit,
  onSelect,
  onReset,
  onSubmit
}: {
  task: Extract<StudentTaskResponse, { itemType: "dropdown" }>;
  optionOrder: Record<string, string[]>;
  answers: Record<string, string>;
  grading: boolean;
  readyToSubmit: boolean;
  onSelect: (blankId: string, option: string) => void;
  onReset: () => void;
  onSubmit: () => void;
}) {
  const answeredCount = task.blanks.filter((blank) => {
    const value = answers[blank.blankId];
    return typeof value === "string" && value.trim().length > 0;
  }).length;

  return (
    <Box
      sx={{
        position: { xl: "sticky" },
        top: { xl: 24 },
        borderRadius: 4,
        border: "1px solid",
        borderColor: alpha("#1E6676", 0.22),
        bgcolor: "background.paper",
        boxShadow: `0 12px 28px ${alpha("#0F172A", 0.05)}`,
        p: { xs: 2.1, md: 2.4 }
      }}
    >
      <Stack spacing={1.6}>
        <SectionHeader
          eyebrow="Step 2"
          title="Pick choices"
          description="One option per blank."
        />

        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <MetaChip label={`${answeredCount}/${task.requiredBlankCount} answered`} tone="primary" />
          {readyToSubmit && <MetaChip label="Ready to submit" tone="success" />}
        </Stack>

        <Box
          sx={{
            minHeight: 280,
            p: 1,
            borderRadius: 3.5,
            border: "1px solid",
            borderColor: alpha("#CED7E1", 0.78),
            bgcolor: alpha("#F8FAFC", 0.9),
            display: "flex",
            flexDirection: "column",
            gap: 1
          }}
        >
          {task.blanks.map((blank, index) => (
            <Paper key={blank.blankId} sx={{ p: 1.15, borderRadius: 3, boxShadow: "none", bgcolor: "background.paper" }}>
              <Stack spacing={1}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                  <Chip size="small" label={`Blank ${index + 1}`} color="primary" />
                  <Typography variant="caption" sx={{ color: answers[blank.blankId] ? "primary.main" : "text.disabled", fontWeight: answers[blank.blankId] ? 600 : 500 }}>
                    {answers[blank.blankId] ? `Selected: ${answers[blank.blankId]}` : blank.placeholder}
                  </Typography>
                </Stack>
                <Stack direction="row" spacing={0.8} flexWrap="wrap" useFlexGap>
                  {(optionOrder[blank.blankId] ?? blank.options).map((option) => {
                    const selected = answers[blank.blankId] === option;
                    return (
                      <Button
                        key={option}
                        size="small"
                        variant={selected ? "contained" : "outlined"}
                        onClick={() => onSelect(blank.blankId, option)}
                      >
                        {option}
                      </Button>
                    );
                  })}
                </Stack>
              </Stack>
            </Paper>
          ))}
        </Box>

        <Stack spacing={1.1}>
          <Typography variant="body2" sx={{ color: readyToSubmit ? "primary.main" : "text.secondary" }}>
            {readyToSubmit ? "Ready to submit." : `${task.requiredBlankCount} blanks to fill.`}
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.1}>
            <Button variant="outlined" startIcon={<ReplayRounded />} onClick={onReset}>
              Reset attempt
            </Button>
            <Button
              variant="contained"
              startIcon={grading ? <CircularProgress size={15} color="inherit" /> : <CheckCircleRounded />}
              onClick={onSubmit}
              disabled={grading}
            >
              Submit answer
            </Button>
          </Stack>
        </Stack>
      </Stack>
    </Box>
  );
}

function ExecutionTracePromptPanel({
  task
}: {
  task: Extract<StudentTaskResponse, { itemType: "execution-trace" }>;
}) {
  return (
    <Box>
      <SectionHeader
        eyebrow="Step 1"
        title="Function"
        description="Trace the call, then fill each checkpoint."
      />
      <Stack spacing={1.35}>
        <Paper sx={{ p: 1.5, borderRadius: 3.5, boxShadow: "none", bgcolor: alpha("#FFFFFF", 0.92) }}>
          <Stack spacing={1.1}>
            <Typography variant="body2" color="text.secondary">
              Concrete call
            </Typography>
            <Typography component="pre" className="code-face" sx={{ m: 0, fontSize: "0.84rem", lineHeight: 1.7, whiteSpace: "pre-wrap" }}>
              {task.callExpression}
            </Typography>
          </Stack>
        </Paper>

        <Paper sx={{ p: 1.5, borderRadius: 3.5, boxShadow: "none", bgcolor: alpha("#FFFFFF", 0.92) }}>
          <CodeTemplatePreview template={task.functionSource} />
        </Paper>

        <Paper
          sx={{
            p: 1.35,
            borderRadius: 3.5,
            boxShadow: "none",
            bgcolor: alpha("#FFFFFF", 0.92)
          }}
        >
          <Stack spacing={1}>
            <Typography variant="body2" color="text.secondary">
              Checkpoints
            </Typography>
            {task.checkpoints.map((checkpoint, index) => (
              <Box key={checkpoint.checkpointId} sx={{ borderTop: index === 0 ? "none" : "1px solid", borderColor: "divider", pt: index === 0 ? 0 : 1 }}>
                <Typography variant="body2" sx={{ fontWeight: 600 }}>
                  {checkpoint.checkpointId}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  After line {checkpoint.lineNumber}: <code>{checkpoint.lineExcerpt.trim()}</code>
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Record the value of <code>{checkpoint.variableName}</code>.
                </Typography>
              </Box>
            ))}
          </Stack>
        </Paper>
      </Stack>
    </Box>
  );
}

function ExecutionTraceAnswerPanel({
  task,
  answers,
  grading,
  readyToSubmit,
  onChange,
  onBlur,
  onReset,
  onSubmit
}: {
  task: Extract<StudentTaskResponse, { itemType: "execution-trace" }>;
  answers: Record<string, string>;
  grading: boolean;
  readyToSubmit: boolean;
  onChange: (checkpointId: string, value: string) => void;
  onBlur: (checkpointId: string, value: string) => void;
  onReset: () => void;
  onSubmit: () => void;
}) {
  const answeredCount = task.checkpoints.filter((checkpoint) => {
    const value = answers[checkpoint.checkpointId];
    return typeof value === "string" && value.trim().length > 0;
  }).length;

  return (
    <Box
      sx={{
        position: { xl: "sticky" },
        top: { xl: 24 },
        borderRadius: 4,
        border: "1px solid",
        borderColor: alpha("#1E6676", 0.22),
        bgcolor: "background.paper",
        boxShadow: `0 12px 28px ${alpha("#0F172A", 0.05)}`,
        p: { xs: 2.1, md: 2.4 }
      }}
    >
      <Stack spacing={1.6}>
        <SectionHeader
          eyebrow="Step 2"
          title="Trace answers"
          description="Enter the observed value at each checkpoint."
        />

        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <MetaChip label={`${answeredCount}/${task.requiredCheckpointCount} answered`} tone="primary" />
          {readyToSubmit && <MetaChip label="Ready to submit" tone="success" />}
        </Stack>

        <Box
          sx={{
            minHeight: 280,
            p: 1,
            borderRadius: 3.5,
            border: "1px solid",
            borderColor: alpha("#CED7E1", 0.78),
            bgcolor: alpha("#F8FAFC", 0.9),
            display: "flex",
            flexDirection: "column",
            gap: 1
          }}
        >
          {task.checkpoints.map((checkpoint, index) => (
            <Paper key={checkpoint.checkpointId} sx={{ p: 1.15, borderRadius: 3, boxShadow: "none", bgcolor: "background.paper" }}>
              <Stack spacing={1}>
                <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
                  <Chip size="small" label={`Checkpoint ${index + 1}`} color="primary" />
                  <Typography variant="caption">{checkpoint.variableName}</Typography>
                </Stack>
                <Typography variant="body2" color="text.secondary">
                  After line {checkpoint.lineNumber}: <code>{checkpoint.lineExcerpt.trim()}</code>
                </Typography>
                <TextField
                  size="small"
                  fullWidth
                  value={answers[checkpoint.checkpointId] ?? ""}
                  onChange={(event) => onChange(checkpoint.checkpointId, event.target.value)}
                  onBlur={(event) => onBlur(checkpoint.checkpointId, event.target.value)}
                  placeholder="e.g. ['hello'] or 'QXZ'"
                />
              </Stack>
            </Paper>
          ))}
        </Box>

        <Stack spacing={1.1}>
          <Typography variant="body2" sx={{ color: readyToSubmit ? "primary.main" : "text.secondary" }}>
            {readyToSubmit ? "Ready to submit." : `${task.requiredCheckpointCount} checkpoints to fill.`}
          </Typography>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.1}>
            <Button variant="outlined" startIcon={<ReplayRounded />} onClick={onReset}>
              Reset attempt
            </Button>
            <Button
              variant="contained"
              startIcon={grading ? <CircularProgress size={15} color="inherit" /> : <CheckCircleRounded />}
              onClick={onSubmit}
              disabled={grading}
            >
              Submit answer
            </Button>
          </Stack>
        </Stack>
      </Stack>
    </Box>
  );
}

function CodeTemplatePreview({
  template,
  substitutions
}: {
  template: string;
  substitutions?: Record<string, string>;
}) {
  return (
    <Box
      className="code-face"
      sx={{
        m: 0,
        color: "text.primary",
        fontSize: "0.84rem",
        lineHeight: 1.78,
        whiteSpace: "pre-wrap",
        wordBreak: "break-word"
      }}
    >
      {template.split(/(__BLANK_\d+__)/g).map((part, index) =>
        /^__BLANK_\d+__$/.test(part) ? (() => {
          const selectedValue = substitutions?.[part]?.trim();
          const filled = Boolean(selectedValue);
          return (
            <Box
              key={`${part}-${index}`}
              component="span"
              sx={{
                display: "inline-block",
                px: 0.75,
                py: 0.15,
                mx: 0.15,
                borderRadius: 999,
                bgcolor: filled ? alpha("#1E6676", 0.16) : alpha("#1E6676", 0.11),
                color: filled ? "text.primary" : "primary.main",
                border: "1px solid",
                borderColor: filled ? alpha("#1E6676", 0.18) : "transparent",
                fontWeight: 600
              }}
            >
              {filled ? selectedValue : part}
            </Box>
          );
        })() : (
          <Box key={`${part}-${index}`} component="span">
            {part}
          </Box>
        )
      )}
    </Box>
  );
}

function AnswerDropArea({
  isEmpty,
  active,
  children,
  onDragOver,
  onDrop
}: {
  isEmpty: boolean;
  active: boolean;
  children: ReactNode;
  onDragOver: DragEventHandler<HTMLDivElement>;
  onDrop: DragEventHandler<HTMLDivElement>;
}) {
  return (
    <Box
      onDragOver={onDragOver}
      onDrop={onDrop}
      sx={{
        minHeight: 280,
        p: 1.1,
        borderRadius: 3.5,
        border: "1px solid",
        borderColor: active ? "primary.main" : isEmpty ? "divider" : alpha("#1E6676", 0.16),
        bgcolor: active ? alpha("#F8FCFD", 0.94) : alpha("#F8FAFC", 0.94),
        transition: "border-color 140ms ease, background-color 140ms ease",
        display: "flex",
        flexDirection: "column",
        justifyContent: isEmpty ? "center" : "flex-start"
      }}
    >
      {children}
    </Box>
  );
}

function AnswerInsertionMarker({
  visible,
  onDragOver,
  onDrop
}: {
  visible: boolean;
  onDragOver: DragEventHandler<HTMLDivElement>;
  onDrop: DragEventHandler<HTMLDivElement>;
}) {
  if (!visible) {
    return null;
  }

  return (
    <Box
      onDragOver={onDragOver}
      onDrop={onDrop}
      sx={{
        height: 10,
        borderRadius: 999,
        bgcolor: alpha("#1E6676", 0.14)
      }}
    />
  );
}

function AnswerBlockCard({
  index,
  text,
  dimmed,
  onDragStart,
  onDragEnd,
  onRemove
}: {
  index: number;
  text: string;
  dimmed: boolean;
  onDragStart: DragEventHandler<HTMLDivElement>;
  onDragEnd: DragEventHandler<HTMLDivElement>;
  onRemove: () => void;
}) {
  return (
    <Paper
      draggable
      onDragStart={onDragStart}
      onDragEnd={onDragEnd}
      sx={{
        px: 1.2,
        py: 1.15,
        borderRadius: 3.25,
        boxShadow: "none",
        cursor: "grab",
        borderColor: alpha("#CED7E1", 0.78),
        opacity: dimmed ? 0.48 : 1
      }}
    >
      <Stack spacing={1}>
        <Stack direction="row" justifyContent="space-between" alignItems="center" spacing={1}>
          <Chip size="small" label={`Step ${index + 1}`} color="primary" />
          <Button size="small" variant="text" color="primary" onClick={onRemove}>
            Remove
          </Button>
        </Stack>
        <Typography
          component="pre"
          className="code-face"
          sx={{
            m: 0,
            color: "text.primary",
            fontSize: "0.84rem",
            lineHeight: 1.72,
            whiteSpace: "pre-wrap",
            wordBreak: "break-word"
          }}
        >
          {text}
        </Typography>
      </Stack>
    </Paper>
  );
}

function FeedbackCard({ feedback, onNext }: { feedback: StudentGradeResponse; onNext: () => void }) {
  const nextAction = getNextAction(feedback);

  return (
    <Paper
      sx={{
        p: { xs: 2, md: 2.2 },
        borderRadius: 3.5,
        borderColor: feedback.correct ? alpha("#46705C", 0.18) : alpha("#8D6A34", 0.18),
        bgcolor: feedback.correct ? alpha("#EEF5F1", 0.84) : alpha("#F8F2E7", 0.84),
        boxShadow: "none"
      }}
    >
      <Stack spacing={1.35}>
        <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
          <MetaChip label={feedback.correct ? "Correct" : "Needs revision"} tone={feedback.correct ? "success" : "warning"} />
          <MetaChip
            label={
              feedback.itemType === "parsons"
                ? `${feedback.correctCount}/${feedback.expectedCount} positions correct`
                : feedback.itemType === "dropdown"
                  ? `${feedback.correctCount}/${feedback.expectedCount} blanks correct`
                  : `${feedback.correctCount}/${feedback.expectedCount} checkpoints correct`
            }
          />
        </Stack>

        <Typography variant="h3">{feedback.correct ? "Answer accepted" : "Needs revision"}</Typography>
        <Typography variant="body1" sx={{ color: "text.primary" }}>
          {feedback.feedback}
        </Typography>

        <Box sx={{ pt: 1.35, borderTop: "1px solid", borderColor: alpha("#18222C", 0.08) }}>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            Next action
          </Typography>
          <Typography variant="body1" sx={{ mt: 0.45 }}>
            {nextAction}
          </Typography>
        </Box>

        <Stack direction={{ xs: "column", sm: "row" }} spacing={1}>
          <Button variant={feedback.correct ? "contained" : "outlined"} onClick={onNext}>
            Go to next item
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
}

function PracticeLockOverlay({
  eventCount,
  latestEvent,
  onResume
}: {
  eventCount: number;
  latestEvent: FocusLossEvent | null;
  onResume: () => void;
}) {
  return (
    <Box
      sx={{
        position: "absolute",
        inset: 0,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        p: 2.5,
        bgcolor: alpha("#F6F8FB", 0.72),
        backdropFilter: "blur(6px)"
      }}
    >
      <Paper
        sx={{
          width: "min(440px, 100%)",
          p: { xs: 2.2, md: 2.5 },
          borderRadius: 4,
          boxShadow: "none"
        }}
      >
        <Stack spacing={1.4}>
          <Stack direction="row" spacing={1} alignItems="center">
            <LockOutlined color="primary" fontSize="small" />
            <Typography variant="h3">Practice locked after focus loss</Typography>
          </Stack>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            The task view was hidden after this browser tab lost focus. Resume only when you are ready to continue here.
          </Typography>
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            <MetaChip label={`${eventCount} focus event${eventCount === 1 ? "" : "s"}`} tone="warning" />
            {latestEvent && (
              <MetaChip
                label={`${latestEvent.reason === "tab-hidden" ? "Tab hidden" : "Window blurred"} · ${formatSessionTime(latestEvent.timestamp)}`}
              />
            )}
          </Stack>
          <Box>
            <Button variant="contained" onClick={onResume}>
              Resume practice
            </Button>
          </Box>
        </Stack>
      </Paper>
    </Box>
  );
}

function MetaChip({
  label,
  tone = "default"
}: {
  label: string;
  tone?: "default" | "primary" | "success" | "warning";
}) {
  const color = tone === "primary" ? "primary" : tone === "success" ? "success" : tone === "warning" ? "warning" : "secondary";
  return <Chip size="small" label={label} color={color} />;
}

function LoadingState({ message }: { message: string }) {
  return (
    <Stack direction="row" spacing={1} alignItems="center">
      <CircularProgress size={18} />
      <Typography variant="body2">{message}</Typography>
    </Stack>
  );
}

function getNextAction(feedback: StudentGradeResponse): string {
  if (feedback.correct) {
    return feedback.itemType === "parsons"
      ? "Move to the next item or retry this one to confirm the ordering pattern."
      : feedback.itemType === "dropdown"
        ? "Move to the next item or retry this one to confirm the blank selection pattern."
        : "Move to the next item or retry this one to confirm the execution trace pattern.";
  }

  if (feedback.selectedCount !== feedback.expectedCount) {
    return feedback.itemType === "parsons"
      ? `Remove or add blocks until exactly ${feedback.expectedCount} remain in the builder.`
      : feedback.itemType === "dropdown"
        ? `Answer all ${feedback.expectedCount} blanks before submitting again.`
        : `Fill in all ${feedback.expectedCount} checkpoint values before submitting again.`;
  }

  if (feedback.correctCount > 0) {
    return feedback.itemType === "parsons"
      ? "Keep the blocks already in the right positions, then reorder the remaining ones."
      : feedback.itemType === "dropdown"
        ? "Keep the blanks you already solved and revise the remaining incorrect selections."
        : "Keep the checkpoint values you already solved and revise the remaining traced values.";
  }

  return feedback.itemType === "parsons"
    ? "A distractor is likely present. Return to the option pool and rebuild the sequence."
    : feedback.itemType === "dropdown"
      ? "Review the code template and reconsider how each option changes the source logic."
      : "Re-run the function mentally from the concrete call and focus on how each checkpoint variable changes.";
}

function makeKey(queryId: string, taskId: string, itemType: "parsons" | "dropdown" | "execution-trace"): string {
  return `${queryId}::${taskId}::${itemType}`;
}

function shuffle<T>(items: T[]): T[] {
  const next = [...items];
  for (let index = next.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(Math.random() * (index + 1));
    [next[index], next[swapIndex]] = [next[swapIndex], next[index]];
  }
  return next;
}

function formatPercent(value: number | null | undefined): string {
  if (value === null || value === undefined || Number.isNaN(value)) {
    return "n/a";
  }
  return `${Math.round(value * 10) / 10}%`;
}

function formatItemTypeLabel(itemType: "parsons" | "dropdown" | "execution-trace"): string {
  return itemType === "execution-trace"
    ? "Execution trace"
    : itemType.charAt(0).toUpperCase() + itemType.slice(1);
}

function formatSessionTime(timestamp: string): string {
  try {
    return new Intl.DateTimeFormat("en", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false
    }).format(new Date(timestamp));
  } catch {
    return timestamp;
  }
}

function createHintBudget(): Record<StudentHintType, number> {
  return { ...HINT_LIMITS };
}

function formatHintTypeLabel(hintType: StudentHintType): string {
  return hintType === "understand"
    ? "Understand"
    : hintType === "next-step"
      ? "Next step"
      : "Check one issue";
}

function getHintDescription(hintType: StudentHintType): string {
  return hintType === "understand"
    ? "Clarify what the task is asking."
    : hintType === "next-step"
      ? "Get a small action to try next."
      : "Inspect one likely source of error.";
}

function getHintInputPlaceholder(hintType: StudentHintType): string {
  return hintType === "understand"
    ? "Example: I understand the story, but I do not know what the output should represent."
    : hintType === "next-step"
      ? "Example: I do not know which block / blank / checkpoint to inspect first."
      : "Example: I think one part is wrong, but I cannot tell whether it is order, logic, or tracing.";
}

function shouldBypassClipboardLock(target: EventTarget | null): boolean {
  return target instanceof Element && Boolean(target.closest('[data-allow-clipboard="true"]'));
}

async function requestHintViaBackend(requestBody: StudentHintRequest): Promise<StudentHintResponse> {
  const response = await fetch(resolveHintApiUrl(), {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(requestBody)
  });
  const payload = (await response.json()) as StudentHintResponse & { error?: string };
  if (!response.ok) {
    throw new Error(payload.error ?? "Failed to generate hint.");
  }

  return payload;
}

async function requestHintWithDeveloperKey(
  requestBody: StudentHintRequest,
  apiKey: string
): Promise<StudentHintResponse> {
  const task = requestBody.taskContext;
  if (!task) {
    throw new Error("taskContext is required for browser-direct hints.");
  }

  if (requestBody.lastFeedback?.correct) {
    return {
      hintId: createClientId("hint"),
      hintType: requestBody.hintType,
      level: requestBody.level,
      title: "Already solved",
      body: "This attempt is already correct. Use the feedback to confirm why it works, or move to the next task.",
      target: null,
      escalationAvailable: false,
      model: "local-status"
    };
  }

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`
    },
    body: JSON.stringify(buildOpenAIHintRequestBody(task, requestBody, DEV_BROWSER_HINT_MODEL))
  });
  const payload = (await response.json()) as OpenAIResponsesPayload;
  if (!response.ok) {
    throw new Error(payload.error?.message ?? "OpenAI hint generation failed.");
  }

  const parsed = parseHintModelOutput(payload);
  return {
    hintId: createClientId("hint"),
    hintType: requestBody.hintType,
    level: requestBody.level,
    title: normalizeHintTitle(parsed.title, requestBody.hintType, requestBody.level),
    body: normalizeHintBody(parsed.body),
    target: normalizeHintTarget(parsed.target),
    escalationAvailable: parsed.escalationAvailable,
    model: DEV_BROWSER_HINT_MODEL
  };
}

function resolveHintApiUrl(): string {
  if (!EXTERNAL_HINT_API_BASE_URL) {
    return "/api/studio/student/hint";
  }

  return `${EXTERNAL_HINT_API_BASE_URL.replace(/\/+$/, "")}/student/hint`;
}

function createClientId(prefix: string): string {
  if (typeof crypto !== "undefined" && typeof crypto.randomUUID === "function") {
    return `${prefix}-${crypto.randomUUID()}`;
  }

  return `${prefix}-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}
