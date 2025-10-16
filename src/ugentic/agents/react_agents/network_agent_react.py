"""
Network Support Agent - ReAct Pattern Implementation
General-purpose LLM-guided diagnostic system for network issues
"""

import logging
from typing import Dict, Any
from ...core.react_engine import ReactEngine
from ...core.tool_registry import ToolRegistry
from ...tools import (
    check_network_bandwidth,
    ping_test,
    check_dns_resolution,
    traceroute,
    measure_network_latency,
    check_firewall_rules,
    get_network_utilization
)


class NetworkSupportAgentReAct:
    """
    Network Support Agent using ReAct pattern
    
    Role: Network connectivity, performance, and security issues
    Pattern: Full ReAct in network domain
    Domain: Network (connectivity, bandwidth, routing, security)
    
    Ubuntu Principles:
    - Collective Problem-Solving: Collaborates with Infrastructure/App teams
    - Knowledge Sharing: Documents network insights
    - Mutual Support: Helps others understand network issues
    - Consensus Building: Involves teams in network changes
    """
    
    def __init__(self, llm, name="Network Support", logger=None, planner=None):
        """
        Initialize Network Support agent with ReAct engine
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            logger: InvestigationLogger instance (optional)
            planner: ExplicitPlanner instance for structured planning
        """
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "Network Connectivity, Performance, Security"
        self.llm = llm
        
        # Initialize tool registry
        self.tools = ToolRegistry("network")
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
        """Register network diagnostic tools"""
        
        self.tools.register(
            check_network_bandwidth,
            "Measures actual network bandwidth and latency. Tests download/upload speed, packet loss, jitter."
        )
        
        self.tools.register(
            ping_test,
            "Tests connectivity to host with ping. Measures latency and packet loss over multiple attempts."
        )
        
        self.tools.register(
            check_dns_resolution,
            "Tests DNS resolution for a domain. Verifies DNS is working and measures resolution time."
        )
        
        self.tools.register(
            traceroute,
            "Traces network path to destination. Identifies slow hops and connectivity issues along the route."
        )
        
        self.tools.register(
            measure_network_latency,
            "Measures network latency between source and destination. Tests round-trip time."
        )
        
        self.tools.register(
            check_firewall_rules,
            "Gets firewall configuration. Returns active rules, blocked ports, recent blocks."
        )
        
        self.tools.register(
            get_network_utilization,
            "Gets current network interface utilization. Returns bytes sent/received, errors, drops."
        )
    
    def investigate(self, problem_report: str, context: Dict = None) -> Dict[str, Any]:
        """
        Investigate network problem using ReAct pattern
        
        Args:
            problem_report: User's problem description
            context: Additional context
            
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
