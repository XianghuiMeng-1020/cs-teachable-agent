import { NextResponse } from "next/server";
import { gradeStudentTask } from "@/src/server/studio-data";
import { recordAttemptRecord } from "@/src/server/student-telemetry";
import type { StudentAttemptRecord } from "@/src/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as {
      sessionId?: string;
      attemptId?: string;
      attemptNumber?: number;
      startedAt?: string;
      focusLossCount?: number;
      itemId?: string;
      queryId?: string;
      taskId?: string;
      itemType?: "parsons" | "dropdown" | "execution-trace";
      selectedBlocks?: string[];
      selectedAnswers?: Record<string, string>;
    };

    if (!body.queryId || !body.taskId || !body.itemType) {
      return NextResponse.json(
        { error: "queryId, taskId, and itemType are required." },
        { status: 400 }
      );
    }

    if (body.itemType === "parsons" && !Array.isArray(body.selectedBlocks)) {
      return NextResponse.json(
        { error: "selectedBlocks are required for Parsons submissions." },
        { status: 400 }
      );
    }

    if (
      (body.itemType === "dropdown" || body.itemType === "execution-trace") &&
      (!body.selectedAnswers || typeof body.selectedAnswers !== "object")
    ) {
      return NextResponse.json(
        { error: "selectedAnswers are required for dropdown and execution-trace submissions." },
        { status: 400 }
      );
    }

    const result = await gradeStudentTask({
      queryId: body.queryId,
      taskId: body.taskId,
      itemType: body.itemType,
      selectedBlocks: body.selectedBlocks,
      selectedAnswers: body.selectedAnswers
    });

    if (
      body.sessionId &&
      body.attemptId &&
      typeof body.attemptNumber === "number" &&
      body.startedAt &&
      body.itemId
    ) {
      const submittedAt = new Date().toISOString();
      const startedAt = new Date(body.startedAt);
      const durationMs = Number.isFinite(startedAt.getTime()) ? Math.max(0, Date.now() - startedAt.getTime()) : 0;
      const submission =
        body.itemType === "parsons"
          ? { selectedBlocks: body.selectedBlocks ?? [] }
          : { selectedAnswers: body.selectedAnswers ?? {} };

      const attemptRecord: StudentAttemptRecord = {
        attemptId: body.attemptId,
        sessionId: body.sessionId,
        attemptNumber: body.attemptNumber,
        queryId: body.queryId,
        taskId: body.taskId,
        itemId: body.itemId,
        itemType: body.itemType,
        startedAt: body.startedAt,
        submittedAt,
        durationMs,
        focusLossCount: typeof body.focusLossCount === "number" ? body.focusLossCount : 0,
        isCorrect: result.correct,
        score: result.expectedCount > 0 ? result.correctCount / result.expectedCount : 0,
        expectedCount: result.expectedCount,
        selectedCount: result.selectedCount,
        correctCount: result.correctCount,
        submission,
        feedback: result
      };

      await recordAttemptRecord(attemptRecord);
    }

    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to grade student submission." },
      { status: 500 }
    );
  }
}
