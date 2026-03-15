"""
Smart Code Evaluation System

Advanced code evaluation using AST analysis and semantic understanding.

Features:
- Abstract Syntax Tree (AST) analysis
- Semantic correctness checking
- Code quality metrics
- Partial credit evaluation
- Detailed error classification

Research Applications:
- Automated assessment systems
- Programming misconception detection
- Code quality analysis in education
"""

import ast
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from enum import Enum


class CodeQualityMetric(Enum):
    """Code quality metrics categories."""
    CORRECTNESS = "correctness"
    STYLE = "style"
    EFFICIENCY = "efficiency"
    READABILITY = "readability"
    COMPLETENESS = "completeness"


@dataclass
class CodeIssue:
    """Represents a code issue or suggestion."""
    line: int
    column: int
    issue_type: str
    severity: str  # error, warning, suggestion
    message: str
    suggestion: Optional[str] = None
    category: str = "general"


@dataclass
class CodeMetrics:
    """Code quality metrics."""
    lines_of_code: int
    cyclomatic_complexity: int
    function_count: int
    comment_ratio: float
    average_function_length: float
    nesting_depth: int


@dataclass
class EvaluationResult:
    """Complete code evaluation result."""
    score: float  # 0-100
    passed: bool
    partial_credit: float  # 0-1
    issues: List[CodeIssue]
    metrics: CodeMetrics
    feedback: List[str]
    expected_behavior: str
    actual_behavior: str
    concepts_used: List[str]
    missing_concepts: List[str]


class ASTAnalyzer:
    """Analyzes Python code using Abstract Syntax Tree."""
    
    def __init__(self, code: str):
        self.code = code
        self.tree = None
        self.issues: List[CodeIssue] = []
        self.concepts_used: List[str] = []
        
    def parse(self) -> bool:
        """Parse code into AST. Returns False if syntax error."""
        try:
            self.tree = ast.parse(self.code)
            return True
        except SyntaxError as e:
            self.issues.append(CodeIssue(
                line=e.lineno or 1,
                column=e.offset or 0,
                issue_type="syntax_error",
                severity="error",
                message=f"Syntax Error: {e.msg}",
            ))
            return False
    
    def analyze_structure(self) -> Dict[str, Any]:
        """Analyze code structure."""
        if not self.tree:
            return {}
        
        analysis = {
            "has_function_def": False,
            "has_loop": False,
            "has_conditional": False,
            "has_list_comprehension": False,
            "has_try_except": False,
            "has_class": False,
            "imports": [],
            "function_calls": [],
            "variable_assignments": [],
        }
        
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                analysis["has_function_def"] = True
                self.concepts_used.append("function_definition")
            elif isinstance(node, (ast.For, ast.While)):
                analysis["has_loop"] = True
                self.concepts_used.append("loops")
            elif isinstance(node, ast.If):
                analysis["has_conditional"] = True
                self.concepts_used.append("conditionals")
            elif isinstance(node, ast.ListComp):
                analysis["has_list_comprehension"] = True
                self.concepts_used.append("list_comprehension")
            elif isinstance(node, ast.Try):
                analysis["has_try_except"] = True
                self.concepts_used.append("exception_handling")
            elif isinstance(node, ast.ClassDef):
                analysis["has_class"] = True
                self.concepts_used.append("classes")
            elif isinstance(node, ast.Import):
                analysis["imports"].extend([alias.name for alias in node.names])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    analysis["function_calls"].append(node.func.id)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        analysis["variable_assignments"].append(target.id)
        
        return analysis
    
    def calculate_complexity(self) -> int:
        """Calculate cyclomatic complexity."""
        if not self.tree:
            return 0
        
        complexity = 1  # Base complexity
        
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
            elif isinstance(node, ast.comprehension):
                complexity += 1
        
        return complexity
    
    def check_style(self) -> List[CodeIssue]:
        """Check code style issues."""
        issues = []
        lines = self.code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check line length
            if len(line) > 100:
                issues.append(CodeIssue(
                    line=i,
                    column=100,
                    issue_type="line_too_long",
                    severity="warning",
                    message="Line exceeds 100 characters",
                    suggestion="Break into multiple lines",
                    category="style",
                ))
            
            # Check trailing whitespace
            if line.rstrip() != line:
                issues.append(CodeIssue(
                    line=i,
                    column=len(line),
                    issue_type="trailing_whitespace",
                    severity="suggestion",
                    message="Trailing whitespace detected",
                    category="style",
                ))
        
        return issues
    
    def find_common_mistakes(self) -> List[CodeIssue]:
        """Find common beginner mistakes."""
        issues = []
        
        # Check for == vs = in conditions
        for i, line in enumerate(self.code.split('\n'), 1):
            if re.search(r'if\s+\w+\s*=\s*', line):
                issues.append(CodeIssue(
                    line=i,
                    column=0,
                    issue_type="assignment_in_condition",
                    severity="error",
                    message="Using = (assignment) instead of == (comparison) in condition",
                    suggestion="Change = to == for comparison",
                    category="correctness",
                ))
        
        # Check for mutable default arguments
        if self.tree:
            for node in ast.walk(self.tree):
                if isinstance(node, ast.FunctionDef):
                    for default in node.args.defaults:
                        if isinstance(default, (ast.List, ast.Dict)):
                            issues.append(CodeIssue(
                                line=node.lineno,
                                column=node.col_offset,
                                issue_type="mutable_default",
                                severity="warning",
                                message="Mutable default argument detected",
                                suggestion="Use None as default and initialize inside function",
                                category="correctness",
                            ))
        
        return issues


