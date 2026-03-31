export type CandidateVariant = {
  id: string;
  label: string;
  stage: string;
  verdict: "Reject" | "Revise" | "Ship";
  verdictTone: "error" | "warning" | "success";
  aiPassRate: number;
  studentPassRate: number;
  coverageRate: number;
  qTestsuite: number;
  qContext: number;
  oneLiner: string;
  blocks: string[];
  distractors: string[];
  notes: string[];
  pipeline: { label: string; value: string; status: "pass" | "warn" | "fail" }[];
  modelBoard: { label: string; role: string; score: number; note: string }[];
};

export const themes = ["Science Fiction", "Mythology", "Cooking", "Board Games"];

export const conceptPool = [
  "Strings",
  "Loops",
  "Dictionaries",
  "Selection Statements",
  "File Handling"
];

export const variants: CandidateVariant[] = [
  {
    id: "code-baseline",
    label: "Original Code Task",
    stage: "Baseline",
    verdict: "Reject",
    verdictTone: "error",
    aiPassRate: 100,
    studentPassRate: 100,
    coverageRate: 100,
    qTestsuite: 100,
    qContext: 100,
    oneLiner: "The source programming task is instructionally sound but trivial for assistants to solve end-to-end.",
    blocks: [
      "def decode_message(galactic_message, codebook):",
      "words = galactic_message.split()",
      "decoded_words = []",
      "for word in words:\n    if word in codebook:\n        decoded_words.append(codebook[word])\n    else:\n        decoded_words.append('UNKNOWN')",
      "return ' '.join(decoded_words)"
    ],
    distractors: [],
    notes: [
      "No closed-form constraints. The assistant writes full code with no friction.",
      "Quality metrics are excellent, but assistant resistance is effectively zero."
    ],
    pipeline: [
      { label: "Generate", value: "1 / 1 kept", status: "pass" },
      { label: "Tutor validation", value: "100% pass", status: "pass" },
      { label: "Student solvability", value: "20 / 20 pass", status: "pass" },
      { label: "Assistant resistance", value: "Too low", status: "fail" }
    ],
    modelBoard: [
      { label: "Strong assistant", role: "Full-code baseline", score: 100, note: "Completes task directly." },
      { label: "Budget assistant", role: "Full-code baseline", score: 100, note: "Still trivial." },
      { label: "Student proxy", role: "Human-facing proxy", score: 100, note: "Clear and learnable." }
    ]
  },
  {
    id: "parsons-lite",
    label: "Parsons + Light Distractors",
    stage: "Typed assessment",
    verdict: "Revise",
    verdictTone: "warning",
    aiPassRate: 75,
    studentPassRate: 92,
    coverageRate: 92,
    qTestsuite: 100,
    qContext: 100,
    oneLiner: "Distractors create some friction, but the canonical flow is still transparent to small models.",
    blocks: [
      "def decode_message(galactic_message, codebook):",
      "words = galactic_message.split()\ndecoded_words = [''] * 0",
      "for word in words:\n    if word in codebook:\n        decoded_words.append(codebook[word])\n    else:\n        decoded_words.append('UNKNOWN')",
      "return ' '.join(decoded_words)"
    ],
    distractors: [
      "decoded_words = ''",
      "for word in words:\n    if word in codebook:\n        decoded_words.extend(codebook[word])\n    else:\n        decoded_words.append('UNKNOWN')"
    ],
    notes: [
      "Most failures come from selecting the semantic distractor with `extend()`.",
      "The format is now useful for probing whether the assistant can detect local semantic traps."
    ],
    pipeline: [
      { label: "Compile", value: "Parsons item ready", status: "pass" },
      { label: "Validator", value: "Passed with caveat", status: "warn" },
      { label: "Student proxy", value: "15 / 20 pass", status: "pass" },
      { label: "Assistant resistance", value: "75% assistant pass", status: "warn" }
    ],
    modelBoard: [
      { label: "Strong assistant", role: "Block selection", score: 88, note: "Still spots the true structure quickly." },
      { label: "Budget assistant", role: "Block selection", score: 75, note: "Confuses `append` and `extend` in some rollouts." },
      { label: "Student proxy", role: "Human-facing proxy", score: 92, note: "Learners keep enough signal to solve." }
    ]
  },
  {
    id: "parsons-semantic",
    label: "Parsons + Semantic Pressure",
    stage: "Recommended candidate",
    verdict: "Ship",
    verdictTone: "success",
    aiPassRate: 58,
    studentPassRate: 84,
    coverageRate: 76,
    qTestsuite: 100,
    qContext: 100,
    oneLiner: "The target zone: assistant pass rate drops near the desired band while student solvability stays high enough.",
    blocks: [
      "def decode_message(galactic_message, codebook):",
      "tokens = galactic_message.split()\ndecoded = []",
      "for token in tokens:\n    if token in codebook:\n        decoded.append(codebook[token])\n    else:\n        decoded.append('UNKNOWN')",
      "return ' '.join(decoded)"
    ],
    distractors: [
      "for token in tokens:\n    if token in codebook:\n        decoded.extend(codebook[token])\n    else:\n        decoded.append('UNKNOWN')",
      "return ''.join(decoded)",
      "if token not in codebook:\n    decoded.append(codebook[token])"
    ],
    notes: [
      "Distractors attack representation, control flow, and output formatting at the same time.",
      "This variant is appropriate when the design goal is to discourage direct assistant outsourcing."
    ],
    pipeline: [
      { label: "Compile", value: "3 semantic distractors", status: "pass" },
      { label: "Tutor validation", value: "Maintains concept alignment", status: "pass" },
      { label: "Student proxy", value: "84% pass", status: "pass" },
      { label: "Assistant resistance", value: "58% assistant pass", status: "pass" }
    ],
    modelBoard: [
      { label: "Strong assistant", role: "Block selection", score: 66, note: "Still resolves most structure but stumbles on join semantics." },
      { label: "Budget assistant", role: "Block selection", score: 58, note: "Falls into semantic distractors often enough to be useful." },
      { label: "Student proxy", role: "Human-facing proxy", score: 84, note: "Keeps the learning objective intact." }
    ]
  }
];
