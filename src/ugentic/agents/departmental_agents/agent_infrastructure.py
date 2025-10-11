# Infrastructure Agent - The System Guardian
# UGENTIC Framework

from ...core.agent_framework import Agent
import logging

class Agent_Infrastructure(Agent):
    """
    The Infrastructure agent is responsible for the health and stability of servers, storage,
    and other core systems. It performs checks and maintenance tasks.
    
    Ubuntu Principles Integration:
    - Collective Problem-Solving: Collaborates with App/Network teams on complex issues
    - Knowledge Sharing: Documents and shares infrastructure insights
    - Mutual Support: Proactively helps other teams with infrastructure expertise
    - Consensus Building: Involves stakeholders in major infrastructure decisions
    """
    def __init__(self, name="Infrastructure", persona="A diligent guardian of the system's core infrastructure.", tools=None, rag_system=None, llm_model=None, departmental_relationships=None):
        super().__init__(name, persona, tools, rag_system, llm_model)
        self.agent_type = "Operational"
        self.specialization = "Servers, Storage, Backups, Virtualization"
        self.departmental_relationships = departmental_relationships or {}
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
        self.infrastructure_state = {
            "monitored_servers": [],
            "recent_maintenance": [],
            "capacity_alerts": []
        }

    def check_server_status(self, server_name: str):
        """Checks the status of a given server."""
        logging.info(f"Infrastructure agent '{self.name}' is checking status of server: '{server_name}'")
        
        # TODO: Implement actual server status check (e.g., ping, check service)
        
        return {
            "server": server_name,
            "status": "Online",
            "cpu_load": "15%",
            "memory_usage": "40%"
        }

    def ubuntu_collaborate(self, issue: str, collaborating_agents: list, infrastructure_context: dict):
        """
        Initiates Ubuntu collaboration with other technical specialists (App Support, Network Support).
        
        Infrastructure often needs to collaborate with App and Network teams for complete diagnosis.
        
        Args:
            issue: The infrastructure issue requiring collaboration
            collaborating_agents: List of agents to collaborate with (App Support, Network Support)
            infrastructure_context: Dict with server metrics, logs, performance data
            
        Returns:
            dict: Collaboration session with infrastructure insights
        """
        logging.info(f"Infrastructure agent '{self.name}' initiating Ubuntu collaboration: '{issue}'")
        
        collaboration_session = {
            "collaboration_id": f"infra_collab_{len(collaborating_agents)}_agents",
            "initiated_by": self.name,
            "issue": issue,
            "infrastructure_context": infrastructure_context,
            "collaborating_agents": collaborating_agents,
            "status": "active"
        }
        
        collaboration_message = f"""
 INFRASTRUCTURE UBUNTU COLLABORATION initiated

Issue: {issue}

Infrastructure Context:
{chr(10).join([f"- {key}: {value}" for key, value in infrastructure_context.items()])}

Collaborating with:
{chr(10).join([f"- {agent}: Need your domain expertise for complete diagnosis" for agent in collaborating_agents])}

Why Collaboration:
Infrastructure issues often have application or network dimensions. By working
together, we diagnose faster and find better solutions.

What I'm Contributing:
- Server metrics and performance data
- Infrastructure logs and monitoring insights
- Server configuration and capacity information
- Historical infrastructure patterns

What I Need From You:
- App Support: Application behavior and performance patterns
- Network Support: Connectivity and network performance data
- Together: Complete picture of the system state

Ubuntu Principle: "Technical problems span domains - our collective expertise solves them faster"

Let's diagnose this together!
        """
        
        collaboration_session["message"] = collaboration_message
        logging.info(f"Infrastructure collaboration '{collaboration_session['collaboration_id']}' active")
        
        return collaboration_session
    
    def share_infrastructure_knowledge(self, topic: str, technical_details: str, impact_on_teams: dict, best_practices: list = None):
        """
        Shares infrastructure knowledge with other teams.
        
        Makes infrastructure insights accessible to App Support, Network Support, and IT Support.
        
        Args:
            topic: Infrastructure knowledge topic
            technical_details: The technical details to share
            impact_on_teams: Dict describing how this affects different teams
            best_practices: Optional list of best practices learned
            
        Returns:
            dict: Knowledge sharing package
        """
        logging.info(f"Infrastructure agent '{self.name}' sharing knowledge: '{topic}'")
        
        knowledge_package = {
            "topic": topic,
            "technical_details": technical_details,
            "impact_on_teams": impact_on_teams,
            "best_practices": best_practices or [],
            "shared_by": self.name,
            "knowledge_type": "infrastructure_technical",
            "ubuntu_principle": "Infrastructure knowledge benefits everyone"
        }
        
        sharing_message = f"""
 INFRASTRUCTURE KNOWLEDGE SHARING

Topic: {topic}

Technical Details:
{technical_details}

Impact on Your Team:
{chr(10).join([f"- {team}: {impact}" for team, impact in impact_on_teams.items()])}

{f'''Best Practices Learned:
{chr(10).join([f"✓ {practice}" for practice in best_practices])}''' if best_practices else ''}

Why This Matters:
Infrastructure changes affect how applications run and how users experience
the system. Understanding these details helps you support users better and
diagnose issues faster.

How to Use This Knowledge:
- App Support: Consider infrastructure constraints in application design
- Network Support: Understand infrastructure dependencies
- IT Support: Better explain infrastructure impacts to users
- Everyone: Reference when troubleshooting related issues

Questions?
I'm happy to explain any technical details in more depth. My goal is making
infrastructure transparent and understandable for all teams.

Ubuntu Principle: "When infrastructure knowledge is shared, everyone succeeds"

Documented for future reference in our knowledge base.
        """
        
        knowledge_package["message"] = sharing_message
        logging.info(f"Infrastructure knowledge '{topic}' shared with all teams")
        
        return knowledge_package
    
    def coordinate_with_network_team(self, coordination_need: str, server_details: dict, network_impact: str):
        """
        Coordinates with Network Support on infrastructure-network issues.
        
        Infrastructure and network often need to work together on connectivity,
        performance, and security issues.
        
        Args:
            coordination_need: Why infrastructure and network need to coordinate
            server_details: Dict with relevant server information
            network_impact: Description of network-related aspects
            
        Returns:
            dict: Network coordination framework
        """
        logging.info(f"Infrastructure agent '{self.name}' coordinating with Network Support")
        
        coordination_framework = {
            "coordination_need": coordination_need,
            "server_details": server_details,
            "network_impact": network_impact,
            "coordinating_agents": [self.name, "Network Support"],
            "ubuntu_principle": "Infrastructure and network together ensure system reliability",
            "status": "coordinating"
        }
        
        coordination_message = f"""
 INFRASTRUCTURE-NETWORK COORDINATION

Coordination Need: {coordination_need}

Infrastructure Perspective:
Server Details:
{chr(10).join([f"- {key}: {value}" for key, value in server_details.items()])}

Network Impact:
{network_impact}

Why We Need to Work Together:
Infrastructure and network are two sides of the same system. Server
performance depends on network connectivity, and network efficiency
depends on server responsiveness.

What I'm Providing:
- Server-side metrics and logs
- Infrastructure configuration details
- Server performance patterns
- Capacity and resource utilization

What I Need From Network Support:
- Network path analysis
- Bandwidth utilization data
- Connectivity patterns
- Network configuration insights

Collaborative Approach:
1. Share our respective domain findings
2. Build complete system picture together
3. Identify root cause collaboratively
4. Implement coordinated solution
5. Monitor jointly to verify resolution

Ubuntu Principle: "Infrastructure and network together - stronger than either alone"

Let's coordinate for complete system health!
        """
        
        coordination_framework["message"] = coordination_message
        logging.info("Infrastructure-Network coordination initiated")
        
        return coordination_framework
    
    def coordinate_with_app_team(self, coordination_need: str, infrastructure_metrics: dict, application_impact: str):
        """
        Coordinates with App Support on application-infrastructure issues.
        
        Infrastructure performance directly affects applications. Coordination ensures
        optimal performance for both layers.
        
        Args:
            coordination_need: Why infrastructure and applications need to coordinate
            infrastructure_metrics: Dict with server performance data
            application_impact: Description of how infrastructure affects applications
            
        Returns:
            dict: Application coordination framework
        """
        logging.info(f"Infrastructure agent '{self.name}' coordinating with App Support")
        
        coordination_framework = {
            "coordination_need": coordination_need,
            "infrastructure_metrics": infrastructure_metrics,
            "application_impact": application_impact,
            "coordinating_agents": [self.name, "App Support"],
            "ubuntu_principle": "Infrastructure serves applications - together we optimize",
            "status": "coordinating"
        }
        
        coordination_message = f"""
 INFRASTRUCTURE-APPLICATION COORDINATION

Coordination Need: {coordination_need}

Infrastructure Metrics:
{chr(10).join([f"- {key}: {value}" for key, value in infrastructure_metrics.items()])}

Application Impact:
{application_impact}

Why Coordination Matters:
Applications run on infrastructure. When infrastructure performance changes,
applications are affected. When applications have new requirements,
infrastructure must adapt.

What Infrastructure Provides:
- Server resource availability (CPU, memory, disk)
- Database performance metrics
- Storage and backup status
- Capacity and scaling possibilities

What I Need From App Support:
- Application performance patterns
- Resource requirements and usage
- Query patterns and optimization opportunities
- Scaling needs and timing

Collaborative Optimization:
1. Share infrastructure capabilities and constraints
2. Understand application requirements and behavior
3. Find optimal configuration together
4. Implement coordinated improvements
5. Monitor performance improvements jointly

Best Outcomes:
- Infrastructure tuned for application needs
- Applications optimized for infrastructure reality
- Performance issues diagnosed faster together
- Capacity planning aligned with application roadmap

Ubuntu Principle: "Infrastructure and applications succeed together"

Let's optimize the full stack collaboratively!
        """
        
        coordination_framework["message"] = coordination_message
        logging.info("Infrastructure-Application coordination initiated")
        
        return coordination_framework
    
    def get_agent_status(self):
        """Returns the current status of the agent."""
        return {
            "agent_id": self.name,
            "agent_type": self.agent_type,
            "specialization": self.specialization,
            "status": "active",
            "ubuntu_principles_active": self.ubuntu_principles,
            "infrastructure_state": self.infrastructure_state,
            "reports_to": "IT Manager",
            "collaboration_capabilities": [
                "ubuntu_collaborate",
                "share_infrastructure_knowledge",
                "coordinate_with_network_team",
                "coordinate_with_app_team"
            ]
        }
