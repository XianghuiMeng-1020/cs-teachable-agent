import { useState } from "react";
import { TranscriptList } from "@/components/transcripts/TranscriptList";
import { TranscriptDetail } from "@/components/transcripts/TranscriptDetail";

export function TranscriptsPage() {
  const [selectedSessionId, setSelectedSessionId] = useState<number | null>(null);

  if (selectedSessionId != null) {
    return (
      <TranscriptDetail
        sessionId={selectedSessionId}
        onBack={() => setSelectedSessionId(null)}
      />
    );
  }

  return <TranscriptList onSelectSession={setSelectedSessionId} />;
}
