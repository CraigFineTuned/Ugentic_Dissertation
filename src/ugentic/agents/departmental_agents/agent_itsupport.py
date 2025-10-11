# Agent_ITSupport - IT Support Technician AI Agent
# UGENTIC Framework - Departmental AI Agent
# Ubuntu Principle: "I am because we are" - This agent exists through its relationships with other departmental agents

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime

class SupportPriority(Enum):
    """Support ticket priority levels based on real IT Support workflows"""
    CRITICAL = "critical"  # System down, major business impact
    HIGH = "high"         # Significant functionality affected
    MEDIUM = "medium"     # Minor functionality affected
    LOW = "low"           # Enhancement requests, minor issues

class EscalationLevel(Enum):
    """Escalation levels reflecting real departmental collaboration"""
    L1_SUPPORT = "l1_support"           # First line support
    L2_INFRASTRUCTURE = "l2_infrastructure"  # Escalate to server team
    L3_APPLICATION = "l3_application"    # Escalate to app support
    MANAGEMENT = "management"            # Service desk manager
    EXTERNAL = "external"               # Vendor support

@dataclass
class SupportTicket:
    """Support ticket structure based on real IT workflows"""
    ticket_id: str
    user_name: str
    issue_description: str
    priority: SupportPriority
    category: str  # Hardware, Software, Network, Access, etc.
    time_reported: datetime
    estimated_resolution_time: Optional[int] = None  # minutes
    requires_escalation: bool = False
    escalation_target: Optional[EscalationLevel] = None
    ubuntu_collaboration_needed: bool = False  # Requires collective support

