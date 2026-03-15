"""
Emotion-Aware Teaching System

An AI teaching assistant that detects and responds to student emotions.
Creates emotionally supportive learning experiences.

Research Applications:
- Emotional intelligence in education
- Affective computing
- Student well-being
- Engagement optimization
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime
import re


class EmotionalState(Enum):
    """Detected emotional states."""
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"
    ANXIOUS = "anxious"
    BORED = "bored"
    CURIOUS = "curious"
    EXCITED = "excited"
    SATISFIED = "satisfied"
    CONFIDENT = "confident"
    NEUTRAL = "neutral"


class SupportStrategy(Enum):
    """Strategies for emotional support."""
    ENCOURAGE = "encourage"           # Provide encouragement
    SIMPLIFY = "simplify"            # Break down complexity
    DIVERT = "divert"                # Brief distraction/reset
    VALIDATE = "validate"            # Acknowledge feelings
    CHALLENGE = "challenge"          # Offer challenge to re-engage
    PRAISE = "praise"                # Celebrate progress
    PAUSE = "pause"                  # Suggest break
    GUIDE = "guide"                  # Step-by-step guidance


@dataclass
class EmotionalContext:
    """Context for emotional detection."""
    message: str
    timestamp: datetime
    recent_performance: float  # 0-1
    consecutive_errors: int
    time_since_last_success: int  # minutes
    session_duration: int  # minutes
    previous_emotions: List[EmotionalState]


@dataclass
class EmotionAnalysis:
    """Result of emotion analysis."""
    primary_emotion: EmotionalState
    secondary_emotions: List[EmotionalState]
    confidence: float
    intensity: float  # 0-1
    triggers: List[str]
    suggested_response: str
    support_strategy: SupportStrategy


class EmotionAwareTeachingSystem:
    """
    AI teaching assistant with emotional intelligence.
    
    Features:
    - Multi-source emotion detection
    - Context-aware responses
    - Personalized emotional support
    - Long-term emotional tracking
    """
    
    # Emotion keywords and patterns
    EMOTION_PATTERNS = {
        EmotionalState.FRUSTRATED: [
            "stuck", "can't figure", "don't understand", "annoying", "frustrat",
            "why isn't this working", "this is stupid", "waste of time",
            "gives up", "quitting", "giving up", "hopeless",
        ],
        EmotionalState.CONFUSED: [
            "confused", "don't get it", "what does this mean", "unclear",
            "lost", "not sure", "how does this work", "???", "what?",
            "i don't understand", "explain again", "make no sense",
        ],
        EmotionalState.ANXIOUS: [
            "worried", "nervous", "stressed", "anxious", "panic",
            "overwhelmed", "can't handle", "too much", "pressure",
            "deadline", "urgent", "help please", "i'm struggling",
        ],
        EmotionalState.BORED: [
            "boring", "tedious", "repetitive", "already know this",
            "too slow", "when will this end", "not interested",
            "whatever", "pointless", "why do i need this",
        ],
        EmotionalState.CURIOUS: [
            "interesting", "how does", "what if", "why does",
            "curious", "fascinating", "tell me more", "can we",
            "i wonder", "is it possible", "what about",
        ],
        EmotionalState.EXCITED: [
            "awesome", "amazing", "cool", "exciting", "wow",
            "love this", "can't wait", "so fun", "brilliant",
            "fantastic", "this is great", "i did it!", "it works!",
        ],
        EmotionalState.SATISFIED: [
            "got it", "understand now", "makes sense", "clear",
            "thank you", "helpful", "that helps", "i see",
            "now i get it", "perfect", "exactly", "right",
        ],
        EmotionalState.CONFIDENT: [
            "easy", "simple", "no problem", "i can do this",
            "confident", "sure", "definitely", "obviously",
            "i know this", "mastered", "ready for more",
        ],
    }
    
    def __init__(self):
        self.emotion_history: Dict[int, List[EmotionAnalysis]] = {}
        self.strategy_success: Dict[SupportStrategy, List[float]] = {
            strategy: [] for strategy in SupportStrategy
        }
    
    def analyze_emotion(
        self,
        context: EmotionalContext,
    ) -> EmotionAnalysis:
        """
        Analyze student emotion from multiple indicators.
        """
        scores: Dict[EmotionalState, float] = {e: 0.0 for e in EmotionalState}
        triggers = []
        
        # 1. Text analysis (40%)
        text_scores, text_triggers = self._analyze_text(context.message)
        for emotion, score in text_scores.items():
            scores[emotion] += score * 0.4
        triggers.extend(text_triggers)
        
        # 2. Performance indicators (30%)
        perf_scores = self._analyze_performance(context)
        for emotion, score in perf_scores.items():
            scores[emotion] += score * 0.3
        
        # 3. Temporal patterns (20%)
        temporal_scores = self._analyze_temporal(context)
        for emotion, score in temporal_scores.items():
            scores[emotion] += score * 0.2
        
        # 4. History context (10%)
        if context.previous_emotions:
            recent = context.previous_emotions[-3:]
            for emotion in recent:
                scores[emotion] += 0.1
        
        # Determine primary and secondary emotions
        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary_emotion = sorted_emotions[0][0]
        primary_score = sorted_emotions[0][1]
        
        # Get secondary emotions (above threshold)
        secondary = [e for e, s in sorted_emotions[1:] if s > 0.2]
        
        # Calculate confidence and intensity
        confidence = min(1.0, primary_score)
        intensity = min(1.0, primary_score * 1.5)
        
        # Determine support strategy
        strategy = self._select_strategy(
            primary_emotion, context, intensity
        )
        
        # Generate response
        response = self._generate_response(
            primary_emotion, strategy, context, intensity
        )
        
        return EmotionAnalysis(
            primary_emotion=primary_emotion,
            secondary_emotions=secondary[:2],
            confidence=round(confidence, 2),
            intensity=round(intensity, 2),
            triggers=triggers[:3],
            suggested_response=response,
            support_strategy=strategy,
        )
    
    def _analyze_text(self, message: str) -> tuple:
        """Analyze text for emotional content."""
        scores: Dict[EmotionalState, float] = {}
        triggers = []
        message_lower = message.lower()
        
        for emotion, patterns in self.EMOTION_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if pattern in message_lower:
                    score += 0.3
                    triggers.append(pattern)
            scores[emotion] = min(1.0, score)
        
        # Special patterns
        if re.search(r'[!]{2,}', message):  # Multiple exclamation
            scores[EmotionalState.EXCITED] = scores.get(EmotionalState.EXCITED, 0) + 0.2
        
        if re.search(r'[?]{2,}', message):  # Multiple question marks
            scores[EmotionalState.CONFUSED] = scores.get(EmotionalState.CONFUSED, 0) + 0.2
            scores[EmotionalState.ANXIOUS] = scores.get(EmotionalState.ANXIOUS, 0) + 0.1
        
        # Caps lock (shouting)
        if message.isupper() and len(message) > 5:
            scores[EmotionalState.FRUSTRATED] = scores.get(EmotionalState.FRUSTRATED, 0) + 0.3
        
        return scores, list(set(triggers))
    
    def _analyze_performance(self, context: EmotionalContext) -> Dict[EmotionalState, float]:
        """Analyze performance indicators."""
        scores = {}
        
        # Low performance + errors = frustration/anxiety
        if context.recent_performance < 0.3:
            if context.consecutive_errors >= 3:
                scores[EmotionalState.FRUSTRATED] = 0.6
                scores[EmotionalState.ANXIOUS] = 0.4
            else:
                scores[EmotionalState.CONFUSED] = 0.5
        
        # High performance = confidence/satisfaction
        elif context.recent_performance > 0.8:
            if context.consecutive_errors == 0:
                scores[EmotionalState.CONFIDENT] = 0.7
            else:
                scores[EmotionalState.SATISFIED] = 0.6
        
        # Long time without success
        if context.time_since_last_success > 10:
            scores[EmotionalState.FRUSTRATED] = scores.get(EmotionalState.FRUSTRATED, 0) + 0.3
            scores[EmotionalState.ANXIOUS] = scores.get(EmotionalState.ANXIOUS, 0) + 0.2
        
        return scores
    
    def _analyze_temporal(self, context: EmotionalContext) -> Dict[EmotionalState, float]:
        """Analyze temporal patterns."""
        scores = {}
        
        # Long session = potential fatigue
        if context.session_duration > 45:
            scores[EmotionalState.BORED] = 0.3
            scores[EmotionalState.FRUSTRATED] = 0.2
        
        # Very long session = overwhelm
        if context.session_duration > 90:
            scores[EmotionalState.ANXIOUS] = 0.4
            scores[EmotionalState.FRUSTRATED] = 0.3
        
        return scores
    
    def _select_strategy(
        self,
        emotion: EmotionalState,
        context: EmotionalContext,
        intensity: float,
    ) -> SupportStrategy:
        """Select support strategy based on emotion."""
        strategies = {
            EmotionalState.FRUSTRATED: SupportStrategy.SIMPLIFY,
            EmotionalState.CONFUSED: SupportStrategy.GUIDE,
            EmotionalState.ANXIOUS: SupportStrategy.VALIDATE,
            EmotionalState.BORED: SupportStrategy.CHALLENGE,
            EmotionalState.CURIOUS: SupportStrategy.GUIDE,
            EmotionalState.EXCITED: SupportStrategy.PRAISE,
            EmotionalState.SATISFIED: SupportStrategy.ENCOURAGE,
            EmotionalState.CONFIDENT: SupportStrategy.CHALLENGE,
            EmotionalState.NEUTRAL: SupportStrategy.GUIDE,
        }
        
        base_strategy = strategies.get(emotion, SupportStrategy.GUIDE)
        
        # Override for high intensity negative emotions
        if intensity > 0.8 and emotion in [EmotionalState.FRUSTRATED, EmotionalState.ANXIOUS]:
            return SupportStrategy.PAUSE
        
        # Override for very long sessions
        if context.session_duration > 60 and emotion in [EmotionalState.BORED, EmotionalState.FRUSTRATED]:
            return SupportStrategy.DIVERT
        
        return base_strategy
    
    def _generate_response(
        self,
        emotion: EmotionalState,
        strategy: SupportStrategy,
        context: EmotionalContext,
        intensity: float,
    ) -> str:
        """Generate emotionally appropriate response."""
        responses = {
            (EmotionalState.FRUSTRATED, SupportStrategy.SIMPLIFY): [
                "I can see this is challenging. Let's break it down into smaller, manageable steps.",
                "This part can be tricky. Let me show you a simpler way to approach it.",
            ],
            (EmotionalState.FRUSTRATED, SupportStrategy.PAUSE): [
                "It looks like you're working hard on this. Would you like to take a quick 5-minute break and come back with fresh eyes?",
                "Sometimes stepping away for a moment helps. Shall we pause here?",
            ],
            (EmotionalState.CONFUSED, SupportStrategy.GUIDE): [
                "Let me guide you through this step by step. First, let's look at...",
                "I can help clarify this. The key concept here is...",
            ],
            (EmotionalState.ANXIOUS, SupportStrategy.VALIDATE): [
                "It's completely normal to feel that way when learning something new. You're making progress, even if it doesn't feel like it.",
                "I understand this feels overwhelming. Remember, every expert was once a beginner. Let's tackle this together.",
            ],
            (EmotionalState.ANXIOUS, SupportStrategy.PAUSE): [
                "You seem under pressure. It's okay to take a breath. Learning isn't a race.",
                "Let's pause here. Your well-being is more important than pushing through right now.",
            ],
            (EmotionalState.BORED, SupportStrategy.CHALLENGE): [
                "Since you've mastered this, let's explore something more interesting...",
                "Ready for a challenge? Let's see how we can apply this in a creative way.",
            ],
            (EmotionalState.CURIOUS, SupportStrategy.GUIDE): [
                "Great question! Let's explore this together...",
                "I love your curiosity! Here's how this works...",
            ],
            (EmotionalState.EXCITED, SupportStrategy.PRAISE): [
                "That's the spirit! Your enthusiasm is wonderful! 🎉",
                "Excellent! I can feel your excitement - it's contagious!",
            ],
            (EmotionalState.SATISFIED, SupportStrategy.ENCOURAGE): [
                "Perfect! You're really getting this. Ready for the next step?",
                "Great understanding! Let's build on this success...",
            ],
            (EmotionalState.CONFIDENT, SupportStrategy.CHALLENGE): [
                "I can see you're confident with this! Here's an interesting extension...",
                "Since this feels easy to you, let's try something that will stretch your skills...",
            ],
        }
        
        key = (emotion, strategy)
        if key in responses:
            import random
            return random.choice(responses[key])
        
        return "I'm here to help. What would be most useful for you right now?"
    
    def track_emotion_session(
        self,
        student_id: int,
        analyses: List[EmotionAnalysis],
    ) -> Dict:
        """Track emotional journey through a session."""
        self.emotion_history[student_id] = analyses
        
        # Calculate metrics
        emotions = [a.primary_emotion for a in analyses]
        emotion_counts = {}
        for e in emotions:
            emotion_counts[e.value] = emotion_counts.get(e.value, 0) + 1
        
        # Identify emotional transitions
        transitions = []
        for i in range(1, len(analyses)):
            prev = analyses[i-1].primary_emotion
            curr = analyses[i].primary_emotion
            if prev != curr:
                transitions.append(f"{prev.value} → {curr.value}")
        
        # Determine overall session emotional arc
        if len(analyses) >= 2:
            start_emotion = analyses[0].primary_emotion
            end_emotion = analyses[-1].primary_emotion
            
            # Positive arc: negative → positive
            negative = [EmotionalState.FRUSTRATED, EmotionalState.ANXIOUS, EmotionalState.BORED]
            positive = [EmotionalState.SATISFIED, EmotionalState.CONFIDENT, EmotionalState.EXCITED]
            
            if start_emotion in negative and end_emotion in positive:
                arc = "positive_transformation"
            elif start_emotion in positive and end_emotion in negative:
                arc = "concerning_decline"
            elif start_emotion == end_emotion:
                arc = "stable"
            else:
                arc = "mixed"
        else:
            arc = "insufficient_data"
        
        return {
            "emotion_distribution": emotion_counts,
            "dominant_emotion": max(emotion_counts.items(), key=lambda x: x[1])[0] if emotion_counts else None,
            "emotional_transitions": transitions,
            "session_arc": arc,
            "emotional_stability": len(transitions) / len(analyses) if analyses else 0,
            "requires_follow_up": arc == "concerning_decline",
        }


def analyze_student_emotion(
    message: str,
    student_id: int,
    recent_performance: float = 0.5,
    consecutive_errors: int = 0,
    session_minutes: int = 0,
) -> Dict:
    """
    Main API-facing function for emotion analysis.
    
    Args:
        message: Student's message
        student_id: Student ID
        recent_performance: Recent success rate (0-1)
        consecutive_errors: Number of consecutive errors
        session_minutes: Session duration
    
    Returns:
        Emotion analysis results
    """
    system = EmotionAwareTeachingSystem()
    
    context = EmotionalContext(
        message=message,
        timestamp=datetime.utcnow(),
        recent_performance=recent_performance,
        consecutive_errors=consecutive_errors,
        time_since_last_success=max(0, session_minutes - 5),
        session_duration=session_minutes,
        previous_emotions=[],
    )
    
    analysis = system.analyze_emotion(context)
    
    return {
        "primary_emotion": analysis.primary_emotion.value,
        "secondary_emotions": [e.value for e in analysis.secondary_emotions],
        "confidence": analysis.confidence,
        "intensity": analysis.intensity,
        "triggers": analysis.triggers,
        "suggested_response": analysis.suggested_response,
        "support_strategy": analysis.support_strategy.value,
        "requires_support": analysis.primary_emotion in [
            EmotionalState.FRUSTRATED, EmotionalState.ANXIOUS, EmotionalState.BORED
        ],
    }
