import { useState, useMemo } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import * as Tabs from "@radix-ui/react-tabs";
import * as Tooltip from "@radix-ui/react-tooltip";
import { CheckCircle2, Bot, Eye, EyeOff, Info, GraduationCap, User, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useAuthStore } from "@/stores/authStore";
import { ROUTES } from "@/lib/constants";
import { toast } from "sonner";
import {
  validateUsername,
  validatePassword,
  getFriendlyAuthError,
  MIN_PASSWORD_LENGTH,
} from "@/lib/validation";

function PasswordStrengthIndicator({ password }: { password: string }) {
  const strength = useMemo(() => {
    let score = 0;
    if (password.length >= MIN_PASSWORD_LENGTH) score++;
    if (password.length >= 10) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) score++;
    return score;
  }, [password]);

  const levels = [
    { label: "Too weak", color: "bg-rose-500", textColor: "text-rose-600" },
    { label: "Weak", color: "bg-orange-500", textColor: "text-orange-600" },
    { label: "Fair", color: "bg-amber-500", textColor: "text-amber-600" },
    { label: "Good", color: "bg-brand-500", textColor: "text-brand-600" },
    { label: "Strong", color: "bg-emerald-500", textColor: "text-emerald-600" },
    { label: "Very Strong", color: "bg-emerald-600", textColor: "text-emerald-700" },
  ];

  if (password.length === 0) return null;

  const level = levels[Math.min(strength, levels.length - 1)];
  const width = Math.min(100, (strength / 5) * 100);

  return (
    <div className="mt-2 space-y-1">
      <div className="h-1.5 w-full bg-slate-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${level.color} transition-all duration-300`}
          style={{ width: `${width}%` }}
        />
      </div>
      <div className="flex items-center justify-between">
        <span className={`text-xs ${level.textColor}`}>{level.label}</span>
        <span className="text-xs text-slate-400">{password.length} chars</span>
      </div>
      <div className="flex flex-wrap gap-1 mt-1">
        {[
          { met: password.length >= MIN_PASSWORD_LENGTH, text: `${MIN_PASSWORD_LENGTH}+ chars` },
          { met: /[a-z]/.test(password) && /[A-Z]/.test(password), text: "Mixed case" },
          { met: /\d/.test(password), text: "Number" },
          { met: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password), text: "Special char" },
        ].map((req, idx) => (
          <span
            key={idx}
            className={`text-[10px] px-1.5 py-0.5 rounded ${
              req.met ? "bg-emerald-100 text-emerald-700" : "bg-slate-100 text-slate-500"
            }`}
          >
            {req.met ? "✓" : "○"} {req.text}
          </span>
        ))}
      </div>
    </div>
  );
}

const bullets = [
  "Knowledge-state-driven TA behavior",
  "Teach and test in one flow",
  "Research-ready trace data",
];