class SemanticEvaluator:
    """Evaluates semantic correctness of code."""
    
    def __init__(self, expected_behavior: str, test_cases: List[Dict]):
        self.expected_behavior = expected_behavior
        self.test_cases = test_cases
    
    def evaluate_semantics(self, code: str, execution_result: Dict) -> Dict[str, Any]:
        """
        Evaluate semantic correctness based on expected behavior.
        
        Returns:
            Dictionary with semantic analysis results
        """
        result = {
            "semantic_score": 0.0,
            "behavior_match": False,
            "partial_credits": [],
            "suggestions": [],
        }
        
        if execution_result.get("passed", False):
            result["semantic_score"] = 1.0
            result["behavior_match"] = True
        else:
            # Analyze why it failed
            error_msg = execution_result.get("error", "")
            
            # Check for specific error patterns
            if "TypeError" in error_msg:
                result["suggestions"].append("Check variable types - you may be mixing incompatible types")
            elif "IndexError" in error_msg:
                result["suggestions"].append("Index out of range - check your list indices")
            elif "KeyError" in error_msg:
                result["suggestions"].append("Dictionary key not found - verify the key exists")
            elif "NameError" in error_msg:
                result["suggestions"].append("Variable not defined - check variable names")
            
            # Calculate partial credit based on what worked
            result["semantic_score"] = 0.3  # Base partial credit for attempt
        
        return result


