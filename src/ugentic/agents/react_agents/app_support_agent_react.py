"""
App Support Agent - ReAct Pattern Implementation
General-purpose LLM-guided diagnostic system for application issues
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...tools import (
    query_app_logs,
    check_app_response_time,
    get_user_session_data,
    check_app_availability,
    get_app_error_rate,
    check_app_database_performance,
    check_client_metrics
)


class AppSupportAgentReAct:
    """
    Application Support Agent using ReAct pattern
    
    Role: Application-specific issues, bugs, performance
    Pattern: Full ReAct in application domain
    Domain: Applications (crashes, performance, errors, integrations)
    
    Ubuntu Principles:
    - Collective Problem-Solving: Collaborates with Infrastructure/Network
    - Knowledge Sharing: Documents application behavior patterns
    - Mutual Support: Helps users and other teams
    - Consensus Building: Involves teams in app changes
    """
    
    def __init__(self, llm, name="App Support", logger=None, planner=None):
        """
        Initialize App Support agent with ReAct engine
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            logger: InvestigationLogger instance (optional)
            planner: ExplicitPlanner instance for structured planning
        """
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "Business Applications, Databases, Custom Software"
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("application")
        self._register_tools()
        
        # Initialize ReAct engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=10,
            logger=logger,
            planner=planner
        )
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
        
        logging.info(f" {self.name} Agent initialized with ReAct pattern")
        logging.info(f"   Tools: {self.tools.count()}")
    
    def _register_tools(self):
        """Register application diagnostic tools"""
        
        self.tools.register(
            query_app_logs,
            "Gets application logs for specific user/timeframe. Returns errors, warnings, crashes with timestamps."
        )
        
        self.tools.register(
            check_app_response_time,
            "Measures application response time. Tests specific operations like login, returns avg/max/min latency."
        )
        
        self.tools.register(
            get_user_session_data,
            "Gets active session information for user. Returns session duration, last activity, device info."
        )
        
        self.tools.register(
            check_app_availability,
            "Checks if application is available and responding. Returns uptime percentage and status."
        )
        
        self.tools.register(
            get_app_error_rate,
            "Gets application error rate over timeframe. Returns total requests, error count, error percentage."
        )
        
        self.tools.register(
            check_app_database_performance,
            "Checks database performance for application. Returns query times, slow queries, connection pool status."
        )
        
        self.tools.register(
            check_client_metrics,
            "Gets metrics from user's client machine. Returns CPU, memory, disk usage on user's computer."
        )
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate application problem using ReAct pattern
        
        Args:
            problem_report: User's problem description
            context: Additional context (user_id, app_name, etc.)
            
        Returns:
            Investigation result with root cause and solution
        """
        logging.info(f"\n{'='*60}")
        logging.info(f" {self.name} Agent - Starting Investigation")
        logging.info(f"{'='*60}")
        logging.info(f"Problem: {problem_report}")
        logging.info(f"{'='*60}\n")
        
        result = self.react_engine.investigate(problem_report, context)
        
        if result.get('status') == 'NEEDS_COLLABORATION':
            logging.info("\n Multi-domain issue detected")
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
            "reports_to": "IT Manager",
            "pattern": "ReAct (Reasoning + Acting)"
        }
