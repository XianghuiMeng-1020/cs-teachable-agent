import { NextResponse } from "next/server";
import { recordTelemetryEvents } from "@/src/server/student-telemetry";
import type { StudentTelemetryEvent } from "@/src/types";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as { events?: StudentTelemetryEvent[] };
    if (!Array.isArray(body.events)) {
      return NextResponse.json({ error: "events array is required." }, { status: 400 });
    }

    await recordTelemetryEvents(body.events);
    return NextResponse.json({ ok: true, count: body.events.length });
  } catch (error) {
    return NextResponse.json(
      { error: error instanceof Error ? error.message : "Failed to record telemetry events." },
      { status: 500 }
    );
  }
}
