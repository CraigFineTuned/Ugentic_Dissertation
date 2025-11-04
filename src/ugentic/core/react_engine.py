"""
ReAct Engine - Reasoning and Acting Pattern (FIXED SESSIONS 23, 25, 27)
General-purpose LLM-guided diagnostic system
Based on 2024/2025 research

SESSION 23 FIX: Tool Selection & Diversity Enforcement
- Added _get_tools_to_avoid() method to prevent repeated tool calls
- Enhanced _generate_thought prompt with tool history and constraints
- Added action validation to enforce tool diversity
- LLM now receives explicit instructions to avoid recently used tools

SESSION 25 FIX (CRITICAL): LLM Reliability & Fallback Mechanisms
- Added exponential backoff retry logic for both thought and reflection generation
- Detects 401/connection errors and automatically retries with delays
- Smart fallback tool selection based on keywords when LLM fails
- Reflection engine now has 2-attempt retry before fallback analysis
- Thought generation has 3-attempt retry before smart tool selection
- All errors logged with specific type detection (auth vs connection vs other)
- Investigation can continue even when LLM service is unavailable

SESSION 27 FIX: Solo Investigation Summary Generation
- Added _synthesize_findings_with_llm() method for LLM-powered summary generation
- Updated _synthesize_solution() to call LLM synthesis instead of placeholders
- Updated _synthesize_from_plan() to call LLM synthesis instead of placeholders
- Added _create_fallback_summary() for graceful degradation when LLM fails
- Solo investigations now produce detailed, specific summaries matching orchestration quality
- Root cause and solution now include technical details from actual findings
"""

