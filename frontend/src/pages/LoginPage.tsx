import { useState, useMemo } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import * as Tabs from "@radix-ui/react-tabs";
import { Eye, EyeOff, BookOpen, GraduationCap, User } from "lucide-react";
import { useTranslation } from "react-i18next";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { LanguageSwitcher } from "@/components/ui/LanguageSwitcher";
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
    { label: "Too weak", color: "bg-red-500", textColor: "text-red-600" },
    { label: "Weak", color: "bg-orange-500", textColor: "text-orange-600" },
    { label: "Fair", color: "bg-amber-500", textColor: "text-amber-600" },
    { label: "Good", color: "bg-brand-600", textColor: "text-brand-700" },
    { label: "Strong", color: "bg-emerald-500", textColor: "text-emerald-600" },
    { label: "Very strong", color: "bg-emerald-600", textColor: "text-emerald-700" },
  ];

  if (password.length === 0) return null;

  const level = levels[Math.min(strength, levels.length - 1)];
  const width = Math.min(100, (strength / 5) * 100);

  return (
    <div className="mt-2.5 space-y-1.5">
      <div className="h-1 w-full overflow-hidden rounded-full bg-stone-200 dark:bg-stone-700">
        <div
          className={`h-full ${level.color} transition-all duration-300`}
          style={{ width: `${width}%` }}
        />
      </div>
      <div className="flex items-center justify-between">
        <span className={`text-xs font-medium ${level.textColor}`}>{level.label}</span>
        <span className="text-xs text-stone-400 dark:text-stone-500">{password.length} chars</span>
      </div>
    </div>
  );
}

