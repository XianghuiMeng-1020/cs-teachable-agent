import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import {
  BookOpen,
  Brain,
  Layers,
  ArrowRight,
  GraduationCap,
  BarChart3,
  MessageSquareText,
  Code2,
} from "lucide-react";
import { ROUTES } from "@/lib/constants";

const fadeUp = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.6, ease: [0.16, 1, 0.3, 1] } },
};

const stagger = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
};

const features = [
  {
    icon: MessageSquareText,
    title: "Teach to Learn",
    description:
      "Explain programming concepts to a virtual agent that starts with zero knowledge. Teaching others is the most effective way to deepen your own understanding.",
    color: "text-brand-700",
    bg: "bg-brand-50",
  },
  {
    icon: Brain,
    title: "Adaptive Knowledge Model",
    description:
      "Bayesian knowledge tracing monitors mastery of each concept. The agent's responses are constrained by what you've successfully taught it.",
    color: "text-amber-700",
    bg: "bg-amber-50",
  },
  {
    icon: Code2,
    title: "Live Code Testing",
    description:
      "Challenge the agent with programming problems to verify its understanding. Watch it generate code based only on the concepts you've taught.",
    color: "text-emerald-700",
    bg: "bg-emerald-50",
  },
  {
    icon: Layers,
    title: "Structured Practice",
    description:
      "Parsons puzzles, fill-in-the-blank exercises, and execution traces help reinforce your understanding through interactive assessment.",
    color: "text-violet-700",
    bg: "bg-violet-50",
  },
  {
    icon: BarChart3,
    title: "Learning Analytics",
    description:
      "Track your mastery journey with detailed visualizations. Identify misconceptions, see concept connections, and monitor progress over time.",
    color: "text-rose-700",
    bg: "bg-rose-50",
  },
  {
    icon: GraduationCap,
    title: "Instructor Dashboard",
    description:
      "Teachers access class-wide analytics, review teaching transcripts, and identify students who need additional support.",
    color: "text-sky-700",
    bg: "bg-sky-50",
  },
];

const stats = [
  { value: "20+", label: "Knowledge Units" },
  { value: "50+", label: "Practice Problems" },
  { value: "3", label: "Assessment Types" },
  { value: "Real-time", label: "Mastery Tracking" },
];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-surface font-sans">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-stone-200/60 bg-white/80 backdrop-blur-md">
        <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-6">
          <div className="flex items-center gap-2.5">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-brand-700">
              <BookOpen className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-stone-900">ARTS-CS</span>
          </div>
          <div className="flex items-center gap-3">
            <Link
              to={ROUTES.login}
              className="rounded-lg px-4 py-2 text-sm font-medium text-stone-600 transition-colors hover:text-stone-900"
            >
              Sign in
            </Link>
            <Link
              to={ROUTES.login}
              className="rounded-lg bg-brand-700 px-4 py-2 text-sm font-semibold text-white shadow-sm transition-colors hover:bg-brand-800"
            >
              Get Started
            </Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="relative overflow-hidden pt-16">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-20%,rgba(20,184,166,0.08),transparent)]" />
        <motion.div
          variants={stagger}
          initial="hidden"
          animate="show"
          className="relative mx-auto flex max-w-4xl flex-col items-center px-6 pb-20 pt-24 text-center sm:pt-32"
        >
          <motion.div
            variants={fadeUp}
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-brand-200 bg-brand-50 px-4 py-1.5"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-brand-500" />
            <span className="text-sm font-medium text-brand-800">
              AI Resistant Teaching System for CS
            </span>
          </motion.div>

          <motion.h1
            variants={fadeUp}
            className="font-serif text-display-lg text-stone-900 sm:text-[4rem]"
          >
            Learn Programming by{" "}
            <span className="text-brand-700">Teaching</span>
          </motion.h1>

          <motion.p
            variants={fadeUp}
            className="mt-6 max-w-2xl text-lg leading-relaxed text-stone-500"
          >
            <strong>ARTS-CS</strong>: A unified, knowledge-state-constrained teaching
            system where students teach AI agents, agents learn through explicit knowledge
            states, and mastery emerges through explanation — resistant to AI shortcuts.
          </motion.p>

          <motion.div variants={fadeUp} className="mt-10 flex items-center gap-4">
            <Link
              to={ROUTES.login}
              className="group inline-flex items-center gap-2 rounded-lg bg-brand-700 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:bg-brand-800 hover:shadow-md"
            >
              Start Teaching
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
            <a
              href="#features"
              className="rounded-lg border border-stone-300 bg-white px-6 py-3 text-sm font-medium text-stone-700 shadow-sm transition-colors hover:bg-stone-50"
            >
              How It Works
            </a>
          </motion.div>
        </motion.div>
      </section>

      {/* Stats Bar */}
      <section className="border-y border-stone-200/60 bg-white">
        <div className="mx-auto grid max-w-6xl grid-cols-2 gap-8 px-6 py-10 md:grid-cols-4">
          {stats.map((s) => (
            <div key={s.label} className="text-center">
              <p className="font-serif text-2xl font-bold text-stone-900">{s.value}</p>
              <p className="mt-1 text-sm text-stone-500">{s.label}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Features */}
      <section id="features" className="py-24">
        <div className="mx-auto max-w-6xl px-6">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="mb-16 text-center"
          >
            <p className="text-sm font-semibold uppercase tracking-widest text-brand-700">
              Platform Features
            </p>
            <h2 className="mt-3 font-serif text-display-sm text-stone-900">
              Everything you need for effective learning
            </h2>
          </motion.div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.08 }}
                className="group rounded-xl border border-stone-200/80 bg-white p-6 shadow-card transition-all duration-200 hover:shadow-card-hover"
              >
                <div
                  className={`mb-4 inline-flex h-11 w-11 items-center justify-center rounded-lg ${f.bg}`}
                >
                  <f.icon className={`h-5 w-5 ${f.color}`} />
                </div>
                <h3 className="text-base font-semibold text-stone-900">{f.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-stone-500">{f.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="border-t border-stone-200/60 bg-stone-900">
        <div className="mx-auto max-w-4xl px-6 py-20 text-center">
          <h2 className="font-serif text-display-sm text-white">
            Ready to learn by teaching?
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-stone-400">
            Create your free account and start teaching your AI agent Python,
            SQL, or AI Literacy concepts. Resistant to shortcuts, designed for mastery.
          </p>
          <Link
            to={ROUTES.login}
            className="mt-8 inline-flex items-center gap-2 rounded-lg bg-brand-500 px-6 py-3 text-sm font-semibold text-white shadow-sm transition-all hover:bg-brand-400"
          >
            Get Started Free
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-stone-200/60 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-md bg-brand-700">
              <BookOpen className="h-4 w-4 text-white" />
            </div>
            <span className="text-sm font-semibold text-stone-700">ARTS-CS</span>
          </div>
          <p className="text-sm text-stone-400">
            AI Resistant Teaching System for Computer Science
          </p>
        </div>
      </footer>
    </div>
  );
}
