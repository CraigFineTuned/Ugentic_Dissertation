"""
ReAct Engine - Reasoning and Acting Pattern
General-purpose LLM-guided diagnostic system
Based on 2024/2025 research
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReActStep:
    """Single step in ReAct loop"""
    iteration: int
    thought: Dict[str, Any]
    action: Dict[str, Any]
    observation: Dict[str, Any]
    reflection: Dict[str, Any]
    timestamp: str


class ReactEngine:
    """
    Core ReAct (Reasoning + Acting) engine
    Works for ANY problem domain
    
    Pattern: Thought → Action → Observation → Reflection → (repeat)
    """
    
    def __init__(self, agent_name: str, tools, llm, max_iterations: int = 10, logger=None):
        """
        Initialize ReAct engine
        
        Args:
            agent_name: Name of the agent using this engine
            tools: ToolRegistry instance with domain-specific tools
            llm: LLM for reasoning
            max_iterations: Maximum ReAct loop iterations
            logger: InvestigationLogger instance (optional)
        """
        self.agent_name = agent_name
        self.tools = tools
        self.llm = llm
        self.max_iterations = max_iterations
        self.logger = logger
        self.current_inv_id = None
        self.history: List[ReActStep] = []
    
    def investigate(self, problem_report: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        General-purpose investigation using ReAct pattern
        Works for ANY problem in agent's domain
        
        Args:
            problem_report: User's problem description
            context: Additional context (user info, system state, etc.)
            
        Returns:
            Investigation result with root cause and solution
        """
        self.history = []
        context = context or {}
        
        # Start investigation logging
        if self.logger:
            self.current_inv_id = self.logger.start_investigation(problem_report, self.agent_name)
        
        print(f"\n{'='*60}")
        print(f" {self.agent_name} - ReAct Investigation Starting")
        print(f"{'='*60}")
        print(f"Problem: {problem_report}")
        print(f"{'='*60}\n")
        
        for iteration in range(self.max_iterations):
            print(f"--- Iteration {iteration + 1}/{self.max_iterations} ---\n")
            
            # THOUGHT: LLM reasons about current state
            thought = self._generate_thought(problem_report, context)
            print(f" THOUGHT:\n{thought.get('reasoning', 'No reasoning')}\n")
            
            # Check if done
            if thought.get('status') == 'ROOT_CAUSE_FOUND':
                print(" ROOT CAUSE IDENTIFIED\n")
                result = self._synthesize_solution(thought)
                if self.logger and self.current_inv_id:
                    self.logger.end_investigation(self.current_inv_id, 'success', str(result))
                return result
            
            if thought.get('status') == 'NEEDS_COLLABORATION':
                print(" COLLABORATION REQUIRED\n")
                result = self._request_collaboration(thought)
                if self.logger and self.current_inv_id:
                    self.logger.log_collaboration_decision(
                        self.current_inv_id, 
                        triggered=True,
                        reason="Multi-domain issue detected during investigation"
                    )
                    self.logger.end_investigation(self.current_inv_id, 'needs_collaboration', str(result))
                return result
            
            # ACTION: LLM decides which tool to use
            action = thought.get('next_action', {})
            if not action:
                print(" No action determined, ending investigation\n")
                result = self._escalate_to_human()
                if self.logger and self.current_inv_id:
                    self.logger.end_investigation(self.current_inv_id, 'error', 'No action determined')
                return result
            
            print(f" ACTION: {action.get('tool_name', 'unknown')}")
            print(f"   Parameters: {action.get('parameters', {})}\n")
            
            # EXECUTE: Call the tool
            observation = self._execute_tool(action)
            print(f" OBSERVATION:")
            print(f"   {json.dumps(observation, indent=2)}\n")
            
            # REFLECTION: LLM interprets results
            reflection = self._generate_reflection(thought, observation)
            print(f" REFLECTION:\n{reflection.get('interpretation', 'No interpretation')}\n")
            
            # Log iteration
            if self.logger and self.current_inv_id:
                self.logger.log_iteration(
                    self.current_inv_id,
                    iteration + 1,
                    thought=thought.get('reasoning', ''),
                    action=action.get('tool_name', ''),
                    parameters=action.get('parameters', {}),
                    observation=observation,
                    reflection=reflection.get('interpretation', '')
                )
            
            # Store step
            step = ReActStep(
                iteration=iteration,
                thought=thought,
                action=action,
                observation=observation,
                reflection=reflection,
                timestamp=datetime.now().isoformat()
            )
            self.history.append(step)
            
            # Check reflection status
            if reflection.get('root_cause_found'):
                print(" ROOT CAUSE FOUND IN REFLECTION\n")
                result = self._synthesize_solution(reflection)
                if self.logger and self.current_inv_id:
                    self.logger.end_investigation(self.current_inv_id, 'success', str(result))
                return result
            
            if reflection.get('needs_collaboration'):
                print(" COLLABORATION NEEDED\n")
                result = self._request_collaboration(reflection)
                if self.logger and self.current_inv_id:
                    self.logger.log_collaboration_decision(
                        self.current_inv_id,
                        triggered=True,
                        reason=reflection.get('interpretation', 'Complex multi-domain issue')
                    )
                    self.logger.end_investigation(self.current_inv_id, 'needs_collaboration', str(result))
                return result
            
            # If hypothesis wrong, continue with new hypothesis
            if reflection.get('hypothesis_refuted'):
                print(" Hypothesis refuted, pivoting...\n")
                continue
        
        # Max iterations reached
        print(" Max iterations reached\n")
        result = self._escalate_to_human()
        if self.logger and self.current_inv_id:
            self.logger.end_investigation(self.current_inv_id, 'escalated', str(result))
        return result
    
    def _generate_thought(self, problem_report: str, context: Dict) -> Dict[str, Any]:
        """
        LLM generates reasoning about current state
        """
        # Extract important context values for emphasis
        context_hints = self._extract_context_hints(context)
        
        prompt = f"""You are {self.agent_name}, investigating this problem:
Problem: {problem_report}

Context Information: {json.dumps(context, indent=2)}
{context_hints}

Investigation History:
{self._format_history()}

Available Tools:
{self._format_tools()}

Think about this problem:
1. What do I currently know from the problem and context?
2. What is my current hypothesis?
3. What should I check next?
4. Which tool should I use?
5. What parameters should I pass (USE VALUES FROM CONTEXT when available)?
6. What do I expect to find?

IMPORTANT: When calling tools, use specific values from the Context Information above.
For example, if context has user_id="user_12345", include {{"user_id": "user_12345"}} in parameters.

Respond in JSON format:
{{
    "reasoning": "Your reasoning here",
    "current_hypothesis": "Your current hypothesis",
    "next_action": {{
        "tool_name": "tool_to_use",
        "parameters": {{"param1": "value_from_context_or_default"}},
        "expectation": "What you expect to find"
    }},
    "status": "INVESTIGATING" or "ROOT_CAUSE_FOUND" or "NEEDS_COLLABORATION"
}}"""

        try:
            response = self.llm.invoke(prompt)
            # Extract JSON from response
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Try to parse JSON
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                # Fallback: create basic thought
                return {
                    "reasoning": response_text,
                    "current_hypothesis": "Initial investigation",
                    "next_action": {
                        "tool_name": self._select_default_tool(),
                        "parameters": {},
                        "expectation": "Gather initial information"
                    },
                    "status": "INVESTIGATING"
                }
        except Exception as e:
            print(f" Error generating thought: {e}")
            return {
                "reasoning": f"Error in thought generation: {e}",
                "status": "INVESTIGATING",
                "next_action": {
                    "tool_name": self._select_default_tool(),
                    "parameters": {},
                    "expectation": "Basic diagnostic check"
                }
            }
    
    def _execute_tool(self, action: Dict) -> Dict[str, Any]:
        """
        Execute diagnostic tool
        """
        tool_name = action.get('tool_name')
        parameters = action.get('parameters', {})
        
        if not tool_name:
            return {"error": "No tool specified"}
        
        # Execute tool (ToolRegistry will handle parameter validation)
        return self.tools.execute(tool_name, parameters)
    
    def _generate_reflection(self, thought: Dict, observation: Dict) -> Dict[str, Any]:
        """
        LLM reflects on observation vs expectation
        """
        prompt = f"""You are {self.agent_name}. Analyze this observation:

Expected: {thought.get('next_action', {}).get('expectation', 'Unknown')}
Observed: {json.dumps(observation, indent=2)}

Reflect on this:
1. Does it confirm or refute my hypothesis?
2. What does this tell me about the problem?
3. Do I need to investigate further?
4. Have I found the root cause?
5. Do I need help from other agents?

Respond in JSON format:
{{
    "interpretation": "What this observation means",
    "hypothesis_confirmed": true/false,
    "hypothesis_refuted": true/false,
    "root_cause_found": true/false,
    "root_cause": "Description if found",
    "needs_collaboration": true/false,
    "required_agents": ["agent1", "agent2"],
    "next_hypothesis": "New hypothesis if needed"
}}"""

        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                return {
                    "interpretation": response_text,
                    "hypothesis_confirmed": False,
                    "hypothesis_refuted": False,
                    "root_cause_found": False,
                    "needs_collaboration": False
                }
        except Exception as e:
            print(f" Error generating reflection: {e}")
            return {
                "interpretation": f"Error in reflection: {e}",
                "hypothesis_confirmed": False,
                "hypothesis_refuted": False,
                "root_cause_found": False
            }
    
    def _synthesize_solution(self, final_state: Dict) -> Dict[str, Any]:
        """
        Create final solution based on investigation
        """
        return {
            "status": "RESOLVED",
            "root_cause": final_state.get('root_cause', 'Identified through investigation'),
            "solution": final_state.get('solution', 'Solution derived from findings'),
            "investigation_history": self._get_history_summary(),
            "iterations": len(self.history)
        }
    
    def _request_collaboration(self, state: Dict) -> Dict[str, Any]:
        """
        Request Ubuntu collaboration
        """
        return {
            "status": "NEEDS_COLLABORATION",
            "reason": state.get('interpretation', 'Complex multi-domain issue'),
            "required_agents": state.get('required_agents', []),
            "investigation_history": self._get_history_summary(),
            "lead_agent": self.agent_name
        }
    
    def _escalate_to_human(self) -> Dict[str, Any]:
        """
        Escalate to human when unable to resolve
        """
        return {
            "status": "ESCALATE_TO_HUMAN",
            "reason": "Unable to identify root cause within iteration limit",
            "investigation_history": self._get_history_summary(),
            "findings": self._summarize_findings()
        }
    
    def _format_history(self) -> str:
        """Format investigation history for LLM"""
        if not self.history:
            return "No previous steps"
        
        summary = []
        for step in self.history[-3:]:  # Last 3 steps
            summary.append(f"Iteration {step.iteration + 1}:")
            summary.append(f"  Thought: {step.thought.get('reasoning', 'N/A')[:100]}")
            summary.append(f"  Action: {step.action.get('tool_name', 'N/A')}")
            summary.append(f"  Finding: {step.reflection.get('interpretation', 'N/A')[:100]}")
        
        return "\n".join(summary)
    
    def _format_tools(self) -> str:
        """Format available tools for LLM"""
        tool_list = self.tools.list()
        formatted = []
        for tool in tool_list:
            # Include parameter hints
            params = tool.get('parameters', {})
            param_str = ", ".join([f"{k}" for k in params.keys()]) if params else "no params"
            formatted.append(f"- {tool['name']}({param_str}): {tool['description']}")
        return "\n".join(formatted)
    
    def _extract_context_hints(self, context: Dict) -> str:
        """Extract and highlight important context values"""
        if not context:
            return "No additional context provided."
        
        hints = ["\nKey Context Values (use these in tool parameters):"]
        for key, value in context.items():
            hints.append(f"  - {key}: {value}")
        
        return "\n".join(hints)
    
    def _select_default_tool(self) -> str:
        """Select a default diagnostic tool"""
        tools = self.tools.list()
        return tools[0]['name'] if tools else "unknown"
    
    def _get_history_summary(self) -> List[Dict]:
        """Get summary of investigation history"""
        return [
            {
                "iteration": step.iteration,
                "tool_used": step.action.get('tool_name'),
                "finding": step.reflection.get('interpretation', '')[:200]
            }
            for step in self.history
        ]
    
    def _summarize_findings(self) -> str:
        """Summarize what was discovered"""
        if not self.history:
            return "No findings"
        
        findings = []
        for step in self.history:
            if step.observation.get('success'):
                findings.append(step.observation.get('data', 'No data'))
        
        return str(findings)
    
    def get_full_history(self) -> List[ReActStep]:
        """Get complete investigation history"""
        return self.history
