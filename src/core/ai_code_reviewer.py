"""
AI Code Reviewer System

Intelligent code review for Python learning.
Provides detailed feedback, suggestions, and learning opportunities.

Research Applications:
- Automated code quality assessment
- Educational code review
- Best practice teaching
- Style guide enforcement
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum
import ast
import re
from collections import defaultdict


class IssueSeverity(Enum):
    """Severity levels for code issues."""
    CRITICAL = "critical"      # Will cause errors
    WARNING = "warning"        # Potential problems
    SUGGESTION = "suggestion"  # Improvements
    STYLE = "style"           # Style issues
    PRAISE = "praise"         # Good practices


class IssueCategory(Enum):
    """Categories of code issues."""
    SYNTAX = "syntax"
    LOGIC = "logic"
    STYLE = "style"
    PERFORMANCE = "performance"
    SECURITY = "security"
    BEST_PRACTICE = "best_practice"
    DOCUMENTATION = "documentation"
    COMPLEXITY = "complexity"


@dataclass
class CodeIssue:
    """A code issue or suggestion."""
    line_number: int
    column: int
    severity: IssueSeverity
    category: IssueCategory
    message: str
    suggestion: str
    example: Optional[str] = None
    rule_id: str = ""


@dataclass
class CodeMetrics:
    """Metrics for code quality."""
    lines_of_code: int
    complexity_score: float
    readability_score: float
    documentation_coverage: float
    test_coverage_estimate: float
    duplicate_code_blocks: List[tuple]
    function_lengths: Dict[str, int]


@dataclass
class ReviewResult:
    """Complete code review result."""
    overall_score: float  # 0-100
    grade: str  # A-F
    issues: List[CodeIssue]
    metrics: CodeMetrics
    summary: str
    learning_opportunities: List[str]
    strengths: List[str]
    next_steps: List[str]


class AICodeReviewer:
    """
    AI-powered code reviewer for educational Python code.
    
    Features:
    - AST-based static analysis
    - Educational-focused feedback
    - Personalized suggestions
    - Learning-oriented metrics
    """
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> Dict:
        """Initialize review rules."""
        return {
            "naming": {
                "pattern": r"^[a-z_][a-z0-9_]*$",
                "message": "Use snake_case for variable names",
            },
            "line_length": {
                "max_length": 79,
                "message": "Line too long (max 79 characters)",
            },
            "complexity_threshold": 10,
            "max_function_length": 50,
        }
    
    def review_code(
        self,
        code: str,
        student_level: str = "beginner",
        focus_areas: Optional[List[str]] = None,
    ) -> ReviewResult:
        """
        Perform comprehensive code review.
        
        Args:
            code: Python code to review
            student_level: beginner/intermediate/advanced
            focus_areas: Specific areas to focus on
        
        Returns:
            Complete review result
        """
        issues = []
        
        # 1. Syntax check
        syntax_issues = self._check_syntax(code)
        issues.extend(syntax_issues)
        
        # If syntax errors, stop here
        if any(i.severity == IssueSeverity.CRITICAL for i in syntax_issues):
            metrics = self._calculate_basic_metrics(code)
            return ReviewResult(
                overall_score=0,
                grade="F",
                issues=issues,
                metrics=metrics,
                summary="Syntax errors must be fixed before detailed review.",
                learning_opportunities=["Review Python syntax basics"],
                strengths=[],
                next_steps=["Fix syntax errors", "Re-submit for review"],
            )
        
        # 2. AST-based analysis
        try:
            tree = ast.parse(code)
            ast_issues = self._analyze_ast(tree, code, student_level)
            issues.extend(ast_issues)
        except SyntaxError:
            pass
        
        # 3. Style check
        style_issues = self._check_style(code, student_level)
        issues.extend(style_issues)
        
        # 4. Best practices
        practice_issues = self._check_best_practices(code, tree, student_level)
        issues.extend(practice_issues)
        
        # 5. Calculate metrics
        metrics = self._calculate_metrics(code, tree)
        
        # 6. Calculate score
        score = self._calculate_score(issues, metrics)
        
        # 7. Generate summary
        summary = self._generate_summary(issues, metrics, score)
        
        # 8. Identify learning opportunities
        learning_opps = self._identify_learning_opportunities(issues, student_level)
        
        # 9. Identify strengths
        strengths = self._identify_strengths(code, issues, metrics)
        
        # 10. Generate next steps
        next_steps = self._generate_next_steps(issues, score, student_level)
        
        return ReviewResult(
            overall_score=score,
            grade=self._score_to_grade(score),
            issues=sorted(issues, key=lambda x: (
                0 if x.severity == IssueSeverity.CRITICAL else
                1 if x.severity == IssueSeverity.WARNING else
                2 if x.severity == IssueSeverity.SUGGESTION else 3
            )),
            metrics=metrics,
            summary=summary,
            learning_opportunities=learning_opps,
            strengths=strengths,
            next_steps=next_steps,
        )
    
    def _check_syntax(self, code: str) -> List[CodeIssue]:
        """Check for syntax errors."""
        issues = []
        
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(CodeIssue(
                line_number=e.lineno or 1,
                column=e.offset or 0,
                severity=IssueSeverity.CRITICAL,
                category=IssueCategory.SYNTAX,
                message=f"Syntax Error: {e.msg}",
                suggestion="Check for missing colons, parentheses, or quotes",
                example=None,
                rule_id="SYNTAX_ERROR",
            ))
        
        return issues
    
    def _analyze_ast(
        self,
        tree: ast.AST,
        code: str,
        student_level: str,
    ) -> List[CodeIssue]:
        """Analyze AST for issues."""
        issues = []
        
        for node in ast.walk(tree):
            # Check for bare except
            if isinstance(node, ast.ExceptHandler):
                if node.type is None:
                    issues.append(CodeIssue(
                        line_number=getattr(node, 'lineno', 1),
                        column=0,
                        severity=IssueSeverity.WARNING,
                        category=IssueCategory.BEST_PRACTICE,
                        message="Bare 'except:' clause catches all exceptions including SystemExit",
                        suggestion="Use 'except Exception:' or specify the exception type",
                        example="except ValueError as e:",
                        rule_id="BARE_EXCEPT",
                    ))
            
            # Check for mutable default arguments
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        issues.append(CodeIssue(
                            line_number=node.lineno,
                            column=0,
                            severity=IssueSeverity.WARNING,
                            category=IssueCategory.LOGIC,
                            message="Mutable default argument can cause unexpected behavior",
                            suggestion="Use None as default and create mutable object inside function",
                            example="def foo(arg=None):\n    if arg is None:\n        arg = []",
                            rule_id="MUTABLE_DEFAULT",
                        ))
                
                # Check function length
                func_length = len(ast.unparse(node).split('\n'))
                if func_length > self.rules["max_function_length"]:
                    issues.append(CodeIssue(
                        line_number=node.lineno,
                        column=0,
                        severity=IssueSeverity.SUGGESTION,
                        category=IssueCategory.COMPLEXITY,
                        message=f"Function is {func_length} lines long",
                        suggestion="Consider breaking into smaller functions",
                        example=None,
                        rule_id="LONG_FUNCTION",
                    ))
            
            # Check for unused variables
            if isinstance(node, ast.Name):
                # Simple check - would need more sophisticated analysis for full detection
                pass
        
        return issues
    
    def _check_style(self, code: str, student_level: str) -> List[CodeIssue]:
        """Check style guidelines."""
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Line length
            if len(line) > self.rules["line_length"]["max_length"]:
                issues.append(CodeIssue(
                    line_number=i,
                    column=0,
                    severity=IssueSeverity.STYLE,
                    category=IssueCategory.STYLE,
                    message=self.rules["line_length"]["message"],
                    suggestion="Break the line into multiple lines or use parentheses for implicit continuation",
                    example=None,
                    rule_id="LINE_TOO_LONG",
                ))
            
            # Trailing whitespace
            if line.rstrip() != line:
                issues.append(CodeIssue(
                    line_number=i,
                    column=len(line.rstrip()),
                    severity=IssueSeverity.STYLE,
                    category=IssueCategory.STYLE,
                    message="Trailing whitespace",
                    suggestion="Remove trailing spaces",
                    example=None,
                    rule_id="TRAILING_WHITESPACE",
                ))
        
        return issues
    
    def _check_best_practices(
        self,
        code: str,
        tree: ast.AST,
        student_level: str,
    ) -> List[CodeIssue]:
        """Check for best practices."""
        issues = []
        code_lower = code.lower()
        
        # Check for print statements (suggest logging for advanced)
        if student_level == "advanced" and "print(" in code_lower:
            issues.append(CodeIssue(
                line_number=1,
                column=0,
                severity=IssueSeverity.SUGGESTION,
                category=IssueCategory.BEST_PRACTICE,
                message="Consider using logging instead of print for production code",
                suggestion="Use the logging module for better output control",
                example="import logging\nlogging.info('Message')",
                rule_id="USE_LOGGING",
            ))
        
        # Check for list comprehensions opportunities
        # This is a simplified check
        if "for" in code_lower and "append" in code_lower:
            issues.append(CodeIssue(
                line_number=1,
                column=0,
                severity=IssueSeverity.SUGGESTION,
                category=IssueCategory.BEST_PRACTICE,
                message="Consider using list comprehension for building lists",
                suggestion="Use [x for x in iterable] instead of loop + append",
                example="squares = [x**2 for x in range(10)]",
                rule_id="USE_LIST_COMP",
            ))
        
        # Check for docstrings
        has_docstring = False
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                if ast.get_docstring(node):
                    has_docstring = True
                    break
        
        if not has_docstring and student_level in ["intermediate", "advanced"]:
            issues.append(CodeIssue(
                line_number=1,
                column=0,
                severity=IssueSeverity.SUGGESTION,
                category=IssueCategory.DOCUMENTATION,
                message="Add docstrings to functions and classes",
                suggestion="Use triple-quoted strings to document your code",
                example='def func():\n    """Brief description."""',
                rule_id="MISSING_DOCSTRING",
            ))
        
        return issues
    
    def _calculate_basic_metrics(self, code: str) -> CodeMetrics:
        """Calculate basic metrics when AST parsing fails."""
        lines = code.split('\n')
        return CodeMetrics(
            lines_of_code=len([l for l in lines if l.strip()]),
            complexity_score=0,
            readability_score=50,
            documentation_coverage=0,
            test_coverage_estimate=0,
            duplicate_code_blocks=[],
            function_lengths={},
        )
    
    def _calculate_metrics(self, code: str, tree: ast.AST) -> CodeMetrics:
        """Calculate code quality metrics."""
        lines = code.split('\n')
        loc = len([l for l in lines if l.strip() and not l.strip().startswith('#')])
        
        # Complexity (simplified)
        complexity = 1
        function_lengths = {}
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                func_lines = len(ast.unparse(node).split('\n'))
                function_lengths[node.name] = func_lines
        
        # Documentation coverage
        documented = 0
        total = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                total += 1
                if ast.get_docstring(node):
                    documented += 1
        
        doc_coverage = documented / total if total > 0 else 1.0
        
        # Readability estimate
        avg_line_length = sum(len(l) for l in lines) / len(lines) if lines else 0
        readability = max(0, 100 - (avg_line_length - 50) * 2)
        
        return CodeMetrics(
            lines_of_code=loc,
            complexity_score=complexity,
            readability_score=round(readability, 1),
            documentation_coverage=round(doc_coverage * 100, 1),
            test_coverage_estimate=0,  # Would need test file analysis
            duplicate_code_blocks=[],
            function_lengths=function_lengths,
        )
    
    def _calculate_score(self, issues: List[CodeIssue], metrics: CodeMetrics) -> float:
        """Calculate overall quality score."""
        score = 100
        
        # Deduct for issues
        deductions = {
            IssueSeverity.CRITICAL: 20,
            IssueSeverity.WARNING: 10,
            IssueSeverity.SUGGESTION: 5,
            IssueSeverity.STYLE: 2,
        }
        
        for issue in issues:
            score -= deductions.get(issue.severity, 1)
        
        # Adjust by metrics
        if metrics.complexity_score > 10:
            score -= (metrics.complexity_score - 10) * 2
        
        score += metrics.readability_score * 0.1
        score += metrics.documentation_coverage * 0.1
        
        return max(0, min(100, score))
    
    def _score_to_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90: return "A"
        if score >= 80: return "B"
        if score >= 70: return "C"
        if score >= 60: return "D"
        return "F"
    
    def _generate_summary(self, issues: List[CodeIssue], metrics: CodeMetrics, score: float) -> str:
        """Generate review summary."""
        critical = sum(1 for i in issues if i.severity == IssueSeverity.CRITICAL)
        warnings = sum(1 for i in issues if i.severity == IssueSeverity.WARNING)
        
        if critical > 0:
            return f"Code has {critical} critical issue(s) that must be fixed. Score: {score:.0f}/100"
        elif warnings > 3:
            return f"Code works but has {warnings} warnings to address. Score: {score:.0f}/100"
        elif score >= 80:
            return f"Good quality code! Score: {score:.0f}/100"
        else:
            return f"Code is functional but could be improved. Score: {score:.0f}/100"
    
    def _identify_learning_opportunities(
        self,
        issues: List[CodeIssue],
        student_level: str,
    ) -> List[str]:
        """Identify learning opportunities from issues."""
        opportunities = []
        
        categories = set(i.category for i in issues)
        
        if IssueCategory.SYNTAX in categories:
            opportunities.append("Review Python syntax fundamentals")
        
        if IssueCategory.BEST_PRACTICE in categories:
            opportunities.append("Learn Python best practices and idioms")
        
        if IssueCategory.STYLE in categories:
            opportunities.append("Study PEP 8 style guide")
        
        if IssueCategory.COMPLEXITY in categories:
            opportunities.append("Practice breaking down complex code")
        
        if not opportunities:
            opportunities.append("Explore advanced Python features")
        
        return opportunities
    
    def _identify_strengths(self, code: str, issues: List[CodeIssue], metrics: CodeMetrics) -> List[str]:
        """Identify code strengths."""
        strengths = []
        
        # Check for good practices
        if metrics.documentation_coverage > 50:
            strengths.append("Good documentation coverage")
        
        if metrics.readability_score > 70:
            strengths.append("Readable code structure")
        
        if metrics.complexity_score < 10:
            strengths.append("Simple, maintainable code")
        
        # Check for language features used
        if "with" in code:
            strengths.append("Proper resource management with context managers")
        
        if "try" in code and "except" in code:
            strengths.append("Error handling implemented")
        
        if "def " in code and len([i for i in issues if i.rule_id == "MUTABLE_DEFAULT"]) == 0:
            strengths.append("Good function design")
        
        if not strengths:
            strengths.append("Code compiles and runs")
        
        return strengths
    
    def _generate_next_steps(
        self,
        issues: List[CodeIssue],
        score: float,
        student_level: str,
    ) -> List[str]:
        """Generate recommended next steps."""
        steps = []
        
        critical = [i for i in issues if i.severity == IssueSeverity.CRITICAL]
        if critical:
            steps.append(f"Fix {len(critical)} critical issue(s)")
        
        warnings = [i for i in issues if i.severity == IssueSeverity.WARNING]
        if warnings:
            steps.append(f"Address {len(warnings)} warning(s)")
        
        if score < 70:
            steps.append("Review the suggested improvements")
            steps.append("Run the code through the review again")
        else:
            steps.append("Consider the style suggestions for cleaner code")
            if student_level == "beginner":
                steps.append("Move on to the next challenge!")
        
        return steps


def review_student_code(
    code: str,
    student_level: str = "beginner",
) -> Dict:
    """
    Main API-facing function for code review.
    
    Args:
        code: Python code to review
        student_level: Student experience level
    
    Returns:
        Review results as dictionary
    """
    reviewer = AICodeReviewer()
    result = reviewer.review_code(code, student_level)
    
    return {
        "overall_score": result.overall_score,
        "grade": result.grade,
        "summary": result.summary,
        "issues": [
            {
                "line": i.line_number,
                "severity": i.severity.value,
                "category": i.category.value,
                "message": i.message,
                "suggestion": i.suggestion,
                "example": i.example,
            }
            for i in result.issues
        ],
        "metrics": {
            "lines_of_code": result.metrics.lines_of_code,
            "complexity": result.metrics.complexity_score,
            "readability": result.metrics.readability_score,
            "documentation": result.metrics.documentation_coverage,
        },
        "learning_opportunities": result.learning_opportunities,
        "strengths": result.strengths,
        "next_steps": result.next_steps,
    }
