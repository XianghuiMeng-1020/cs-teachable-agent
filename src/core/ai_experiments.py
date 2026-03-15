"""
Advanced AI Experiments Module

Features:
- Prompt Optimizer: Uses LLM to improve prompts
- Token Analyzer: Estimates token usage and visualizes distribution
- Response Comparator: Advanced comparison with similarity metrics
"""

import re
from typing import Optional
from src.llm.client import llm_completion


class TokenEstimator:
    """Estimate token count for text (rough approximation)."""
    
    # Average tokens per word for different languages
    AVG_TOKENS_PER_WORD = 1.3  # English average
    
    @staticmethod
    def estimate(text: str) -> int:
        """Estimate token count for a given text."""
        if not text:
            return 0
        
        # Count words
        words = len(text.split())
        
        # Count special tokens (code blocks, etc.)
        code_blocks = len(re.findall(r'```[\s\S]*?```', text))
        special_chars = len(re.findall(r'[^\w\s]', text))
        
        # Estimate: words * avg + code_penalty + special_char_penalty
        base_estimate = int(words * TokenEstimator.AVG_TOKENS_PER_WORD)
        code_penalty = code_blocks * 10  # Code blocks use more tokens
        special_penalty = special_chars // 5  # Special chars often split into tokens
        
        return base_estimate + code_penalty + special_penalty
    
    @staticmethod
    def breakdown(text: str) -> dict:
        """Provide a detailed token breakdown."""
        words = text.split()
        word_count = len(words)
        
        # Identify components
        code_blocks = re.findall(r'```([\s\S]*?)```', text)
        code_text = '\n'.join(code_blocks)
        code_tokens = TokenEstimator.estimate(code_text) if code_text else 0
        
        normal_text = re.sub(r'```[\s\S]*?```', '', text)
        normal_tokens = TokenEstimator.estimate(normal_text)
        
        return {
            "total_tokens": TokenEstimator.estimate(text),
            "word_count": word_count,
            "char_count": len(text),
            "code_blocks": len(code_blocks),
            "code_tokens": code_tokens,
            "text_tokens": normal_tokens,
            "estimated_cost_gpt4": TokenEstimator.estimate(text) * 0.00003,  # $0.03 per 1K tokens
            "estimated_cost_gpt3": TokenEstimator.estimate(text) * 0.000002,  # $0.002 per 1K tokens
        }


class PromptOptimizer:
    """Optimize prompts using LLM-based enhancement."""
    
    OPTIMIZATION_SYSTEM_PROMPT = """You are a prompt engineering expert. Analyze the given prompt and provide an improved version.

Your task:
1. Identify weaknesses in the original prompt (vagueness, missing context, ambiguous instructions)
2. Provide an optimized version that is:
   - Clear and specific
   - Well-structured with appropriate formatting
   - Includes necessary context and constraints
   - Uses best practices for the task type

Respond in this format:
ANALYSIS: <brief analysis of original prompt issues>
OPTIMIZED: <the improved prompt>
TIPS: <3-5 specific tips for better prompting>"""

    @staticmethod
    def optimize_prompt(prompt: str, domain: str = "general") -> dict:
        """Optimize a user prompt using LLM."""
        if not prompt or len(prompt) < 5:
            return {
                "original": prompt,
                "optimized": prompt,
                "analysis": "Prompt too short to optimize.",
                "tips": ["Add more detail to your prompt for better results."],
            }
        
        try:
            result = llm_completion(
                system=PromptOptimizer.OPTIMIZATION_SYSTEM_PROMPT,
                user=f"Domain: {domain}\n\nOriginal prompt: {prompt}",
                temperature=0.3,
                max_tokens=500,
            )
            
            # Parse the response
            analysis_match = re.search(r'ANALYSIS:\s*(.+?)(?=OPTIMIZED:|$)', result, re.DOTALL)
            optimized_match = re.search(r'OPTIMIZED:\s*(.+?)(?=TIPS:|$)', result, re.DOTALL)
            tips_match = re.search(r'TIPS:\s*(.+?)$', result, re.DOTALL)
            
            analysis = analysis_match.group(1).strip() if analysis_match else "No specific issues identified."
            optimized = optimized_match.group(1).strip() if optimized_match else prompt
            tips_text = tips_match.group(1).strip() if tips_match else ""
            
            # Parse tips into list
            tips = [t.strip('- ') for t in tips_text.split('\n') if t.strip() and t.strip()[0] in '-0123456789']
            if not tips:
                tips = ["Be specific in your instructions.", "Provide context when needed.", "Use examples to clarify expectations."]
            
            return {
                "original": prompt,
                "optimized": optimized,
                "analysis": analysis,
                "tips": tips[:5],
                "improvement_score": PromptOptimizer._calculate_improvement_score(prompt, optimized),
            }
        except Exception as e:
            return {
                "original": prompt,
                "optimized": prompt,
                "analysis": f"Optimization failed: {str(e)}",
                "tips": ["Check your prompt length and try again."],
                "error": True,
            }
    
    @staticmethod
    def _calculate_improvement_score(original: str, optimized: str) -> float:
        """Calculate a simple improvement score (0-100)."""
        score = 50.0  # Base score
        
        # Factors that indicate improvement
        if len(optimized) > len(original) * 1.1:  # More detailed
            score += 10
        if '```' in optimized or '**' in optimized:  # Better formatting
            score += 15
        if any(word in optimized.lower() for word in ['example', 'specific', 'step', 'clear']):
            score += 10
        
        # Factors that indicate problems
        if len(optimized) > len(original) * 3:  # Too long might be verbose
            score -= 10
        
        return min(100, max(0, score))


