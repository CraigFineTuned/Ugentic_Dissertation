"""
Ubuntu Orchestrator - Multi-Agent Coordination
Based on 2024/2025 orchestrator-subagent pattern
Sequential execution for reliability
"""

import logging
from typing import Dict, Any, List
from datetime import datetime


class UbuntuOrchestrator:
    """
    Implements 2024/2025 orchestrator-subagent pattern
    
    Based on:
    - Anthropic 2025: Lead agent decomposes, subagents execute sequentially
    - Microsoft Build 2025: Orchestrator manages specialists
    - Cognition AI 2025: Sequential over parallel for reliability
    
    Ubuntu Principles:
    - Collective Problem-Solving: Coordinates multiple experts
    - Knowledge Sharing: Synthesizes collective findings
    - Mutual Support: Each agent contributes their expertise
    - Consensus Building: Solution reflects collective wisdom
    """
    
    def __init__(self, llm, agents: Dict[str, Any], logger=None, planner=None):
        """
        Initialize Ubuntu Orchestrator
        
        Args:
            llm: Language model for coordination reasoning
            agents: Dictionary of available agents {name: agent_instance}
            logger: InvestigationLogger instance (optional)
            planner: ExplicitPlanner for collaboration planning (optional)
        """
        self.llm = llm
        self.agents = agents
        self.logger = logger
        self.planner = planner
        self.collaboration_history = []
        
        logging.info(" Ubuntu Orchestrator initialized")
        logging.info(f"   Available agents: {list(agents.keys())}")
    
    def orchestrate(self, 
                   complex_issue: str, 
                   lead_agent_name: str,
                   investigation_history: List[Dict]) -> Dict[str, Any]:
        """
        Orchestrate multi-agent collaboration on complex issue
        
        Pattern: Lead agent coordinates, subagents execute sequentially
        
        Args:
            complex_issue: The multi-domain problem
            lead_agent_name: Agent that detected need for collaboration
            investigation_history: Lead agent's investigation so far
            
        Returns:
            Coordinated solution from collective expertise
        """
        logging.info(f"\n{'='*70}")
        logging.info(f" UBUNTU ORCHESTRATION INITIATED")
        logging.info(f"{'='*70}")
        logging.info(f"Issue: {complex_issue}")
        logging.info(f"Lead Agent: {lead_agent_name}")
        logging.info(f"{'='*70}\n")
        
        collaboration_id = f"ubuntu_collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create Ubuntu collaboration plan (Deep Agents)
        collab_plan_id = None
        if self.planner:
            collab_plan_id = self.planner.create_plan(
                objective=f"Ubuntu Collaboration: {complex_issue}",
                agent_name="Ubuntu_Orchestrator",
                problem_context={
                    "type": "multi_agent_collaboration",
                    "lead_agent": lead_agent_name,
                    "issue": complex_issue,
                    "investigation_history": str(investigation_history)[:500]
                }
            )
            logging.info(f"\n🤝 Ubuntu Collaboration Plan: {collab_plan_id}\n")
        
        # STEP 1: LLM analyzes complexity and plans coordination
        plan = self._create_coordination_plan(
            complex_issue, 
            lead_agent_name, 
            investigation_history
        )
        
        logging.info(f" COORDINATION PLAN:")
        logging.info(f"   Required agents: {plan.get('required_agents', [])}")
        logging.info(f"   Execution order: {plan.get('execution_order', [])}")
        logging.info(f"   Approach: {plan.get('approach', 'sequential')}\n")
        
        # STEP 2: Execute sequential investigation
        findings = {
            lead_agent_name: {
                "agent": lead_agent_name,
                "investigation": investigation_history,
                "role": "lead_orchestrator"
            }
        }
        
        for agent_name in plan.get('execution_order', []):
            if agent_name in self.agents and agent_name != lead_agent_name:
                logging.info(f" {agent_name} investigating...")
                
                # Get agent's task from plan
                task = plan.get('agent_tasks', {}).get(agent_name, {})
                
                # Agent investigates their domain
                result = self._agent_investigate_subtask(
                    agent=self.agents[agent_name],
                    agent_name=agent_name,
                    issue=complex_issue,
                    task=task,
                    prior_findings=findings
                )
                
                findings[agent_name] = result
                
                logging.info(f"    {agent_name} completed investigation\n")
        
        # STEP 3: Lead agent synthesizes collective findings
        logging.info(f" {lead_agent_name} synthesizing collective findings...\n")
        
        synthesis = self._synthesize_collective_findings(
            complex_issue,
            lead_agent_name,
            findings,
            plan
        )
        
        # Record collaboration
        collaboration_record = {
            "collaboration_id": collaboration_id,
            "issue": complex_issue,
            "lead_agent": lead_agent_name,
            "participating_agents": list(findings.keys()),
            "execution_order": plan.get('execution_order', []),
            "findings": findings,
            "synthesis": synthesis,
            "timestamp": datetime.now().isoformat()
        }
        
        self.collaboration_history.append(collaboration_record)
        
        logging.info(f"{'='*70}")
        logging.info(f" UBUNTU ORCHESTRATION COMPLETE")
        logging.info(f"   Collaboration ID: {collaboration_id}")
        logging.info(f"   Agents participated: {len(findings)}")
        logging.info(f"{'='*70}\n")
        
        # Log orchestration event
        if self.logger:
            knowledge_articles = []  # TODO: Extract from context if available
            self.logger.log_orchestration(
                collab_id=collaboration_id,
                participating_agents=list(findings.keys()),
                root_cause=synthesis.get('root_cause', 'Multi-domain issue'),
                solution=synthesis.get('solution', 'Coordinated solution'),
                ubuntu_value=synthesis.get('ubuntu_value', 'Collective expertise'),
                knowledge_articles=knowledge_articles
            )
        
        return {
            "status": "UBUNTU_COLLABORATION_COMPLETE",
            "collaboration_id": collaboration_id,
            "root_cause": synthesis.get('root_cause'),
            "solution": synthesis.get('solution'),
            "collective_findings": findings,
            "ubuntu_value": synthesis.get('ubuntu_value'),
            "participating_agents": list(findings.keys())
        }
    
    def _create_coordination_plan(self,
                                  issue: str,
                                  lead_agent: str,
                                  history: List[Dict]) -> Dict[str, Any]:
        """
        LLM creates coordination plan for multi-agent investigation
        """
        history_summary = self._summarize_history(history)
        
        prompt = f"""You are coordinating a multi-agent Ubuntu collaboration.

Issue: {issue}
Lead Agent: {lead_agent}
Lead Agent's Investigation So Far: {history_summary}

Available Agents:
{self._format_available_agents()}

This is a complex multi-domain issue requiring collective expertise.

Create a coordination plan:
1. Which agents should investigate (besides lead)?
2. What should each agent investigate?
3. In what order (sequential execution)?

Respond in JSON format:
{{
    "approach": "sequential",
    "required_agents": ["agent1", "agent2"],
    "execution_order": ["agent1", "agent2"],
    "agent_tasks": {{
        "agent1": {{
            "focus": "What this agent should check",
            "questions": ["Specific question 1", "Specific question 2"]
        }},
        "agent2": {{
            "focus": "What this agent should check",
            "questions": ["Specific question 1", "Specific question 2"]
        }}
    }},
    "coordination_rationale": "Why these agents in this order"
}}"""

        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                import json
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                plan = json.loads(response_text[start:end])
            else:
                # Fallback plan
                plan = {
                    "approach": "sequential",
                    "required_agents": list(self.agents.keys())[:2],
                    "execution_order": list(self.agents.keys())[:2],
                    "agent_tasks": {},
                    "coordination_rationale": "Default coordination"
                }
            
            return plan
            
        except Exception as e:
            logging.error(f" Error creating plan: {e}")
            # Fallback: use available agents
            available = [name for name in self.agents.keys() if name != lead_agent][:2]
            return {
                "approach": "sequential",
                "required_agents": available,
                "execution_order": available,
                "agent_tasks": {},
                "coordination_rationale": "Automatic coordination"
            }
    
    def _agent_investigate_subtask(self,
                                   agent: Any,
                                   agent_name: str,
                                   issue: str,
                                   task: Dict,
                                   prior_findings: Dict) -> Dict[str, Any]:
        """
        Agent investigates their specific subtask
        """
        # Create context with prior findings
        context = {
            "subtask_mode": True,
            "focus": task.get('focus', 'Investigate your domain'),
            "questions": task.get('questions', []),
            "prior_findings": self._format_prior_findings(prior_findings)
        }
        
        # Agent investigates
        result = agent.investigate(issue, context)
        
        return {
            "agent": agent_name,
            "task": task,
            "investigation_result": result,
            "role": "specialist_contributor"
        }
    
    def _synthesize_collective_findings(self,
                                       issue: str,
                                       lead_agent: str,
                                       findings: Dict,
                                       plan: Dict) -> Dict[str, Any]:
        """
        LLM synthesizes collective findings into Ubuntu solution
        """
        findings_summary = []
        for agent_name, finding in findings.items():
            if agent_name == lead_agent:
                findings_summary.append(f"{agent_name} (Lead): Initial investigation detected multi-domain issue")
            else:
                result = finding.get('investigation_result', {})
                findings_summary.append(f"{agent_name}: {result.get('root_cause', 'Investigated domain')}")
        
        prompt = f"""You are synthesizing a Ubuntu collaboration.

Issue: {issue}

Collective Findings:
{chr(10).join(findings_summary)}

Based on collective investigation:
1. What is the ROOT CAUSE (considering all findings)?
2. What is the SOLUTION (that addresses all aspects)?
3. How did UBUNTU COLLABORATION help?

Respond in JSON format:
{{
    "root_cause": "The actual root cause based on collective findings",
    "solution": "Comprehensive solution addressing all aspects",
    "how_each_contributed": {{
        "agent_name": "Their specific contribution"
    }},
    "ubuntu_value": "How collective approach improved the solution",
    "key_insight": "What we learned together that no single agent would have found"
}}"""

        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                import json
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                synthesis = json.loads(response_text[start:end])
            else:
                synthesis = {
                    "root_cause": "Multi-domain issue identified",
                    "solution": "Coordinated solution from collective expertise",
                    "ubuntu_value": "Collective investigation provided complete picture"
                }
            
            return synthesis
            
        except Exception as e:
            logging.error(f" Error synthesizing: {e}")
            return {
                "root_cause": "Complex multi-domain issue",
                "solution": "Requires coordinated approach",
                "ubuntu_value": "Multiple perspectives needed"
            }
    
    def _summarize_history(self, history: List[Dict]) -> str:
        """Summarize investigation history"""
        if not history:
            return "No prior investigation"
        
        summary = []
        for step in history[-3:]:  # Last 3 steps
            tool = step.get('action', {}).get('tool_name', 'unknown')
            finding = step.get('reflection', {}).get('interpretation', '')
            finding = finding.replace('\\', '\\\\') # Escape backslashes for JSON
            summary.append(f"- Used {tool}: {finding[:100]}")
        
        return "\n".join(summary) if summary else "Initial investigation"
    
    def _format_available_agents(self) -> str:
        """Format available agents for LLM"""
        agent_list = []
        for name, agent in self.agents.items():
            if hasattr(agent, 'specialization'):
                agent_list.append(f"- {name}: {agent.specialization}")
            else:
                agent_list.append(f"- {name}")
        return "\n".join(agent_list)
    
    def _format_prior_findings(self, findings: Dict) -> str:
        """Format prior findings for agent context"""
        summary = []
        for agent_name, finding in findings.items():
            if isinstance(finding, dict) and 'investigation_result' in finding:
                result = finding['investigation_result']
                summary.append(f"{agent_name}: {result.get('root_cause', 'Investigated')[:100]}")
        return "\n".join(summary) if summary else "No prior findings"
    
    def get_collaboration_history(self) -> List[Dict]:
        """Get all collaboration history"""
        return self.collaboration_history
