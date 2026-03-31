import { Link } from "react-router-dom";
import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";
import {
  BookOpen,
  Brain,
  Layers,
  ArrowRight,
  GraduationCap,
  BarChart3,
  MessageSquareText,
  Code2,
  Sparkles,
  Zap,
  Shield,
  Users,
  Play,
  Target,
  Lightbulb,
  LineChart,
  Clock,
  Award,
  Cpu,
  Database,
  Bot,
} from "lucide-react";
import { ROUTES } from "@/lib/constants";

const fadeUp = {
  hidden: { opacity: 0, y: 30 },
  show: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
};

const fadeIn = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { duration: 0.6 } },
};

const stagger = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.1 } },
};

const scaleUp = {
  hidden: { opacity: 0, scale: 0.95 },
  show: { opacity: 1, scale: 1, transition: { duration: 0.5 } },
};

// All features organized by category
const featureCategories = [
  {
    title: "Learning by Teaching",
    description: "The most effective way to learn is to teach",
    features: [
      {
        icon: MessageSquareText,
        title: "Interactive Teaching",
        description: "Explain concepts to a virtual agent that starts with zero knowledge. Teaching deepens your own understanding.",
        color: "text-emerald-600",
        bg: "bg-emerald-50",
        border: "border-emerald-200",
      },
      {
        icon: Brain,
        title: "Adaptive Knowledge Model",
        description: "Bayesian knowledge tracing monitors mastery. Agent responses are constrained by what you've taught.",
        color: "text-violet-600",
        bg: "bg-violet-50",
        border: "border-violet-200",
      },
      {
        icon: Code2,
        title: "Live Code Testing",
        description: "Challenge the agent with programming problems. Watch it generate code based only on your teaching.",
        color: "text-blue-600",
        bg: "bg-blue-50",
        border: "border-blue-200",
      },
    ],
  },
  {
    title: "Misconception Engine",
    description: "Complete lifecycle from activation to relearning",
    features: [
      {
        icon: Target,
        title: "Misconception Detection",
        description: "Automatically detects and tracks student misconceptions through teaching interactions and test failures.",
        color: "text-rose-600",
        bg: "bg-rose-50",
        border: "border-rose-200",
      },
      {
        icon: Zap,
        title: "Activation → Behavior",
        description: "Misconceptions activate based on teaching input, then manifest in TA's code generation and problem-solving.",
        color: "text-amber-600",
        bg: "bg-amber-50",
        border: "border-amber-200",
      },
      {
        icon: Lightbulb,
        title: "Correction → Relearning",
        description: "Targeted teaching corrects misconceptions. Forgetting and relearning complete the full lifecycle.",
        color: "text-cyan-600",
        bg: "bg-cyan-50",
        border: "border-cyan-200",
      },
    ],
  },
  {
    title: "Assessment & Practice",
    description: "Multiple assessment types for comprehensive evaluation",
    features: [
      {
        icon: Layers,
        title: "Parsons Puzzles",
        description: "Drag-and-drop code blocks to build correct program structure. Tests understanding of syntax order.",
        color: "text-indigo-600",
        bg: "bg-indigo-50",
        border: "border-indigo-200",
      },
      {
        icon: BarChart3,
        title: "Execution Traces",
        description: "Predict output or identify bugs by tracing code execution line by line.",
        color: "text-teal-600",
        bg: "bg-teal-50",
        border: "border-teal-200",
      },
      {
        icon: Database,
        title: "Fill-in-the-Blank",
        description: "Complete partially written code to test specific concept understanding.",
        color: "text-fuchsia-600",
        bg: "bg-fuchsia-50",
        border: "border-fuchsia-200",
      },
    ],
  },
];

const instructorFeatures = [
  {
    icon: Users,
    title: "Student Analytics",
    description: "Track class-wide progress, identify struggling students, view detailed mastery breakdowns.",
  },
  {
    icon: LineChart,
    title: "Learning Trajectories",
    description: "Visualize each student's learning journey with timeline views and concept mastery progression.",
  },
  {
    icon: Shield,
    title: "AI-Resistant Proctoring",
    description: "Detect suspicious patterns that may indicate AI-assisted cheating. Maintain assessment integrity.",
  },
  {
    icon: BookOpen,
    title: "Teaching Transcripts",
    description: "Review complete teaching dialogues between students and their TAs for assessment insights.",
  },
];

