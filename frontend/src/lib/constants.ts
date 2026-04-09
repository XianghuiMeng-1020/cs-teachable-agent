export const ROUTES = {
  home: "/",
  login: "/login",
  dashboard: "/dashboard",
  teach: "/teach",
  test: "/test",
  practice: "/practice",
  practiceItem: (itemId: number | string) => `/practice/${itemId}`,
  mastery: "/mastery",
  history: "/history",
  // M-40: Additional student routes
  learningAnalytics: "/learning-analytics",
  review: "/review",
  report: "/report",
  collaborate: "/collaborate",
  teacher: {
    overview: "/teacher",
    students: "/teacher/students",
    studentDetail: (id: number) => `/teacher/students/${id}`,
    transcripts: "/teacher/transcripts",
    analytics: "/teacher/analytics",
    assessments: "/teacher/assessments",
    metrics: "/teacher/metrics",
    proctoring: "/teacher/proctoring",
  },
} as const;

export const KU_DISPLAY_NAMES: Record<string, string> = {
  variable_assignment: "Variable assignment",
  print_function: "print()",
  input_function: "input()",
  type_conversion: "Type conversion",
  comparison_operators: "Comparison operators",
  logical_operators: "Logical operators",
  if_else: "if/else",
  for_loop_range: "for + range()",
  while_loop: "while loop",
  list_basics: "Lists",
  list_indexing: "List indexing",
  string_basics: "Strings",
  string_methods: "String methods",
  function_def: "Function definition",
  function_params: "Function parameters",
  return_statement: "return",
  default_arguments: "Default arguments",
  // extend as needed from seed data
};

export const MISCONCEPTION_DISPLAY: Record<string, string> = {
  assign_vs_equal: "Confuses = with ==",
  off_by_one_range: "Off-by-one in range()",
  string_int_concat: "String + int concatenation",
  mutable_default: "Mutable default argument",
  loop_var_scope: "Loop variable scope",
  indentation_block: "Indentation as block",
  // extend as needed
};
