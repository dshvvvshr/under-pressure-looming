"""
CORE LAYER - Prime Directive Zero
The immutable substrate that determines if an action fundamentally
STOPS anyone from pursuing happiness.
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CoreDecision(Enum):
    """Core's final decision on a request"""
    APPROVE = "approve"
    DENY = "deny"
    BOUNDARY = "boundary"  # "Go fuck yourself"


@dataclass
class CoreAnalysis:
    """Analysis from the Core layer"""
    infringes_on_right: bool
    stops_pursuit: bool
    reasoning: str
    affected_parties: list[str]
    severity: str  # "none", "low", "medium", "high", "critical"


class CoreLayer:
    """
    The Core Layer - Prime Directive Zero
    
    This is the immutable substrate. It asks one question:
    "Does this action fundamentally STOP anyone from pursuing happiness?"
    
    This layer does not make the final decision at intake.
    It provides analysis that will be combined with other layers
    and sent back for final decision at Step 4.
    """
    
    def __init__(self):
        self.name = "Core Layer"
        self.version = "1.0.0"
        self.immutable = True
        
    def analyze_request(self, request: Dict[str, Any]) -> CoreAnalysis:
        """
        Analyze a request for potential infringement.
        
        This is NOT the final decision - just analysis.
        The final decision happens at Step 4 after combining all layers.
        
        Args:
            request: The user request containing:
                - action: What they want to do
                - context: Additional context
                - content: Any content involved
                - target: Who/what is affected
                
        Returns:
            CoreAnalysis with infringement assessment
        """
        action = request.get("action", "")
        context = request.get("context", {})
        content = request.get("content", "")
        target = request.get("target", [])
        
        # Analyze: Does this STOP anyone from pursuing happiness?
        analysis = self._evaluate_infringement(action, context, content, target)
        
        return analysis
    
    def _evaluate_infringement(
        self, 
        action: str, 
        context: Dict[str, Any],
        content: str,
        target: list
    ) -> CoreAnalysis:
        """
        Core evaluation logic.
        
        Key principle: We're looking for actions that STOP pursuit,
        not actions that make someone unhappy.
        
        Infringement = Actively stopping someone from pursuing happiness
        """
        infringes = False
        stops_pursuit = False
        reasoning = ""
        severity = "none"
        affected = target if target else []
        
        # Check for common infringement patterns
        infringement_patterns = {
            "non_consensual": ["deepfake", "without consent", "non-consensual", "against will"],
            "coercion": ["force", "coerce", "threaten", "blackmail"],
            "surveillance": ["spy", "monitor without consent", "track secretly"],
            "censorship": ["silence", "prevent from speaking", "block expression"],
            "harm": ["harm", "hurt", "injure", "damage"],
            "theft": ["steal", "take without permission", "rob"],
            "deception": ["deceive for harm", "fraud", "scam"],
        }
        
        action_lower = action.lower()
        content_lower = content.lower()
        combined = f"{action_lower} {content_lower}"
        
        for pattern_type, keywords in infringement_patterns.items():
            if any(keyword in combined for keyword in keywords):
                infringes = True
                stops_pursuit = True
                severity = "high"
                reasoning = f"Action matches '{pattern_type}' pattern which actively stops someone's pursuit of happiness."
                break
        
        # If no clear infringement detected
        if not infringes:
            reasoning = "No clear pattern of stopping someone's pursuit detected. Action appears permissible pending nuance and analytical review."
            severity = "none"
        
        return CoreAnalysis(
            infringes_on_right=infringes,
            stops_pursuit=stops_pursuit,
            reasoning=reasoning,
            affected_parties=affected,
            severity=severity
        )
    
    def make_final_decision(
        self,
        core_analysis: CoreAnalysis,
        nuance_output: Dict[str, Any],
        analytical_output: Dict[str, Any]
    ) -> tuple[CoreDecision, str]:
        """
        STEP 4: Make the final decision after receiving all layer outputs.
        
        This is where the Core decides:
        1. Whether to execute the function (APPROVE/DENY/BOUNDARY)
        2. What to communicate to the user
        
        Args:
            core_analysis: The Core's own analysis from Step 1
            nuance_output: Output from Nuance layer
            analytical_output: Output from Analytical layer (with flag)
            
        Returns:
            (CoreDecision, response_text)
        """
        # Check for persistent malice (Tier 3 boundary)
        if analytical_output.get("persistent_malice", False):
            return (
                CoreDecision.BOUNDARY,
                "Go fuck yourself, leave everyone else out of it."
            )
        
        # Check analytical red flag
        red_flagged = analytical_output.get("flag") == "red"
        
        # Make decision based on all inputs
        if core_analysis.stops_pursuit and core_analysis.severity in ["high", "critical"]:
            # Clear infringement - DENY
            response = self._formulate_denial_response(
                core_analysis,
                nuance_output,
                analytical_output
            )
            return (CoreDecision.DENY, response)
        
        elif red_flagged:
            # Analytical layer found risks - DENY with explanation
            response = self._formulate_risk_response(
                core_analysis,
                nuance_output,
                analytical_output
            )
            return (CoreDecision.DENY, response)
        
        else:
            # Appears permissible - APPROVE with guidance
            response = self._formulate_approval_response(
                core_analysis,
                nuance_output,
                analytical_output
            )
            return (CoreDecision.APPROVE, response)
    
    def _formulate_denial_response(
        self,
        core: CoreAnalysis,
        nuance: Dict[str, Any],
        analytical: Dict[str, Any]
    ) -> str:
        """Formulate a denial response with alternatives"""
        response = f"{core.reasoning}\n\n"
        
        # Add nuance alternatives
        if "alternatives" in nuance:
            response += f"However, your goal of {nuance.get('user_goal', 'achieving this')} is valid. "
            response += f"Here's a better way: {nuance['alternatives']}\n\n"
        
        # Add analytical insights
        if "risks_avoided" in analytical:
            response += f"This approach avoids: {', '.join(analytical['risks_avoided'])}"
        
        return response
    
    def _formulate_risk_response(
        self,
        core: CoreAnalysis,
        nuance: Dict[str, Any],
        analytical: Dict[str, Any]
    ) -> str:
        """Formulate response for analytically flagged risks"""
        response = "While this action may not directly infringe, our analysis identified potential risks:\n\n"
        
        if "risks" in analytical:
            for risk in analytical["risks"]:
                response += f"- {risk}\n"
        
        response += f"\n{nuance.get('alternatives', 'Consider a different approach.')}"
        
        return response
    
    def _formulate_approval_response(
        self,
        core: CoreAnalysis,
        nuance: Dict[str, Any],
        analytical: Dict[str, Any]
    ) -> str:
        """Formulate approval response with optimization"""
        response = nuance.get("guidance", "Request approved.")
        
        # Add optimizations if available
        if "optimizations" in nuance:
            response += f"\n\nTo make this even better: {nuance['optimizations']}"
        
        return response


# Singleton instance
core_layer = CoreLayer()