const stats = [
  { value: "3", label: "Domains", suffix: "", icon: Cpu },
  { value: "35+", label: "Knowledge Units", suffix: "", icon: Layers },
  { value: "100+", label: "Problems", suffix: "+", icon: Target },
  { value: "5", label: "Assessment Types", suffix: "", icon: BarChart3 },
];

const domains = [
  { name: "Python", icon: Code2, color: "from-yellow-400 to-blue-500", description: "Variables, I/O, loops, conditions, functions, data structures" },
  { name: "Database (SQL)", icon: Database, color: "from-blue-400 to-indigo-500", description: "Queries, joins, aggregation, schema design" },
  { name: "AI Literacy", icon: Bot, color: "from-purple-400 to-pink-500", description: "Prompt engineering, AI capabilities, ethical considerations" },
];

// Animated gradient background component
function AnimatedBackground() {
  return (
    <div className="absolute inset-0 overflow-hidden">
      <div className="absolute -top-1/2 -left-1/2 w-full h-full bg-gradient-to-br from-brand-100/40 via-transparent to-violet-100/40 animate-pulse" style={{ animationDuration: '8s' }} />
      <div className="absolute top-0 right-0 w-[600px] h-[600px] bg-gradient-to-bl from-emerald-100/30 to-transparent rounded-full blur-3xl" />
      <div className="absolute bottom-0 left-0 w-[500px] h-[500px] bg-gradient-to-tr from-violet-100/30 to-transparent rounded-full blur-3xl" />
    </div>
  );
}

// Floating card component for visual demo
function FloatingCard({ children, className, delay = 0 }: { children: React.ReactNode; className?: string; delay?: number }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6 }}
      className={`absolute bg-white rounded-xl shadow-2xl border border-stone-100 ${className}`}
    >
      {children}
    </motion.div>
  );
}

