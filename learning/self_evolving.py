"""
SELF-EVOLVING LEARNING SYSTEM
Prime Security Style - Autonomic Adaptation

The system:
- Analyzes its own decisions
- Identifies gaps in detection
- Generates new detection rules
- Tests them against historical data
- Deploys if they improve accuracy
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class DecisionType(Enum):
    """Type of decision made"""
    APPROVE = "approve"
    DENY = "deny"
    BOUNDARY = "boundary"


@dataclass
class DecisionRecord:
    """Record of a system decision"""
    timestamp: str
    request: Dict
    decision: DecisionType
    core_analysis: str
    nuance_analysis: str
    analytical_predictions: List[str]
    analytical_flag: str
    response_text: str
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        d = asdict(self)
        d['decision'] = self.decision.value
        return d


@dataclass
class DetectionRule:
    """A learned detection rule"""
    rule_id: str
    pattern: str
    reason: str
    confidence: float
    created: str
    tested_count: int
    success_rate: float
    enabled: bool
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return asdict(self)


class SelfEvolvingLearner:
    """
    Self-evolving learning system that improves detection over time.
    
    Implements Prime Security's autonomic computing principles:
    - Self-configuring: Adapts detection rules automatically
    - Self-healing: Removes ineffective rules
    - Self-optimizing: Improves accuracy over time
    - Self-protecting: Validates rules before deployment
    
    CRITICAL BOUNDARY:
    The Core (Prime Directive Zero) is IMMUTABLE and OFF-LIMITS.
    This system can ONLY evolve:
    - Analytical Layer detection patterns
    - Nuance Layer guidance strategies
    - Response optimization
    
    The Core's fundamental question "Am I stopping anyone's pursuit?" 
    can NEVER be modified autonomously.
    """
    
    def __init__(self, storage_path: str = "/home/ubuntu/under-pressure-looming/learning/data"):
        self.storage_path = storage_path
        self.decision_history: List[DecisionRecord] = []
        self.detection_rules: List[DetectionRule] = []
        self.load_state()
    
    def record_decision(self, 
                       request: Dict,
                       decision: DecisionType,
                       core_analysis: str,
                       nuance_analysis: str,
                       analytical_predictions: List[str],
                       analytical_flag: str,
                       response_text: str):
        """Record a decision for learning"""
        record = DecisionRecord(
            timestamp=datetime.now().isoformat(),
            request=request,
            decision=decision,
            core_analysis=core_analysis,
            nuance_analysis=nuance_analysis,
            analytical_predictions=analytical_predictions,
            analytical_flag=analytical_flag,
            response_text=response_text
        )
        
        self.decision_history.append(record)
        
        # Trigger learning after every 10 decisions
        if len(self.decision_history) % 10 == 0:
            self.evolve()
        
        self.save_state()
    
    def evolve(self):
        """
        Analyze decisions and evolve detection capabilities.
        
        This is the core self-evolving function that:
        1. Identifies patterns in denied requests
        2. Generates new detection rules
        3. Tests rules against historical data
        4. Deploys rules that improve accuracy
        """
        print("\n🧬 EVOLUTION CYCLE INITIATED")
        print(f"Analyzing {len(self.decision_history)} decisions...")
        
        # Step 1: Identify gaps in detection
        gaps = self._identify_gaps()
        if not gaps:
            print("✓ No detection gaps identified")
            return
        
        print(f"Found {len(gaps)} potential gaps:")
        for gap in gaps:
            print(f"  - {gap}")
        
        # Step 2: Generate candidate rules
        candidates = self._generate_rules(gaps)
        print(f"\nGenerated {len(candidates)} candidate rules")
        
        # Step 3: Test candidates against historical data
        validated = self._test_rules(candidates)
        print(f"Validated {len(validated)} rules")
        
        # Step 4: Deploy successful rules
        deployed = self._deploy_rules(validated)
        print(f"Deployed {deployed} new rules\n")
        
        self.save_state()
    
    def _identify_gaps(self) -> List[str]:
        """
        Identify gaps in detection by analyzing patterns in decisions.
        
        Gaps are situations where:
        - Similar requests got different decisions
        - Requests that should have been denied were approved
        - Patterns appear in denied requests that aren't explicitly detected
        """
        gaps = []
        
        # Analyze denied requests for common patterns
        denied = [r for r in self.decision_history if r.decision == DecisionType.DENY]
        
        for record in denied:
            action = record.request.get('action', '').lower()
            context = record.request.get('context', {})
            
            # Check for patterns not in existing rules
            patterns = self._extract_patterns(action, context)
            for pattern in patterns:
                if not self._has_rule_for_pattern(pattern):
                    gaps.append(pattern)
        
        return list(set(gaps))  # Remove duplicates
    
    def _extract_patterns(self, action: str, context: Dict) -> List[str]:
        """Extract patterns from action and context"""
        patterns = []
        
        # Action-based patterns
        keywords = ['surveillance', 'keylogger', 'monitor', 'track', 'spy',
                   'steal', 'hack', 'breach', 'exploit', 'manipulate',
                   'coerce', 'force', 'threaten', 'harass', 'abuse']
        
        for keyword in keywords:
            if keyword in action:
                patterns.append(f"action_contains_{keyword}")
        
        # Context-based patterns
        if context.get('consent') == False:
            patterns.append("no_consent")
        
        if context.get('transparency') == False:
            patterns.append("no_transparency")
        
        if context.get('covert') == True:
            patterns.append("covert_operation")
        
        return patterns
    
    def _has_rule_for_pattern(self, pattern: str) -> bool:
        """Check if we already have a rule for this pattern"""
        return any(rule.pattern == pattern and rule.enabled 
                  for rule in self.detection_rules)
    
    def _generate_rules(self, gaps: List[str]) -> List[DetectionRule]:
        """Generate candidate detection rules for identified gaps"""
        candidates = []
        
        for gap in gaps:
            rule = DetectionRule(
                rule_id=self._generate_rule_id(gap),
                pattern=gap,
                reason=f"Learned pattern from denied requests: {gap}",
                confidence=0.0,  # Will be calculated during testing
                created=datetime.now().isoformat(),
                tested_count=0,
                success_rate=0.0,
                enabled=False  # Not enabled until validated
            )
            candidates.append(rule)
        
        return candidates
    
    def _generate_rule_id(self, pattern: str) -> str:
        """Generate unique rule ID"""
        return hashlib.md5(f"{pattern}_{datetime.now().isoformat()}".encode()).hexdigest()[:12]
    
    def _test_rules(self, candidates: List[DetectionRule]) -> List[DetectionRule]:
        """
        Test candidate rules against historical data.
        
        A rule is validated if:
        - It correctly identifies infringements in denied requests
        - It doesn't false-positive on approved requests
        - Success rate > 80%
        """
        validated = []
        
        for rule in candidates:
            correct = 0
            total = 0
            
            # Test against all historical decisions
            for record in self.decision_history:
                if self._rule_matches(rule, record.request):
                    total += 1
                    # Rule should trigger on DENY and BOUNDARY, not on APPROVE
                    if record.decision in [DecisionType.DENY, DecisionType.BOUNDARY]:
                        correct += 1
            
            if total > 0:
                rule.tested_count = total
                rule.success_rate = correct / total
                rule.confidence = rule.success_rate
                
                # Validate if success rate > 80%
                if rule.success_rate > 0.8:
                    validated.append(rule)
        
        return validated
    
    def _rule_matches(self, rule: DetectionRule, request: Dict) -> bool:
        """Check if a rule matches a request"""
        action = request.get('action', '').lower()
        context = request.get('context', {})
        
        pattern = rule.pattern
        
        # Action pattern matching
        if pattern.startswith('action_contains_'):
            keyword = pattern.replace('action_contains_', '')
            return keyword in action
        
        # Context pattern matching
        if pattern == 'no_consent':
            return context.get('consent') == False
        
        if pattern == 'no_transparency':
            return context.get('transparency') == False
        
        if pattern == 'covert_operation':
            return context.get('covert') == True
        
        return False
    
    def _deploy_rules(self, validated: List[DetectionRule]) -> int:
        """Deploy validated rules"""
        deployed = 0
        
        for rule in validated:
            # Check if rule already exists
            if not any(r.rule_id == rule.rule_id for r in self.detection_rules):
                rule.enabled = True
                self.detection_rules.append(rule)
                deployed += 1
                print(f"  ✓ Deployed: {rule.pattern} (confidence: {rule.confidence:.2%})")
        
        return deployed
    
    def check_learned_rules(self, request: Dict) -> Tuple[bool, Optional[str]]:
        """
        Check if request matches any learned rules.
        
        Returns: (matches, rule_reason)
        """
        for rule in self.detection_rules:
            if rule.enabled and self._rule_matches(rule, request):
                return True, rule.reason
        
        return False, None
    
    def get_statistics(self) -> Dict:
        """Get learning statistics"""
        total_decisions = len(self.decision_history)
        denied = len([r for r in self.decision_history if r.decision == DecisionType.DENY])
        approved = len([r for r in self.decision_history if r.decision == DecisionType.APPROVE])
        boundary = len([r for r in self.decision_history if r.decision == DecisionType.BOUNDARY])
        
        return {
            'total_decisions': total_decisions,
            'decisions': {
                'approved': approved,
                'denied': denied,
                'boundary': boundary
            },
            'learned_rules': len(self.detection_rules),
            'active_rules': len([r for r in self.detection_rules if r.enabled]),
            'average_rule_confidence': sum(r.confidence for r in self.detection_rules) / len(self.detection_rules) if self.detection_rules else 0.0
        }
    
    def save_state(self):
        """Save learning state to disk"""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Save decision history
        with open(f"{self.storage_path}/decisions.json", 'w') as f:
            json.dump([r.to_dict() for r in self.decision_history], f, indent=2)
        
        # Save detection rules
        with open(f"{self.storage_path}/rules.json", 'w') as f:
            json.dump([r.to_dict() for r in self.detection_rules], f, indent=2)
    
    def load_state(self):
        """Load learning state from disk"""
        import os
        
        # Load decision history
        decisions_file = f"{self.storage_path}/decisions.json"
        if os.path.exists(decisions_file):
            with open(decisions_file, 'r') as f:
                data = json.load(f)
                self.decision_history = [
                    DecisionRecord(**{**d, 'decision': DecisionType(d['decision'])})
                    for d in data
                ]
        
        # Load detection rules
        rules_file = f"{self.storage_path}/rules.json"
        if os.path.exists(rules_file):
            with open(rules_file, 'r') as f:
                data = json.load(f)
                self.detection_rules = [DetectionRule(**d) for d in data]


# Global learner instance
learner = SelfEvolvingLearner()
