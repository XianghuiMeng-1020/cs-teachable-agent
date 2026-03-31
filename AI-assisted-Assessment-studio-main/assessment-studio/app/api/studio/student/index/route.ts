import { NextResponse } from "next/server";
import { getStudentEligibleTaskPayload } from "@/src/server/studio-data";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const maxAiPassRate = Number(searchParams.get("maxAiPassRate") ?? 75);
  const bypassCache = searchParams.get("refresh") === "1";

  try {
    const payload = await getStudentEligibleTaskPayload(maxAiPassRate, { bypassCache });
    return NextResponse.json(payload);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to load student task list." },
      { status: 500 }
    );
  }
}
