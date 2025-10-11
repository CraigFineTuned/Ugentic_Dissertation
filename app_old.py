# Main application entry point for the UGENTIC framework.

import os
import json
import subprocess
import argparse
from unittest.mock import MagicMock

from src.ugentic.core.rag_core import RAGCore, get_text_splitter, get_ollama_embeddings, get_embedding_model_from_config
from src.ugentic.core.orchestrator_tool import OrchestratorTool
from src.ugentic.agents.it_departmental_agents import initialize_it_departmental_agents
from src.ugentic.core.filesystem_tool import FilesystemTool
from src.ugentic.core.git_tool import GitTool
from src.ugentic.core.research_tool import ResearchTool

from langchain_ollama.llms import OllamaLLM as Ollama # Import Ollama for live LLM interaction

def direct_ubuntu_interaction(user_goal, departmental_agents, rag_system):
    """Direct interaction with Ubuntu departmental agents."""
    print(f"\n--- Ubuntu Collective Response to: '{user_goal}' ---")
    
    # Get the main IT Support agent for demonstration
    it_support_agent = departmental_agents.get('ITSupport')
    if it_support_agent:
        print(f"🤖 {it_support_agent.agent_id} (IT Support) engaging with Ubuntu principles...")
        
        # Simulate a support request analysis
        from src.ugentic.agents.departmental_agents.agent_itsupport import SupportTicket, SupportPriority
        from datetime import datetime
        
        # Create a simulated support ticket from the user goal
        ticket = SupportTicket(
            ticket_id=f"USER_{datetime.now().timestamp()}",
            user_name="UGENTIC User",
            issue_description=user_goal,
            priority=SupportPriority.HIGH,
            category="user_request",
            time_reported=datetime.now()
        )
        
        # Analyze with Ubuntu principles
        analysis = it_support_agent.analyze_support_request(ticket)
        print(f"📋 Analysis: {analysis}")
        
        # Generate Ubuntu-enhanced communication
        communication = it_support_agent.provide_user_communication(ticket, analysis)
        print(f"💬 Ubuntu Response: {communication}")
        
        # Show Ubuntu collaboration if needed
        if analysis.get("requires_collaboration"):
            collaboration = it_support_agent.ubuntu_collaborate(
                user_goal, analysis["collaboration_targets"]
            )
            print(f"🤝 Ubuntu Collaboration: {collaboration}")
        
        # Query RAG system for relevant knowledge
        retrieved_docs = rag_system.retrieve(user_goal, top_k=2)
        if retrieved_docs:
            print(f"\n📚 Relevant Knowledge from RAG System:")
            for doc in retrieved_docs:
                print(f"  - ({doc['similarity']:.3f}) {doc['chunk_text'][:200]}...")
    else:
        print("⚠️ IT Support agent not available, but Ubuntu framework is operational!")

def route_to_infrastructure(task_goal, departmental_agents, rag_system):
    """Route task to Infrastructure agent with Ubuntu collaboration."""
    print(f"\n--- Infrastructure Ubuntu Response to: '{task_goal}' ---")
    
    infrastructure_agent = departmental_agents.get('Infrastructure')
    if infrastructure_agent:
        agent_id = getattr(infrastructure_agent, 'agent_id', getattr(infrastructure_agent, 'name', 'Infrastructure'))
        print(f"🤖 {agent_id} (Infrastructure) engaging with Ubuntu principles...")
        
        # Simple analysis for demonstration
        analysis = {
            "agent": agent_id,
            "task": task_goal,
            "requires_collaboration": True,
            "collaboration_targets": ["NetworkSupport", "AppSupport"],
            "ubuntu_approach": "strategic_consultation"
        }
        print(f"📋 Analysis: {analysis}")
        
        # Show Ubuntu collaboration if method exists
        if hasattr(infrastructure_agent, 'ubuntu_collaborate'):
            collaboration = infrastructure_agent.ubuntu_collaborate(
                task_goal, analysis.get("collaboration_targets", []), {}
            )
            print(f"🤝 Ubuntu Collaboration: {collaboration}")
        
        # Query RAG for infrastructure knowledge
        retrieved_docs = rag_system.retrieve(task_goal, top_k=2)
        if retrieved_docs:
            print(f"\n📚 Relevant Knowledge from RAG System:")
            for doc in retrieved_docs:
                print(f"  - ({doc['similarity']:.3f}) {doc['chunk_text'][:200]}...")
    else:
        print("⚠️ Infrastructure agent not available!")

