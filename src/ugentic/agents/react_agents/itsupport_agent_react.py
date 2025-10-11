"""
IT Support Agent - ReAct Pattern Implementation
General-purpose LLM-guided diagnostic system for user support issues
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...tools import (
    get_user_profile,
    check_user_permissions,
    reset_user_password,
    unlock_user_account,
    check_printer_status,
    verify_email_config,
    test_remote_access,
    check_software_installation,
    get_recent_tickets
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
    
    def __init__(self, llm, name="IT Support"):
        """
        Initialize IT Support agent with ReAct engine
        
        Args:
            llm: Language model for reasoning
            name: Agent name
        """
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "User Support, Basic Troubleshooting, Account Management"
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("user_support")
        self._register_tools()
        
        # Initialize ReAct engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=8  # Shorter for simpler issues
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
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate user support issue using ReAct pattern
        
        Args:
            problem_report: User's problem description
            context: Additional context (user_id, etc.)
            
        Returns:
            Investigation result with root cause and solution
        """
        logging.info(f"\n{'='*60}")
        logging.info(f" {self.name} Agent - Starting Investigation")
        logging.info(f"{'='*60}")
        logging.info(f"Problem: {problem_report}")
        if context and 'user_id' in context:
            logging.info(f"User: {context['user_id']}")
        logging.info(f"{'='*60}\n")
        
        result = self.react_engine.investigate(problem_report, context)
        
        if result.get('status') == 'NEEDS_COLLABORATION':
            logging.info("\n Escalation needed to specialist team")
            logging.info(f"   Required agents: {result.get('required_agents', [])}")
        
        return result
    
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
