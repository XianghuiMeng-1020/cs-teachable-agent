import { NextResponse } from "next/server";
import { getStudioIndexData } from "@/src/server/studio-data";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const data = await getStudioIndexData();
    return NextResponse.json(data);
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to load studio index." },
      { status: 500 }
    );
  }
}
