/**
 * Invisible Unicode watermarking.
 *
 * Encodes a numeric user-id into a sequence of zero-width characters and
 * injects them at predictable positions inside displayed code text.
 *
 * When a student copies code to an AI tool the invisible characters corrupt
 * the prompt, making AI output unreliable. If the text is OCR'd the
 * watermarks don't appear, but any copy-paste will include them.
 */

const ZW_CHARS = [
  "\u200B", // ZERO WIDTH SPACE
  "\u200C", // ZERO WIDTH NON-JOINER
  "\u200D", // ZERO WIDTH JOINER
  "\uFEFF", // ZERO WIDTH NO-BREAK SPACE
] as const;

/**
 * Encode a numeric id into a base-4 zero-width string.
 * The result is invisible to the human eye.
 */
export function encodeWatermark(userId: number): string {
  if (userId <= 0) return "";
  let n = userId;
  const digits: string[] = [];
  while (n > 0) {
    digits.push(ZW_CHARS[n % 4]);
    n = Math.floor(n / 4);
  }
  return digits.reverse().join("");
}

/**
 * Decode a zero-width watermark string back to the original user-id.
 * Returns 0 if the string contains no valid watermark.
 */
export function decodeWatermark(text: string): number {
  const zwSet = new Set<string>(ZW_CHARS);
  const chars = [...text].filter((c) => zwSet.has(c));
  if (chars.length === 0) return 0;
  let n = 0;
  for (const c of chars) {
    n = n * 4 + ZW_CHARS.indexOf(c as (typeof ZW_CHARS)[number]);
  }
  return n;
}

/**
 * Inject invisible watermarks into a code string.
 *
 * Places the encoded userId watermark after every `interval`-th newline
 * (and once at the very start). The text looks identical to the original
 * for any human reader.
 */
export function watermarkCode(
  code: string,
  userId: number,
  interval = 3
): string {
  if (userId <= 0) return code;
  const mark = encodeWatermark(userId);
  if (!mark) return code;

  const lines = code.split("\n");
  const result: string[] = [];
  for (let i = 0; i < lines.length; i++) {
    if (i % interval === 0) {
      result.push(mark + lines[i]);
    } else {
      result.push(lines[i]);
    }
  }
  return result.join("\n");
}

/**
 * Strip all zero-width watermark characters from text.
 * Useful for grading / comparison where watermarks should not interfere.
 */
export function stripWatermarks(text: string): string {
  const re = new RegExp(`[${ZW_CHARS.join("")}]`, "g");
  return text.replace(re, "");
}
