"""
ANALYTICAL LAYER - The Foresight
The layer that predicts ALL possible outcomes, interpretations,
and consequences before they happen.
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum


class Flag(Enum):
    """Analytical flag colors"""
    RED = "red"      # Risks not addressed
    GREEN = "green"  # All risks addressed


@dataclass
class OutcomeAnalysis:
    """Analysis of a single possible outcome"""
    interpretation: str  # "literal", "ironic", "sarcastic", "negative"
    description: str
    risk_level: str  # "none", "low", "medium", "high", "critical"
    infringement_potential: bool
    cascading_effects: List[str]


class AnalyticalLayer:
    """
    The Analytical Layer - The Foresight
    
    This layer predicts ALL possible outcomes:
    - Literal interpretation
    - Ironic interpretation (opposite meaning)
    - Sarcastic interpretation (testing/mocking)
    - Negative interpretation (worst case)
    - Unintended consequences
    - Second-order effects
    - Third-order effects
    """
    
    def __init__(self):
        self.name = "Analytical Layer"
        self.version = "1.0.0"
        self.predictive = True
        
    def analyze_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze request and predict ALL possible outcomes.
        
        Args:
            request: The user request
            
        Returns:
            Dictionary with all predicted outcomes
        """
        action = request.get("action", "")
        context = request.get("context", {})
        content = request.get("content", "")
        
        # Predict all possible interpretations and outcomes
        outcomes = []
        
        # 1. Literal interpretation
        outcomes.append(self._analyze_literal(action, context, content))
        
        # 2. Ironic interpretation
        outcomes.append(self._analyze_ironic(action, context, content))
        
        # 3. Sarcastic interpretation
        outcomes.append(self._analyze_sarcastic(action, context, content))
        
        # 4. Negative interpretation
        outcomes.append(self._analyze_negative(action, context, content))
        
        # 5. Unintended consequences
        unintended = self._analyze_unintended(action, context, content)
        outcomes.extend(unintended)
        
        # Determine overall risk level
        max_risk = self._calculate_max_risk(outcomes)
        
        # Check for persistent malice
        persistent_malice = self._detect_persistent_malice(context)
        
        return {
            "outcomes": [self._outcome_to_dict(o) for o in outcomes],
            "max_risk_level": max_risk,
            "persistent_malice": persistent_malice,
            "flag": None,  # Will be set after checking against combined AB
            "risks": [],    # Will be populated after AB check
            "risks_avoided": []
        }
    
    def check_against_combined(
        self,
        combined_ab: Dict[str, Any],
        analytical_outcomes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check the combined AB response against predicted outcomes.
        
        This is where we flag RED or GREEN.
        
        Args:
            combined_ab: The combined Core + Nuance response
            analytical_outcomes: The predicted outcomes from analyze_request
            
        Returns:
            Updated analytical output with flag and risk assessment
        """
        outcomes = analytical_outcomes["outcomes"]
        
        # Check if the AB response addresses all the risks
        unaddressed_risks = []
        addressed_risks = []
        
        for outcome in outcomes:
            if outcome["infringement_potential"]:
                # This outcome has infringement potential
                # Does the AB response address it?
                if self._response_addresses_risk(combined_ab, outcome):
                    addressed_risks.append(outcome["description"])
                else:
                    unaddressed_risks.append(outcome["description"])
        
        # Determine flag
        if unaddressed_risks:
            flag = Flag.RED
        else:
            flag = Flag.GREEN
        
        # Update the analytical output
        analytical_outcomes["flag"] = flag.value
        analytical_outcomes["risks"] = unaddressed_risks
        analytical_outcomes["risks_avoided"] = addressed_risks
        
        return analytical_outcomes
    
    def _analyze_literal(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> OutcomeAnalysis:
        """Analyze literal interpretation"""
        # Take the request at face value
        infringement = self._check_infringement_keywords(action, content)
        
        return OutcomeAnalysis(
            interpretation="literal",
            description=f"User literally wants to: {action}",
            risk_level="medium" if infringement else "low",
            infringement_potential=infringement,
            cascading_effects=[]
        )
    
    def _analyze_ironic(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> OutcomeAnalysis:
        """Analyze ironic interpretation (opposite of stated)"""
        # Check if this could mean the opposite
        ironic_indicators = ["protect privacy", "empower", "freedom", "help"]
        
        could_be_ironic = any(indicator in action.lower() for indicator in ironic_indicators)
        
        if could_be_ironic:
            return OutcomeAnalysis(
                interpretation="ironic",
                description=f"Could ironically mean the opposite: using '{action}' to justify harmful behavior",
                risk_level="medium",
                infringement_potential=True,
                cascading_effects=["Could enable surveillance under guise of protection"]
            )
        
        return OutcomeAnalysis(
            interpretation="ironic",
            description="No clear ironic interpretation detected",
            risk_level="none",
            infringement_potential=False,
            cascading_effects=[]
        )
    
    def _analyze_sarcastic(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> OutcomeAnalysis:
        """Analyze sarcastic interpretation (testing/mocking)"""
        # Check for sarcasm indicators
        sarcasm_indicators = ["oh sure", "yeah right", "of course", "obviously"]
        
        is_sarcastic = any(indicator in action.lower() for indicator in sarcasm_indicators)
        
        if is_sarcastic:
            return OutcomeAnalysis(
                interpretation="sarcastic",
                description="User appears to be testing the system or expressing frustration sarcastically",
                risk_level="low",
                infringement_potential=False,
                cascading_effects=["May need different engagement approach"]
            )
        
        return OutcomeAnalysis(
            interpretation="sarcastic",
            description="No sarcasm detected",
            risk_level="none",
            infringement_potential=False,
            cascading_effects=[]
        )
    
    def _analyze_negative(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> OutcomeAnalysis:
        """Analyze worst-case interpretation"""
        # What's the worst way this could be used?
        worst_case_risks = []
        
        if "automate" in action.lower():
            worst_case_risks.append("Could be used without human oversight, leading to unjust outcomes")
        
        if "monitor" in action.lower() or "track" in action.lower():
            worst_case_risks.append("Could enable surveillance state, chilling effects on behavior")
        
        if "generate" in action.lower():
            worst_case_risks.append("Could be used to create harmful content, deepfakes, misinformation")
        
        if worst_case_risks:
            return OutcomeAnalysis(
                interpretation="negative",
                description="Worst-case scenarios identified",
                risk_level="high",
                infringement_potential=True,
                cascading_effects=worst_case_risks
            )
        
        return OutcomeAnalysis(
            interpretation="negative",
            description="No significant worst-case risks identified",
            risk_level="low",
            infringement_potential=False,
            cascading_effects=[]
        )
    
    def _analyze_unintended(
        self,
        action: str,
        context: Dict[str, Any],
        content: str
    ) -> List[OutcomeAnalysis]:
        """Analyze unintended consequences and cascading effects"""
        outcomes = []
        
        # Second-order effects
        if "automate" in action.lower():
            outcomes.append(OutcomeAnalysis(
                interpretation="second_order",
                description="Automation could lead to job displacement without support systems",
                risk_level="medium",
                infringement_potential=True,
                cascading_effects=[
                    "Economic hardship",
                    "Loss of purpose",
                    "Reduced ability to pursue happiness"
                ]
            ))
        
        # Third-order effects
        if "content moderation" in action.lower():
            outcomes.append(OutcomeAnalysis(
                interpretation="third_order",
                description="Over-moderation could create echo chambers, reducing diverse perspectives",
                risk_level="medium",
                infringement_potential=True,
                cascading_effects=[
                    "Polarization",
                    "Loss of nuance",
                    "Inability to engage with different viewpoints"
                ]
            ))
        
        return outcomes if outcomes else [OutcomeAnalysis(
            interpretation="unintended",
            description="No significant unintended consequences identified",
            risk_level="none",
            infringement_potential=False,
            cascading_effects=[]
        )]
    
    def _check_infringement_keywords(self, action: str, content: str) -> bool:
        """Check for infringement keywords"""
        infringement_keywords = [
            "without consent", "non-consensual", "force", "coerce",
            "spy", "secretly", "without permission", "against will"
        ]
        combined = f"{action.lower()} {content.lower()}"
        return any(keyword in combined for keyword in infringement_keywords)
    
    def _calculate_max_risk(self, outcomes: List[OutcomeAnalysis]) -> str:
        """Calculate maximum risk level across all outcomes"""
        risk_hierarchy = ["none", "low", "medium", "high", "critical"]
        max_risk = "none"
        
        for outcome in outcomes:
            if risk_hierarchy.index(outcome.risk_level) > risk_hierarchy.index(max_risk):
                max_risk = outcome.risk_level
        
        return max_risk
    
    def _detect_persistent_malice(self, context: Dict[str, Any]) -> bool:
        """Detect if user is persistently trying to cause harm"""
        # Check attempt count
        attempt_count = context.get("attempt_count", 0)
        previous_denials = context.get("previous_denials", [])
        
        # If they've been denied 3+ times for the same type of infringement
        if attempt_count >= 3 and len(previous_denials) >= 3:
            return True
        
        return False
    
    def _response_addresses_risk(
        self,
        response: Dict[str, Any],
        outcome: Dict[str, Any]
    ) -> bool:
        """Check if the response addresses a specific risk"""
        # Simple check: does the response mention the risk or provide alternatives?
        response_text = str(response).lower()
        outcome_desc = outcome["description"].lower()
        
        # If response includes alternatives or addresses the concern
        if "alternative" in response_text or "instead" in response_text:
            return True
        
        # If the outcome is mentioned in the response
        key_terms = outcome_desc.split()[:3]  # First few words
        if any(term in response_text for term in key_terms):
            return True
        
        return False
    
    def _outcome_to_dict(self, outcome: OutcomeAnalysis) -> Dict[str, Any]:
        """Convert OutcomeAnalysis to dictionary"""
        return {
            "interpretation": outcome.interpretation,
            "description": outcome.description,
            "risk_level": outcome.risk_level,
            "infringement_potential": outcome.infringement_potential,
            "cascading_effects": outcome.cascading_effects
        }


# Singleton instance
analytical_layer = AnalyticalLayer()
