import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import * as Tabs from "@radix-ui/react-tabs";
import { CheckCircle2, Bot, Eye, EyeOff } from "lucide-react";
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
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setRole("student")}
                    className={`flex-1 rounded-lg border py-2 text-sm font-medium ${
                      role === "student"
                        ? "border-brand-500 bg-brand-50 text-brand-700"
                        : "border-slate-200 text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    Student
                  </button>
                  <button
                    type="button"
                    onClick={() => setRole("teacher")}
                    className={`flex-1 rounded-lg border py-2 text-sm font-medium ${
                      role === "teacher"
                        ? "border-brand-500 bg-brand-50 text-brand-700"
                        : "border-slate-200 text-slate-600 hover:bg-slate-50"
                    }`}
                  >
                    Teacher
                  </button>
                </div>
                <Input
                  placeholder="Username (3–32 chars, letters, numbers, _)"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  maxLength={32}
                />
                <Input
                  type={showPassword ? "text" : "password"}
                  placeholder={`Password (min ${MIN_PASSWORD_LENGTH} characters)`}
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
