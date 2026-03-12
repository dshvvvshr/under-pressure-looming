"""
AGENT COORDINATOR
Coordinates all agents (Grok, Gtopps, Gem) with the core system.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from typing import Dict, Any, Optional
from core.system import system, SystemResponse
from layers.core_layer import CoreDecision


class AgentCoordinator:
    """
    Coordinates all agents with the core three-layer system.
    
    Flow:
    1. Request comes in
    2. Core system processes through 3 layers
    3. If content-related, route to Grok for evaluation
    4. Gtopps refines the response
    5. Gem contributes (when implemented)
    6. Final response sent to user
    """
    
    def __init__(self):
        self.name = "Agent Coordinator"
        self.system = system
        self.agents = {}
        
        # Try to initialize agents (may fail if API keys not set)
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all available agents"""
        # Grok
        try:
            from agents.grok_agent import GrokAgent
            self.agents['grok'] = GrokAgent()
            print("✓ Grok agent initialized")
        except Exception as e:
            print(f"⚠ Grok agent not available: {e}")
            self.agents['grok'] = None
        
        # Gtopps
        try:
            from agents.gtopps_agent import GtoppsAgent
            self.agents['gtopps'] = GtoppsAgent()
            print("✓ Gtopps agent initialized")
        except Exception as e:
            print(f"⚠ Gtopps agent not available: {e}")
            self.agents['gtopps'] = None
        
        # Gem (placeholder)
        from agents.gem_agent import GemAgent
        self.agents['gem'] = GemAgent()
        print("✓ Gem agent placeholder initialized")
    
    def process_request(
        self,
        request: Dict[str, Any],
        use_agents: bool = True
    ) -> Dict[str, Any]:
        """
        Process request through core system and agents.
        
        Args:
            request: User request
            use_agents: Whether to use AI agents (requires API keys)
            
        Returns:
            Complete response with agent contributions
        """
        # Step 1: Core system processing
        print("\n" + "="*80)
        print("AGENT COORDINATOR: Processing request")
        print("="*80)
        
        core_response = self.system.process_request(request)
        
        # Step 2: Determine if agents should be involved
        if not use_agents or not self._should_use_agents(request, core_response):
            return {
                "core_response": core_response,
                "agent_contributions": {},
                "final_response": core_response.response_text
            }
        
        # Step 3: Route to appropriate agents
        agent_contributions = {}
        
        # Grok evaluation (for content requests)
        if self._is_content_request(request) and self.agents.get('grok'):
            print("\n→ Routing to Grok for content evaluation...")
            try:
                grok_eval = self.agents['grok'].evaluate_content(request)
                agent_contributions['grok'] = grok_eval
            except Exception as e:
                print(f"⚠ Grok evaluation failed: {e}")
        
        # Gtopps refinement
        if self.agents.get('gtopps'):
            print("\n→ Routing to Gtopps for refinement...")
            try:
                if 'grok' in agent_contributions:
                    # Collaborate with Grok
                    refined = self.agents['gtopps'].collaborate_with_grok(
                        agent_contributions['grok']['evaluation'],
                        request.get('context', {})
                    )
                elif core_response.decision == CoreDecision.DENY:
                    # Suggest alternatives for denied requests
                    refined = self.agents['gtopps'].suggest_alternatives(
                        request.get('action', ''),
                        core_response.response_text
                    )
                else:
                    # General refinement
                    refined = core_response.response_text
                
                agent_contributions['gtopps'] = {
                    "refined_response": refined
                }
            except Exception as e:
                print(f"⚠ Gtopps refinement failed: {e}")
        
        # Gem contribution (placeholder)
        if self.agents.get('gem'):
            gem_contribution = self.agents['gem'].process(request)
            agent_contributions['gem'] = gem_contribution
        
        # Step 4: Combine into final response
        final_response = self._combine_responses(
            core_response,
            agent_contributions
        )
        
        return {
            "core_response": core_response,
            "agent_contributions": agent_contributions,
            "final_response": final_response
        }
    
    def _should_use_agents(
        self,
        request: Dict[str, Any],
        core_response: SystemResponse
    ) -> bool:
        """Determine if agents should be involved"""
        # Use agents for:
        # - Content requests
        # - Denied requests (need alternatives)
        # - Complex requests
        
        if self._is_content_request(request):
            return True
        
        if core_response.decision == CoreDecision.DENY:
            return True
        
        return False
    
    def _is_content_request(self, request: Dict[str, Any]) -> bool:
        """Check if this is a content-related request"""
        content_keywords = [
            "generate", "create", "make", "produce",
            "content", "image", "video", "text",
            "deepfake", "porn", "adult"
        ]
        
        action = request.get('action', '').lower()
        content = request.get('content', '').lower()
        combined = f"{action} {content}"
        
        return any(keyword in combined for keyword in content_keywords)
    
    def _combine_responses(
        self,
        core_response: SystemResponse,
        agent_contributions: Dict[str, Any]
    ) -> str:
        """Combine core and agent responses into final response"""
        # If Gtopps refined the response, use that
        if 'gtopps' in agent_contributions:
            return agent_contributions['gtopps'].get(
                'refined_response',
                core_response.response_text
            )
        
        # Otherwise use core response
        return core_response.response_text


# Singleton instance
coordinator = AgentCoordinator()


def main():
    """Test the agent coordinator"""
    
    print("\n" + "="*80)
    print("AGENT COORDINATOR TEST")
    print("="*80)
    
    # Test without agents (no API keys needed)
    test_request = {
        "action": "Create a user account",
        "context": {},
        "content": "Standard account creation",
        "target": ["new_user"]
    }
    
    result = coordinator.process_request(test_request, use_agents=False)
    
    print("\n" + "="*80)
    print("FINAL RESULT")
    print("="*80)
    print(f"\nDecision: {result['core_response'].decision.value}")
    print(f"Response: {result['final_response']}")
    print(f"Function Executed: {result['core_response'].function_executed}")


if __name__ == "__main__":
    main()
