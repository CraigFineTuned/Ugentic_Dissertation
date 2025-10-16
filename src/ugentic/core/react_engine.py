"""
ReAct Engine - Reasoning and Acting Pattern (FIXED SESSION 23)
General-purpose LLM-guided diagnostic system
Based on 2024/2025 research

SESSION 23 FIX: Tool Selection & Diversity Enforcement
- Added _get_tools_to_avoid() method to prevent repeated tool calls
- Enhanced _generate_thought prompt with tool history and constraints
- Added action validation to enforce tool diversity
- LLM now receives explicit instructions to avoid recently used tools
"""

import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from collections import Counter
from .reflection_engine import ReflectionEngine
from .progress_tracker import ProgressTracker


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
    
    def __init__(self, agent_name: str, tools, llm, max_iterations: int = 10, logger=None, planner=None):
        """
        Initialize ReAct engine with optimization suite
        
        Args:
            agent_name: Name of the agent using this engine
            tools: ToolRegistry instance with domain-specific tools
            llm: LLM for reasoning
            max_iterations: Maximum ReAct loop iterations
            logger: InvestigationLogger instance (optional)
            planner: ExplicitPlanner instance for structured planning (optional)
        """
        self.agent_name = agent_name
        self.tools = tools
        self.llm = llm
        self.max_iterations = max_iterations
        self.logger = logger
        self.planner = planner
        self.current_inv_id = None
        self.current_plan_id = None
        self.history: List[ReActStep] = []
        self.tool_usage_history: List[str] = []  # Track tool usage for loop detection
        
        # NEW: Optimization modules
        self.reflection_engine = ReflectionEngine()
        self.progress_tracker = ProgressTracker(diversity_threshold=0.5)
    
    def _get_tools_to_avoid(self) -> List[str]:
        """
        FIXED Session 23: Identify tools to avoid (recently used)
        Prevents consecutive tool calls and promotes diversity
        
        Returns:
            List of tool names that should not be used in the next action
        """
        tools_to_avoid = []
        
        if len(self.tool_usage_history) >= 1:
            # Strongly avoid the tool just called
            tools_to_avoid.append(self.tool_usage_history[-1])
        
        if len(self.tool_usage_history) >= 3:
            # If a tool was called 3+ times total, avoid it
            tool_counts = Counter(self.tool_usage_history)
            for tool, count in tool_counts.items():
                if count >= 3:
                    tools_to_avoid.append(tool)
        
        return list(set(tools_to_avoid))  # Remove duplicates
    
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
        self.tool_usage_history = []  # Reset tool tracking
        context = context or {}
        
        # NEW: Reset optimization modules
        self.reflection_engine = ReflectionEngine()
        self.progress_tracker.reset()
        
        # Start investigation logging
        if self.logger:
            self.current_inv_id = self.logger.start_investigation(problem_report, self.agent_name)
        
        # Create investigation plan (Deep Agents Pillar #1)
        if self.planner:
            self.current_plan_id = self.planner.create_plan(
                objective=problem_report,
                agent_name=self.agent_name,
                problem_context=context
            )
            context["plan_id"] = self.current_plan_id
            print(f"\n📋 Investigation Plan Created: {self.current_plan_id}")
            
            # Show plan summary
            progress = self.planner.check_progress(self.current_plan_id)
            print(f"   Objective: {progress['objective']}")
            print(f"   Total Steps: {progress['progress'].split('/')[1]}")
            if progress['next_step']:
                print(f"   Next Step: {progress['next_step']['description']}\n")
        
        print(f"\n{'='*60}")
        print(f" {self.agent_name} - ReAct Investigation Starting")
        print(f"{'='*60}")
        print(f"Problem: {problem_report}")
        print(f"{'='*60}\n")
        
        for iteration in range(self.max_iterations):
            print(f"--- Iteration {iteration + 1}/{self.max_iterations} ---\n")
            
            # Check plan progress (Deep Agents)
            if self.planner and self.current_plan_id:
                progress = self.planner.check_progress(self.current_plan_id)
                print(f"📊 Plan Progress: {progress['progress']} ({progress['completion_percentage']}%)")
                
                if progress['next_step']:
                    print(f"   Current Step: {progress['next_step']['description']}")
                
                # If plan complete, synthesize solution
                if progress['status'] == 'completed':
                    print("\n✅ Investigation Plan COMPLETED\n")
                    result = self._synthesize_from_plan(self.current_plan_id)
                    if self.logger and self.current_inv_id:
                        self.logger.end_investigation(self.current_inv_id, 'success', str(result))
                    return result
                print()
            
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
            
            # Track tool usage for loop detection
            tool_used = action.get('tool_name', 'unknown')
            self.tool_usage_history.append(tool_used)
            
            # NEW: Record tool usage for progress tracking
            self.progress_tracker.record_tool_usage(tool_used, iteration + 1)
            self.progress_tracker.record_observation(observation, iteration + 1)
            
            # Detect tool loop: same tool 5 times in a row
            if len(self.tool_usage_history) >= 5:
                last_five = self.tool_usage_history[-5:]
                if len(set(last_five)) == 1:  # All same tool
                    print(f"⚠️  TOOL LOOP DETECTED: '{tool_used}' used 5 consecutive times")
                    print(f"   Concluding investigation to prevent inefficiency\n")
                    result = self._conclude_early(
                        reason=f"Tool loop detected - '{tool_used}' used repeatedly without progress",
                        tool_name=tool_used
                    )
                    if self.logger and self.current_inv_id:
                        self.logger.end_investigation(
                            self.current_inv_id, 
                            'INVESTIGATION_COMPLETE',
                            str(result)
                        )
                    return result
            
            # NEW: Reflection - Evaluate progress every 2 iterations
            if (iteration + 1) % 2 == 0:  # Only on even iterations (2, 4, 6, ...)
                reflection_result = self.reflection_engine.evaluate_progress(
                    current_iteration=iteration + 1,
                    current_observation=observation,
                    previous_observations=[s.observation for s in self.history],
                    current_thought=thought
                )
                
                print(f" 🧠 REFLECTION (every 2 iterations):")
                print(f"   Progress Score: {reflection_result['progress_score']:.2f}")
                print(f"   Info Gain: {reflection_result['information_gain']:.2f}")
                print(f"   Strategy: {reflection_result['strategy_effectiveness']:.2f}")
                print(f"   Recommendation: {reflection_result['recommendation']}")
                
                if reflection_result['is_stuck']:
                    print(f"   ⚠️  Agent appears stuck - low progress detected")
                print()
            else:
                reflection_result = None
            
            # NEW: Check if should change strategy
            if reflection_result and reflection_result['should_change_strategy']:
                progress_report = self.progress_tracker.get_progress_report(iteration + 1)
                
                if progress_report['tool_diversity'] < 0.3:
                    available_tools = [t['name'] for t in self.tools.list()]
                    suggested_tools = self.progress_tracker.suggest_alternative_tools(available_tools)
                    print(f" 💡 SUGGESTION: Try alternative tools: {', '.join(suggested_tools[:2])}\n")
            
            # NEW: Check if should conclude based on progress
            should_conclude, conclude_reason = self.progress_tracker.should_conclude_investigation(
                current_iteration=iteration + 1,
                max_iterations=self.max_iterations
            )
            
            if should_conclude and conclude_reason != "CONTINUE":
                print(f" ⏸️  EARLY CONCLUSION: {conclude_reason}\n")
                result = self._conclude_early(
                    reason=conclude_reason,
                    tool_name=tool_used
                )
                if self.logger and self.current_inv_id:
                    self.logger.end_investigation(
                        self.current_inv_id,
                        'INVESTIGATION_COMPLETE',
                        str(result)
                    )
                return result
            
            # UPDATE PLAN: Mark step complete/failed based on observation
            if self.planner and self.current_plan_id:
                self._update_plan_with_action(action, observation)
            
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
        
        # NEW: Print final optimization summary
        self._print_optimization_summary()
        
        result = self._escalate_to_human()
        if self.logger and self.current_inv_id:
            self.logger.end_investigation(self.current_inv_id, 'escalated', str(result))
        return result
    
    def _generate_thought(self, problem_report: str, context: Dict) -> Dict[str, Any]:
        """
        FIXED Session 23: LLM generates reasoning with tool diversity constraints
        
        Now includes:
        - Recent tool history
        - Explicit forbidden tools
        - Tool alternative suggestions
        - Action validation to enforce constraints
        """
        # Extract important context values
        context_hints = self._extract_context_hints(context)
        
        # FIXED Session 23: Get tools to avoid
        tools_to_avoid = self._get_tools_to_avoid()
        all_tools = [t['name'] for t in self.tools.list()]
        alternative_tools = [t for t in all_tools if t not in tools_to_avoid]
        
        # Build recent tool history string
        recent_tools_str = " → ".join(self.tool_usage_history[-4:]) if self.tool_usage_history else "None"
        
        # Build constraint instructions
        constraint_text = ""
        if tools_to_avoid:
            constraint_text = f"""
TOOL CONSTRAINTS (Session 23 - Tool Diversity Fix):
- DO NOT use: {', '.join(tools_to_avoid)} (recently used, will reset investigation)
- MUST use alternatives: {', '.join(alternative_tools[:4])}
- Recent tool sequence: {recent_tools_str}
- CRITICAL: Tool repetition causes investigation failure!
"""
        
        prompt = f"""You are {self.agent_name}, investigating this problem:
Problem: {problem_report}

Context Information: {json.dumps(context, indent=2)}
{context_hints}

Investigation History:
{self._format_history()}
{constraint_text}

Available Tools:
{self._format_tools()}

STRATEGIC INVESTIGATION:
1. What have I discovered so far from recent findings?
2. What angles remain unexplored? (permissions? status? config? network?)
3. What is my current hypothesis?
4. What DIFFERENT tool would provide NEW information?
5. Why is this tool different from recent ones?

MANDATORY: Respond in JSON with this EXACT structure:
{{
    "reasoning": "Your strategic reasoning",
    "why_this_tool": "Why this tool is different from recent ones",
    "current_hypothesis": "Your working hypothesis",
    "next_action": {{
        "tool_name": "tool_name_here (NOT from the DO NOT USE list!)",
        "parameters": {{"param": "value_from_context"}},
        "expectation": "What you expect to find"
    }},
    "status": "INVESTIGATING" or "ROOT_CAUSE_FOUND"
}}"""
        
        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                thought = json.loads(json_str)
                
                # FIXED Session 23: VALIDATE tool selection
                tool_name = thought.get('next_action', {}).get('tool_name', '')
                if tool_name in tools_to_avoid:
                    print(f"   [FORCED OVERRIDE] LLM selected forbidden tool '{tool_name}', forcing alternative...")
                    if alternative_tools:
                        thought['next_action']['tool_name'] = alternative_tools[0]
                        thought['next_action']['parameters'] = {}
                        print(f"   [NOW USING] {alternative_tools[0]}")
                    else:
                        thought['next_action']['tool_name'] = self._select_default_tool()
                
                return thought
            else:
                return {
                    "reasoning": response_text,
                    "current_hypothesis": "Investigation",
                    "next_action": {
                        "tool_name": (alternative_tools[0] if alternative_tools else self._select_default_tool()),
                        "parameters": {},
                        "expectation": "Gather information"
                    },
                    "status": "INVESTIGATING"
                }
        except Exception as e:
            print(f" Error generating thought: {e}")
            return {
                "reasoning": f"Error: {e}",
                "status": "INVESTIGATING",
                "next_action": {
                    "tool_name": (alternative_tools[0] if alternative_tools else self._select_default_tool()),
                    "parameters": {},
                    "expectation": "Basic check"
                }
            }
    
    def _execute_tool(self, action: Dict) -> Dict[str, Any]:
        """Execute diagnostic tool with validation"""
        tool_name = action.get('tool_name')
        parameters = action.get('parameters', {})
        
        if not tool_name:
            return {"error": "No tool specified"}
        
        available_tools = [t['name'] for t in self.tools.list()]
        if tool_name not in available_tools:
            return {
                "success": False,
                "error": f"Tool {tool_name} not found",
                "hint": f"Use one of: {', '.join(available_tools[:5])}"
            }
        
        return self.tools.execute(tool_name, parameters)
    
    def _generate_reflection(self, thought: Dict, observation: Dict) -> Dict[str, Any]:
        """LLM reflects on observation vs expectation"""
        prompt = f"""You are {self.agent_name}. Analyze this:

Expected: {thought.get('next_action', {}).get('expectation', 'Unknown')}
Observed: {json.dumps(observation, indent=2)}

Respond in JSON:
{{
    "interpretation": "What this means",
    "hypothesis_confirmed": true/false,
    "hypothesis_refuted": true/false,
    "root_cause_found": true/false,
    "needs_collaboration": true/false
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
            return {
                "interpretation": f"Reflection error: {e}",
                "hypothesis_confirmed": False,
                "hypothesis_refuted": False,
                "root_cause_found": False
            }
    
    def _synthesize_solution(self, final_state: Dict) -> Dict[str, Any]:
        """Create final solution"""
        return {
            "status": "RESOLVED",
            "root_cause": final_state.get('root_cause', 'Identified through investigation'),
            "solution": final_state.get('solution', 'Solution derived from findings'),
            "investigation_history": self._get_history_summary(),
            "iterations": len(self.history)
        }
    
    def _request_collaboration(self, state: Dict) -> Dict[str, Any]:
        """Request Ubuntu collaboration"""
        return {
            "status": "NEEDS_COLLABORATION",
            "reason": state.get('interpretation', 'Complex multi-domain issue'),
            "required_agents": state.get('required_agents', []),
            "investigation_history": self._get_history_summary(),
            "lead_agent": self.agent_name
        }
    
    def _escalate_to_human(self) -> Dict[str, Any]:
        """Escalate to human"""
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
        for step in self.history[-3:]:
            summary.append(f"Iteration {step.iteration + 1}:")
            summary.append(f"  Tool: {step.action.get('tool_name', 'N/A')}")
            summary.append(f"  Finding: {step.reflection.get('interpretation', 'N/A')[:100]}")
        
        return "\n".join(summary)
    
    def _format_tools(self) -> str:
        """Format available tools for LLM"""
        tool_list = self.tools.list()
        formatted = []
        for tool in tool_list:
            formatted.append(f"- {tool['name']}: {tool['description']}")
        return "\n".join(formatted)
    
    def _extract_context_hints(self, context: Dict) -> str:
        """Extract important context values"""
        if not context:
            return "No additional context."
        
        hints = ["\nKey Context:"]
        for key, value in context.items():
            hints.append(f"  - {key}: {value}")
        
        return "\n".join(hints)
    
    def _select_default_tool(self) -> str:
        """Select a default tool"""
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
        """Summarize discoveries"""
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
    
    def _print_optimization_summary(self):
        """Print summary of optimization metrics"""
        print(f"\n{'='*60}")
        print(f" OPTIMIZATION SUMMARY")
        print(f"{'='*60}")
        
        progress_report = self.progress_tracker.get_progress_report(len(self.history))
        tool_summary = self.progress_tracker.get_tool_usage_summary()
        
        print(f"\n 📈 Progress Metrics:")
        print(f"   Status: {progress_report['status']}")
        print(f"   Progress Velocity: {progress_report['progress_velocity']:.2f}")
        
        print(f"\n 🛠️  Tool Usage:")
        print(f"   Total Calls: {tool_summary['total_calls']}")
        print(f"   Unique Tools: {tool_summary['unique_tools']}")
        print(f"   Diversity Score: {tool_summary['diversity_score']:.2f}")
        if tool_summary.get('most_used_tool'):
            print(f"   Most Used: {tool_summary['most_used_tool']} ({tool_summary['most_used_count']}x)")
        
        print(f"\n{'='*60}\n")
    
    def _synthesize_conclusion(self) -> Dict[str, Any]:
        """Synthesize findings into conclusion"""
        if not self.history:
            return {
                "conclusion": "No data",
                "recommendations": ["Insufficient data"],
                "detailed_findings": []
            }
        
        detailed_findings = []
        success_count = 0
        error_count = 0
        
        for step in self.history:
            obs = step.observation
            if obs.get('success'):
                success_count += 1
                detailed_findings.append({
                    "type": "success",
                    "tool": step.action.get('tool_name'),
                    "data": obs.get('data', 'No data')
                })
            elif obs.get('error'):
                error_count += 1
                detailed_findings.append({
                    "type": "error",
                    "tool": step.action.get('tool_name'),
                    "error": obs.get('error', 'Unknown')
                })
        
        if success_count > 0:
            conclusion = f"Investigation completed with {success_count} successful findings and {error_count} errors."
        else:
            conclusion = f"Investigation encountered {error_count} errors."
        
        recommendations = []
        if success_count > 0:
            recommendations.append(f"Review the {success_count} findings above")
        if error_count > 0:
            recommendations.append(f"Investigate {error_count} error(s)")
        if not recommendations:
            recommendations.append("Escalate for manual investigation")
        
        return {
            "conclusion": conclusion,
            "recommendations": recommendations,
            "detailed_findings": detailed_findings
        }
    
    def _conclude_early(self, reason: str, tool_name: str = None) -> Dict[str, Any]:
        """Conclude investigation early"""
        self._print_optimization_summary()
        synthesized = self._synthesize_conclusion()
        
        result = {
            "status": "INVESTIGATION_COMPLETE",
            "outcome": "INVESTIGATION_COMPLETE",
            "reason": reason,
            "early_termination": True,
            "iterations_completed": len(self.history),
            "max_iterations": self.max_iterations,
            "findings": self._summarize_findings(),
            "investigation_history": self._get_history_summary(),
            "conclusion": synthesized['conclusion'],
            "recommendations": synthesized['recommendations'],
            "detailed_findings": synthesized['detailed_findings']
        }
        
        if tool_name:
            result["loop_tool"] = tool_name
            result["tool_usage_pattern"] = self.tool_usage_history
        
        return result
    
    def _update_plan_with_action(self, action: Dict, observation: Dict):
        """Update investigation plan with action results"""
        if not self.planner or not self.current_plan_id:
            return
        
        progress = self.planner.check_progress(self.current_plan_id)
        if not progress['next_step']:
            return
        
        step_number = progress['next_step']['step_number']
        status = "completed" if observation.get('success') else "failed"
        findings = observation.get('data', observation.get('result', 'No findings'))
        if isinstance(findings, dict):
            findings = str(findings)
        
        self.planner.update_step(
            plan_id=self.current_plan_id,
            step_number=step_number,
            status=status,
            findings=findings[:500],
            tools_used=[action.get('tool_name', 'unknown')]
        )
    
    def _synthesize_from_plan(self, plan_id: str) -> Dict[str, Any]:
        """Synthesize solution from completed plan"""
        plan = self.planner.get_plan(plan_id)
        
        all_findings = []
        for step in plan['steps']:
            if step['findings']:
                all_findings.append({
                    'step': step['description'],
                    'finding': step['findings']
                })
        
        return {
            "status": "INVESTIGATION_COMPLETE",
            "plan_id": plan_id,
            "objective": plan['objective'],
            "steps_completed": len([s for s in plan['steps'] if s['status'] == 'completed']),
            "findings": all_findings,
            "solution": "Solution synthesized from completed investigation plan",
            "root_cause": "Identified through structured investigation"
        }
