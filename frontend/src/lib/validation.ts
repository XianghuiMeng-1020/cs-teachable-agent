/** Username: 3–32 chars, letters, numbers, underscore only */
export const USERNAME_REGEX = /^[a-zA-Z0-9_]{3,32}$/;
export const MIN_PASSWORD_LENGTH = 6;

export function validateUsername(value: string): string | null {
  const t = value.trim();
  if (!t) return "Username is required";
  if (t.length < 3) return "Username must be at least 3 characters";
  if (t.length > 32) return "Username must be at most 32 characters";
  if (!USERNAME_REGEX.test(t)) return "Username can only contain letters, numbers, and underscores";
  return null;
}

export function validatePassword(value: string): string | null {
  if (!value) return "Password is required";
  if (value.length < MIN_PASSWORD_LENGTH) return `Password must be at least ${MIN_PASSWORD_LENGTH} characters`;
  return null;
}

/** Map API error messages to user-friendly text */
export function getFriendlyAuthError(err: unknown): string {
  let msg = "";
  if (err instanceof Error) msg = err.message;
  else if (typeof err === "string") msg = err;
  if (msg) {
    try {
      const parsed = JSON.parse(msg) as { detail?: string | Array<{ msg?: string }> };
      if (typeof parsed.detail === "string") msg = parsed.detail;
      else if (Array.isArray(parsed.detail) && parsed.detail[0]?.msg) msg = parsed.detail[0].msg;
    } catch {
      // not JSON, use as-is
    }
    const lower = msg.toLowerCase();
    if (lower.includes("username already registered") || lower.includes("already registered")) return "This username is already taken. Try another.";
    if (lower.includes("invalid username or password") || lower.includes("401")) return "Invalid username or password. Please try again.";
    if (lower.includes("password must be at least")) return "Password must be at least 6 characters.";
    if (lower.includes("network") || lower.includes("fetch")) return "Network error. Check your connection and try again.";
    if (lower.includes("timeout")) return "Request timed out. Please try again.";
    if (lower.includes("username") && lower.includes("character")) return msg;
    return msg;
  }
  return "Something went wrong. Please try again.";
}
