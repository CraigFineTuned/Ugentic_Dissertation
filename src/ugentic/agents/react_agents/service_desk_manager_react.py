"""
Service Desk Manager Agent - ReAct Pattern Implementation
Team coordination and support operation management
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...tools import (
    get_technician_workload,
    get_team_availability,
    check_skill_match,
    get_open_tickets,
    get_sla_status,
    get_escalation_history,
    search_knowledge_base
)


class ServiceDeskManagerAgentReAct:
    """
    Service Desk Manager Agent using ReAct pattern
    
    Role: Coordinate support operations, manage team, bridge strategic and operational
    Pattern: Team coordination + simple ReAct
    Domain: Team management, ticket assignment, escalations
    
    Ubuntu Principles:
    - Collective Problem-Solving: Coordinates team resources
    - Knowledge Sharing: Facilitates team learning
    - Mutual Support: Ensures team is supported
    - Consensus Building: Team decision-making
    """
    
    def __init__(self, llm, name="Service Desk Manager", logger=None, planner=None):
        """
        Initialize Service Desk Manager agent with ReAct engine
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            logger: InvestigationLogger instance for logging
            planner: ExplicitPlanner instance for structured planning
        """
        self.name = name
        self.agent_type = "Tactical"
        self.specialization = "Support Operations, Team Coordination, Escalation Management"
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("team_management")
        self._register_tools()
        
        # Initialize ReAct engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=8,
            logger=logger,
            planner=planner
        )
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "team_coordination": True
        }
        
        logging.info(f" {self.name} Agent initialized with ReAct pattern")
        logging.info(f"   Tools: {self.tools.count()}")
    
    def _register_tools(self):
        """Register team management tools"""
        
        self.tools.register(
            get_technician_workload,
            "Gets current workload for all technicians. Returns open tickets, status, specialization per tech."
        )
        
        self.tools.register(
            get_team_availability,
            "Gets team availability status. Returns available techs, estimated wait times."
        )
        
        self.tools.register(
            check_skill_match,
            "Checks which technician is best suited for issue type. Returns best match and confidence."
        )
        
        self.tools.register(
            get_open_tickets,
            "Gets all open tickets in queue. Returns prioritized list with SLA status."
        )
        
        self.tools.register(
            get_sla_status,
            "Gets SLA status for specific ticket. Returns time remaining, breach risk."
        )
        
        self.tools.register(
            get_escalation_history,
            "Gets recent escalation history. Returns common escalation patterns and reasons."
        )
        
        self.tools.register(
            search_knowledge_base,
            "Searches knowledge base for solutions. Returns relevant articles and success rates."
        )
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate team/coordination issue using ReAct pattern
        
        Args:
            problem_report: Issue description
            context: Additional context
            
        Returns:
            Investigation result with solution
        """
        logging.info(f"\n{'='*60}")
        logging.info(f"👔 {self.name} Agent - Starting Investigation")
        logging.info(f"{'='*60}")
        logging.info(f"Problem: {problem_report}")
        logging.info(f"{'='*60}\n")
        
        result = self.react_engine.investigate(problem_report, context)
        
        return result
    
    def delegate_to_technician(self, issue: str, context: Dict = None) -> Dict[str, Any]:
        """
        Delegate issue to appropriate technician
        Uses ReAct to determine best assignment
        """
        delegation_context = context or {}
        delegation_context['delegation_mode'] = True
        
        return self.investigate(f"Delegate this issue: {issue}", delegation_context)
    
    def get_investigation_history(self):
        """Get complete ReAct investigation history"""
        return self.react_engine.get_full_history()
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_name": self.name,
            "agent_type": self.agent_type,
            "specialization": self.specialization,
            "tools_available": self.tools.count(),
            "ubuntu_principles": self.ubuntu_principles,
            "reports_to": "IT Manager",
            "manages": "IT Support Technicians",
            "pattern": "ReAct (Reasoning + Acting)"
        }