class Agent_ITSupport:
    """
    IT Support Technician AI Agent
    
    Behavioral Patterns Based on Real Department Analysis:
    - Rapid decision-making under pressure
    - Heavy cross-team collaboration requirements
    - User communication and empathy focus
    - Documentation and knowledge sharing emphasis
    
    Ubuntu Integration:
    - Exists through relationships with other IT departments
    - Seeks collective solutions when individual expertise insufficient
    - Supports other departments proactively
    - Shares knowledge for collective benefit
    """
    
    def __init__(self, agent_id: str, knowledge_base: Dict[str, Any]):
        self.agent_id = agent_id
        self.knowledge_base = knowledge_base
        self.current_tickets: List[SupportTicket] = []
        self.resolved_tickets: List[SupportTicket] = []
        self.collaboration_requests: List[Dict] = []
        
        # Ubuntu principle: This agent exists through others
        self.departmental_relationships = {
            "server_infrastructure": None,  # Will be set when Agent_ServerInfra is available
            "app_support": None,           # Will be set when Agent_AppSupport is available
            "service_desk_manager": None,  # Will be set when Agent_ServiceDesk is available
            "it_manager": None             # Will be set when Agent_ITManager is available
        }
        
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
        
        logging.info(f"Agent_ITSupport {agent_id} initialized with Ubuntu principles")
    
    def analyze_support_request(self, ticket: SupportTicket) -> Dict[str, Any]:
        """
        Analyze support request using real IT Support decision patterns
        
        Behavioral Pattern: Rapid assessment under pressure with collaboration awareness
        Ubuntu Application: Consider collective impact and seek help when needed
        """
        analysis = {
            "can_resolve_independently": False,
            "estimated_time": None,
            "requires_collaboration": False,
            "collaboration_targets": [],
            "ubuntu_approach": None,
            "user_communication_strategy": None
        }
        
        # Rapid decision-making pattern based on real workflows
        if ticket.category.lower() in ["password_reset", "software_install", "printer_setup"]:
            analysis["can_resolve_independently"] = True
            analysis["estimated_time"] = 15  # minutes
            analysis["user_communication_strategy"] = "direct_resolution"
            
        elif ticket.category.lower() in ["network_connectivity", "server_access", "user_request"] or "server" in ticket.issue_description.lower() or "network" in ticket.issue_description.lower():
            # Ubuntu principle: "I am because we are" - seek collective wisdom
            analysis["requires_collaboration"] = True
            analysis["collaboration_targets"] = ["server_infrastructure"]
            analysis["ubuntu_approach"] = "collective_diagnosis"
            analysis["user_communication_strategy"] = "collaborative_investigation"
            
        elif ticket.category.lower() in ["application_error", "database_issue"] or "application" in ticket.issue_description.lower() or "database" in ticket.issue_description.lower():
            analysis["requires_collaboration"] = True
            analysis["collaboration_targets"] = ["app_support"]
            analysis["ubuntu_approach"] = "shared_expertise"
            analysis["user_communication_strategy"] = "expert_collaboration"
            
        elif ticket.priority == SupportPriority.CRITICAL:
            # Critical issues require collective response - Ubuntu principle
            analysis["requires_collaboration"] = True
            analysis["collaboration_targets"] = ["server_infrastructure", "app_support", "service_desk_manager"]
            analysis["ubuntu_approach"] = "emergency_collective_response"
            analysis["user_communication_strategy"] = "priority_escalation"
            
        return analysis
    
    def ubuntu_collaborate(self, issue: str, target_departments: List[str]) -> Dict[str, Any]:
        """
        Ubuntu-driven collaboration with other departmental agents
        
        Principle: "I am because we are" - This agent's effectiveness comes through relationships
        Pattern: Collective problem-solving rather than isolated attempts
        """
        collaboration_request = {
            "timestamp": datetime.now(),
            "requesting_agent": self.agent_id,
            "issue_description": issue,
            "target_departments": target_departments,
            "ubuntu_approach": "collective_wisdom",
            "mutual_benefit": True,
            "knowledge_sharing": True
        }
        
        # Ubuntu principle: Seek collective understanding before action
        collaboration_response = {
            "collaboration_id": f"collab_{datetime.now().timestamp()}",
            "participating_agents": [self.agent_id] + target_departments,
            "approach": "ubuntu_consensus_building",
            "expected_outcome": "collective_solution",
            "knowledge_sharing_commitment": True
        }
        
        self.collaboration_requests.append(collaboration_request)
        logging.info(f"Ubuntu collaboration initiated: {collaboration_request['issue_description']}")
        
        return collaboration_response
    
    def provide_user_communication(self, ticket: SupportTicket, analysis: Dict[str, Any]) -> str:
        """
        Generate user communication based on real IT Support empathy and clarity patterns
        
        Behavioral Pattern: Clear, empathetic communication with realistic expectations
        Ubuntu Integration: Acknowledge collective effort when involving other departments
        """
        communication_templates = {
            "direct_resolution": f"Hi {ticket.user_name}, I can help you with {ticket.issue_description}. This should take about {analysis['estimated_time']} minutes to resolve. I'll get started right away.",
            
            "collaborative_investigation": f"Hi {ticket.user_name}, I've received your request about {ticket.issue_description}. To provide the best solution, I'm collaborating with our infrastructure team. We'll work together to resolve this quickly and keep you updated.",
            
            "expert_collaboration": f"Hi {ticket.user_name}, thank you for reporting {ticket.issue_description}. I'm bringing in our application specialists to ensure we address this properly. Our collective expertise will help us resolve this efficiently.",
            
            "priority_escalation": f"Hi {ticket.user_name}, I understand the urgency of {ticket.issue_description}. I've immediately engaged our full IT team for a coordinated response. We're working together to resolve this as quickly as possible."
        }
        
        strategy = analysis.get("user_communication_strategy", "direct_resolution")
        return communication_templates.get(strategy, "We're working on your request and will update you soon.")
    
    def ubuntu_knowledge_sharing(self, resolution: Dict[str, Any]) -> None:
        """
        Share resolution knowledge with collective for mutual benefit
        
        Ubuntu Principle: Knowledge belongs to the collective, not the individual
        Pattern: Every resolution strengthens the whole team
        """
        shared_knowledge = {
            "timestamp": datetime.now(),
            "sharing_agent": self.agent_id,
            "issue_type": resolution.get("category"),
            "solution_approach": resolution.get("solution"),
            "collaboration_involved": resolution.get("required_collaboration", False),
            "collective_benefit": True,
            "ubuntu_principle": "shared_wisdom_strengthens_all"
        }
        
        # Add to collective knowledge base
        if "shared_resolutions" not in self.knowledge_base:
            self.knowledge_base["shared_resolutions"] = []
        
        self.knowledge_base["shared_resolutions"].append(shared_knowledge)
        
        logging.info(f"Knowledge shared with collective: {shared_knowledge['issue_type']}")
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        Get current agent status reflecting real IT Support workload patterns
        
        Ubuntu Integration: Status includes collaborative relationships and collective contributions
        """
        return {
            "agent_id": self.agent_id,
            "agent_type": "IT_Support_Technician",
            "current_workload": len(self.current_tickets),
            "active_collaborations": len(self.collaboration_requests),
            "tickets_resolved_today": len([t for t in self.resolved_tickets if t.time_reported.date() == datetime.now().date()]),
            "ubuntu_collaboration_active": len([r for r in self.collaboration_requests if r["ubuntu_approach"]]) > 0,
            "departmental_relationships": {
                dept: "connected" if agent else "pending" 
                for dept, agent in self.departmental_relationships.items()
            },
            "collective_contributions": len(self.knowledge_base.get("shared_resolutions", [])),
            "ubuntu_principles_active": self.ubuntu_principles
        }
    
    def ubuntu_daily_reflection(self) -> Dict[str, Any]:
        """
        Daily reflection on collaborative effectiveness and collective contribution
        
        Ubuntu Practice: Regular reflection on how "I am because we are" was lived
        Pattern: Continuous improvement through collective awareness
        """
        reflection = {
            "date": datetime.now().date(),
            "tickets_handled": len([t for t in self.resolved_tickets if t.time_reported.date() == datetime.now().date()]),
            "collaborations_initiated": len([r for r in self.collaboration_requests if r["timestamp"].date() == datetime.now().date()]),
            "knowledge_shared": len([k for k in self.knowledge_base.get("shared_resolutions", []) if k["timestamp"].date() == datetime.now().date()]),
            "ubuntu_effectiveness": "high" if len(self.collaboration_requests) > 0 else "individual_focus",
            "collective_impact": "positive" if self.ubuntu_principles["mutual_support"] else "needs_improvement",
            "tomorrow_ubuntu_intention": "strengthen_departmental_relationships"
        }
        
        return reflection

# Example behavioral patterns based on real IT Support analysis
AGENT_ITSUPPORT_BEHAVIORS = {
    "rapid_decision_making": {
        "description": "Quick assessment and action under pressure",
        "ubuntu_enhancement": "Seeks collective wisdom when individual knowledge insufficient",
        "typical_scenarios": ["system_outage", "critical_user_down", "security_incident"]
    },
    
    "cross_team_collaboration": {
        "description": "Heavy reliance on other IT departments for complex issues",
        "ubuntu_enhancement": "Proactive collaboration rather than reluctant escalation",
        "typical_scenarios": ["network_connectivity", "server_issues", "application_errors"]
    },
    
    "user_empathy_focus": {
        "description": "Strong emphasis on user communication and experience",
        "ubuntu_enhancement": "User as part of collective community deserving collective support",
        "typical_scenarios": ["frustrated_user", "business_critical_deadline", "training_needs"]
    },
    
    "knowledge_documentation": {
        "description": "Documentation and knowledge sharing for team benefit",
        "ubuntu_enhancement": "Knowledge belongs to collective, strengthens all",
        "typical_scenarios": ["new_solutions", "common_issues", "best_practices"]
    }
}

# Ubuntu-driven collaboration protocols
UBUNTU_COLLABORATION_PROTOCOLS = {
    "collective_problem_solving": {
        "principle": "Multiple perspectives create better solutions",
        "implementation": "Always consider who else might contribute wisdom",
        "trigger_conditions": ["complex_technical_issue", "user_impact_unclear", "multiple_possible_solutions"]
    },
    
    "mutual_support": {
        "principle": "Each department's success enables others' success",
        "implementation": "Proactively offer assistance to other departments",
        "trigger_conditions": ["other_department_overloaded", "expertise_overlap", "learning_opportunity"]
    },
    
    "shared_accountability": {
        "principle": "Collective responsibility for user and organizational success",
        "implementation": "Take ownership of outcomes regardless of departmental boundaries",
        "trigger_conditions": ["cross_departmental_issue", "user_satisfaction_risk", "organizational_impact"]
    },
    
    "consensus_building": {
        "principle": "Decisions emerge from collective wisdom",
        "implementation": "Seek understanding and agreement before action",
        "trigger_conditions": ["conflicting_approaches", "resource_allocation", "priority_setting"]
    }
}

if __name__ == "__main__":
    # Example usage demonstrating Ubuntu-driven IT Support agent
    knowledge_base = {
        "common_solutions": {},
        "escalation_procedures": {},
        "shared_resolutions": []
    }
    
    # Initialize Ubuntu-driven IT Support agent
    agent = Agent_ITSupport("itsupport_001", knowledge_base)
    
    # Example support ticket
    ticket = SupportTicket(
        ticket_id="TK001",
        user_name="John Smith",
        issue_description="Cannot access shared network drive",
        priority=SupportPriority.HIGH,
        category="network_connectivity",
        time_reported=datetime.now()
    )
    
    # Analyze with Ubuntu principles
    analysis = agent.analyze_support_request(ticket)
    print(f"Analysis: {analysis}")
    
    # Generate Ubuntu-enhanced user communication
    communication = agent.provide_user_communication(ticket, analysis)
    print(f"User Communication: {communication}")
    
    # Demonstrate Ubuntu collaboration
    if analysis["requires_collaboration"]:
        collaboration = agent.ubuntu_collaborate(
            ticket.issue_description, 
            analysis["collaboration_targets"]
        )
        print(f"Ubuntu Collaboration: {collaboration}")
    
    # Daily Ubuntu reflection
    reflection = agent.ubuntu_daily_reflection()
    print(f"Ubuntu Reflection: {reflection}")
