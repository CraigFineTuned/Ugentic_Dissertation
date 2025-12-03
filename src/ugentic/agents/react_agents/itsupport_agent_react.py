"""
IT Support Agent - ReAct Pattern Implementation
General-purpose LLM-guided diagnostic system for user support issues
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...core.diagnostic_trees import DiagnosticTrees
from ...tools import (
    get_user_profile,
    check_user_permissions,
    reset_user_password,
    unlock_user_account,
    check_printer_status,
    verify_email_config,
    test_remote_access,
    check_software_installation,
    get_recent_tickets,
    ask_questions
)


class ITSupportAgentReAct:
    """
    IT Support Agent using ReAct pattern
    
    Role: Front-line user support, basic troubleshooting
    Pattern: ReAct for user issues
    Domain: User accounts, permissions, basic IT issues
    
    Ubuntu Principles:
    - Collective Problem-Solving: Escalates complex issues, learns from team
    - Knowledge Sharing: Documents common solutions
    - Mutual Support: Helps users and teammates
    - Consensus Building: Involves users in solutions
    """
    
    def __init__(self, llm, name="IT Support", logger=None, planner=None):
        """
        Initialize IT Support agent with ReAct engine
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            logger: InvestigationLogger instance for logging
            planner: ExplicitPlanner instance for structured planning
        """
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "User Support, Basic Troubleshooting, Account Management"
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("user_support")
        self._register_tools()
        
        # SESSION 30 OPTIMIZATION: Initialize diagnostic trees
        self.diagnostic_trees = DiagnosticTrees()
        
        # Initialize ReAct engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=8,  # Shorter for simpler issues
            logger=logger,
            planner=planner
        )
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "user_empathy": True
        }
        
        logging.info(f" {self.name} Agent initialized with ReAct pattern")
        logging.info(f"   Tools: {self.tools.count()}")
        logging.info(f"   Diagnostic Trees: {len(self.diagnostic_trees.get_available_trees())} (SESSION 30 optimization)")
    
    def _register_tools(self):
        """Register IT support diagnostic tools"""
        
        self.tools.register(
            get_user_profile,
            "Gets user profile information. Returns account status, department, password expiry, groups."
        )
        
        self.tools.register(
            check_user_permissions,
            "Checks user permissions for specific resource. Returns access level and permissions."
        )
        
        self.tools.register(
            reset_user_password,
            "Resets user password. Generates temporary password that must be changed on login."
        )
        
        self.tools.register(
            unlock_user_account,
            "Unlocks locked user account. Returns success status and new account state."
        )
        
        self.tools.register(
            check_printer_status,
            "Checks printer status. Returns online status, queue, paper/toner levels."
        )
        
        self.tools.register(
            verify_email_config,
            "Verifies email configuration for user. Checks server settings, authentication, connectivity."
        )
        
        self.tools.register(
            test_remote_access,
            "Tests remote access (VPN) for user. Verifies connection and returns status."
        )
        
        self.tools.register(
            check_software_installation,
            "Checks if software is installed on user's machine. Returns version and license status."
        )
        
        self.tools.register(
            get_recent_tickets,
            "Gets recent support tickets for user. Returns ticket history and current status."
        )
        
        self.tools.register(
            ask_questions,
            "Asks questions to gather additional information for troubleshooting. Queries knowledge base or simulates user inquiry. Returns contextualized answers."
        )
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate user support issue using ReAct pattern

        ARCHITECTURAL CHANGE (Dec 3, 2025):
        IT Support is now Level 1 entry point - attempts resolution first,
        escalates to Service Desk Manager if beyond capabilities

        Args:
            problem_report: User's problem description
            context: Additional context (user_id, etc.)

        Returns:
            Investigation result with root cause and solution OR escalation details
        """
        logging.info(f"\n{'='*60}")
        logging.info(f"🎧 {self.name} Agent - Level 1 Investigation")
        logging.info(f"{'='*60}")
        logging.info(f"Problem: {problem_report}")
        if context and 'user_id' in context:
            logging.info(f"User: {context['user_id']}")
        logging.info(f"{'='*60}\n")

        # SESSION 30 OPTIMIZATION: Identify problem type and provide diagnostic tree
        problem_type = self.diagnostic_trees.identify_problem_type(problem_report)
        diagnostic_tree = self.diagnostic_trees.get_diagnostic_tree(problem_type)

        if diagnostic_tree:
            logging.info(f"📋 Diagnostic tree identified: {problem_type.upper()}")
            logging.info(f"   Providing {len(diagnostic_tree)}-step procedure to guide investigation\n")

            # Add tree to context for ReAct engine
            if context is None:
                context = {}
            context['diagnostic_tree'] = self.diagnostic_trees.format_tree_for_prompt(diagnostic_tree)
            context['problem_type'] = problem_type
        else:
            logging.info(f"   No specific diagnostic tree for this issue - using general ReAct pattern\n")

        # Attempt Level 1 resolution
        result = self.react_engine.investigate(problem_report, context)

        # ARCHITECTURAL CHANGE: Check if escalation needed
        should_escalate, escalation_details = self._should_escalate(problem_report, result)

        if should_escalate:
            logging.info("\n⬆️  ESCALATION REQUIRED")
            logging.info(f"   Reason: {escalation_details.get('reason')}")
            logging.info(f"   Type: {escalation_details.get('type')}")
            if 'suggested_specialist' in escalation_details:
                logging.info(f"   Suggested: {escalation_details.get('suggested_specialist')}\n")

            return {
                'status': 'NEEDS_ESCALATION',
                'escalation_details': escalation_details,
                'level1_findings': result,
                'agent': self.name
            }

        # Level 1 resolution successful
        logging.info("\n✅ Level 1 Resolution Complete")
        return result

    def _should_escalate(self, problem_report: str, investigation_result: Dict) -> tuple:
        """
        Determine if issue should escalate to Service Desk Manager

        LEVEL 1 ESCALATION TRIGGERS:
        - Needs specialist tools (network, app, infrastructure diagnostics)
        - Department-wide impact (affects multiple users)
        - Strategic decision needed (policy, budget, approval)
        - Multi-agent collaboration explicitly requested (NEEDS_COLLABORATION)

        DOES NOT ESCALATE:
        - Simple Level 1 issues (password, basic printer, account access)
        - Investigation exhausted iterations but is Level 1 domain (attempt with tools directly)

        TUNING (Dec 3): Only escalate if truly needs specialist, not just failed investigation

        Args:
            problem_report: Original problem description
            investigation_result: Result from ReAct investigation

        Returns:
            (should_escalate: bool, escalation_details: dict)
        """
        status = investigation_result.get('status', 'UNKNOWN')

        # Already resolved at Level 1 - no escalation
        if status == 'RESOLVED':
            logging.info("   Level 1 resolution successful - no escalation needed")
            return False, None

        # Check for specialist tool needs FIRST (highest priority)
        if self._needs_specialist_tools(problem_report, investigation_result):
            specialist = self._suggest_specialist(problem_report, investigation_result)
            return True, {
                'type': 'technical',
                'reason': f'Requires {specialist} specialist tools/expertise',
                'suggested_specialist': specialist
            }

        # Check for department-wide impact
        if self._is_department_wide(problem_report):
            return True, {
                'type': 'technical',
                'reason': 'Department-wide issue requires coordination',
                'suggested_specialist': 'Infrastructure'  # Orchestrator for multi-domain
            }

        # Check for strategic decision needs
        if self._needs_strategic_decision(problem_report):
            return True, {
                'type': 'strategic',
                'reason': 'Requires management approval/policy decision'
            }

        # NEEDS_COLLABORATION: Multi-domain issue detected during investigation
        if status == 'NEEDS_COLLABORATION':
            return True, {
                'type': 'technical',
                'reason': 'Multi-domain issue requires specialist collaboration',
                'suggested_specialist': 'Infrastructure'  # Orchestrator
            }

        # TUNING (Dec 3): Check if this is a common Level 1 issue before escalating
        if self._is_common_level1_issue(problem_report):
            logging.info("   Common Level 1 issue - attempting resolution without escalation")
            logging.info("   Issue may require direct tool execution rather than investigation")
            # Don't escalate - return False to attempt resolution
            return False, None

        # Only escalate if none of the above conditions met AND investigation truly stuck
        # This catches edge cases where investigation failed but isn't a specialist issue
        iterations = investigation_result.get('iterations', 0)
        if iterations < 3:
            # Investigation didn't try enough - don't escalate yet
            logging.info(f"   Investigation only completed {iterations} iterations - no escalation")
            return False, None

        # Final fallback: escalate for truly unresolvable issues
        return True, {
            'type': 'technical',
            'reason': 'Level 1 unable to resolve after thorough investigation',
            'suggested_specialist': self._suggest_specialist(problem_report, investigation_result)
        }

    def _needs_specialist_tools(self, problem_report: str, result: Dict) -> bool:
        """Check if issue requires specialist diagnostic tools"""
        problem_lower = problem_report.lower()

        # Network specialist indicators
        network_indicators = ['network', 'connectivity', 'dns', 'firewall', 'bandwidth',
                            'latency', 'routing', 'wifi', 'ethernet', 'vpn slow']

        # App specialist indicators
        app_indicators = ['application', 'app crash', 'database', 'query', 'error message',
                         'slow performance', 'timeout', 'integration']

        # Infrastructure specialist indicators
        infra_indicators = ['server', 'disk space', 'cpu', 'memory', 'service down',
                          'backup', 'virtual machine', 'container']

        # Check if problem mentions specialist domains
        if any(indicator in problem_lower for indicator in network_indicators):
            return True
        if any(indicator in problem_lower for indicator in app_indicators):
            return True
        if any(indicator in problem_lower for indicator in infra_indicators):
            return True

        return False

    def _is_department_wide(self, problem_report: str) -> bool:
        """Check if issue affects entire department/multiple users"""
        problem_lower = problem_report.lower()

        department_indicators = [
            'entire department', 'whole team', 'all users', 'everyone',
            'multiple users', 'several people', 'team', 'department',
            'company-wide', 'organization', 'everyone in'
        ]

        return any(indicator in problem_lower for indicator in department_indicators)

    def _needs_strategic_decision(self, problem_report: str) -> bool:
        """Check if issue requires strategic/management decision"""
        problem_lower = problem_report.lower()

        strategic_indicators = [
            'budget', 'purchase', 'approval', 'policy', 'new software',
            'license', 'contract', 'vendor', 'upgrade all', 'department policy'
        ]

        return any(indicator in problem_lower for indicator in strategic_indicators)

    def _is_common_level1_issue(self, problem_report: str) -> bool:
        """
        Check if this is a common Level 1 issue that IT Support should handle
        without escalation, even if initial investigation struggled

        TUNING (Dec 3): Added to prevent premature escalation of basic issues
        """
        problem_lower = problem_report.lower()

        # Common Level 1 issues that should NOT escalate
        level1_indicators = [
            # Password & Account Access
            'password', 'locked account', 'cannot login', 'forgot password',
            'password expired', 'password reset', 'unlock account',

            # Basic Printer Issues
            'printer', 'print', 'printing', 'cannot print', 'printer offline',

            # Basic Email Issues
            'email', 'outlook', 'cannot send email', 'email not working',

            # Software Access
            'cannot access', 'access denied', 'need access to',

            # VPN Basics
            'vpn not working', 'vpn connection', 'cannot connect vpn',

            # User Profile
            'user profile', 'profile settings', 'account settings'
        ]

        return any(indicator in problem_lower for indicator in level1_indicators)

    def _suggest_specialist(self, problem_report: str, result: Dict) -> str:
        """Suggest which specialist should handle escalation"""
        problem_lower = problem_report.lower()

        # Check for network issues
        if any(word in problem_lower for word in ['network', 'connectivity', 'dns',
                                                    'firewall', 'bandwidth', 'wifi']):
            return 'Network Support'

        # Check for application issues
        if any(word in problem_lower for word in ['application', 'app', 'database',
                                                    'crash', 'error', 'slow app']):
            return 'App Support'

        # Default to Infrastructure (can orchestrate if multi-domain)
        return 'Infrastructure'
    
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
            "reports_to": "Service Desk Manager",
            "pattern": "ReAct (Reasoning + Acting)"
        }