class ResponseComparator:
    """Advanced comparison of LLM responses."""
    
    @staticmethod
    def compare_responses(response_a: str, response_b: str) -> dict:
        """Compare two responses and provide detailed analysis."""
        
        # Basic metrics
        len_a, len_b = len(response_a), len(response_b)
        word_count_a = len(response_a.split())
        word_count_b = len(response_b.split())
        
        # Calculate similarity (simple word overlap)
        words_a = set(response_a.lower().split())
        words_b = set(response_b.lower().split())
        intersection = words_a & words_b
        union = words_a | words_b
        jaccard_similarity = len(intersection) / len(union) if union else 0
        
        # Structure analysis
        has_code_a = '```' in response_a
        has_code_b = '```' in response_b
        has_list_a = bool(re.search(r'^\s*[-*\d]', response_a, re.MULTILINE))
        has_list_b = bool(re.search(r'^\s*[-*\d]', response_b, re.MULTILINE))
        
        # Content diversity
        unique_words_a = len(words_a)
        unique_words_b = len(words_b)
        
        return {
            "similarity_score": round(jaccard_similarity * 100, 1),
            "length_comparison": {
                "response_a_chars": len_a,
                "response_b_chars": len_b,
                "response_a_words": word_count_a,
                "response_b_words": word_count_b,
                "length_difference_pct": round(((len_b - len_a) / max(1, len_a)) * 100, 1),
            },
            "structure_analysis": {
                "response_a_has_code": has_code_a,
                "response_b_has_code": has_code_b,
                "response_a_has_list": has_list_a,
                "response_b_has_list": has_list_b,
                "formatting_winner": "A" if (has_code_a and not has_code_b) or (has_list_a and not has_list_b) else 
                                    "B" if (has_code_b and not has_code_a) or (has_list_b and not has_list_a) else "Tie",
            },
            "content_analysis": {
                "response_a_unique_words": unique_words_a,
                "response_b_unique_words": unique_words_b,
                "vocabulary_richness_winner": "A" if unique_words_a > unique_words_b else "B" if unique_words_b > unique_words_a else "Tie",
            },
            "key_differences": ResponseComparator._extract_key_differences(response_a, response_b),
        }
    
    @staticmethod
    def _extract_key_differences(text_a: str, text_b: str, max_differences: int = 5) -> list[str]:
        """Extract key differences between two texts."""
        sentences_a = set(re.split(r'[.!?]+', text_a.lower()))
        sentences_b = set(re.split(r'[.!?]+', text_b.lower()))
        
        # Find sentences unique to each
        unique_to_a = sentences_a - sentences_b
        unique_to_b = sentences_b - sentences_a
        
        differences = []
        for s in list(unique_to_a)[:max_differences//2]:
            clean = s.strip()
            if len(clean) > 10:
                differences.append(f"Only in A: '{clean[:80]}...'")
        
        for s in list(unique_to_b)[:max_differences//2]:
            clean = s.strip()
            if len(clean) > 10:
                differences.append(f"Only in B: '{clean[:80]}...'")
        
        return differences[:max_differences]


def run_ai_experiment(experiment_type: str, input_data: dict, domain: str = "general") -> dict:
    """
    Run an AI experiment based on type.
    
    experiment_type: 'optimize_prompt', 'token_analysis', 'compare_responses'
    """
    if experiment_type == "optimize_prompt":
        prompt = input_data.get("prompt", "")
        return PromptOptimizer.optimize_prompt(prompt, domain)
    
    elif experiment_type == "token_analysis":
        text = input_data.get("text", "")
        return {
            "text": text,
            "token_analysis": TokenEstimator.breakdown(text),
        }
    
    elif experiment_type == "compare_responses":
        response_a = input_data.get("response_a", "")
        response_b = input_data.get("response_b", "")
        return ResponseComparator.compare_responses(response_a, response_b)
    
    else:
        return {"error": f"Unknown experiment type: {experiment_type}"}
