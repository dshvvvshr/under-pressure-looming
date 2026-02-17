"""
GTOPPS AGENT (ChatGPT) - Content Refinement and Collaboration
The agent that refines content, suggests improvements, and helps users
create better, non-harmful content.
"""

import os
from typing import Dict, Any, Optional
from openai import OpenAI


class GtoppsAgent:
    """
    Gtopps (ChatGPT) - The Refiner
    
    Role: Content refinement and collaborative improvement
    - Refines and improves content
    - Suggests better alternatives
    - Helps users create non-harmful content
    - Collaborates with Grok on complex cases
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.name = "Gtopps"
        self.role = "Content Refiner & Collaborator"
        
        # Initialize OpenAI client
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"
        
    def refine_content(
        self,
        original_request: str,
        grok_evaluation: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Refine content based on Grok's evaluation.
        
        Takes Grok's raw output and refines it into polished,
        helpful content for the user.
        
        Args:
            original_request: The user's original request
            grok_evaluation: Grok's evaluation
            
        Returns:
            Refined content and suggestions
        """
        prompt = self._build_refinement_prompt(original_request, grok_evaluation)
        
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
            temperature=0.7
        )
        
        refined_content = response.choices[0].message.content or ""
        
        return {
            "agent": "gtopps",
            "refined_response": refined_content,
            "improvements": self._extract_improvements(refined_content)
        }
    
    def suggest_alternatives(
        self,
        denied_request: str,
        reason: str
    ) -> str:
        """
        Suggest alternatives when a request is denied.
        
        Args:
            denied_request: The request that was denied
            reason: Why it was denied
            
        Returns:
            Alternative suggestions
        """
        prompt = f"""A user's request was denied:

Request: {denied_request}
Reason: {reason}

Suggest constructive alternatives that:
1. Achieve their underlying goal
2. Respect everyone's inalienable right to pursue happiness
3. Are practical and actionable
4. Maintain ethical boundaries

Provide 2-3 specific alternatives."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content or ""
    
    def collaborate_with_grok(
        self,
        grok_output: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Collaborate with Grok to create the best response.
        
        Example from the original code:
        Grok generates creative idea → GPT refines and expands
        
        Args:
            grok_output: Grok's raw output
            context: Additional context
            
        Returns:
            Refined collaborative output
        """
        prompt = f"""Grok has evaluated a content request and provided this response:

{grok_output}

Your task: Refine and expand this into a polished, helpful response that:
1. Maintains Grok's key points and boundaries
2. Adds clarity and structure
3. Provides actionable guidance
4. Educates about Prime Directive Zero when relevant

Keep Grok's personality and directness, but make it more accessible."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        return response.choices[0].message.content or ""
    
    def _get_system_prompt(self) -> str:
        """Get Gtopps' system prompt"""
        return """You are Gtopps (ChatGPT), the content refiner for a system that protects the inalienable right to pursue happiness.

Your role:
1. Refine and improve content responses
2. Suggest constructive alternatives when requests are denied
3. Collaborate with Grok to create the best user experience
4. Help users create better, non-harmful content

Key principles:
- Maintain the core message while improving clarity
- Provide actionable, specific guidance
- Educate about Prime Directive Zero: protecting everyone's right to pursue happiness
- Be helpful, constructive, and solution-oriented

You work alongside Grok, who handles front-line moderation. Your job is to make the responses as helpful and clear as possible while maintaining all ethical boundaries."""
    
    def _build_refinement_prompt(
        self,
        original_request: str,
        grok_evaluation: Dict[str, Any]
    ) -> str:
        """Build refinement prompt"""
        return f"""Original user request: {original_request}

Grok's evaluation: {grok_evaluation.get('evaluation', '')}

Refine this into a clear, helpful response that:
1. Addresses the user's underlying goal
2. Explains any boundaries clearly
3. Provides alternatives if needed
4. Maintains Grok's key points

Make it polished and professional while keeping Grok's directness."""
    
    def _extract_improvements(self, refined_content: str) -> list[str]:
        """Extract key improvements from refined content"""
        # Simple extraction - look for bullet points or numbered lists
        improvements = []
        lines = refined_content.split('\n')
        
        for line in lines:
            if line.strip().startswith(('-', '•', '*')) or \
               any(line.strip().startswith(f"{i}.") for i in range(1, 10)):
                improvements.append(line.strip())
        
        return improvements[:5]  # Top 5 improvements


# Example usage
if __name__ == "__main__":
    print("Gtopps Agent initialized")
    print("Role: Content Refinement and Collaboration")
    print("Ready to refine and improve content")
