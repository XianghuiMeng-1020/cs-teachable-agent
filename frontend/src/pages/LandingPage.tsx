import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { BookOpen, Brain, Layers, ChevronDown } from "lucide-react";
import { Button } from "@/components/ui/Button";
import { ROUTES } from "@/lib/constants";

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.1 },
  },
};

const item = {
  hidden: { opacity: 0, y: 12 },
  show: { opacity: 1, y: 0 },
};

const features = [
  {
    icon: BookOpen,
    title: "Learning by Teaching",
    description: "Students teach the TA; knowledge state drives behavior.",
    gradient: "from-brand-500 to-brand-700",
  },
  {
    icon: Brain,
    title: "Misconception Lifecycle",
    description: "Model activation, correction, unlearning, and relearning.",
    gradient: "from-accent-500 to-accent-700",
  },
  {
    icon: Layers,
    title: "Cross-Domain Framework",
    description: "Shared core with domain adapters for Python, DB, AI Literacy.",
    gradient: "from-emerald-500 to-emerald-700",
  },
];

const stats = [
  { value: 20, suffix: "+", label: "KUs" },
  { value: 50, suffix: "+", label: "Problems" },
  { value: 6, suffix: "", label: "Misconception Types" },
  { value: 3, suffix: "", label: "Domains" },
];

export function LandingPage() {
  return (
    <div className="min-h-screen bg-slate-50">
      <section className="relative min-h-screen bg-gradient-to-br from-brand-950 via-brand-900 to-brand-800 flex flex-col items-center justify-center px-6">
        <motion.div
          variants={container}
          initial="hidden"
          animate="show"
          className="flex flex-col items-center text-center"
        >
          <motion.span
            variants={item}
            className="mb-6 rounded-full border border-white/20 bg-white/10 px-4 py-1.5 text-sm font-medium text-white/90"
          >
            HKU CS Teachable Agent
          </motion.span>
          <motion.h1
            variants={item}
            className="text-5xl font-bold tracking-tight text-white md:text-7xl"
          >
            Learn by Teaching
          </motion.h1>
          <motion.p
            variants={item}
            className="mt-4 max-w-2xl text-xl text-brand-200"
          >
            A knowledge-state-constrained teachable agent for CS education.
          </motion.p>
          <motion.div variants={item} className="mt-8 flex gap-4">
            <Link to={ROUTES.login}>
              <Button
                variant="primary"
                size="lg"
                className="bg-white text-brand-600 hover:bg-slate-100"
              >
                Get Started
              </Button>
            </Link>
            <a href="#features">
              <Button variant="ghost" size="lg" className="border border-white/40 text-white hover:bg-white/10">
                Learn More
              </Button>
            </a>
          </motion.div>
          <motion.div
            variants={item}
            className="mt-16 animate-bounce text-white/70"
            aria-hidden
          >
            <ChevronDown className="h-8 w-8" />
          </motion.div>
        </motion.div>
      </section>

      <section id="features" className="py-24 bg-surface">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-8 md:grid-cols-3">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4 }}
                className="glass-card rounded-xl p-6"
              >
                <div
                  className={`mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br ${f.gradient} text-white`}
                >
                  <f.icon className="h-6 w-6" />
                </div>
                <h3 className="text-lg font-semibold text-slate-900">{f.title}</h3>
                <p className="mt-2 text-sm text-slate-600">{f.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-16 bg-brand-950">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
            {stats.map((s) => (
              <div key={s.label} className="text-center">
                <p className="text-3xl font-bold text-white">
                  {s.value}
                  {s.suffix}
                </p>
                <p className="mt-1 text-sm text-brand-300">{s.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <footer className="border-t border-brand-800 py-8 text-center text-sm text-brand-300">
        Built for HKU CS Education Research
      </footer>
    </div>
  );
}
