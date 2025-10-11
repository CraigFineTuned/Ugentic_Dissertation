# IT Departmental Agents for Sun International GrandWest Case Study
# UGENTIC Framework - Ubuntu-Driven Departmental Collective Intelligence  

import logging
from ..core.rag_core import RAGCore

# Import standard working agents
from .departmental_agents.agent_itsupport import Agent_ITSupport
from .departmental_agents.agent_itmanager import Agent_ITManager
from .departmental_agents.agent_infrastructure import Agent_Infrastructure
from .departmental_agents.agent_service_desk_manager import Agent_Service_Desk_Manager
from .departmental_agents.agent_network_support import Agent_Network_Support
from .departmental_agents.agent_app_support import Agent_App_Support

def initialize_it_departmental_agents(rag_system_instance: RAGCore, llm_model=None, filesystem_tool=None, git_tool=None, research_tool=None):
    """
    Initialize Sun International GrandWest IT departmental agents
    
    Ubuntu Principle: Each agent exists through its relationships with others
    Case Study: Real IT department structure and workflows
    
    Returns:
        Dict of IT departmental agents ready for Ubuntu collaboration
    """
    
    logging.info(" Initializing UGENTIC agents with Ubuntu framework...")
    
    # Shared knowledge base for collective learning
    shared_knowledge_base = {
        "shared_resolutions": [],
        "collaboration_history": [],
        "ubuntu_practices": {
            "collective_decision_making": True,
            "mutual_support": True,
            "knowledge_sharing": True,
            "shared_accountability": True
        }
    }
    
    # Initialize agents
    agent_itsupport = Agent_ITSupport(
        agent_id="itsupport_001",
        knowledge_base=shared_knowledge_base.copy()
    )
    
    agent_itmanager = Agent_ITManager(
        rag_system=rag_system_instance,
        llm_model=llm_model
    )
    
    agent_infrastructure = Agent_Infrastructure(
        rag_system=rag_system_instance,
        llm_model=llm_model
    )

    agent_service_desk_manager = Agent_Service_Desk_Manager(
        name="Service Desk Manager",
        persona="A tactical coordinator focused on operational efficiency and user satisfaction",
        rag_system=rag_system_instance,
        llm_model=llm_model
    )
    
    agent_network_support = Agent_Network_Support(
        name="Network Support",
        persona="A proactive guardian of network connectivity and security",
        rag_system=rag_system_instance,
        llm_model=llm_model
    )
    
    agent_app_support = Agent_App_Support(
        name="App Support",
        persona="A bridge between business applications and technical infrastructure",
        rag_system=rag_system_instance,
        llm_model=llm_model
    )
    
    # Build the agent collective
    it_agents = {
        "ITSupport": agent_itsupport,
        "ITManager": agent_itmanager,
        "Infrastructure": agent_infrastructure,
        "ServiceDeskManager": agent_service_desk_manager,
        "NetworkSupport": agent_network_support,
        "AppSupport": agent_app_support,
    }
    
    # Ubuntu principle: Register relationships so agents know they exist through others
    for agent_name, agent_obj in it_agents.items():
        if hasattr(agent_obj, 'departmental_relationships'):
            dept_mapping = {
                "server_infrastructure": "Infrastructure",
                "app_support": "AppSupport",
                "service_desk_manager": "ServiceDeskManager",
                "it_manager": "ITManager",
                "it_support": "ITSupport",
                "network_support": "NetworkSupport",
                "application_support": "AppSupport"
            }
            
            for dept_key in list(agent_obj.departmental_relationships.keys()):
                mapped_agent = dept_mapping.get(dept_key)
                if mapped_agent and mapped_agent in it_agents:
                    agent_obj.departmental_relationships[dept_key] = it_agents[mapped_agent]
    
    logging.info(f" Initialized {len(it_agents)} IT departmental agents with Ubuntu principles")
    logging.info(f" Framework: Standard Agents + Ubuntu Collaboration")
    
    return it_agents

def get_it_agent_status_summary(it_agents: dict) -> dict:
    """Get collective status summary of all IT agents"""
    summary = {
        "total_agents": len(it_agents),
        "framework": "Standard_Ubuntu",
        "agent_statuses": {}
    }
    
    for agent_name, agent_obj in it_agents.items():
        if hasattr(agent_obj, 'get_agent_status'):
            agent_status = agent_obj.get_agent_status()
            summary["agent_statuses"][agent_name] = agent_status
    
    return summary

# Export main functions
__all__ = [
    'initialize_it_departmental_agents',
    'get_it_agent_status_summary',
]
