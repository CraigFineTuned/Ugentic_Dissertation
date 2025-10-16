import json
import os
import argparse
from langchain_ollama import ChatOllama
from src.ugentic.agents.react_agents import (
    ITManagerAgentReAct,
    InfrastructureAgentReAct,
    NetworkSupportAgentReAct,
    AppSupportAgentReAct,
    ITSupportAgentReAct,
    ServiceDeskManagerAgentReAct
)
from src.ugentic.core.rag_core import RAGCore, get_ollama_embeddings, get_text_splitter
from src.ugentic.utils.investigation_logger import InvestigationLogger
from src.ugentic.core.explicit_planning import ExplicitPlanner
from src.ugentic.core.agent_memory import AgentMemory
from src.ugentic.logging_config import setup_logging
from src.ugentic.tools.support_tools import set_rag_system  # FIXED Session 22

def get_embedding_model_from_config():
    """Reads the embedding model name from the config file."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config.get('embedding_model', 'nomic-embed-text:latest')
    except FileNotFoundError:
        return 'nomic-embed-text:latest'

def initialize_react_agents(llm, logger=None, planner=None):
    """Initialize all React agents with orchestration, logging, and planning"""
    
    # Initialize specialist agents first
    agents = {
        'Network Support': NetworkSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'App Support': AppSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'IT Support': ITSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'Service Desk Manager': ServiceDeskManagerAgentReAct(llm=llm, logger=logger, planner=planner)
    }
    
    # Initialize Infrastructure with orchestration (lead agent)
    agents['Infrastructure'] = InfrastructureAgentReAct(
        llm=llm,
        orchestrator=True,
        agents=agents,
        logger=logger,
        planner=planner
    )
    
    # Initialize IT Manager (delegates only, no investigation)
    agents['IT Manager'] = ITManagerAgentReAct(llm=llm, agents=agents)
    
    return agents

def process_user_request(user_input, agents, rag_system):
    """Process user request through React agents with orchestration"""
    
    print(f"\n{'='*60}")
    print(f"Processing: {user_input}")
    print(f"{ '='*60}\n")
    
    # Step 1: IT Manager delegates
    print("IT Manager analyzing request...")
    it_manager = agents.get('IT Manager')
    delegation = it_manager.delegate(user_input)
    
    target_agent_name = delegation['agent']
    print(f"   -> Delegating to: {target_agent_name}\n")
    
    # Step 2: Agent investigates with ReAct
    target_agent = agents.get(target_agent_name)
    
    # Add RAG context
    rag_context = rag_system.retrieve(user_input, top_k=3)
    context = {
        'user_input': user_input,
        'knowledge_base': rag_context
    }
    
    # Agent investigates (ReAct + automatic orchestration)
    result = target_agent.investigate(user_input, context)

    # Check if collaboration is needed and escalate if necessary
    if result.get('status') == 'NEEDS_COLLABORATION' and not getattr(target_agent, 'is_orchestrator', False):
        print(f"\n{'! ESCALATION !'*4}")
        print(f" {target_agent_name} requires collaboration. Escalating to the lead orchestrator...")
        print(f"{'! ESCALATION !'*4}\n")
        
        # Get the orchestrator agent (assuming Infrastructure agent is the lead)
        orchestrator_agent = agents.get('Infrastructure')
        if orchestrator_agent:
            # The orchestrator agent's investigate method will trigger the orchestration
            result = orchestrator_agent.investigate(user_input, context)
        else:
            print("CRITICAL ERROR: Orchestrator agent not found!")

    # Step 3: Display results
    display_results(result, rag_context)
    
    return result

def display_results(result, rag_docs):
    """Display investigation results to user"""
    
    print(f"\n{'='*60}")
    print(f"INVESTIGATION RESULT")
    print(f"{ '='*60}\n")
    
    status = result.get('status')
    
    if status == 'UBUNTU_COLLABORATION_COMPLETE':
        print("UBUNTU ORCHESTRATION EXECUTED")
        print(f"\nCollaboration ID: {result.get('collaboration_id')}")
        print(f"Participating Agents: {', '.join(result.get('participating_agents', []))}")
        print(f"\nRoot Cause:")
        print(f"   {result.get('root_cause')}")
        print(f"\nSolution:")
        print(f"   {result.get('solution')}")
        print(f"\nUbuntu Value:")
        print(f"   {result.get('ubuntu_value')}")
    elif status == 'RESOLVED':
        print("ISSUE RESOLVED")
        print(f"\nRoot Cause:")
        print(f"   {result.get('root_cause')}")
        print(f"\nSolution:")
        print(f"   {result.get('solution')}")
        print(f"\nIterations: {result.get('iterations', 'N/A')}")
    elif status == 'NEEDS_COLLABORATION':
        print("REQUIRES COLLABORATION")
        print(f"\nReason: {result.get('reason')}")
        print(f"Required Agents: {', '.join(result.get('required_agents', []))}")
    else:
        print(f"Status: {status}")
        print(f"Details: {result}")
    
    # Show relevant knowledge base articles
    if rag_docs:
        print(f"\nRelevant Knowledge Base Articles:")
        for doc in rag_docs:
            print(f"   • ({doc['similarity']:.2f}) {doc['chunk_text'][:150]}...")
    
    print(f"\n{'='*60}\n")

def run_demo(fast_mode=False):
    """Main demonstration function"""
    
    setup_logging()
    
    # Get model
    if fast_mode:
        model_name = "gemma:2b"
        print("\nRunning in FAST MODE (gemma:2b)")
    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
        model_name = config.get('reasoning_model', 'qwen2.5:7b')
        print(f"\nRunning in STANDARD MODE ({model_name})")
    
    print(f"{ '='*60}\n")
    
    # Initialize LLM
    print("1. Initializing LLM...")
    llm = ChatOllama(model=model_name, temperature=0.7)
    print("   LLM initialized\n")
    
    # Initialize Embeddings Model (for both RAG and Memory)
    print("1.2. Initializing Embeddings Model...")
    embedding_model_name = get_embedding_model_from_config()
    ollama_embed = get_ollama_embeddings(embedding_model_name)
    print(f"   Embeddings ready: {embedding_model_name}\n")
    
    # Initialize Agent Memory with embeddings (optional - graceful fallback if not available)
    print("1.4. Initializing Agent Memory System...")
    try:
        memory = AgentMemory(embeddings_model=ollama_embed)
        memory_started = memory.start()
        if memory_started:
            print("   ✅ Agent Memory: Enabled (cross-session learning with semantic similarity)\n")
        else:
            print("   ⚠️  Agent Memory: Failed to start (falling back to logs only)\n")
            memory = None
    except Exception as e:
        print(f"   ⚠️  Agent Memory: Not available ({e})")
        print("   Running with investigation logs only\n")
        memory = None
    
    # Initialize Investigation Logger (with optional memory)
    print("1.5. Initializing Investigation Logger...")
    logger = InvestigationLogger(base_dir="logs", memory=memory)
    print("   Investigation Logger ready\n")
    
    # Initialize Explicit Planning System
    print("1.6. Initializing Explicit Planning System...")
    planner = ExplicitPlanner(plans_directory="plans")
    print("   Explicit Planner ready\n")
    
    # Initialize React agents with orchestration, logging, and planning
    print("2. Initializing React Agents with Ubuntu Orchestration + Planning...")
    agents = initialize_react_agents(llm, logger=logger, planner=planner)
    print(f"   {len(agents)} agents initialized")
    print(f"   Ubuntu Orchestration: Enabled")
    print(f"   Explicit Planning: Enabled\n")
    
    # Initialize RAG system
    print("3. Initializing RAG Knowledge Base...")
    splitter = get_text_splitter()
    rag_system = RAGCore(ollama_embed, splitter, None) # Using shared embeddings model
    doc_path = "knowledge_base"
    if os.path.exists(doc_path) and os.listdir(doc_path):
        rag_system.load_documents_from_directory(doc_path)
        print(f"   RAG system ready with {len(os.listdir(doc_path))} documents\n")
    else:
        print("   No documents found or directory is empty, RAG system initialized empty\n")
    
    # FIXED Session 22: Connect RAG system to support_tools for ask_questions
    set_rag_system(rag_system)
    print("   ✅ RAG system connected to IT Support tools\n")
    
    # Interactive loop
    print(f"{ '='*60}")
    print("UGENTIC UBUNTU IT SUPPORT SYSTEM")
    print(f"{ '='*60}\n")
    print("Enter IT support requests (or 'quit' to exit)")
    print("Examples:")
    print("  - Users experiencing slow application performance")
    print("  - Server disk space at 95%")
    print("  - VPN connectivity issues for remote users")
    print("  - Application crashes when users log in\n")
    
    while True:
        user_input = input("Your request: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\nSaving session summary...")
            logger.save_session_summary()
            
            # Display memory statistics if available
            if logger.memory:
                print("\n" + "="*60)
                print("AGENT MEMORY STATISTICS")
                print("="*60)
                memory_stats = logger.get_memory_stats()
                if memory_stats:
                    print(f"Total Investigations: {memory_stats.get('total_investigations', 0)}")
                    print(f"Ubuntu Collaborations: {memory_stats.get('ubuntu_investigations', 0)}")
                    print(f"Solo Investigations: {memory_stats.get('solo_investigations', 0)}")
                    print(f"Ubuntu Success Rate: {memory_stats.get('ubuntu_success_rate', 0):.1f}%")
                    print(f"Solo Success Rate: {memory_stats.get('solo_success_rate', 0):.1f}%")
                    print(f"Ubuntu Advantage: {memory_stats.get('ubuntu_advantage', 0):+.1f}%")
                print("="*60 + "\n")
                
                # Stop memory server
                logger.memory.stop()
            
            print("\nThank you for using UGENTIC!")
            break
        
        if not user_input:
            continue
        
        # Process request
        process_user_request(user_input, agents, rag_system)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UGENTIC Ubuntu Multi-Agent IT Support System')
    parser.add_argument('--fast', action='store_true', 
                       help='Use fast model (gemma:2b) instead of config.json model')
    args = parser.parse_args()
    
    run_demo(fast_mode=args.fast)