class SmartCodeEvaluator:
    """Main class for intelligent code evaluation."""
    
    def __init__(self):
        self.weight_correctness = 0.4
        self.weight_functionality = 0.3
        self.weight_style = 0.15
        self.weight_efficiency = 0.15
    
    def evaluate(
        self,
        code: str,
        test_cases: List[Dict],
        expected_concepts: List[str],
        execution_result: Optional[Dict] = None
    ) -> EvaluationResult:
        """
        Perform comprehensive code evaluation.
        
        Args:
            code: The code to evaluate
            test_cases: List of test case dictionaries
            expected_concepts: List of expected concepts
            execution_result: Optional execution results
        
        Returns:
            Complete evaluation result
        """
        # AST Analysis
        ast_analyzer = ASTAnalyzer(code)
        can_parse = ast_analyzer.parse()
        
        all_issues = []
        concepts_used = []
        metrics = CodeMetrics(0, 0, 0, 0.0, 0.0, 0)
        
        if can_parse:
            # Structure analysis
            structure = ast_analyzer.analyze_structure()
            concepts_used = list(set(ast_analyzer.concepts_used))
            
            # Style checking
            style_issues = ast_analyzer.check_style()
            all_issues.extend(style_issues)
            
            # Common mistakes
            mistakes = ast_analyzer.find_common_mistakes()
            all_issues.extend(mistakes)
            
            # Calculate metrics
            lines = code.split('\n')
            non_empty = [l for l in lines if l.strip()]
            metrics = CodeMetrics(
                lines_of_code=len(non_empty),
                cyclomatic_complexity=ast_analyzer.calculate_complexity(),
                function_count=1 if structure.get("has_function_def") else 0,
                comment_ratio=len([l for l in lines if l.strip().startswith('#')]) / max(1, len(non_empty)),
                average_function_length=len(non_empty) / max(1, sum(1 for l in lines if 'def ' in l)),
                nesting_depth=self._calculate_nesting_depth(code),
            )
        
        # Semantic evaluation
        semantic_score = 0.0
        if execution_result:
            semantic_eval = SemanticEvaluator("", test_cases)
            semantic_result = semantic_eval.evaluate_semantics(code, execution_result)
            semantic_score = semantic_result["semantic_score"]
        
        # Calculate scores
        correctness_score = 1.0 if can_parse and not any(i.severity == "error" for i in all_issues) else 0.0
        if execution_result:
            correctness_score *= 0.5 + (0.5 if execution_result.get("passed", False) else 0.0)
        
        style_score = 1.0 - (len([i for i in all_issues if i.category == "style"]) * 0.1)
        style_score = max(0, style_score)
        
        efficiency_score = 1.0 - (metrics.cyclomatic_complexity - 1) * 0.05
        efficiency_score = max(0, efficiency_score)
        
        # Concept coverage
        concept_coverage = len(set(concepts_used) & set(expected_concepts)) / max(1, len(expected_concepts))
        
        # Calculate total score
        total_score = (
            correctness_score * self.weight_correctness +
            semantic_score * self.weight_functionality +
            style_score * self.weight_style +
            efficiency_score * self.weight_efficiency
        ) * 100
        
        # Generate feedback
        feedback = self._generate_feedback(
            all_issues, concepts_used, expected_concepts, metrics, execution_result
        )
        
        # Missing concepts
        missing_concepts = list(set(expected_concepts) - set(concepts_used))
        
        return EvaluationResult(
            score=round(total_score, 1),
            passed=total_score >= 70 and can_parse,
            partial_credit=round(semantic_score, 2),
            issues=all_issues,
            metrics=metrics,
            feedback=feedback,
            expected_behavior="Code should pass all test cases",
            actual_behavior="Execution completed" if execution_result else "Not executed",
            concepts_used=concepts_used,
            missing_concepts=missing_concepts,
        )
    
    def _calculate_nesting_depth(self, code: str) -> int:
        """Calculate maximum nesting depth."""
        max_depth = 0
        current_depth = 0
        
        for line in code.split('\n'):
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            depth = indent // 4  # Assuming 4-space indentation
            max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _generate_feedback(
        self,
        issues: List[CodeIssue],
        concepts_used: List[str],
        expected_concepts: List[str],
        metrics: CodeMetrics,
        execution_result: Optional[Dict]
    ) -> List[str]:
        """Generate human-readable feedback."""
        feedback = []
        
        # Add issue-based feedback
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        
        if errors:
            feedback.append(f"❌ Found {len(errors)} error(s) that need to be fixed")
        elif warnings:
            feedback.append(f"⚠️ Code works but has {len(warnings)} warning(s) to improve")
        else:
            feedback.append("✅ Code has no style issues")
        
        # Concept feedback
        missing = set(expected_concepts) - set(concepts_used)
        if missing:
            feedback.append(f"📚 Consider using: {', '.join(missing)}")
        else:
            feedback.append("✅ All expected concepts are used")
        
        # Execution feedback
        if execution_result:
            if execution_result.get("passed"):
                feedback.append("✅ All test cases passed")
            else:
                feedback.append("❌ Some test cases failed - check your logic")
        
        # Metrics feedback
        if metrics.cyclomatic_complexity > 5:
            feedback.append("⚠️ Code is getting complex - consider breaking into smaller functions")
        
        if metrics.comment_ratio < 0.05:
            feedback.append("💡 Consider adding comments to explain complex logic")
        
        return feedback
    
    def generate_detailed_report(self, result: EvaluationResult) -> Dict[str, Any]:
        """Generate detailed evaluation report."""
        return {
            "summary": {
                "score": result.score,
                "passed": result.passed,
                "grade": self._score_to_grade(result.score),
            },
            "breakdown": {
                "correctness": "✅" if result.score >= 70 else "❌",
                "style_issues": len([i for i in result.issues if i.category == "style"]),
                "concepts_used": len(result.concepts_used),
                "complexity": result.metrics.cyclomatic_complexity,
            },
            "feedback": result.feedback,
            "issues_by_severity": {
                "errors": [i for i in result.issues if i.severity == "error"],
                "warnings": [i for i in result.issues if i.severity == "warning"],
                "suggestions": [i for i in result.issues if i.severity == "suggestion"],
            },
            "improvement_areas": self._identify_improvement_areas(result),
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"
    
    def _identify_improvement_areas(self, result: EvaluationResult) -> List[str]:
        """Identify areas for improvement."""
        areas = []
        
        if result.score < 70:
            areas.append("Address errors to make code functional")
        
        if result.metrics.cyclomatic_complexity > 5:
            areas.append("Simplify code structure")
        
        if result.missing_concepts:
            areas.append(f"Learn and apply: {', '.join(result.missing_concepts[:3])}")
        
        if result.metrics.comment_ratio < 0.05:
            areas.append("Add documentation comments")
        
        return areas


def evaluate_code_smart(
    code: str,
    test_cases: List[Dict],
    expected_concepts: List[str] = None,
    execution_result: Dict = None
) -> EvaluationResult:
    """
    Convenience function for smart code evaluation.
    
    This is the main API-facing function.
    """
    evaluator = SmartCodeEvaluator()
    return evaluator.evaluate(
        code=code,
        test_cases=test_cases or [],
        expected_concepts=expected_concepts or [],
        execution_result=execution_result
    )
