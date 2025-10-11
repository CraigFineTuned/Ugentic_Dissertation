"""
Infrastructure Agent - ReAct Pattern + Ubuntu Orchestration
General-purpose LLM-guided diagnostic system + Multi-agent coordinator
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...core.ubuntu_orchestrator import UbuntuOrchestrator
from ...core.collaboration_detector import CollaborationDetector
from ...tools import (
    check_server_metrics,
    check_server_logs,
    check_service_status,
    check_disk_space,
    check_process_list,
    measure_server_response_time,
    get_system_uptime,
    check_backup_status
)


class InfrastructureAgentReAct:
    """
    Infrastructure Agent using ReAct pattern + Ubuntu Orchestration
    
    Role: Server/infrastructure issues + Lead orchestrator for complex problems
    Pattern: Full ReAct + Ubuntu Orchestration
    Domain: Infrastructure (servers, storage, backups, virtualization)
    
    Ubuntu Principles:
    - Collective Problem-Solving: Coordinates with other agents
    - Knowledge Sharing: Documents infrastructure insights
    - Mutual Support: Helps other teams understand infrastructure
    - Consensus Building: Involves teams in infrastructure decisions
    """
    
    def __init__(self, llm, name="Infrastructure", orchestrator=True, agents=None):
        """
        Initialize Infrastructure agent with ReAct engine and orchestration
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            orchestrator: Can this agent orchestrate collaborations?
            agents: Dict of other agents for orchestration
        """
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "Servers, Storage, Backups, Virtualization"
        self.is_orchestrator = orchestrator
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("infrastructure")
        self._register_tools()
        
        # Initialize ReAct engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=10
        )
        
        # Initialize Ubuntu orchestration (if orchestrator)
        self.ubuntu_orchestrator = None
        self.collaboration_detector = None
        if orchestrator and agents:
            self.ubuntu_orchestrator = UbuntuOrchestrator(llm=llm, agents=agents)
            self.collaboration_detector = CollaborationDetector(llm=llm)
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
        
        logging.info(f" {self.name} Agent initialized with ReAct pattern")
        logging.info(f"   Tools: {self.tools.count()}")
        logging.info(f"   Orchestrator: {self.is_orchestrator}")
        if self.is_orchestrator and self.ubuntu_orchestrator:
            logging.info(f"   Ubuntu Orchestration: Enabled")
    
    def _register_tools(self):
        """Register infrastructure diagnostic tools"""
        
        self.tools.register(
            check_server_metrics,
            "Checks actual server CPU, memory, disk usage. Returns real-time performance data."
        )
        
        self.tools.register(
            check_server_logs,
            "Reads server error logs for specified timeframe. Returns error summaries and patterns."
        )
        
        self.tools.register(
            check_service_status,
            "Checks if specific service is running. Returns service state, uptime, restart count."
        )
        
        self.tools.register(
            check_disk_space,
            "Checks disk space on all mounted drives. Returns usage percentages and critical alerts."
        )
        
        self.tools.register(
            check_process_list,
            "Gets list of running processes sorted by resource usage. Returns top CPU/memory consumers."
        )
        
        self.tools.register(
            measure_server_response_time,
            "Measures server response time for basic operations. Returns latency and status."
        )
        
        self.tools.register(
            get_system_uptime,
            "Gets system uptime. Returns boot time and uptime duration."
        )
        
        self.tools.register(
            check_backup_status,
            "Checks backup status and last backup time. Returns backup health and schedule."
        )
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate infrastructure problem using ReAct pattern
        Triggers Ubuntu orchestration for multi-domain issues
        
        Args:
            problem_report: User's problem description
            context: Additional context (user info, system state)
            
        Returns:
            Investigation result with root cause and solution
        """
        logging.info(f"\n{'='*60}")
        logging.info(f" {self.name} Agent - Starting Investigation")
        logging.info(f"{'='*60}")
        logging.info(f"Problem: {problem_report}")
        logging.info(f"{'='*60}\n")
        
        # Use ReAct engine to investigate
        result = self.react_engine.investigate(problem_report, context)
        
        # Check if collaboration needed (only if we're orchestrator)
        if result.get('status') == 'NEEDS_COLLABORATION':
            if self.is_orchestrator and self.ubuntu_orchestrator:
                logging.info("\n Multi-domain issue detected - Initiating Ubuntu Orchestration")
                
                # Get investigation history
                history = self.get_investigation_history()
                
                # Orchestrate collaboration
                collaboration_result = self.ubuntu_orchestrator.orchestrate(
                    complex_issue=problem_report,
                    lead_agent_name=self.name,
                    investigation_history=[
                        {
                            'action': step.action,
                            'observation': step.observation,
                            'reflection': step.reflection
                        }
                        for step in history
                    ]
                )
                
                return collaboration_result
            else:
                logging.warning(" Collaboration needed but orchestration not available")
                return result
        
        # Alternative: Check if investigation suggests multi-domain
        if self.is_orchestrator and self.collaboration_detector and len(self.get_investigation_history()) > 0:
            needs_collab, collab_details = self.collaboration_detector.should_collaborate(
                agent_name=self.name,
                problem=problem_report,
                investigation_history=[
                    {
                        'action': step.action,
                        'observation': step.observation,
                        'reflection': step.reflection
                    }
                    for step in self.get_investigation_history()
                ]
            )
            
            if needs_collab and collab_details.get('confidence', 0) > 0.7:
                logging.info("\n Collaboration detected as beneficial - Initiating Ubuntu Orchestration")
                
                collaboration_result = self.ubuntu_orchestrator.orchestrate(
                    complex_issue=problem_report,
                    lead_agent_name=self.name,
                    investigation_history=[
                        {
                            'action': step.action,
                            'observation': step.observation,
                            'reflection': step.reflection
                        }
                        for step in self.get_investigation_history()
                    ]
                )
                
                return collaboration_result
        
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
            "is_orchestrator": self.is_orchestrator,
            "orchestration_enabled": self.ubuntu_orchestrator is not None,
            "tools_available": self.tools.count(),
            "ubuntu_principles": self.ubuntu_principles,
            "reports_to": "IT Manager",
            "pattern": "ReAct (Reasoning + Acting) + Ubuntu Orchestration"
        }
