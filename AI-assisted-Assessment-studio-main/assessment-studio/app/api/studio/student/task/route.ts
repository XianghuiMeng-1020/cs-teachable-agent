import { NextResponse } from "next/server";
import { getStudentTask } from "@/src/server/studio-data";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const queryId = searchParams.get("queryId");
  const taskId = searchParams.get("taskId");
  const itemType = searchParams.get("itemType");
  const bypassCache = searchParams.get("refresh") === "1";

  if (!queryId || !taskId) {
    return NextResponse.json({ error: "queryId and taskId are required." }, { status: 400 });
  }

  try {
    const normalizedItemType =
      itemType === "dropdown" || itemType === "execution-trace" ? itemType : "parsons";
    const task = await getStudentTask(queryId, taskId, normalizedItemType, { bypassCache });
    return NextResponse.json(task);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to load student task." },
      { status: 500 }
    );
  }
}
