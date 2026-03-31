import { NextResponse } from "next/server";
import { generateStudentHint } from "@/src/server/hint-service";
import type { StudentHintRequest } from "@/src/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  if (!process.env.OPENAI_API_KEY) {
    return NextResponse.json(
      { error: "OPENAI_API_KEY is not available in the Next.js server environment." },
      { status: 400 }
    );
  }

  try {
    const body = (await request.json()) as Partial<StudentHintRequest>;

    if (!body.queryId || !body.taskId || !body.itemType || !body.hintType || !body.level) {
      return NextResponse.json(
        { error: "queryId, taskId, itemType, hintType, and level are required." },
        { status: 400 }
      );
    }

    if (
      body.itemType !== "parsons" &&
      body.itemType !== "dropdown" &&
      body.itemType !== "execution-trace"
    ) {
      return NextResponse.json({ error: "Unsupported itemType." }, { status: 400 });
    }

    if (
      body.hintType !== "understand" &&
      body.hintType !== "next-step" &&
      body.hintType !== "check-one-issue"
    ) {
      return NextResponse.json({ error: "Unsupported hintType." }, { status: 400 });
    }

    if (body.level !== 1 && body.level !== 2 && body.level !== 3) {
      return NextResponse.json({ error: "level must be 1, 2, or 3." }, { status: 400 });
    }

    const hint = await generateStudentHint({
      queryId: body.queryId,
      taskId: body.taskId,
      itemType: body.itemType,
      hintType: body.hintType,
      level: body.level,
      taskContext: body.taskContext,
      reflection: body.reflection,
      progressSummary: body.progressSummary,
      attemptNumber: body.attemptNumber ?? null,
      lastFeedback: body.lastFeedback ?? null,
      selectedBlocks: Array.isArray(body.selectedBlocks) ? body.selectedBlocks : undefined,
      selectedAnswers:
        body.selectedAnswers && typeof body.selectedAnswers === "object"
          ? body.selectedAnswers
          : undefined
    });

    return NextResponse.json(hint);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to generate hint." },
      { status: 500 }
    );
  }
}
