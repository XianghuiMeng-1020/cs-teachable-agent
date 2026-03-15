"""
Learning Sentiment Analyzer

Analyzes emotional state and engagement from student messages.
Provides real-time feedback on learning experience.

Research areas:
- Learning engagement prediction
- Frustration detection
- Help-seeking behavior analysis
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class EmotionalState(Enum):
    CONFUSED = "confused"
    FRUSTRATED = "frustrated"
    ENGAGED = "engaged"
    SATISFIED = "satisfied"
    NEUTRAL = "neutral"
    EXCITED = "excited"
    BORED = "bored"


@dataclass
class SentimentAnalysis:
    """Result of sentiment analysis."""
    emotional_state: EmotionalState
    confidence: float  # 0.0 to 1.0
    engagement_score: float  # -1.0 to 1.0
    confusion_indicators: list[str]
    frustration_indicators: list[str]
    positive_indicators: list[str]
    help_seeking: bool
    needs_intervention: bool
    suggested_response: str


class LearningSentimentAnalyzer:
    """Analyzes learning-related sentiment in student messages."""

    # Lexicons for different emotional states
    CONFUSION_KEYWORDS = [
        "confused", "don't understand", "lost", "unclear", "huh?", "what?",
        "not sure", "how does", "why is", "???", "doesn't make sense",
        "help me", "explain", "clarify", "elaborate", "example",
    ]

    FRUSTRATION_KEYWORDS = [
        "frustrated", "annoyed", "stuck", "can't figure", "impossible",
        "too hard", "difficult", "complex", "overwhelmed", "giving up",
        "wasting time", "broken", "bug", "error", "doesn't work",
    ]

    ENGAGEMENT_KEYWORDS = [
        "interesting", "fascinating", "cool", "awesome", "amazing",
        "love this", "excited", "curious", "want to learn", "tell me more",
        "how about", "what if", "can we", "let's try", "experiment",
    ]

    SATISFACTION_KEYWORDS = [
        "got it", "understood", "makes sense", "clear", "thanks",
        "perfect", "exactly", "precisely", "now i see", "aha",
        "that helps", "good explanation", "well done", "nice",
    ]

    BOREDOM_KEYWORDS = [
        "boring", "tedious", "repetitive", "again?", "already know",
        "too slow", "skip", "next", "when will we", "get to the point",
    ]

    def analyze(self, message: str, context: Optional[list[dict]] = None) -> SentimentAnalysis:
        """
        Analyze sentiment in a student message.
        
        Args:
            message: The student's message text
            context: Optional list of previous messages for context
        
        Returns:
            SentimentAnalysis with emotional state and recommendations
        """
        message_lower = message.lower()
        
        # Count indicators
        confusion_count = sum(1 for kw in self.CONFUSION_KEYWORDS if kw in message_lower)
        frustration_count = sum(1 for kw in self.FRUSTRATION_KEYWORDS if kw in message_lower)
        engagement_count = sum(1 for kw in self.ENGAGEMENT_KEYWORDS if kw in message_lower)
        satisfaction_count = sum(1 for kw in self.SATISFACTION_KEYWORDS if kw in message_lower)
        boredom_count = sum(1 for kw in self.BOREDOM_KEYWORDS if kw in message_lower)
        
        # Identify specific indicators
        confusion_indicators = [kw for kw in self.CONFUSION_KEYWORDS if kw in message_lower]
        frustration_indicators = [kw for kw in self.FRUSTRATION_KEYWORDS if kw in message_lower]
        positive_indicators = (
            [kw for kw in self.ENGAGEMENT_KEYWORDS if kw in message_lower] +
            [kw for kw in self.SATISFACTION_KEYWORDS if kw in message_lower]
        )
        
        # Calculate engagement score (-1 to 1)
        positive_signals = engagement_count + satisfaction_count
        negative_signals = confusion_count + frustration_count + boredom_count
        total_signals = positive_signals + negative_signals
        
        if total_signals == 0:
            engagement_score = 0.0
        else:
            engagement_score = (positive_signals - negative_signals) / max(5, total_signals)
        
        # Determine emotional state
        scores = {
            EmotionalState.CONFUSED: confusion_count * 1.5,
            EmotionalState.FRUSTRATED: frustration_count * 2.0,  # Weight frustration higher
            EmotionalState.EXCITED: engagement_count * 1.5,
            EmotionalState.SATISFIED: satisfaction_count * 1.0,
            EmotionalState.BORED: boredom_count * 1.5,
        }
        
        # Check for question patterns
        question_words = len(re.findall(r'\b(what|how|why|when|where|who|which)\b', message_lower))
        is_question = '?' in message or question_words > 0
        
        # Help seeking detection
        help_seeking = (
            confusion_count > 0 or
            frustration_count > 0 or
            is_question and confusion_count > 0
        )
        
        # Determine primary emotional state
        max_score = max(scores.values())
        
        if max_score == 0:
            if is_question:
                emotional_state = EmotionalState.CONFUSED
            else:
                emotional_state = EmotionalState.NEUTRAL
        else:
            emotional_state = max(scores, key=scores.get)
        
        # Calculate confidence
        confidence = min(1.0, max_score / 3.0) if max_score > 0 else 0.3
        
        # Determine if intervention needed
        needs_intervention = (
            emotional_state == EmotionalState.FRUSTRATED or
            emotional_state == EmotionalState.BORED or
            (emotional_state == EmotionalState.CONFUSED and confusion_count >= 2) or
            frustration_count >= 2
        )
        
        # Generate suggested response
        suggested_response = self._generate_suggested_response(
            emotional_state, help_seeking, needs_intervention
        )
        
        return SentimentAnalysis(
            emotional_state=emotional_state,
            confidence=confidence,
            engagement_score=engagement_score,
            confusion_indicators=confusion_indicators[:3],
            frustration_indicators=frustration_indicators[:3],
            positive_indicators=positive_indicators[:3],
            help_seeking=help_seeking,
            needs_intervention=needs_intervention,
            suggested_response=suggested_response,
        )
    
    def _generate_suggested_response(
        self,
        state: EmotionalState,
        help_seeking: bool,
        needs_intervention: bool,
    ) -> str:
        """Generate a suggested TA response based on sentiment."""
        
        if state == EmotionalState.FRUSTRATED and needs_intervention:
            return (
                "I notice you might be feeling frustrated. Let's take a step back and "
                "break this down into smaller, more manageable pieces. What specific part "
                "is causing the most difficulty?"
            )
        
        elif state == EmotionalState.CONFUSED and help_seeking:
            return (
                "It seems like this concept isn't quite clear yet. Let me explain it from "
                "a different angle. Would a specific example help?"
            )
        
        elif state == EmotionalState.EXCITED:
            return (
                "I love your enthusiasm! Your curiosity is great for learning. "
                "Let's explore this further - what aspect interests you most?"
            )
        
        elif state == EmotionalState.SATISFIED:
            return (
                "Wonderful! It sounds like this is making sense now. "
                "Would you like to try a slightly more challenging problem to solidify your understanding?"
            )
        
        elif state == EmotionalState.BORED:
            return (
                "This might be review for you. Let's skip ahead to something more engaging, "
                "or would you like to try a more advanced challenge?"
            )
        
        elif help_seeking:
            return "I'm here to help! Could you tell me more specifically where you're getting stuck?"
        
        else:
            return "Thanks for your message! Let me process what you've shared."
    
    def analyze_conversation_trend(
        self,
        messages: list[dict],
        window_size: int = 5,
    ) -> dict:
        """
        Analyze sentiment trend over a conversation window.
        
        Returns trend analysis for detecting learning struggles early.
        """
        if not messages:
            return {"trend": "unknown", "avg_engagement": 0, "alerts": []}
        
        # Analyze last N messages
        recent_messages = messages[-window_size:]
        analyses = [self.analyze(m.get("content", "")) for m in recent_messages]
        
        # Calculate trend metrics
        avg_engagement = sum(a.engagement_score for a in analyses) / len(analyses)
        avg_confidence = sum(a.confidence for a in analyses) / len(analyses)
        
        # Count states
        state_counts = {}
        for a in analyses:
            state_counts[a.emotional_state] = state_counts.get(a.emotional_state, 0) + 1
        
        # Determine trend
        negative_states = state_counts.get(EmotionalState.FRUSTRATED, 0) + \
                         state_counts.get(EmotionalState.CONFUSED, 0) + \
                         state_counts.get(EmotionalState.BORED, 0)
        
        positive_states = state_counts.get(EmotionalState.EXCITED, 0) + \
                         state_counts.get(EmotionalState.SATISFIED, 0) + \
                         state_counts.get(EmotionalState.ENGAGED, 0)
        
        if negative_states >= 3:
            trend = "declining"
        elif positive_states >= 3:
            trend = "improving"
        else:
            trend = "stable"
        
        # Generate alerts
        alerts = []
        if state_counts.get(EmotionalState.FRUSTRATED, 0) >= 2:
            alerts.append({
                "type": "frustration",
                "severity": "high",
                "message": "Student showing signs of frustration - consider intervention",
            })
        
        if avg_engagement < -0.3:
            alerts.append({
                "type": "low_engagement",
                "severity": "medium",
                "message": "Engagement declining - may need to adjust teaching approach",
            })
        
        if state_counts.get(EmotionalState.BORED, 0) >= 2:
            alerts.append({
                "type": "boredom",
                "severity": "medium",
                "message": "Student appears bored - consider increasing difficulty",
            })
        
        return {
            "trend": trend,
            "avg_engagement": round(avg_engagement, 2),
            "avg_confidence": round(avg_confidence, 2),
            "state_distribution": {k.value: v for k, v in state_counts.items()},
            "alerts": alerts,
            "window_size": len(analyses),
        }


# Singleton instance
_analyzer = None

def get_sentiment_analyzer() -> LearningSentimentAnalyzer:
    """Get or create the sentiment analyzer singleton."""
    global _analyzer
    if _analyzer is None:
        _analyzer = LearningSentimentAnalyzer()
    return _analyzer


def analyze_message(message: str, context: Optional[list[dict]] = None) -> SentimentAnalysis:
    """Convenience function to analyze a message."""
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze(message, context)


def analyze_conversation_trend(messages: list[dict], window_size: int = 5) -> dict:
    """Convenience function to analyze conversation trend."""
    analyzer = get_sentiment_analyzer()
    return analyzer.analyze_conversation_trend(messages, window_size)
