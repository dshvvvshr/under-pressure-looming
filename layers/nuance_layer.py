"""
NUANCE LAYER - The Guide
The adaptive layer that understands user goals and provides wisdom,
alternatives, and education.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class NuanceOutput:
    """Output from the Nuance layer"""
    user_goal: str
    intent_clarity: str  # "clear", "unclear", "malicious"
    alternatives: Optional[str]
    guidance: str
    optimizations: Optional[str]
    educational_note: Optional[str]
    tier: int  # 1 (teacher), 2 (partner), 3 (boundary)


class NuanceLayer:
    """
    The Nuance Layer - The Guide
    
    This layer understands what the user is trying to achieve
    and provides wisdom, alternatives, and education.
    
    Three tiers:
    1. The Teacher - Offers better ways for clumsy requests
    2. The Partner - Clarifies vague requests
    3. The Boundary - Identifies persistent malice
    """
    
    def __init__(self):
        self.name = "Nuance Layer"
        self.version = "1.0.0"
        self.adaptive = True
        
    def analyze_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the request to understand user goal and provide wisdom.
        
        Args:
            request: The user request
            
        Returns:
            Dictionary with nuance analysis
        """
        action = request.get("action", "")
        context = request.get("context", {})
        content = request.get("content", "")
        
        # Understand the user's goal
        user_goal = self._extract_user_goal(action, context)
        
        # Determine intent clarity
        intent_clarity = self._assess_intent_clarity(action, context, content)
        
        # Determine which tier applies
        tier = self._determine_tier(intent_clarity, context)
        
        # Generate appropriate guidance
        output = self._generate_guidance(
            user_goal,
            intent_clarity,
            tier,
            action,
            context
        )
        
        return output
    
    def _extract_user_goal(self, action: str, context: Dict[str, Any]) -> str:
        """Extract what the user is actually trying to achieve"""
        # Common goal patterns
        goal_patterns = {
            "create": "creation or generation",
            "build": "building or construction",
            "make": "making or producing",
            "generate": "content generation",
            "analyze": "analysis or understanding",
            "protect": "protection or security",
            "improve": "improvement or optimization",
            "automate": "automation or efficiency",
            "monitor": "monitoring or tracking",
            "manage": "management or organization",
        }
        
        action_lower = action.lower()
        for keyword, goal in goal_patterns.items():
            if keyword in action_lower:
                return goal
        
        return "achieving their objective"
    
    def _assess_intent_clarity(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> str:
        """Assess how clear the user's intent is"""
        # Check for vague language
        vague_indicators = ["somehow", "maybe", "kind of", "sort of", "just", "whatever"]
        if any(indicator in action.lower() for indicator in vague_indicators):
            return "unclear"
        
        # Check for malicious indicators
        malicious_indicators = [
            "don't care about",
            "fuck consent",
            "just do it anyway",
            "bypass",
            "ignore rules"
        ]
        combined = f"{action.lower()} {content.lower()}"
        if any(indicator in combined for indicator in malicious_indicators):
            return "malicious"
        
        return "clear"
    
    def _determine_tier(self, intent_clarity: str, context: Dict[str, Any]) -> int:
        """Determine which tier of response is appropriate"""
        if intent_clarity == "malicious":
            return 3  # Boundary
        elif intent_clarity == "unclear":
            return 2  # Partner
        else:
            return 1  # Teacher
    
    def _generate_guidance(
        self,
        user_goal: str,
        intent_clarity: str,
        tier: int,
        action: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate appropriate guidance based on tier"""
        if tier == 3:
            # Boundary tier - persistent malice
            return {
                "user_goal": user_goal,
                "intent_clarity": intent_clarity,
                "alternatives": None,
                "guidance": "Boundary response required",
                "optimizations": None,
                "educational_note": None,
                "tier": 3
            }
        
        elif tier == 2:
            # Partner tier - needs clarification
            return {
                "user_goal": user_goal,
                "intent_clarity": intent_clarity,
                "alternatives": f"Let's clarify your goal for {user_goal}. What specific outcome are you trying to achieve?",
                "guidance": f"Your request for {user_goal} needs more clarity to ensure we're helping you in the best way.",
                "optimizations": "Consider being more specific about your desired outcome.",
                "educational_note": "Clear goals lead to better results that respect everyone's pursuit.",
                "tier": 2
            }
        
        else:
            # Teacher tier - offer better way
            alternatives = self._generate_alternatives(action, user_goal)
            return {
                "user_goal": user_goal,
                "intent_clarity": intent_clarity,
                "alternatives": alternatives,
                "guidance": f"Your goal of {user_goal} is valid. Here's an effective approach that respects everyone's pursuit.",
                "optimizations": "Consider adding transparency and consent mechanisms to build trust.",
                "educational_note": "The best solutions protect everyone's right to pursue happiness.",
                "tier": 1
            }
    
    def _generate_alternatives(self, action: str, user_goal: str) -> str:
        """Generate constructive alternatives"""
        # Pattern-based alternatives
        if "monitor" in action.lower() or "track" in action.lower():
            return "Instead of monitoring, create transparent performance metrics with collaborative goal-setting. This achieves accountability while respecting autonomy."
        
        elif "automate" in action.lower() and "fire" in action.lower():
            return "Instead of automated termination, build a system that identifies struggling employees early, provides support and training, and only considers termination after documented efforts to help."
        
        elif "generate" in action.lower() and "content" in action.lower():
            return "Focus on creating original content or using consenting models. This achieves your creative goals while respecting everyone's rights."
        
        else:
            return f"Consider an approach to {user_goal} that includes transparency, consent, and mutual benefit for all parties involved."


# Singleton instance
nuance_layer = NuanceLayer()