export function LandingPage() {
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });
  const heroY = useTransform(scrollYProgress, [0, 1], [0, 150]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.5], [1, 0]);

  return (
    <div className="min-h-screen bg-white font-sans overflow-x-hidden">
      {/* Navigation */}
      <motion.nav
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6 }}
        className="fixed top-0 left-0 right-0 z-50 border-b border-stone-200/60 bg-white/90 backdrop-blur-xl"
      >
        <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-brand-600 to-brand-700 shadow-lg group-hover:shadow-xl transition-shadow">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-lg font-bold text-stone-900 leading-tight">ARTS-CS</span>
              <span className="text-[10px] text-stone-500 font-medium">AI Resistant Teaching</span>
            </div>
          </Link>
          <div className="flex items-center gap-4">
            <Link
              to={ROUTES.login}
              className="hidden sm:block rounded-lg px-4 py-2 text-sm font-medium text-stone-600 transition-colors hover:text-stone-900"
            >
              Sign in
            </Link>
            <Link
              to={ROUTES.login}
              className="group flex items-center gap-2 rounded-lg bg-gradient-to-r from-brand-600 to-brand-700 px-5 py-2.5 text-sm font-semibold text-white shadow-lg shadow-brand-500/25 transition-all hover:shadow-xl hover:shadow-brand-500/30 hover:-translate-y-0.5"
            >
              Get Started
              <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </Link>
          </div>
        </div>
      </motion.nav>

      {/* Hero Section */}
      <section ref={heroRef} className="relative min-h-screen pt-16 overflow-hidden">
        <AnimatedBackground />
        
        <motion.div style={{ y: heroY, opacity: heroOpacity }} className="relative">
          <div className="mx-auto max-w-7xl px-6 pt-20 pb-32">
            <div className="grid lg:grid-cols-2 gap-12 items-center">
              {/* Left: Text Content */}
              <motion.div
                variants={stagger}
                initial="hidden"
                animate="show"
                className="text-center lg:text-left"
              >
                <motion.div
                  variants={fadeUp}
                  className="mb-6 inline-flex items-center gap-2 rounded-full border border-brand-200 bg-gradient-to-r from-brand-50 to-emerald-50 px-4 py-1.5"
                >
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500" />
                  </span>
                  <span className="text-sm font-semibold text-brand-800">
                    Now with Misconception Lifecycle Tracking
                  </span>
                </motion.div>

                <motion.h1
                  variants={fadeUp}
                  className="text-5xl sm:text-6xl lg:text-7xl font-bold text-stone-900 tracking-tight"
                >
                  Master CS by{" "}
                  <span className="bg-gradient-to-r from-brand-600 to-emerald-600 bg-clip-text text-transparent">
                    Teaching AI
                  </span>
                </motion.h1>

                <motion.p
                  variants={fadeUp}
                  className="mt-6 text-xl text-stone-600 leading-relaxed max-w-xl mx-auto lg:mx-0"
                >
                  ARTS-CS: An <strong>AI-Resistant Teaching System</strong> where you teach virtual agents 
                  Python, SQL, and AI concepts. Agents learn through explicit knowledge states — 
                  resistant to shortcuts, designed for deep mastery.
                </motion.p>

                <motion.div variants={fadeUp} className="mt-10 flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
                  <Link
                    to={ROUTES.login}
                    className="group w-full sm:w-auto flex items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-brand-600 to-brand-700 px-8 py-4 text-base font-semibold text-white shadow-xl shadow-brand-500/25 transition-all hover:shadow-2xl hover:shadow-brand-500/30 hover:-translate-y-0.5"
                  >
                    <Play className="h-5 w-5" />
                    Start Teaching Now
                  </Link>
                  <div className="flex items-center gap-3 text-sm text-stone-500">
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-emerald-500" />
                      Free to use
                    </span>
                    <span className="flex items-center gap-1">
                      <span className="w-2 h-2 rounded-full bg-blue-500" />
                      Demo: demo_student / demo123
                    </span>
                  </div>
                </motion.div>
              </motion.div>

              {/* Right: Visual Demo */}
              <div className="relative h-[500px] hidden lg:block">
                {/* Main chat interface mockup */}
                <FloatingCard className="top-0 right-0 w-80 p-4" delay={0.2}>
                  <div className="flex items-center gap-2 mb-3 pb-3 border-b border-stone-100">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand-500 to-brand-600 flex items-center justify-center">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div>
                      <div className="text-sm font-semibold text-stone-900">Python TA</div>
                      <div className="text-xs text-stone-500">Learning: Variables</div>
                    </div>
                    <div className="ml-auto flex gap-1">
                      <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    </div>
                  </div>
                  <div className="space-y-3">
                    <div className="bg-stone-50 rounded-lg p-3 text-sm text-stone-600">
                      "A variable stores data. Use = to assign, like x = 5."
                    </div>
                    <div className="bg-brand-50 rounded-lg p-3 text-sm text-brand-800 border border-brand-100">
                      Can you show me an example with a different value?
                    </div>
                    <div className="bg-stone-50 rounded-lg p-3 text-sm text-stone-600">
                      "Sure! name = 'Alice' stores text in the variable."
                    </div>
                  </div>
                </FloatingCard>

                {/* Knowledge state card */}
                <FloatingCard className="bottom-20 left-0 w-64 p-4" delay={0.4}>
                  <div className="flex items-center gap-2 mb-3">
                    <Brain className="w-5 h-5 text-violet-600" />
                    <span className="text-sm font-semibold text-stone-900">Knowledge State</span>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-stone-600">Variables</span>
                      <div className="flex gap-1">
                        {[1,2,3,4].map(i => (
                          <div key={i} className="w-4 h-2 rounded-sm bg-emerald-500" />
                        ))}
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-stone-600">Loops</span>
                      <div className="flex gap-1">
                        {[1,2].map(i => (
                          <div key={i} className="w-4 h-2 rounded-sm bg-amber-500" />
                        ))}
                        {[1,2].map(i => (
                          <div key={i} className="w-4 h-2 rounded-sm bg-stone-200" />
                        ))}
                      </div>
                    </div>
                    <div className="flex justify-between items-center text-sm">
                      <span className="text-stone-600">Functions</span>
                      <div className="flex gap-1">
                        {[1,2,3,4].map(i => (
                          <div key={i} className="w-4 h-2 rounded-sm bg-stone-200" />
                        ))}
                      </div>
                    </div>
                  </div>
                </FloatingCard>

                {/* Stats card */}
                <FloatingCard className="top-40 left-10 w-48 p-3" delay={0.6}>
                  <div className="text-xs text-stone-500 mb-1">Mastery Progress</div>
                  <div className="text-2xl font-bold text-stone-900">68%</div>
                  <div className="w-full bg-stone-100 rounded-full h-2 mt-2">
                    <div className="bg-gradient-to-r from-brand-500 to-emerald-500 h-2 rounded-full" style={{ width: '68%' }} />
                  </div>
                </FloatingCard>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* Stats Bar - Modern Design */}
      <section className="relative -mt-20 z-10 mx-auto max-w-5xl px-6">
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="rounded-2xl bg-white shadow-2xl shadow-stone-200/50 border border-stone-100 overflow-hidden"
        >
          <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-stone-100">
            {stats.map((s, i) => (
              <motion.div
                key={s.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.1 }}
                className="p-6 text-center group hover:bg-stone-50 transition-colors"
              >
                <div className="flex justify-center mb-2">
                  <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-100 to-brand-50 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <s.icon className="w-5 h-5 text-brand-600" />
                  </div>
                </div>
                <p className="text-3xl font-bold text-stone-900">{s.value}{s.suffix}</p>
                <p className="text-sm text-stone-500 font-medium">{s.label}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </section>

      {/* Domains Section */}
      <section className="py-24 bg-gradient-to-b from-white to-stone-50/50">
        <div className="mx-auto max-w-7xl px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <span className="inline-block px-4 py-1.5 rounded-full bg-brand-100 text-brand-700 text-sm font-semibold mb-4">
              Multi-Domain Support
            </span>
            <h2 className="text-4xl font-bold text-stone-900 mb-4">Three Learning Domains</h2>
            <p className="text-lg text-stone-600 max-w-2xl mx-auto">
              Teach agents across different computer science disciplines with domain-specific knowledge models
            </p>
          </motion.div>

          <div className="grid md:grid-cols-3 gap-6">
            {domains.map((domain, i) => (
              <motion.div
                key={domain.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: i * 0.15 }}
                className="group relative rounded-2xl bg-white p-8 shadow-lg shadow-stone-200/50 border border-stone-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
              >
                <div className={`absolute inset-0 rounded-2xl bg-gradient-to-br ${domain.color} opacity-0 group-hover:opacity-5 transition-opacity`} />
                <div className={`w-14 h-14 rounded-xl bg-gradient-to-br ${domain.color} flex items-center justify-center mb-6 shadow-lg`}>
                  <domain.icon className="w-7 h-7 text-white" />
                </div>
                <h3 className="text-xl font-bold text-stone-900 mb-2">{domain.name}</h3>
                <p className="text-stone-600 leading-relaxed">{domain.description}</p>
                <div className="mt-6 flex items-center gap-2 text-sm font-semibold text-brand-600">
                  <span>Explore domain</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      {featureCategories.map((category, categoryIndex) => (
        <section key={category.title} className={`py-24 ${categoryIndex % 2 === 0 ? 'bg-white' : 'bg-stone-50/50'}`}>
          <div className="mx-auto max-w-7xl px-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              className="text-center mb-16"
            >
              <span className="inline-block px-4 py-1.5 rounded-full bg-violet-100 text-violet-700 text-sm font-semibold mb-4">
                {category.title}
              </span>
              <p className="text-lg text-stone-600 max-w-2xl mx-auto">{category.description}</p>
            </motion.div>

            <div className="grid md:grid-cols-3 gap-6">
              {category.features.map((f, i) => (
                <motion.div
                  key={f.title}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ delay: i * 0.1 }}
                  className={`group rounded-2xl border ${f.border} bg-white p-8 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300`}
                >
                  <div className={`mb-6 inline-flex h-14 w-14 items-center justify-center rounded-xl ${f.bg} shadow-sm group-hover:scale-110 transition-transform`}>
                    <f.icon className={`h-7 w-7 ${f.color}`} />
                  </div>
                  <h3 className="text-xl font-bold text-stone-900 mb-3">{f.title}</h3>
                  <p className="text-stone-600 leading-relaxed">{f.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>
      ))}

      {/* Instructor Dashboard Preview */}
      <section className="py-24 bg-gradient-to-br from-stone-900 via-stone-800 to-stone-900 text-white overflow-hidden relative">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-brand-900/20 via-transparent to-transparent" />
        
        <div className="mx-auto max-w-7xl px-6 relative">
          <div className="grid lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <span className="inline-block px-4 py-1.5 rounded-full bg-brand-500/20 text-brand-300 text-sm font-semibold mb-6">
                For Educators
              </span>
              <h2 className="text-4xl lg:text-5xl font-bold mb-6">
                Powerful Instructor Dashboard
              </h2>
              <p className="text-xl text-stone-300 mb-8 leading-relaxed">
                Track student progress, identify misconceptions, review teaching transcripts, 
                and ensure assessment integrity with AI-resistant proctoring.
              </p>
              
              <div className="grid sm:grid-cols-2 gap-4">
                {instructorFeatures.map((f, i) => (
                  <motion.div
                    key={f.title}
                    initial={{ opacity: 0, y: 20 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: i * 0.1 }}
                    className="flex items-start gap-3"
                  >
                    <div className="w-10 h-10 rounded-lg bg-brand-500/20 flex items-center justify-center flex-shrink-0">
                      <f.icon className="w-5 h-5 text-brand-400" />
                    </div>
                    <div>
                      <h4 className="font-semibold text-white mb-1">{f.title}</h4>
                      <p className="text-sm text-stone-400">{f.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.95 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative"
            >
              {/* Dashboard mockup */}
              <div className="rounded-2xl bg-stone-800/50 border border-stone-700 p-6 shadow-2xl backdrop-blur-sm">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-brand-500 to-brand-600 flex items-center justify-center">
                      <BarChart3 className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <div className="font-semibold text-white">Class Analytics</div>
                      <div className="text-xs text-stone-400">CS101 - Fall 2024</div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <div className="w-3 h-3 rounded-full bg-rose-500" />
                    <div className="w-3 h-3 rounded-full bg-amber-500" />
                    <div className="w-3 h-3 rounded-full bg-emerald-500" />
                  </div>
                </div>
                
                <div className="grid grid-cols-3 gap-4 mb-6">
                  {[
                    { label: "Active Students", value: "42", color: "text-emerald-400" },
                    { label: "Avg Mastery", value: "64%", color: "text-brand-400" },
                    { label: "Active TAs", value: "87", color: "text-violet-400" },
                  ].map((stat) => (
                    <div key={stat.label} className="rounded-xl bg-stone-700/50 p-4 text-center">
                      <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
                      <div className="text-xs text-stone-400">{stat.label}</div>
                    </div>
                  ))}
                </div>

                <div className="rounded-xl bg-stone-700/30 p-4">
                  <div className="text-sm font-semibold text-stone-300 mb-3">Recent Teaching Activity</div>
                  <div className="space-y-2">
                    {[
                      { name: "Alice Chen", action: "Taught Variables to Python TA", time: "2m ago" },
                      { name: "Bob Smith", action: "Completed Loop Assessment", time: "5m ago" },
                      { name: "Carol Wu", action: "Misconception detected in Functions", time: "12m ago" },
                    ].map((item, i) => (
                      <div key={i} className="flex items-center justify-between text-sm py-2 border-b border-stone-700/50 last:border-0">
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 rounded-full bg-brand-500/20 flex items-center justify-center text-xs text-brand-400">
                            {item.name[0]}
                          </div>
                          <span className="text-stone-300">{item.name}</span>
                          <span className="text-stone-500">{item.action}</span>
                        </div>
                        <span className="text-stone-500 text-xs">{item.time}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Demo Account Section */}
      <section className="py-24 bg-gradient-to-b from-brand-50/50 to-white">
        <div className="mx-auto max-w-4xl px-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="rounded-3xl bg-gradient-to-br from-brand-600 to-brand-700 p-1 shadow-2xl shadow-brand-500/25"
          >
            <div className="rounded-[22px] bg-white p-8 md:p-12">
              <div className="text-center mb-8">
                <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-brand-100 mb-4">
                  <Sparkles className="w-8 h-8 text-brand-600" />
                </div>
                <h2 className="text-3xl font-bold text-stone-900 mb-2">Try It Now</h2>
                <p className="text-stone-600">Use these demo accounts to explore all features instantly</p>
              </div>

              <div className="grid md:grid-cols-2 gap-6">
                <div className="rounded-xl bg-stone-50 p-6 border border-stone-200">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center">
                      <GraduationCap className="w-5 h-5 text-emerald-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-stone-900">Student Account</div>
                      <div className="text-xs text-stone-500">Full learning experience</div>
                    </div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-stone-500">Username:</span>
                      <code className="bg-white px-2 py-0.5 rounded border border-stone-200 font-mono text-stone-900">demo_student</code>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-stone-500">Password:</span>
                      <code className="bg-white px-2 py-0.5 rounded border border-stone-200 font-mono text-stone-900">demo123</code>
                    </div>
                  </div>
                </div>

                <div className="rounded-xl bg-stone-50 p-6 border border-stone-200">
                  <div className="flex items-center gap-3 mb-4">
                    <div className="w-10 h-10 rounded-lg bg-violet-100 flex items-center justify-center">
                      <Users className="w-5 h-5 text-violet-600" />
                    </div>
                    <div>
                      <div className="font-semibold text-stone-900">Teacher Account</div>
                      <div className="text-xs text-stone-500">Dashboard & analytics</div>
                    </div>
                  </div>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-stone-500">Username:</span>
                      <code className="bg-white px-2 py-0.5 rounded border border-stone-200 font-mono text-stone-900">demo_teacher</code>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-stone-500">Password:</span>
                      <code className="bg-white px-2 py-0.5 rounded border border-stone-200 font-mono text-stone-900">demo123</code>
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-8 text-center">
                <Link
                  to={ROUTES.login}
                  className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-brand-600 to-brand-700 px-8 py-4 text-base font-semibold text-white shadow-lg shadow-brand-500/25 transition-all hover:shadow-xl hover:-translate-y-0.5"
                >
                  <Play className="w-5 h-5" />
                  Launch ARTS-CS
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-stone-900">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform CS Education?
            </h2>
            <p className="text-xl text-stone-400 mb-10 max-w-2xl mx-auto">
              Join researchers and educators using ARTS-CS to implement "Learning by Teaching" 
              with AI-resistant assessment and misconception tracking.
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link
                to={ROUTES.login}
                className="group flex items-center gap-2 rounded-xl bg-white px-8 py-4 text-base font-semibold text-stone-900 shadow-lg transition-all hover:shadow-xl hover:-translate-y-0.5"
              >
                Get Started Free
                <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
              </Link>
              <a
                href="https://github.com/XianghuiMeng-1020/cs-teachable-agent"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 rounded-xl border border-stone-700 bg-stone-800/50 px-8 py-4 text-base font-semibold text-white transition-all hover:bg-stone-800"
              >
                View on GitHub
              </a>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-stone-950 border-t border-stone-800">
        <div className="mx-auto max-w-7xl px-6 py-12">
          <div className="grid md:grid-cols-4 gap-8 mb-8">
            <div className="md:col-span-2">
              <div className="flex items-center gap-2.5 mb-4">
                <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-gradient-to-br from-brand-600 to-brand-700">
                  <Sparkles className="h-5 w-5 text-white" />
                </div>
                <span className="text-lg font-bold text-white">ARTS-CS</span>
              </div>
              <p className="text-stone-400 max-w-sm">
                AI Resistant Teaching System for Computer Science. 
                A research platform for Learning by Teaching pedagogy.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Platform</h4>
              <ul className="space-y-2 text-sm text-stone-400">
                <li><Link to={ROUTES.login} className="hover:text-white transition-colors">Student Dashboard</Link></li>
                <li><Link to={ROUTES.login} className="hover:text-white transition-colors">Teach TA</Link></li>
                <li><Link to={ROUTES.login} className="hover:text-white transition-colors">Test TA</Link></li>
                <li><Link to={ROUTES.login} className="hover:text-white transition-colors">Analytics</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-white mb-4">Resources</h4>
              <ul className="space-y-2 text-sm text-stone-400">
                <li><a href="https://github.com/XianghuiMeng-1020/cs-teachable-agent" className="hover:text-white transition-colors">GitHub</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Research Paper</a></li>
                <li><Link to={ROUTES.login} className="hover:text-white transition-colors">Demo</Link></li>
              </ul>
            </div>
          </div>
          <div className="pt-8 border-t border-stone-800 flex flex-col md:flex-row items-center justify-between gap-4">
            <p className="text-sm text-stone-500">
              © 2026 ARTS-CS. AI Resistant Teaching System for Computer Science.
            </p>
            <div className="flex items-center gap-6 text-sm text-stone-500">
              <span>Built with FastAPI + React</span>
              <span>•</span>
              <span>Deployed on Render + Cloudflare</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
