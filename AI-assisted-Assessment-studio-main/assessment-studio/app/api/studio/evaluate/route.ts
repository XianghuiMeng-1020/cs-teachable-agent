import { NextResponse } from "next/server";
import { evaluateTypedAssessment } from "@/src/server/studio-data";

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
    const body = (await request.json()) as {
      queryId?: string;
      taskId?: string;
      model?: string;
      temperature?: number;
      numStudents?: number;
      passThreshold?: number;
    };

    if (!body.queryId || !body.taskId) {
      return NextResponse.json({ error: "queryId and taskId are required." }, { status: 400 });
    }

    const result = await evaluateTypedAssessment({
      queryId: body.queryId,
      taskId: body.taskId,
      model: body.model,
      temperature: body.temperature,
      numStudents: body.numStudents,
      passThreshold: body.passThreshold
    });

    return NextResponse.json(result);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to run typed assessment evaluation." },
      { status: 500 }
    );
  }
}