import json
import time
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
    
    def _select_fallback_tool(self, problem_report: str) -> str:
        """
        Session 25 Fix: Smart tool selection when LLM fails
        Uses keyword matching to select appropriate tool based on problem statement
        """
        problem_lower = problem_report.lower()
        
        # Keyword-based tool selection
        keywords_to_tools = {
            'printer': 'check_printer_status',
            'network': 'check_network_bandwidth',
            'dns': 'check_dns_resolution',
            'firewall': 'check_firewall_rules',
            'vpn': 'check_service_status',
            'permission': 'check_user_permissions',
            'cpu': 'check_server_metrics',
            'memory': 'check_server_metrics',
            'disk': 'check_disk_space',
            'error': 'check_server_logs',
            'crash': 'check_server_logs',
            'service': 'check_service_status',
            'process': 'check_process_list',
            'response': 'measure_server_response_time',
            'connection': 'check_network_bandwidth',
            'disconnect': 'check_network_bandwidth',
            'slowness': 'measure_server_response_time'
        }
        
        # Find best matching tool
        available_tools = [t['name'] for t in self.tools.list()]
        tools_to_avoid = self._get_tools_to_avoid()
        available_tools = [t for t in available_tools if t not in tools_to_avoid]
        
        for keyword, tool in keywords_to_tools.items():
            if keyword in problem_lower and tool in available_tools:
                return tool
        
        # Fallback: return first available tool not in avoid list
        return available_tools[0] if available_tools else self._select_default_tool()
    
    def _generate_thought(self, problem_report: str, context: Dict) -> Dict[str, Any]:
        """
        FIXED Session 25: LLM generates reasoning with RETRY LOGIC
        
        Added:
        - Exponential backoff retry on 401/connection errors
        - Smart fallback tool selection when LLM fails
        - Better error detection and reporting
        - Tool diversity from Session 23 still enforced
        """
        # Extract important context values
        context_hints = self._extract_context_hints(context)
        
        # SESSION 30: Extract diagnostic tree if available
        diagnostic_tree_text = ""
        if context and 'diagnostic_tree' in context:
            diagnostic_tree_text = f"""
{context['diagnostic_tree']}

NOTE: This is a proven procedure for '{context.get('problem_type', 'this issue')}' issues.
Follow these steps UNLESS you have a good reason to deviate.
"""
        
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
{diagnostic_tree_text}
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
        
        # SESSION 25 FIX: Retry logic with exponential backoff
        max_retries = 3
        retry_delay = 1
        
        for attempt in range(max_retries):
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
                error_msg = str(e)
                is_auth_error = "401" in error_msg or "unauthorized" in error_msg.lower()
                is_connection_error = "connection" in error_msg.lower() or "refused" in error_msg.lower()
                
                print(f" [Attempt {attempt + 1}/{max_retries}] LLM Error: {type(e).__name__}")
                
                if is_auth_error:
                    print(f" ✗ AUTHENTICATION ERROR (401): Possible Ollama connection issue")
                elif is_connection_error:
                    print(f" ✗ CONNECTION ERROR: Ollama not responding")
                else:
                    print(f" ✗ ERROR: {error_msg[:80]}")
                
                if attempt < max_retries - 1:
                    print(f" ⏳ Retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print(f" ✗ All {max_retries} attempts failed. Using fallback tool selection.")
                    
                    # Fallback: Smart tool selection without LLM
                    fallback_tool = self._select_fallback_tool(problem_report)
                    
                    return {
                        "reasoning": f"LLM unavailable. Using fallback tool selection based on problem keywords.",
                        "current_hypothesis": "Fallback investigation mode",
                        "next_action": {
                            "tool_name": fallback_tool,
                            "parameters": {},
                            "expectation": "Gather baseline information"
                        },
                        "status": "INVESTIGATING",
                        "fallback_mode": True,
                        "error": error_msg[:100]
                    }
        
        # Should not reach here, but fallback just in case
        return {
            "reasoning": "Critical error in thought generation",
            "status": "INVESTIGATING",
            "next_action": {
                "tool_name": self._select_fallback_tool(problem_report),
                "parameters": {},
                "expectation": "Gather information"
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
        """LLM reflects on observation vs expectation - WITH RETRY LOGIC (Session 25)"""
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
        
        # Session 25 Fix: Retry logic for reflection
        max_retries = 2
        retry_delay = 0.5
        
        for attempt in range(max_retries):
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
                error_msg = str(e)
                is_critical = "401" in error_msg or "unauthorized" in error_msg.lower()
                
                if attempt < max_retries - 1:
                    print(f" [Reflection Attempt {attempt + 1}/{max_retries}] Retrying...")
                    time.sleep(retry_delay)
                else:
                    print(f" [Reflection] Using fallback after {max_retries} attempts")
                    # Fallback: Simple analysis based on observation
                    return {
                        "interpretation": f"Unable to analyze. Observation success: {observation.get('success', False)}",
                        "hypothesis_confirmed": observation.get('success', False),
                        "hypothesis_refuted": not observation.get('success', True),
                        "root_cause_found": False,
                        "needs_collaboration": False,
                        "fallback_mode": True,
                        "error": error_msg[:80]
                    }
        
        # Ultimate fallback
        return {
            "interpretation": "Unable to reflect",
            "hypothesis_confirmed": False,
            "hypothesis_refuted": False,
            "root_cause_found": False,
            "needs_collaboration": False
        }
    
    def _synthesize_solution(self, final_state: Dict) -> Dict[str, Any]:
        """Create final solution with LLM synthesis"""
        # Use LLM to synthesize professional summary
        summary = self._synthesize_findings_with_llm(final_state)
        
        return {
            "status": "RESOLVED",
            "root_cause": summary.get('root_cause', 'Root cause identified through investigation'),
            "solution": summary.get('solution', 'Solution recommendations based on findings'),
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
        
        # SESSION 30: Don't include diagnostic_tree in hints (it's shown separately)
        filtered_context = {k: v for k, v in context.items() 
                          if k not in ['diagnostic_tree', 'problem_type']}
        
        if not filtered_context:
            return "No additional context."
        
        hints = ["\nKey Context:"]
        for key, value in filtered_context.items():
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
    
    def _synthesize_findings_with_llm(self, context: Dict) -> Dict[str, Any]:
        """
        SESSION 27 FIX: Use LLM to synthesize professional investigation summary
        
        Args:
            context: Dict containing investigation context (findings, objective, etc.)
            
        Returns:
            Dict with 'root_cause' and 'solution' keys
        """
        # Prepare investigation summary
        objective = context.get('objective', 'Unknown problem')
        findings = context.get('findings', [])
        
        # Format investigation steps for context
        steps_summary = []
        if isinstance(findings, list):
            for i, finding in enumerate(findings, 1):
                if isinstance(finding, dict):
                    step_desc = finding.get('step', f"Step {i}")
                    step_result = finding.get('finding', 'No result')
                    steps_summary.append(f"Step {i}: {step_desc}\n  Result: {str(step_result)[:200]}")
                else:
                    steps_summary.append(f"Step {i}: {str(finding)[:200]}")
        
        steps_text = "\n".join(steps_summary) if steps_summary else "No detailed steps available"
        
        # Format tool usage history
        tools_used = " → ".join(self.tool_usage_history[-5:]) if self.tool_usage_history else "Various tools"
        
        # Format recent observations
        recent_observations = []
        for step in self.history[-3:]:
            obs = step.observation
            if obs.get('success'):
                tool = step.action.get('tool_name', 'unknown')
                data = obs.get('data', {})
                recent_observations.append(f"- {tool}: {str(data)[:150]}")
        
        observations_text = "\n".join(recent_observations) if recent_observations else "No observations"
        
        # Create LLM synthesis prompt
        prompt = f"""You are {self.agent_name}, completing an IT support investigation.

PROBLEM:
{objective}

INVESTIGATION CONDUCTED:
{steps_text}

TOOLS USED:
{tools_used}

KEY OBSERVATIONS:
{observations_text}

Based on this investigation, provide a professional summary with:
1. ROOT CAUSE: A clear, specific explanation of what caused the problem (be technical and precise)
2. SOLUTION: Step-by-step instructions to resolve the issue (be actionable and detailed)

Respond in JSON format:
{{
    "root_cause": "Detailed technical explanation of the root cause",
    "solution": "Step-by-step solution with specific actions"
}}

IMPORTANT: Be specific and reference actual findings from the investigation. Do NOT use generic phrases."""
        
        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Extract JSON from response
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                summary = json.loads(json_str)
                
                return {
                    'root_cause': summary.get('root_cause', 'Root cause identified through investigation'),
                    'solution': summary.get('solution', 'Solution derived from findings')
                }
            else:
                # Fallback: Create better summary from observations
                return self._create_fallback_summary(context)
                
        except Exception as e:
            print(f" [Summary Synthesis] LLM error: {str(e)[:50]}. Using fallback.")
            return self._create_fallback_summary(context)
    
    def _create_fallback_summary(self, context: Dict) -> Dict[str, Any]:
        """
        Create summary from findings when LLM synthesis fails
        Better than generic placeholders
        """
        findings = context.get('findings', [])
        objective = context.get('objective', 'Unknown')
        
        # Try to extract meaningful info from last finding
        if findings and isinstance(findings, list) and len(findings) > 0:
            last_finding = findings[-1]
            if isinstance(last_finding, dict):
                finding_text = str(last_finding.get('finding', ''))
                root_cause = f"Investigation identified: {finding_text[:200]}"
                solution = "Review findings above and apply appropriate remediation based on root cause"
            else:
                root_cause = f"Issue related to: {objective[:150]}"
                solution = "Detailed solution requires manual review of investigation findings"
        else:
            root_cause = f"Investigation completed for: {objective[:150]}"
            solution = "Refer to investigation findings for remediation steps"
        
        return {
            'root_cause': root_cause,
            'solution': solution
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
        """Synthesize solution from completed plan with LLM synthesis"""
        plan = self.planner.get_plan(plan_id)
        
        all_findings = []
        for step in plan['steps']:
            if step['findings']:
                all_findings.append({
                    'step': step['description'],
                    'finding': step['findings']
                })
        
        # Use LLM to synthesize professional summary
        summary = self._synthesize_findings_with_llm({
            'objective': plan['objective'],
            'findings': all_findings,
            'investigation_type': 'plan_based'
        })
        
        return {
            "status": "INVESTIGATION_COMPLETE",
            "plan_id": plan_id,
            "objective": plan['objective'],
            "steps_completed": len([s for s in plan['steps'] if s['status'] == 'completed']),
            "findings": all_findings,
            "solution": summary.get('solution', 'Solution derived from investigation findings'),
            "root_cause": summary.get('root_cause', 'Root cause identified through investigation')
        }
