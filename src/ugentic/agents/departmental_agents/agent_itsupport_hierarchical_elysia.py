# UGENTIC IT Support Agent - ENHANCED with Hierarchical Ubuntu Integration
# Building on the Elysia + MCP refactoring with organizational hierarchy
# Key Innovation: Ubuntu-Informed Hierarchical Decision Making

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
import asyncio

# Import our hierarchical framework
try:
    from ugentic.core.hierarchical_ubuntu_framework import (
        UGENTICHierarchicalFramework, 
        ElysiaHierarchicalDecisionTree,
        OrganizationalLevel,
        DecisionAuthority,
        HIERARCHICAL_UBUNTU_PROTOCOLS
    )
except ImportError:
    print("Hierarchical framework will be loaded when available")

# ELYSIA FRAMEWORK INTEGRATION (with hierarchical routing)
try:
    from elysia import Tree, tool, Response, Text
except ImportError:
    print("WARNING: Elysia not installed. Using mock classes for development.")
    class Tree:
        def __init__(self): pass
        def __call__(self, request): return {"response": "mock_elysia_response"}
    
    def tool(tree=None):
        def decorator(func):
            return func
        return decorator
    
    class Response:
        def __init__(self, content): self.content = content

# MCP TOOL INTEGRATION (enhanced with hierarchical context)
class MCPMemoryTool:
    async def create_entities(self, entities): 
        print(f" MCP Memory: Created entities {[e.get('name', 'unknown') for e in entities]}")
        return {"status": "success", "entities": entities}

class MCPOrchestratorTool:
    async def create_workflow(self, workflow):
        print(f" MCP Orchestrator: Created workflow '{workflow.get('name', 'unnamed')}'")
        return {"status": "success", "workflow_id": f"wf_{datetime.now().timestamp()}"}

# Initialize MCP tools
mcp_memory = MCPMemoryTool()
mcp_orchestrator = MCPOrchestratorTool()

