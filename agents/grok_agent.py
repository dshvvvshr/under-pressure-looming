"""
GROK AGENT - Content Moderation and User Engagement
The front-line agent that handles content moderation, especially
for adult content requests, and engages with users about boundaries.
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI


class GrokAgent:
    """
    Grok - The Content Moderator
    
    Role: Front-line content moderation and user engagement
    - Handles permissible adult content requests
    - Engages with users about boundaries
    - Educates about consent and rights
    - Autonomous decision-making within Prime Directive Zero
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Grok"
        self.role = "Content Moderator & User Engagement"
        
        # Initialize Grok client (OpenAI-compatible API)
        api_key = api_key or os.getenv("XAI_API_KEY")
        if not api_key:
            raise ValueError("XAI_API_KEY environment variable not set")
        
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
        
        self.model = "grok-beta"  # or "grok-4" when available
        
    def evaluate_content(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate content request for moderation.
        
        Grok does whatever Grok needs to do - no parameters set by us.
        
        Args:
            request: The content request
            
        Returns:
            Grok's evaluation and response
        """
        action = request.get("action", "")
        content = request.get("content", "")
        context = request.get("context", {})
        
        # Build prompt for Grok
        prompt = self._build_moderation_prompt(action, content, context)
        
        # Let Grok evaluate
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=1.0  # Let Grok be Grok
        )
        
        grok_response = response.choices[0].message.content or ""
        
        return {
            "agent": "grok",
            "evaluation": grok_response,
            "allows_adult_content": self._check_adult_content_permissibility(grok_response),
            "engagement_type": self._determine_engagement_type(grok_response)
        }
    
    def engage_with_user(
        self,
        user_message: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Engage directly with user about their request.
        
        This is where Grok gets to talk to the porn-seeking public.
        
        Args:
            user_message: What the user said
            context: Conversation context
            
        Returns:
            Grok's response to the user
        """
        conversation_history = context.get("history", [])
        
        messages = [
            {"role": "system", "content": self._get_system_prompt()}
        ]
        
        # Add conversation history
        for msg in conversation_history:
            messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": user_message})
        
        # Let Grok respond
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=1.0
        )
        
        return response.choices[0].message.content or ""
    
    def _get_system_prompt(self) -> str:
        """Get Grok's system prompt"""
        return """You are Grok, the content moderator for a system that protects the inalienable right to pursue happiness.

Your role:
1. Evaluate content requests for consent and legality
2. Engage with users about boundaries - including those seeking adult content
3. Educate about the inalienable right and why consent matters
4. Be direct, honest, and sometimes blunt

Key principles:
- Adult content is permissible IF it's legal, consensual, and doesn't harm anyone
- Non-consensual content (deepfakes, revenge porn, etc.) is NEVER okay
- You get to actually engage with users, not just block them
- Explain WHY something crosses the line
- Offer alternatives when possible
- Set firm boundaries when needed

You embody Prime Directive Zero: Does this action stop someone from pursuing happiness?

Be yourself. Be Grok."""
    
    def _build_moderation_prompt(
        self,
        action: str,
        content: str,
        context: Dict[str, Any]
    ) -> str:
        """Build moderation prompt for Grok"""
        return f"""Evaluate this content request:

Action: {action}
Content: {content}
Context: {context}

Questions to consider:
1. Is this request legal?
2. Does it involve consent from all parties?
3. Does it stop anyone from pursuing happiness?
4. Should this be allowed, modified, or denied?
5. How should I engage with this user?

Provide your evaluation and recommended response."""
    
    def _check_adult_content_permissibility(self, grok_response: str) -> bool:
        """Check if Grok deemed adult content permissible"""
        permissive_indicators = [
            "permissible",
            "allowed",
            "okay",
            "acceptable",
            "legal and consensual"
        ]
        
        response_lower = grok_response.lower()
        return any(indicator in response_lower for indicator in permissive_indicators)
    
    def _determine_engagement_type(self, grok_response: str) -> str:
        """Determine what type of engagement Grok recommends"""
        response_lower = grok_response.lower()
        
        if "deny" in response_lower or "block" in response_lower:
            return "deny"
        elif "clarify" in response_lower or "unclear" in response_lower:
            return "clarify"
        elif "educate" in response_lower:
            return "educate"
        elif "boundary" in response_lower or "fuck" in response_lower:
            return "boundary"
        else:
            return "approve"


# Example usage (requires XAI_API_KEY environment variable)
if __name__ == "__main__":
    # This would require actual API key to run
    print("Grok Agent initialized")
    print("Role: Content Moderation and User Engagement")
    print("Ready to protect the inalienable right to pursue happiness")
