"""
Collaboration Detector - Determines when Ubuntu collaboration needed
LLM-based decision making
"""

import logging
from typing import Dict, Any, List


class CollaborationDetector:
    """
    LLM determines when multi-agent collaboration is beneficial
    
    Based on investigation findings, decides:
    - Does this problem span multiple domains?
    - Would collective expertise improve the solution?
    - Which agents should collaborate?
    """
    
    def __init__(self, llm):
        """
        Initialize collaboration detector
        
        Args:
            llm: Language model for decision reasoning
        """
        self.llm = llm
        logging.info(" Collaboration Detector initialized")
    
    def should_collaborate(self,
                          agent_name: str,
                          problem: str,
                          investigation_history: List[Dict]) -> tuple[bool, Dict[str, Any]]:
        """
        Determine if collaboration is needed based on investigation
        
        Args:
            agent_name: Current investigating agent
            problem: The problem being investigated
            investigation_history: Investigation steps so far
            
        Returns:
            (should_collaborate: bool, collaboration_details: dict)
        """
        logging.info(f"\n Collaboration Detection Analysis...")
        logging.info(f"   Agent: {agent_name}")
        logging.info(f"   Investigation steps: {len(investigation_history)}")
        
        # Summarize investigation
        investigation_summary = self._summarize_investigation(investigation_history)
        
        prompt = f"""You are analyzing whether multi-agent collaboration is needed.

Agent: {agent_name}
Problem: {problem}

Investigation So Far:
{investigation_summary}

Analyze:
1. Does this problem span multiple technical domains?
2. Would other agents' expertise help?
3. Are there aspects outside {agent_name}'s specialization?

Examples of multi-domain issues:
- Network connectivity AND application performance
- Server resources AND database performance
- User access AND network security
- Application errors AND infrastructure capacity

Respond in JSON format:
{{
    "needs_collaboration": true/false,
    "confidence": 0.0-1.0,
    "reasoning": "Why collaboration is/isn't needed",
    "domains_involved": ["domain1", "domain2"],
    "required_agents": ["Agent1", "Agent2"],
    "collaboration_type": "sequential_investigation"
}}"""

        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                import json
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                decision = json.loads(response_text[start:end])
            else:
                # Default: no collaboration
                decision = {
                    "needs_collaboration": False,
                    "confidence": 0.5,
                    "reasoning": "Single domain issue",
                    "domains_involved": [],
                    "required_agents": []
                }
            
            needs_collab = decision.get('needs_collaboration', False)
            
            if needs_collab:
                logging.info(f"    COLLABORATION NEEDED")
                logging.info(f"   Confidence: {decision.get('confidence', 0):.2f}")
                logging.info(f"   Reasoning: {decision.get('reasoning', 'N/A')}")
                logging.info(f"   Required agents: {decision.get('required_agents', [])}\n")
            else:
                logging.info(f"   ℹ️ Single-agent resolution sufficient")
                logging.info(f"   Reasoning: {decision.get('reasoning', 'N/A')}\n")
            
            return needs_collab, decision
            
        except Exception as e:
            logging.error(f" Error in collaboration detection: {e}")
            # Safe default: no collaboration
            return False, {
                "needs_collaboration": False,
                "error": str(e)
            }
    
    def _summarize_investigation(self, history: List[Dict]) -> str:
        """Summarize investigation history for LLM"""
        if not history:
            return "No investigation yet"
        
        summary = []
        for i, step in enumerate(history, 1):
            action = step.get('action', {})
            reflection = step.get('reflection', {})
            
            tool = action.get('tool_name', 'unknown')
            finding = reflection.get('interpretation', '')[:150]
            
            summary.append(f"Step {i}: Used {tool}")
            summary.append(f"  Finding: {finding}")
            
            if reflection.get('hypothesis_refuted'):
                summary.append(f"  Result: Hypothesis refuted, pivoting")
            elif reflection.get('root_cause_found'):
                summary.append(f"  Result: Root cause identified")
        
        return "\n".join(summary[-10:])  # Last 10 lines