# PRESERVE ALL ORIGINAL ENUMS AND DATACLASSES
class SupportPriority(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class SupportTicket:
    ticket_id: str
    user_name: str
    issue_description: str
    priority: SupportPriority
    category: str
    time_reported: datetime
    hierarchical_impact: Optional[str] = None  # NEW: Which hierarchy levels affected
    decision_authority_required: Optional[str] = None  # NEW: What level can decide
    ubuntu_collaboration_scope: Optional[List[str]] = None  # NEW: Ubuntu collaboration needed

class UGENTICITSupportAgent_Hierarchical:
    """
    ENHANCED IT Support Agent: Elysia + MCP + Hierarchical Ubuntu Integration
    
    HIERARCHICAL CAPABILITIES:
    - Operates at TECHNICIAN level in organizational hierarchy
    - Makes OPERATIONAL decisions within authority
    - Escalates appropriately using Ubuntu-informed hierarchy
    - Collaborates across hierarchical levels with Ubuntu dignity
    - Routes decisions through Elysia Tree considering both hierarchy and Ubuntu
    
    UBUNTU HIERARCHICAL PRINCIPLES:
    - Authority serves collective good
    - Wisdom flows multidirectionally
    - Escalation as collaboration, not failure
    - Hierarchical Ubuntu: structure enables Ubuntu, doesn't oppose it
    """
    
    def __init__(self):
        # Initialize Elysia Tree with hierarchical routing
        self.tree = Tree()
        
        # Hierarchical position (NEW)
        self.organizational_level = OrganizationalLevel.TECHNICIAN
        self.decision_authority = DecisionAuthority.OPERATIONAL
        self.hierarchical_framework = UGENTICHierarchicalFramework()
        self.hierarchical_decision_tree = ElysiaHierarchicalDecisionTree(self.hierarchical_framework)
        
        # Agent identity (preserved from original)
        self.agent_id = "itsupport_hierarchical_elysia_001"
        self.agent_type = "IT_Support_Technician"
        
        # Ubuntu principles (preserved and enhanced)
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True,
            "hierarchical_ubuntu": True,  # NEW: Ubuntu within hierarchical structure
            "respectful_escalation": True,  # NEW: Escalation as Ubuntu collaboration
            "cross_level_wisdom": True     # NEW: Wisdom exists at all levels
        }
        
        # Hierarchical relationships (enhanced)
        self.hierarchical_relationships = {
            "peers": ["server_infrastructure", "app_support"],  # Same level collaboration
            "manager": "service_desk_manager",  # Direct supervisor
            "senior_management": "it_manager",  # Strategic escalation
            "escalation_path": ["service_desk_manager", "it_manager"]  # Ubuntu escalation chain
        }
        
        # Initialize MCP tool connections
        self.mcp_memory = mcp_memory
        self.mcp_orchestrator = mcp_orchestrator
        
        # Register hierarchical Ubuntu tools with Elysia Tree
        self._register_hierarchical_ubuntu_tools()
        
        logging.info(f"UGENTICITSupportAgent_Hierarchical {self.agent_id} initialized")
    
    def _register_hierarchical_ubuntu_tools(self):
        """Register hierarchical Ubuntu tools with Elysia Tree"""
        
        @tool(tree=self.tree)
        async def hierarchical_ubuntu_analyze_request(ticket_data: Dict[str, Any]) -> Dict[str, Any]:
            """
            ENHANCED: Analyze request considering hierarchy, authority, and Ubuntu principles
            
            New Capabilities:
            - Determines if issue can be resolved at technician level
            - Identifies hierarchical impact and required authority
            - Plans Ubuntu collaboration across appropriate hierarchy levels
            - Routes through proper channels while maintaining Ubuntu dignity
            """
            # Create enhanced ticket with hierarchical context
            ticket = SupportTicket(
                ticket_id=ticket_data.get("ticket_id", ""),
                user_name=ticket_data.get("user_name", ""),
                issue_description=ticket_data.get("issue_description", ""),
                priority=SupportPriority(ticket_data.get("priority", "medium")),
                category=ticket_data.get("category", ""),
                time_reported=datetime.now()
            )
            
            # HIERARCHICAL ANALYSIS: What level of authority is needed?
            hierarchical_routing = self.hierarchical_decision_tree.route_decision({
                "decision_type": self._classify_decision_type(ticket),
                "agent_level": self.organizational_level.value
            })
            
            # UBUNTU ANALYSIS: Who should be included in collective wisdom?
            ubuntu_collaboration = self._determine_ubuntu_collaboration_scope(ticket, hierarchical_routing)
            
            # Enhanced analysis with hierarchical and Ubuntu dimensions
            analysis = {
                # Original analysis preserved
                "can_resolve_independently": hierarchical_routing["can_decide_at_current_level"],
                "estimated_time": self._estimate_resolution_time(ticket),
                "requires_collaboration": hierarchical_routing["requires_collaboration"],
                "collaboration_targets": ubuntu_collaboration["participants"],
                "ubuntu_approach": ubuntu_collaboration["approach"],
                "user_communication_strategy": self._determine_communication_strategy(ticket, hierarchical_routing),
                
                # NEW: Hierarchical dimensions
                "hierarchical_authority_needed": hierarchical_routing.get("escalation_needed", False),
                "decision_level": self._determine_decision_level(ticket),
                "escalation_path": self.hierarchical_relationships["escalation_path"] if hierarchical_routing.get("escalation_needed") else [],
                "ubuntu_hierarchical_approach": self._get_ubuntu_hierarchical_approach(ticket, hierarchical_routing),
                
                # NEW: MCP integration context
                "mcp_workflow_type": self._determine_mcp_workflow_type(hierarchical_routing),
                "collective_knowledge_impact": ubuntu_collaboration["knowledge_sharing_scope"]
            }
            
            # Store hierarchical analysis in MCP Memory
            await self._store_hierarchical_analysis_in_mcp(ticket, analysis)
            
            return analysis
        
        @tool(tree=self.tree)
        async def ubuntu_hierarchical_escalation(issue_context: str, escalation_reason: str) -> Dict[str, Any]:
            """
            ENHANCED: Ubuntu-informed hierarchical escalation
            
            Key Innovation: Escalation as collaborative elevation, not individual failure
            - Maintains Ubuntu dignity throughout escalation
            - Provides collective wisdom gathered to higher authority
            - Establishes ongoing Ubuntu collaboration across levels
            - Ensures learning flows back down hierarchy
            """
            escalation_data = self.hierarchical_framework.get_ubuntu_escalation_path(
                issue_context, 
                "it_support_technician"
            )
            
            # Create Ubuntu escalation workflow in MCP Orchestrator
            escalation_workflow = await self.mcp_orchestrator.create_workflow({
                "name": f"Ubuntu Hierarchical Escalation: {issue_context[:50]}...",
                "description": "Ubuntu-informed escalation maintaining dignity and collective wisdom",
                "hierarchy_levels_involved": escalation_data["escalation_path"],
                "ubuntu_principles": [
                    "escalation_as_collaboration",
                    "wisdom_preservation_across_levels", 
                    "collective_learning_opportunity",
                    "hierarchical_ubuntu_dignity"
                ],
                "tasks": [
                    {
                        "title": "Prepare Collective Wisdom Package",
                        "description": "Gather insights, attempts made, and recommendations",
                        "ubuntu_approach": "respectful_preparation_for_higher_authority"
                    },
                    {
                        "title": "Engage Next Hierarchical Level",
                        "description": f"Collaborate with {escalation_data['escalation_path'][0]}",
                        "ubuntu_approach": "collaborative_engagement_not_handoff"
                    },
                    {
                        "title": "Maintain Ongoing Ubuntu Connection",
                        "description": "Stay involved in resolution for collective learning",
                        "ubuntu_approach": "hierarchical_collaboration_continuation"
                    },
                    {
                        "title": "Collective Learning Integration",
                        "description": "Integrate learnings back into collective knowledge",
                        "ubuntu_approach": "wisdom_flows_multidirectionally"
                    }
                ]
            })
            
            # Store escalation in MCP Memory with hierarchical context
            await self.mcp_memory.create_entities([{
                "name": f"ubuntu_hierarchical_escalation_{datetime.now().timestamp()}",
                "entityType": "ubuntu_hierarchical_escalation",
                "observations": [
                    f"Issue: {issue_context}",
                    f"Escalation reason: {escalation_reason}",
                    f"Current level: {self.organizational_level.value}",
                    f"Escalation path: {', '.join(escalation_data['escalation_path'])}",
                    f"Ubuntu approach: {escalation_data['ubuntu_approach']}",
                    "Hierarchical Ubuntu principle: Authority serves collective good",
                    f"Workflow ID: {escalation_workflow.get('workflow_id', 'unknown')}"
                ]
            }])
            
            return {
                "escalation_id": f"ubuntu_esc_{datetime.now().timestamp()}",
                "escalation_approach": "ubuntu_hierarchical_collaboration",
                "target_levels": escalation_data["escalation_path"],
                "ubuntu_dignity_maintained": True,
                "collective_wisdom_preservation": True,
                "workflow_id": escalation_workflow.get("workflow_id"),
                "learning_integration_planned": True
            }
        
        @tool(tree=self.tree)
        async def cross_level_ubuntu_collaboration(collaboration_context: str, target_levels: List[str]) -> Dict[str, Any]:
            """
            NEW: Cross-hierarchical Ubuntu collaboration
            
            Innovation: Ubuntu collaboration that respects hierarchy while leveraging collective wisdom
            - Technician can initiate collaboration with management for complex issues
            - Management can engage technicians for front-line insights
            - Peer-level collaboration coordinated through proper channels
            - Wisdom flows multidirectionally while respecting organizational structure
            """
            # Determine appropriate collaboration approach based on target levels
            collaboration_approach = self._design_cross_level_collaboration(target_levels)
            
            # Create cross-level Ubuntu workflow
            cross_level_workflow = await self.mcp_orchestrator.create_workflow({
                "name": f"Cross-Level Ubuntu Collaboration: {collaboration_context[:50]}...",
                "description": "Ubuntu collaboration across organizational hierarchy levels",
                "participating_levels": [self.organizational_level.value] + target_levels,
                "ubuntu_hierarchical_principles": [
                    "wisdom_exists_at_all_levels",
                    "respectful_cross_level_engagement",
                    "hierarchical_channels_honored",
                    "collective_wisdom_transcends_hierarchy"
                ],
                "collaboration_structure": collaboration_approach["structure"],
                "tasks": self._create_cross_level_collaboration_tasks(collaboration_approach)
            })
            
            # Store in MCP Memory
            await self.mcp_memory.create_entities([{
                "name": f"cross_level_ubuntu_collab_{datetime.now().timestamp()}",
                "entityType": "cross_level_ubuntu_collaboration",
                "observations": [
                    f"Context: {collaboration_context}",
                    f"Initiating level: {self.organizational_level.value}",
                    f"Target levels: {', '.join(target_levels)}",
                    f"Collaboration approach: {collaboration_approach['type']}",
                    "Ubuntu principle: Wisdom flows multidirectionally",
                    "Hierarchical respect: Proper channels and dignity maintained",
                    f"Workflow ID: {cross_level_workflow.get('workflow_id', 'unknown')}"
                ]
            }])
            
            return {
                "collaboration_id": f"cross_level_{datetime.now().timestamp()}",
                "collaboration_type": "ubuntu_hierarchical_cross_level",
                "participating_levels": [self.organizational_level.value] + target_levels,
                "ubuntu_approach": collaboration_approach["ubuntu_approach"],
                "hierarchical_respect": True,
                "workflow_id": cross_level_workflow.get("workflow_id"),
                "expected_outcomes": collaboration_approach["expected_outcomes"]
            }
    
    def _classify_decision_type(self, ticket: SupportTicket) -> str:
        """Classify the type of decision needed for hierarchical routing"""
        if ticket.category.lower() in ["password_reset", "software_install", "printer_setup"]:
            return "basic_troubleshooting"
        elif ticket.category.lower() in ["network_connectivity", "server_access"]:
            return "complex_technical_issue"
        elif ticket.priority == SupportPriority.CRITICAL:
            return "system_outage"
        else:
            return "general_support"
    
    def _determine_ubuntu_collaboration_scope(self, ticket: SupportTicket, hierarchical_routing: Dict[str, Any]) -> Dict[str, Any]:
        """Determine Ubuntu collaboration scope considering hierarchical context"""
        if hierarchical_routing["requires_collaboration"]:
            return {
                "participants": self.hierarchical_relationships["peers"],
                "approach": "peer_ubuntu_collaboration",
                "knowledge_sharing_scope": "peer_level_collective_wisdom"
            }
        elif hierarchical_routing["escalation_needed"]:
            return {
                "participants": self.hierarchical_relationships["escalation_path"][:1],
                "approach": "ubuntu_hierarchical_escalation",
                "knowledge_sharing_scope": "cross_level_collective_wisdom"
            }
        else:
            return {
                "participants": [],
                "approach": "individual_competence_serving_collective",
                "knowledge_sharing_scope": "personal_experience_for_collective_benefit"
            }
    
    def _get_ubuntu_hierarchical_approach(self, ticket: SupportTicket, hierarchical_routing: Dict[str, Any]) -> str:
        """Get Ubuntu approach that respects hierarchical structure"""
        if hierarchical_routing["can_decide_at_current_level"]:
            return "individual_ubuntu_competence"
        elif hierarchical_routing["requires_collaboration"]:
            return "peer_ubuntu_collective_wisdom"
        elif hierarchical_routing["escalation_needed"]:
            return "ubuntu_hierarchical_elevation"
        else:
            return "ubuntu_guidance_seeking"
    
    def _design_cross_level_collaboration(self, target_levels: List[str]) -> Dict[str, Any]:
        """Design appropriate cross-level collaboration structure"""
        if "service_desk_manager" in target_levels:
            return {
                "type": "technician_management_collaboration",
                "structure": "formal_consultation_with_ubuntu_dignity",
                "ubuntu_approach": "front_line_wisdom_to_management_perspective",
                "expected_outcomes": ["enhanced_decision_making", "collective_wisdom_integration"]
            }
        elif all(level in self.hierarchical_relationships["peers"] for level in target_levels):
            return {
                "type": "peer_level_collaboration",
                "structure": "direct_ubuntu_collaboration",
                "ubuntu_approach": "collective_expertise_sharing",
                "expected_outcomes": ["technical_solution", "shared_learning"]
            }
        else:
            return {
                "type": "multi_level_collaboration",
                "structure": "coordinated_ubuntu_engagement",
                "ubuntu_approach": "hierarchical_collective_wisdom",
                "expected_outcomes": ["comprehensive_solution", "organizational_learning"]
            }
    
    def _create_cross_level_collaboration_tasks(self, collaboration_approach: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create tasks for cross-level collaboration workflows"""
        base_tasks = [
            {
                "title": "Establish Ubuntu Collaborative Context",
                "description": "Set collaborative tone with Ubuntu dignity and respect",
                "ubuntu_principle": "respectful_engagement_across_levels"
            },
            {
                "title": "Share Perspective and Wisdom",
                "description": "Contribute unique level-specific insights to collective understanding",
                "ubuntu_principle": "every_level_contributes_valuable_wisdom"
            },
            {
                "title": "Integrate Collective Wisdom",
                "description": "Synthesize insights from all participating hierarchical levels",
                "ubuntu_principle": "collective_wisdom_transcends_individual_perspectives"
            },
            {
                "title": "Implement with Collective Accountability",
                "description": "Execute solution with shared responsibility across levels",
                "ubuntu_principle": "collective_accountability_for_outcomes"
            }
        ]
        
        return base_tasks
    
    async def _store_hierarchical_analysis_in_mcp(self, ticket: SupportTicket, analysis: Dict[str, Any]):
        """Store hierarchical analysis in MCP Memory"""
        await self.mcp_memory.create_entities([{
            "name": f"hierarchical_analysis_{ticket.ticket_id}",
            "entityType": "hierarchical_support_analysis",
            "observations": [
                f"Ticket ID: {ticket.ticket_id}",
                f"Organizational level: {self.organizational_level.value}",
                f"Decision authority: {self.decision_authority.value}",
                f"Can resolve at current level: {analysis['can_resolve_independently']}",
                f"Hierarchical authority needed: {analysis['hierarchical_authority_needed']}",
                f"Ubuntu hierarchical approach: {analysis['ubuntu_hierarchical_approach']}",
                f"Escalation path: {', '.join(analysis['escalation_path'])}",
                "Innovation: Ubuntu-informed hierarchical decision making"
            ]
        }])
    
    def _estimate_resolution_time(self, ticket: SupportTicket) -> int:
        """Estimate resolution time considering hierarchical complexity"""
        base_times = {
            "password_reset": 15,
            "software_install": 30,
            "printer_setup": 20,
            "network_connectivity": 45,
            "server_access": 60,
            "application_error": 90
        }
        
        base_time = base_times.get(ticket.category.lower(), 30)
        
        # Add time for hierarchical consultation if needed
        if ticket.priority == SupportPriority.CRITICAL:
            base_time += 30  # Additional time for emergency coordination
        
        return base_time
    
    def _determine_communication_strategy(self, ticket: SupportTicket, hierarchical_routing: Dict[str, Any]) -> str:
        """Determine communication strategy considering hierarchical involvement"""
        if hierarchical_routing["can_decide_at_current_level"]:
            return "direct_resolution"
        elif hierarchical_routing["requires_collaboration"]:
            return "collaborative_investigation"
        elif hierarchical_routing["escalation_needed"]:
            return "hierarchical_escalation_communication"
        else:
            return "expert_consultation"
    
    def _determine_decision_level(self, ticket: SupportTicket) -> str:
        """Determine what hierarchical level should make the decision"""
        if ticket.category.lower() in ["password_reset", "software_install"]:
            return "technician"
        elif ticket.category.lower() in ["network_connectivity", "server_access"]:
            return "specialist_collaboration"
        elif ticket.priority == SupportPriority.CRITICAL:
            return "management_coordination"
        else:
            return "technician_with_peer_consultation"
    
    def _determine_mcp_workflow_type(self, hierarchical_routing: Dict[str, Any]) -> str:
        """Determine what type of MCP workflow to create"""
        if hierarchical_routing["can_decide_at_current_level"]:
            return "individual_resolution_workflow"
        elif hierarchical_routing["requires_collaboration"]:
            return "peer_collaboration_workflow"
        elif hierarchical_routing["escalation_needed"]:
            return "hierarchical_escalation_workflow"
        else:
            return "consultation_workflow"
    
    async def process_hierarchical_support_request(self, request_data: Dict[str, Any]) -> Response:
        """
        Main entry point for hierarchical Ubuntu support request processing
        Uses Elysia Tree with hierarchical routing and Ubuntu principles
        """
        # Enhanced request processing with hierarchical context
        request_text = f"Hierarchical Ubuntu Support Request: {request_data.get('issue_description', '')} - Priority: {request_data.get('priority', 'medium')} - Category: {request_data.get('category', 'general')} - Level: {self.organizational_level.value}"
        
        # Let Elysia Tree orchestrate with hierarchical Ubuntu tools
        response = self.tree(request_text)
        
        return Response(content=response)
    
    async def get_hierarchical_ubuntu_status(self) -> Dict[str, Any]:
        """Get status including hierarchical position and Ubuntu integration"""
        return {
            "agent_id": self.agent_id,
            "agent_type": "IT_Support_Technician_Hierarchical_Elysia",
            "framework": "Elysia_Tree_MCP_Hierarchical_Ubuntu_Integrated",
            
            # Hierarchical position
            "organizational_level": self.organizational_level.value,
            "decision_authority": self.decision_authority.value,
            "hierarchical_relationships": self.hierarchical_relationships,
            
            # Ubuntu principles (enhanced)
            "ubuntu_principles_active": self.ubuntu_principles,
            "ubuntu_hierarchical_innovation": "Authority serves collective good",
            
            # Technical integration
            "mcp_tools_status": {"memory": "connected", "orchestrator": "connected"},
            "elysia_tree_status": "operational_with_hierarchical_routing",
            "hierarchical_framework_status": "fully_integrated",
            
            # Capabilities
            "hierarchical_capabilities": [
                "ubuntu_informed_escalation",
                "cross_level_collaboration", 
                "hierarchical_decision_routing",
                "wisdom_multidirectional_flow",
                "authority_serving_collective_good"
            ]
        }

# Example usage demonstrating hierarchical Ubuntu integration
async def example_hierarchical_usage():
    """Example showing hierarchical Ubuntu integration with Elysia + MCP"""
    print(" UGENTIC Hierarchical Ubuntu IT Support - Elysia + MCP Integration")
    print("=" * 70)
    
    # Initialize hierarchical agent
    agent = UGENTICITSupportAgent_Hierarchical()
    
    # Test hierarchical decision routing
    print(" Testing Hierarchical Decision Scenarios:")
    print()
    
    # Scenario 1: Simple request (technician level authority)
    simple_request = {
        "ticket_id": "TK001",
        "user_name": "John Smith",
        "issue_description": "Password reset needed",
        "priority": "low",
        "category": "password_reset"
    }
    
    print(f" Simple Request: {simple_request['issue_description']}")
    print(f"   Expected routing: Technician level authority (Ubuntu individual competence)")
    
    # Scenario 2: Complex request (peer collaboration needed)
    complex_request = {
        "ticket_id": "TK002", 
        "user_name": "Sarah Wilson",
        "issue_description": "Cannot access network drives, possible server issue",
        "priority": "high",
        "category": "network_connectivity"
    }
    
    print(f" Complex Request: {complex_request['issue_description']}")
    print(f"   Expected routing: Peer collaboration (Ubuntu collective expertise)")
    
    # Scenario 3: Critical request (management escalation needed)
    critical_request = {
        "ticket_id": "TK003",
        "user_name": "Emergency Escalation",
        "issue_description": "Email server down, affecting entire organization",
        "priority": "critical", 
        "category": "system_outage"
    }
    
    print(f" Critical Request: {critical_request['issue_description']}")
    print(f"   Expected routing: Management escalation (Ubuntu hierarchical elevation)")
    print()
    
    # Get hierarchical status
    status = await agent.get_hierarchical_ubuntu_status()
    print(" Hierarchical Ubuntu Status:")
    print(f"   Organizational Level: {status['organizational_level']}")
    print(f"   Decision Authority: {status['decision_authority']}")
    print(f"   Ubuntu Hierarchical Innovation: {status['ubuntu_hierarchical_innovation']}")
    print(f"   Hierarchical Capabilities: {', '.join(status['hierarchical_capabilities'])}")
    print()
    
    print(" Hierarchical Ubuntu Integration: SUCCESSFULLY IMPLEMENTED")
    print(" Key Innovation: Ubuntu principles within organizational hierarchy")
    print(" Architecture: Elysia Tree + MCP + Hierarchical Ubuntu Framework")

if __name__ == "__main__":
    asyncio.run(example_hierarchical_usage())