export function LoginPage() {
  const { t } = useTranslation();
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
    if (userError) { toast.error(userError); return; }
    const pwdError = validatePassword(password);
    if (pwdError) { toast.error(pwdError); return; }
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
    if (userError) { toast.error(userError); return; }
    const pwdError = validatePassword(password);
    if (pwdError) { toast.error(pwdError); return; }
    if (password !== confirmPassword) { toast.error("Passwords do not match"); return; }
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
    <div className="grid min-h-screen lg:grid-cols-2">
      {/* Left panel */}
      <div className="hidden lg:flex flex-col justify-between bg-stone-900 dark:bg-black p-12">
        <div>
          <Link to="/" className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-600">
              <BookOpen className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-white">ARTS-CS</span>
          </Link>
          <LanguageSwitcher variant="landing" />
        </div>

        <div className="max-w-sm">
          <h2 className="font-serif text-3xl font-bold leading-tight text-white">
            {t("landing.lbtTitle")} {t("landing.lbtDesc")}
          </h2>
          <p className="mt-4 text-base leading-relaxed text-stone-400">
            {t("landing.heroDesc")}
          </p>
          <div className="mt-10 space-y-4">
            {[
              "Teach concepts in natural language",
              "Test the agent with real coding problems",
              "Track your knowledge mastery in real time",
            ].map((text) => (
              <div key={text} className="flex items-center gap-3">
                <div className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-brand-900/50">
                  <div className="h-1.5 w-1.5 rounded-full bg-brand-400" />
                </div>
                <span className="text-sm text-stone-300">{text}</span>
              </div>
            ))}
          </div>
        </div>

        <p className="text-xs text-stone-600 dark:text-stone-700">{t("login.brandLine")}</p>
      </div>

      {/* Right panel */}
      <div className="flex items-center justify-center bg-surface dark:bg-surfaceDark p-6 sm:p-12">
        <div className="w-full max-w-[400px]">
          {/* Mobile logo */}
          <Link to="/" className="mb-8 flex items-center gap-2.5 lg:hidden">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-700">
              <BookOpen className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-stone-900 dark:text-stone-100">ARTS-CS</span>
          </Link>

          <Tabs.Root value={activeTab} onValueChange={(v) => setActiveTab(v as "login" | "register")}>
            <Tabs.List className="mb-8 flex rounded-lg bg-stone-100 dark:bg-stone-800 p-1">
              <Tabs.Trigger
                value="login"
                className="flex-1 rounded-md px-4 py-2 text-sm font-medium text-stone-500 dark:text-stone-400 transition-all data-[state=active]:bg-white data-[state=active]:dark:bg-surfaceDark-card data-[state=active]:text-stone-900 data-[state=active]:dark:text-stone-100 data-[state=active]:shadow-sm"
              >
                {t("common.signIn")}
              </Tabs.Trigger>
              <Tabs.Trigger
                value="register"
                className="flex-1 rounded-md px-4 py-2 text-sm font-medium text-stone-500 dark:text-stone-400 transition-all data-[state=active]:bg-white data-[state=active]:dark:bg-surfaceDark-card data-[state=active]:text-stone-900 data-[state=active]:dark:text-stone-100 data-[state=active]:shadow-sm"
              >
                {t("common.createAccount")}
              </Tabs.Trigger>
            </Tabs.List>

            <Tabs.Content value="login">
              <div className="mb-6">
                <h2 className="font-serif text-2xl font-bold text-stone-900 dark:text-stone-100">{t("common.welcomeBack")}</h2>
                <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">{t("login.signInDesc")}</p>
              </div>
              <form onSubmit={handleLogin} className="space-y-4">
                <Input
                  label="Username"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  maxLength={32}
                />
                <Input
                  label="Password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete="current-password"
                  rightIcon={
                    <button
                      type="button"
                      onClick={() => setShowPassword((s) => !s)}
                      className="text-stone-400 hover:text-stone-600"
                      aria-label={showPassword ? "Hide password" : "Show password"}
                    >
                      {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                />
                <Button type="submit" fullWidth size="lg" loading={loading}>
                  {t("common.signIn")}
                </Button>
              </form>
            </Tabs.Content>

            <Tabs.Content value="register">
              <div className="mb-6">
                <h2 className="font-serif text-2xl font-bold text-stone-900 dark:text-stone-100">{t("common.createAccount")}</h2>
                <p className="mt-1 text-sm text-stone-500 dark:text-stone-400">{t("login.registerDesc")}</p>
              </div>
              <form onSubmit={handleRegister} className="space-y-4">
                <div>
                  <label className="mb-1.5 block text-sm font-medium text-stone-700">
                    {t("login.iAmA")}
                  </label>
                  <div className="grid grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => setRole("student")}
                      className={`flex items-center gap-3 rounded-lg border-2 p-3.5 text-left transition-all ${
                        role === "student"
                          ? "border-brand-600 bg-brand-50"
                          : "border-stone-200 bg-white hover:border-stone-300"
                      }`}
                    >
                      <User className={`h-5 w-5 ${role === "student" ? "text-brand-700" : "text-stone-400"}`} />
                      <div>
                        <div className={`text-sm font-semibold ${role === "student" ? "text-brand-900" : "text-stone-700"}`}>
                          {t("login.student")}
                        </div>
                        <div className="text-xs text-stone-500">{t("login.studentDesc")}</div>
                      </div>
                    </button>
                    <button
                      type="button"
                      onClick={() => setRole("teacher")}
                      className={`flex items-center gap-3 rounded-lg border-2 p-3.5 text-left transition-all ${
                        role === "teacher"
                          ? "border-brand-600 bg-brand-50"
                          : "border-stone-200 bg-white hover:border-stone-300"
                      }`}
                    >
                      <GraduationCap className={`h-5 w-5 ${role === "teacher" ? "text-brand-700" : "text-stone-400"}`} />
                      <div>
                        <div className={`text-sm font-semibold ${role === "teacher" ? "text-brand-900" : "text-stone-700"}`}>
                          {t("login.teacher")}
                        </div>
                        <div className="text-xs text-stone-500">{t("login.teacherDesc")}</div>
                      </div>
                    </button>
                  </div>
                </div>
                <Input
                  label="Username"
                  placeholder="Choose a username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="username"
                  maxLength={32}
                />
                <div>
                  <Input
                    label="Password"
                    type={showPassword ? "text" : "password"}
                    placeholder="Create a password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="new-password"
                    rightIcon={
                      <button
                        type="button"
                        onClick={() => setShowPassword((s) => !s)}
                        className="text-stone-400 hover:text-stone-600"
                        aria-label={showPassword ? "Hide password" : "Show password"}
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    }
                  />
                  <PasswordStrengthIndicator password={password} />
                </div>
                <Input
                  label="Confirm Password"
                  type={showConfirmPassword ? "text" : "password"}
                  placeholder="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  autoComplete="new-password"
                  rightIcon={
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword((s) => !s)}
                      className="text-stone-400 hover:text-stone-600"
                      aria-label={showConfirmPassword ? "Hide password" : "Show password"}
                    >
                      {showConfirmPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                />
                <Button type="submit" fullWidth size="lg" loading={loading}>
                  {t("common.createAccount")}
                </Button>
              </form>
            </Tabs.Content>
          </Tabs.Root>

          <p className="mt-6 text-center text-sm text-stone-500">
            {activeTab === "login" ? (
              <>
                Don&apos;t have an account?{" "}
                <button
                  type="button"
                  className="font-semibold text-brand-700 hover:text-brand-800"
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
                  className="font-semibold text-brand-700 hover:text-brand-800"
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