def route_to_network_support(task_goal, departmental_agents, rag_system):
    """Route task to Network Support agent with Ubuntu collaboration."""
    print(f"\n--- Network Support Ubuntu Response to: '{task_goal}' ---")
    
    network_agent = departmental_agents.get('NetworkSupport')
    if network_agent:
        agent_id = getattr(network_agent, 'agent_id', getattr(network_agent, 'name', 'NetworkSupport'))
        print(f"🤖 {agent_id} (Network Support) engaging with Ubuntu principles...")
        
        # Simple analysis for demonstration
        analysis = {
            "agent": agent_id,
            "task": task_goal,
            "requires_collaboration": True,
            "collaboration_targets": ["Infrastructure"],
            "ubuntu_approach": "network_diagnosis"
        }
        print(f"📋 Analysis: {analysis}")
        
        # Show Ubuntu collaboration if method exists
        if hasattr(network_agent, 'ubuntu_collaborate'):
            collaboration = network_agent.ubuntu_collaborate(
                task_goal, analysis.get("collaboration_targets", []), {}
            )
            print(f"🤝 Ubuntu Collaboration: {collaboration}")
        
        # Query RAG for network knowledge
        retrieved_docs = rag_system.retrieve(task_goal, top_k=2)
        if retrieved_docs:
            print(f"\n📚 Relevant Knowledge from RAG System:")
            for doc in retrieved_docs:
                print(f"  - ({doc['similarity']:.3f}) {doc['chunk_text'][:200]}...")
    else:
        print("⚠️ Network Support agent not available!")

def route_to_app_support(task_goal, departmental_agents, rag_system):
    """Route task to Application Support agent with Ubuntu collaboration."""
    print(f"\n--- Application Support Ubuntu Response to: '{task_goal}' ---")
    
    app_agent = departmental_agents.get('AppSupport')
    if app_agent:
        agent_id = getattr(app_agent, 'agent_id', getattr(app_agent, 'name', 'AppSupport'))
        print(f"🤖 {agent_id} (Application Support) engaging with Ubuntu principles...")
        
        # Simple analysis for demonstration
        analysis = {
            "agent": agent_id,
            "task": task_goal,
            "requires_collaboration": True,
            "collaboration_targets": ["Infrastructure"],
            "ubuntu_approach": "application_diagnosis"
        }
        print(f"📋 Analysis: {analysis}")
        
        # Show Ubuntu collaboration if method exists
        if hasattr(app_agent, 'ubuntu_collaborate'):
            collaboration = app_agent.ubuntu_collaborate(
                task_goal, analysis.get("collaboration_targets", []), {}
            )
            print(f"🤝 Ubuntu Collaboration: {collaboration}")
        
        # Query RAG for application knowledge
        retrieved_docs = rag_system.retrieve(task_goal, top_k=2)
        if retrieved_docs:
            print(f"\n📚 Relevant Knowledge from RAG System:")
            for doc in retrieved_docs:
                print(f"  - ({doc['similarity']:.3f}) {doc['chunk_text'][:200]}...")
    else:
        print("⚠️ Application Support agent not available!")

def route_to_service_desk_manager(task_goal, departmental_agents, rag_system):
    """Route task to Service Desk Manager with Ubuntu collaboration."""
    print(f"\n--- Service Desk Manager Ubuntu Response to: '{task_goal}' ---")
    
    sdm_agent = departmental_agents.get('ServiceDeskManager')
    if sdm_agent:
        agent_id = getattr(sdm_agent, 'agent_id', getattr(sdm_agent, 'name', 'ServiceDeskManager'))
        print(f"🤖 {agent_id} (Service Desk Manager) engaging with Ubuntu principles...")
        
        # Simple analysis for demonstration
        analysis = {
            "agent": agent_id,
            "task": task_goal,
            "requires_collaboration": True,
            "team_members": ["ITSupport"],
            "ubuntu_approach": "team_coordination"
        }
        print(f"📋 Analysis: {analysis}")
        
        # Show Ubuntu collaboration if method exists
        if hasattr(sdm_agent, 'ubuntu_collaborate'):
            collaboration = sdm_agent.ubuntu_collaborate(
                task_goal, analysis.get("team_members", [])
            )
            print(f"🤝 Ubuntu Collaboration: {collaboration}")
        
        # Query RAG for team management knowledge
        retrieved_docs = rag_system.retrieve(task_goal, top_k=2)
        if retrieved_docs:
            print(f"\n📚 Relevant Knowledge from RAG System:")
            for doc in retrieved_docs:
                print(f"  - ({doc['similarity']:.3f}) {doc['chunk_text'][:200]}...")
    else:
        print("⚠️ Service Desk Manager agent not available!")

