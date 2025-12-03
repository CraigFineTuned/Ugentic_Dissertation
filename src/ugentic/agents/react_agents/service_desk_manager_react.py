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
    
    def route_escalation(self, issue: str, level1_findings: Dict, context: Dict = None) -> str:
        """
        Route escalated ticket to appropriate specialist

        ARCHITECTURAL CHANGE (Dec 3, 2025):
        Service Desk Manager now coordinates Level 1 → Level 2 escalations
        Uses Level 1 findings + workload balancing + skill matching

        Args:
            issue: Original problem description
            level1_findings: Investigation results from IT Support (Level 1)
            context: Additional context

        Returns:
            Name of specialist agent to handle escalation
        """
        logging.info(f"\n{'='*60}")
        logging.info(f"📋 {self.name} - Routing Escalation")
        logging.info(f"{'='*60}")
        logging.info(f"Issue: {issue}")
        logging.info(f"Level 1 Agent: {level1_findings.get('agent', 'Unknown')}")

        escalation_details = level1_findings.get('escalation_details', {})
        suggested_specialist = escalation_details.get('suggested_specialist')

        logging.info(f"Level 1 Suggestion: {suggested_specialist}")
        logging.info(f"Escalation Reason: {escalation_details.get('reason', 'N/A')}")
        logging.info(f"{'='*60}\n")

        # TUNING (Dec 3): Validate escalation before routing
        # Defense-in-depth: catch issues that shouldn't have escalated
        if self._should_stay_at_level1(issue, escalation_details):
            logging.info("⚠️  Escalation validation failed - this is a Level 1 issue")
            logging.info("   Routing back to IT Support for direct resolution\n")
            return 'IT Support'

        # Use Level 1 suggestion if available
        if suggested_specialist:
            # Verify suggestion is appropriate
            validated_specialist = self._validate_specialist_suggestion(
                issue, suggested_specialist, escalation_details
            )

            # Verify specialist is available and not overloaded
            specialist = self._verify_specialist_availability(validated_specialist)
            logging.info(f"✅ Routing to: {specialist}\n")
            return specialist

        # Fallback: Use skill matching
        logging.info("No suggestion from Level 1, using skill matching...")
        specialist = self._match_specialist_by_skill(issue)
        logging.info(f"✅ Skill match: {specialist}\n")
        return specialist

    def _verify_specialist_availability(self, suggested_specialist: str) -> str:
        """
        Verify specialist is available and not overloaded

        TODO: In production, this would check:
        - Current workload (get_technician_workload tool)
        - SLA status (get_sla_status tool)
        - Skill match (check_skill_match tool)

        For now: Return suggestion as-is (research prototype)
        """
        # In production, would check workload:
        # workload = self.tools.execute('get_technician_workload', {})
        # if workload for suggested_specialist is too high, route to alternate

        return suggested_specialist

    def _should_stay_at_level1(self, issue: str, escalation_details: Dict) -> bool:
        """
        Validate if issue truly needs escalation or should stay at Level 1

        TUNING (Dec 3): Defense-in-depth validation to catch misrouted issues

        Returns:
            True if issue should stay at Level 1 (don't escalate)
            False if escalation is appropriate
        """
        issue_lower = issue.lower()

        # Common Level 1 issues that should NOT reach Service Desk
        level1_only_issues = [
            'password reset', 'password expired', 'forgot password',
            'locked account', 'unlock account', 'cannot login',
            'printer offline', 'basic printer', 'printer access',
            'email not working', 'outlook issue', 'cannot send email',
            'need access', 'access denied', 'user profile'
        ]

        # Check if this is clearly a Level 1 issue
        is_level1_issue = any(indicator in issue_lower for indicator in level1_only_issues)

        # Check escalation reason - if it says "unable to resolve", verify it's not a simple issue
        reason = escalation_details.get('reason', '').lower()
        weak_escalation = 'unable to resolve' in reason and is_level1_issue

        if weak_escalation:
            logging.info(f"   Detected weak escalation: Level 1 issue with generic reason")
            return True

        return False

    def _validate_specialist_suggestion(self, issue: str, suggested: str,
                                       escalation_details: Dict) -> str:
        """
        Validate and potentially override Level 1 specialist suggestion

        TUNING (Dec 3): Ensure routing matches actual issue domain

        Args:
            issue: Problem description
            suggested: Specialist suggested by Level 1
            escalation_details: Escalation details from Level 1

        Returns:
            Validated specialist name (may differ from suggestion)
        """
        issue_lower = issue.lower()

        # Strong indicators for each specialist
        network_strong = ['network slow', 'dns', 'firewall', 'bandwidth', 'routing', 'wifi down']
        app_strong = ['application crash', 'database error', 'app timeout', 'integration failure']
        infra_strong = ['server down', 'disk space', 'service unavailable', 'cpu high']

        # Override if suggestion doesn't match strong indicators
        if any(indicator in issue_lower for indicator in network_strong):
            if suggested != 'Network Support':
                logging.info(f"   Overriding suggestion: {suggested} → Network Support (strong network indicators)")
                return 'Network Support'

        if any(indicator in issue_lower for indicator in app_strong):
            if suggested != 'App Support':
                logging.info(f"   Overriding suggestion: {suggested} → App Support (strong app indicators)")
                return 'App Support'

        if any(indicator in issue_lower for indicator in infra_strong):
            if suggested != 'Infrastructure':
                logging.info(f"   Overriding suggestion: {suggested} → Infrastructure (strong infra indicators)")
                return 'Infrastructure'

        # Suggestion is appropriate
        return suggested

    def _match_specialist_by_skill(self, issue: str) -> str:
        """
        Match issue to specialist based on skill/expertise

        Pattern matching similar to IT Manager triage (pre-refactor),
        but used as fallback when Level 1 doesn't suggest specialist
        """
        issue_lower = issue.lower()

        # Network specialist keywords
        if any(word in issue_lower for word in ['network', 'connectivity', 'dns', 'firewall', 'wifi']):
            return 'Network Support'

        # App specialist keywords
        if any(word in issue_lower for word in ['application', 'app', 'database', 'crash', 'error']):
            return 'App Support'

        # Infrastructure (default, can orchestrate if needed)
        return 'Infrastructure'

    def delegate_to_technician(self, issue: str, context: Dict = None) -> Dict[str, Any]:
        """
        Delegate issue to appropriate technician
        Uses ReAct to determine best assignment

        NOTE: This method is for internal team management,
        not for Level 1 → Level 2 escalations (use route_escalation instead)
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
