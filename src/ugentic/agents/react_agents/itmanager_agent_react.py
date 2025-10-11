"""
IT Manager Agent - Simple Delegation Pattern
Strategic oversight and intelligent routing
"""

import logging
from typing import Dict, Any


class ITManagerAgentReAct:
    """
    IT Manager Agent - Strategic Router
    
    Role: Strategic oversight, delegation, resource allocation
    Pattern: Simple routing (not full ReAct) - delegates to appropriate agent
    Domain: Strategic decisions, agent coordination
    
    Ubuntu Principles:
    - Collective Problem-Solving: Ensures right agent handles each issue
    - Knowledge Sharing: Facilitates cross-team collaboration
    - Mutual Support: Supports all teams
    - Consensus Building: Strategic decisions involve teams
    """
    
    def __init__(self, llm, name="IT Manager", agents=None):
        """
        Initialize IT Manager agent
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            agents: Dictionary of available agents to delegate to
        """
        self.name = name
        self.agent_type = "Strategic"
        self.specialization = "Strategic Oversight, Delegation, Resource Allocation"
        self.llm = llm
        self.agents = agents or {}
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True,
            "strategic_vision": True
        }
        
        logging.info(f" {self.name} Agent initialized")
        logging.info(f"   Available agents: {list(self.agents.keys())}")
    
    def delegate(self, user_issue: str, context: Dict = None) -> Dict[str, Any]:
        """
        Delegate issue to appropriate agent based on LLM reasoning.
        This method ONLY decides which agent should handle the task.
        
        Args:
            user_issue: User's problem description
            context: Additional context
            
        Returns:
            A dictionary containing the name of the selected agent.
        """
        logging.info(f"\n{'='*60}")
        logging.info(f" {self.name} - Analyzing Issue for Delegation")
        logging.info(f"{'='*60}")
        logging.info(f"Issue: {user_issue}")
        logging.info(f"{'='*60}\n")
        
        delegation_prompt = f"""You are the IT Manager. Analyze this issue and decide which agent should handle it:

Issue: {user_issue}

Available Agents:
{self._format_agents()}

Consider:
- Issue complexity
- Domain expertise required
- Agent specializations

Respond in JSON format:
{{
    "selected_agent": "agent_name",
    "reasoning": "Why this agent is best suited",
    "issue_type": "simple/moderate/complex"
}}"""

        try:
            response = self.llm.invoke(delegation_prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                import json
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                decision = json.loads(response_text[start:end])
            else:
                decision = {
                    "selected_agent": "Service Desk Manager",
                    "reasoning": "Triage and assessment needed",
                }
            
            selected_agent_name = decision.get('selected_agent')
            
            if selected_agent_name not in self.agents:
                logging.warning(f"LLM chose an invalid agent '{selected_agent_name}'. Defaulting to Infrastructure.")
                selected_agent_name = "Infrastructure"

            logging.info(f" Delegation Decision:")
            logging.info(f"   Agent: {selected_agent_name}")
            logging.info(f"   Reasoning: {decision.get('reasoning')}\n")
            
            return {
                "agent": selected_agent_name,
                "reasoning": decision.get('reasoning')
            }
        
        except Exception as e:
            logging.error(f" Delegation error: {e}")
            return {
                "agent": "Infrastructure", # Safe fallback
                "reasoning": f"Error during delegation: {e}"
            }
    
    def _format_agents(self) -> str:
        """Format available agents for LLM"""
        agent_descriptions = []
        for name, agent in self.agents.items():
            if hasattr(agent, 'specialization'):
                agent_descriptions.append(f"- {name}: {agent.specialization}")
            else:
                agent_descriptions.append(f"- {name}")
        return "\n".join(agent_descriptions)
    
    def register_agent(self, name: str, agent):
        """Register an agent for delegation"""
        self.agents[name] = agent
        logging.info(f" Registered agent: {name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_name": self.name,
            "agent_type": self.agent_type,
            "specialization": self.specialization,
            "available_agents": list(self.agents.keys()),
            "ubuntu_principles": self.ubuntu_principles,
            "reports_to": "Executive Management",
            "manages": list(self.agents.keys()),
            "pattern": "Strategic Delegation"
        }