def run_demo(fast_mode=False):
    """Runs a demonstration of the UGENTIC framework.
    
    Args:
        fast_mode: If True, use gemma3:4b for quick iterations. If False, use config.json model.
    """
    mode_name = "FAST MODE (gemma3:4b)" if fast_mode else "STANDARD MODE (config.json)"
    print(f"--- Initializing UGENTIC Framework Demonstration - {mode_name} ---")

    # --- Filesystem Tool Setup ---
    with open('config.json', 'r') as f:
        config = json.load(f)
    filesystem_tool_config = config.get("filesystem_tool", {})
    filesystem_tool = FilesystemTool(**filesystem_tool_config)

    # --- Git Tool Setup ---
    git_tool_config = config.get("git_tool", {})
    git_tool = GitTool(**git_tool_config)

    # --- Research Tool Setup ---
    research_tool_config = config.get("research_tool", {})
    research_tool = ResearchTool(**research_tool_config)

    # --- Orchestrator Tool Setup ---
    orchestrator_tool_config = config.get("orchestrator_tool", {})
    orchestrator_tool = OrchestratorTool(**orchestrator_tool_config)

    # --- Live LLM Setup ---
    available_models = get_available_models()
    if not available_models:
        print("No Ollama models found. Please ensure Ollama is running and models are pulled.")
        print("Exiting.")
        return

    # Determine which model to use
    if fast_mode:
        # Fast mode: Force gemma3:4b
        selected_model_name = "gemma3:4b"
        if selected_model_name in available_models:
            print(f"🚀 FAST MODE: Using {selected_model_name} for quick iterations")
        else:
            print(f"Warning: gemma3:4b not found. Available models: {available_models}")
            selected_model_name = select_model_interactively(available_models)
    else:
        # Standard mode: Use config.json
        selected_model_name = get_configured_model()
        if selected_model_name and selected_model_name in available_models:
            print(f"⚙️  STANDARD MODE: Using configured model from config.json: {selected_model_name}")
        else:
            if selected_model_name:
                print(f"Warning: Configured model '{selected_model_name}' not found.")
            else:
                print("No model configured in config.json.")
            selected_model_name = select_model_interactively(available_models)

    if selected_model_name is None:
        print("Exiting due to no LLM model selection.")
        return

    llm_model = Ollama(model=selected_model_name) # Use a live LLM model

    # --- RAG System Setup ---
    embedding_model_name = get_embedding_model_from_config(filesystem_tool)
    # Initialize live Ollama embeddings for RAG
    ollama_embeddings = get_ollama_embeddings(embedding_model_name)
    rag_system_instance = RAGCore(ollama_embeddings, get_text_splitter(), filesystem_tool)

    # Load policy documents from the dedicated directory
    policy_documents_path = os.path.join(os.path.dirname(__file__), 'documents', 'policies')
    rag_system_instance.load_documents_from_directory(policy_documents_path, file_extensions=['.md', '.txt', '.csv'])


    # Pass the live LLM model to initialize_it_departmental_agents
    departmental_agents = initialize_it_departmental_agents(
        rag_system_instance,
        llm_model,
        filesystem_tool=filesystem_tool,
        git_tool=git_tool,
        research_tool=research_tool
    )

    # Pass the live LLM model to the Orchestrator
    # The new orchestrator tool will manage workflows and tasks
    # We will use it to create a workflow and add tasks to it
    # The departmental agents will still be used to execute the tasks
    orchestrator_tool_instance = orchestrator_tool

    # --- Test Execution ---
    # Try to create a workflow, but continue even if it fails
    workflow_name = "User Goal Workflow"
    workflow_description = "Workflow for executing user-provided high-level goals."
    workflow_id = None
    
    try:
        create_workflow_response = orchestrator_tool_instance.create_workflow(workflow_name, workflow_description)
        if create_workflow_response["status"] == "success":
            workflow_data = json.loads(create_workflow_response["content"])
            workflow_id = workflow_data["id"]
            print(f"Created workflow: {workflow_name} (ID: {workflow_id})")
        else:
            print(f"Note: Workflow creation failed ({create_workflow_response['message']}), but UGENTIC agents are still available!")
    except Exception as e:
        print(f"Note: Workflow creation failed ({str(e)}), but UGENTIC agents are still available!")
    
    # Continue with UGENTIC demonstration regardless of workflow status
    print("\n🎆 UGENTIC Framework Successfully Initialized! 🎆")
    print(f"✅ RAG System: Operational with {len(rag_system_instance.vector_store)} documents loaded")
    print(f"✅ Ubuntu Agents: {len(departmental_agents)} departmental agents ready")
    print(f"✅ LLM Model: {selected_model_name}")
    print(f"✅ Embedding Model: {embedding_model_name}")
    
    print("\n--- Available Ubuntu Departmental Agents ---")
    for agent_name, agent_obj in departmental_agents.items():
        if hasattr(agent_obj, 'get_agent_status'):
            status = agent_obj.get_agent_status()
            print(f"🤖 {agent_name}: {status['agent_type']} (Ubuntu Principles Active: {status.get('ubuntu_principles_active', {})})")
    
    print("\n--- UGENTIC Ubuntu Interaction Available ---")

    while True:
        user_input = input("\nEnter a high-level goal for the UGENTIC Ubuntu Agents (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        if user_input:
            # Try workflow approach first if available
            if workflow_id:
                try:
                    add_task_response = orchestrator_tool_instance.add_task(
                        workflowId=workflow_id,
                        title=user_input,
                        description=f"High-level goal: {user_input}",
                        priority="high",
                        estimatedDuration=60,
                        dependencies=[],
                        tags=["user_goal"]
                    )
                    if add_task_response["status"] == "success":
                        task_data = json.loads(add_task_response["content"])
                        task_id = task_data["id"]
                        print(f"Added task to workflow: {user_input} (Task ID: {task_id})")
                        print("\n--- Now engaging Ubuntu agents for this task ---")
                        direct_ubuntu_interaction(user_input, departmental_agents, rag_system_instance)
                    else:
                        print(f"Task creation failed, engaging Ubuntu agents directly...")
                        direct_ubuntu_interaction(user_input, departmental_agents, rag_system_instance)
                except Exception as e:
                    print(f"Workflow interaction failed, engaging Ubuntu agents directly...")
                    direct_ubuntu_interaction(user_input, departmental_agents, rag_system_instance)
            else:
                # Pass the goal to the IT Manager for delegation
                it_manager_agent = departmental_agents.get('ITManager')
                if it_manager_agent:
                    print(f"Goal '{user_input}' sent to IT Manager for delegation.")
                    delegation_result = it_manager_agent.decide_and_delegate(user_input)
                    print(f"IT Manager decision: {delegation_result}")
                    
                    # Handle the delegation result
                    target_agent_name = delegation_result.get("target_agent")
                    task_goal = delegation_result.get("task")

                    if target_agent_name == "ITSupport":
                        print(f"Routing task '{task_goal}' to ITSupport agent...")
                        direct_ubuntu_interaction(task_goal, departmental_agents, rag_system_instance)
                    elif target_agent_name == "Infrastructure":
                        print(f"Routing task '{task_goal}' to Infrastructure agent...")
                        route_to_infrastructure(task_goal, departmental_agents, rag_system_instance)
                    elif target_agent_name == "NetworkSupport":
                        print(f"Routing task '{task_goal}' to NetworkSupport agent...")
                        route_to_network_support(task_goal, departmental_agents, rag_system_instance)
                    elif target_agent_name == "AppSupport":
                        print(f"Routing task '{task_goal}' to AppSupport agent...")
                        route_to_app_support(task_goal, departmental_agents, rag_system_instance)
                    elif target_agent_name == "ServiceDeskManager":
                        print(f"Routing task '{task_goal}' to Service Desk Manager...")
                        route_to_service_desk_manager(task_goal, departmental_agents, rag_system_instance)
                    else:
                        print(f"Warning: Delegation target '{target_agent_name}' is not yet implemented. Cannot route task.")
                else:
                    print("IT Manager agent not found. Falling back to direct IT Support interaction.")
                    direct_ubuntu_interaction(user_input, departmental_agents, rag_system_instance)

    print("\n--- UGENTIC Framework Demonstration Complete ---")

def get_available_models():
    """Gets a list of available models from the Ollama server."""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split('\n')
        models = [line.split()[0] for line in lines[1:] if line.split()]
        return sorted(list(set(models)))
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"Error getting Ollama models: {e}")
        return []

def get_configured_model():
    """Reads the reasoning model from config.json directly."""
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get("reasoning_model")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Could not read reasoning model from config.json: {e}")
        return None

def select_model_interactively(available_models):
    """Prompts the user to select a model from a list."""
    print("\n--- Please Select an Available Ollama Model ---")
    for i, model_name in enumerate(available_models):
        print(f"{i+1}. {model_name}")

    while True:
        try:
            choice = int(input("Enter the number of the model you want to use: "))
            if 1 <= choice <= len(available_models):
                return available_models[choice - 1]
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='UGENTIC Framework - Ubuntu Multi-Agent IT Support System')
    parser.add_argument('--fast', action='store_true', 
                       help='Use fast model (gemma3:4b) instead of powerful model from config')
    args = parser.parse_args()
    
    run_demo(fast_mode=args.fast)
