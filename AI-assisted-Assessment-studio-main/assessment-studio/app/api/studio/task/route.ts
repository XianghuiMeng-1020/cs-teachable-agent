import { NextResponse } from "next/server";
import { getTaskDetail } from "@/src/server/studio-data";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const queryId = searchParams.get("queryId");
  const taskId = searchParams.get("taskId");

  if (!queryId || !taskId) {
    return NextResponse.json({ error: "queryId and taskId are required." }, { status: 400 });
  }

  try {
    const detail = await getTaskDetail(queryId, taskId);
    return NextResponse.json(detail);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to load task detail." },
      { status: 500 }
    );
  }
}