export function LoginPage() {
  const [activeTab, setActiveTab] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [role, setRole] = useState<"student" | "teacher">("student");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const { login, register } = useAuthStore();
  const navigate = useNavigate();
  const location = useLocation();
  const from = (location.state as { from?: { pathname: string } })?.from?.pathname ?? ROUTES.dashboard;

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    const userError = validateUsername(username);
    if (userError) {
      toast.error(userError);
      return;
    }
    const pwdError = validatePassword(password);
    if (pwdError) {
      toast.error(pwdError);
      return;
    }
    setLoading(true);
    try {
      await login(username.trim(), password);
      toast.success("Signed in");
      navigate(from, { replace: true });
    } catch (err) {
      toast.error(getFriendlyAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    const userError = validateUsername(username);
    if (userError) {
      toast.error(userError);
      return;
    }
    const pwdError = validatePassword(password);
    if (pwdError) {
      toast.error(pwdError);
      return;
    }
    if (password !== confirmPassword) {
      toast.error("Passwords do not match");
      return;
    }
    setLoading(true);
    try {
      await register(username.trim(), password, role);
      toast.success("Account created");
      navigate(from, { replace: true });
    } catch (err) {
      toast.error(getFriendlyAuthError(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen md:grid-cols-2">
      <div className="flex flex-col justify-center bg-brand-950 p-12">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-white/10">
            <Bot className="h-6 w-6 text-white" />
          </div>
          <span className="text-xl font-semibold text-white">CS Teachable Agent</span>
        </div>
        <ul className="mt-10 space-y-4">
          {bullets.map((text) => (
            <li key={text} className="flex items-center gap-3 text-brand-200">
              <CheckCircle2 className="h-5 w-5 shrink-0 text-brand-400" />
              <span>{text}</span>
            </li>
          ))}
        </ul>
        <div className="mt-16 opacity-30">
          <svg viewBox="0 0 200 100" className="h-24 w-full text-white">
            <circle cx="40" cy="50" r="8" fill="currentColor" />
            <circle cx="100" cy="50" r="8" fill="currentColor" />
            <circle cx="160" cy="50" r="8" fill="currentColor" />
            <path d="M0 50 Q50 20 100 50 T200 50" stroke="currentColor" strokeWidth="1" fill="none" />
          </svg>
        </div>
      </div>

      <div className="flex items-center justify-center bg-white p-12">
        <div className="w-full max-w-sm">
          <Tabs.Root value={activeTab} onValueChange={(v) => setActiveTab(v as "login" | "register")}>
            <Tabs.List className="mb-6 flex gap-2 border-b border-slate-200">
              <Tabs.Trigger
                value="login"
                className="border-b-2 border-transparent px-4 py-2 text-sm font-medium text-slate-600 data-[state=active]:border-brand-500 data-[state=active]:text-brand-600"
              >
                Sign in
              </Tabs.Trigger>
              <Tabs.Trigger
                value="register"
                className="border-b-2 border-transparent px-4 py-2 text-sm font-medium text-slate-600 data-[state=active]:border-brand-500 data-[state=active]:text-brand-600"
              >
                Sign up
              </Tabs.Trigger>
            </Tabs.List>

            <Tabs.Content value="login">
              <h2 className="text-xl font-semibold text-slate-900">Welcome back</h2>
              <form onSubmit={handleLogin} className="mt-6 space-y-4">
                <Input
                  placeholder="Username (letters, numbers, underscore)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  maxLength={32}
                />
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder="Password (min 6 characters)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  rightIcon={
                    <button
                      type="button"
                      onClick={() => setShowPassword((s) => !s)}
                      className="text-slate-400 hover:text-slate-600"
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                />
                <Button type="submit" fullWidth loading={loading}>
                  Sign in
                </Button>
              </form>
            </Tabs.Content>

            <Tabs.Content value="register">
              <h2 className="text-xl font-semibold text-slate-900">Create your account</h2>
              <form onSubmit={handleRegister} className="mt-6 space-y-4">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-medium text-slate-700">Select your role</span>
                    <Tooltip.Provider delayDuration={100}>
                      <Tooltip.Root>
                        <Tooltip.Trigger asChild>
                          <button type="button" className="text-slate-400 hover:text-slate-600">
                            <Info className="w-4 h-4" />
                          </button>
                        </Tooltip.Trigger>
                        <Tooltip.Portal>
                          <Tooltip.Content
                            className="z-50 max-w-xs rounded-lg bg-slate-900 px-3 py-2 text-xs text-white shadow-lg"
                            sideOffset={4}
                          >
                            <p className="font-medium mb-1">Student:</p>
                            <p className="text-slate-300 mb-2">Teach the TA concepts and test its understanding</p>
                            <p className="font-medium mb-1">Teacher:</p>
                            <p className="text-slate-300">View student progress and analytics</p>
                            <Tooltip.Arrow className="fill-slate-900" />
                          </Tooltip.Content>
                        </Tooltip.Portal>
                      </Tooltip.Root>
                    </Tooltip.Provider>
                  </div>
                  <div className="grid grid-cols-2 gap-3">
                    <Tooltip.Provider delayDuration={100}>
                      <Tooltip.Root>
                        <Tooltip.Trigger asChild>
                          <button
                            type="button"
                            onClick={() => setRole("student")}
                            className={`flex items-center gap-2 rounded-lg border p-3 text-left transition-colors ${
                              role === "student"
                                ? "border-brand-500 bg-brand-50 text-brand-700"
                                : "border-slate-200 text-slate-600 hover:bg-slate-50"
                            }`}
                          >
                            <User className={`w-5 h-5 ${role === "student" ? "text-brand-600" : "text-slate-400"}`} />
                            <div>
                              <div className="text-sm font-medium">Student</div>
                              <div className="text-xs opacity-75">Teach & Test</div>
                            </div>
                          </button>
                        </Tooltip.Trigger>
                        <Tooltip.Portal>
                          <Tooltip.Content
                            className="z-50 max-w-xs rounded-lg bg-slate-900 px-3 py-2 text-xs text-white shadow-lg"
                            sideOffset={4}
                          >
                            <p>Learn by teaching! You explain concepts to the TA, then run tests to see how well it learned.</p>
                            <Tooltip.Arrow className="fill-slate-900" />
                          </Tooltip.Content>
                        </Tooltip.Portal>
                      </Tooltip.Root>
                    </Tooltip.Provider>

                    <Tooltip.Provider delayDuration={100}>
                      <Tooltip.Root>
                        <Tooltip.Trigger asChild>
                          <button
                            type="button"
                            onClick={() => setRole("teacher")}
                            className={`flex items-center gap-2 rounded-lg border p-3 text-left transition-colors ${
                              role === "teacher"
                                ? "border-brand-500 bg-brand-50 text-brand-700"
                                : "border-slate-200 text-slate-600 hover:bg-slate-50"
                            }`}
                          >
                            <GraduationCap className={`w-5 h-5 ${role === "teacher" ? "text-brand-600" : "text-slate-400"}`} />
                            <div>
                              <div className="text-sm font-medium">Teacher</div>
                              <div className="text-xs opacity-75">Monitor & Analyze</div>
                            </div>
                          </button>
                        </Tooltip.Trigger>
                        <Tooltip.Portal>
                          <Tooltip.Content
                            className="z-50 max-w-xs rounded-lg bg-slate-900 px-3 py-2 text-xs text-white shadow-lg"
                            sideOffset={4}
                          >
                            <p>View student progress, analyze learning patterns, and export teaching transcripts.</p>
                            <Tooltip.Arrow className="fill-slate-900" />
                          </Tooltip.Content>
                        </Tooltip.Portal>
                      </Tooltip.Root>
                    </Tooltip.Provider>
                  </div>
                </div>
                <Input
                  placeholder="Username (3–32 chars, letters, numbers, _)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  maxLength={32}
                />
                <div>
                  <Input
                    type={showPassword ? "text" : "password"}
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    rightIcon={
                      <button
                        type="button"
                        onClick={() => setShowPassword((s) => !s)}
                        className="text-slate-400 hover:text-slate-600"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    }
                  />
                  <PasswordStrengthIndicator password={password} />
                </div>
                <Input
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Confirm password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  autoComplete="new-password"
                  rightIcon={
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword((s) => !s)}
                      className="text-slate-400 hover:text-slate-600"
                      aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                />
                <Button type="submit" fullWidth loading={loading}>
                  Create account
                </Button>
              </form>
            </Tabs.Content>
          </Tabs.Root>

          <p className="mt-6 text-center text-sm text-slate-500">
            {activeTab === "login" ? (
              <>
                Don&apos;t have an account?{" "}
                <button
                  type="button"
                  className="font-medium text-brand-600 hover:underline"
                  onClick={() => setActiveTab("register")}
                >
                  Sign up
                </button>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <button
                  type="button"
                  className="font-medium text-brand-600 hover:underline"
                  onClick={() => setActiveTab("login")}
                >
                  Sign in
                </button>
              </>
            )}
          </p>
        </div>
      </div>
    </div>
  );
}
