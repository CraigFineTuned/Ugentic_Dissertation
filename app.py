"""
UGENTIC - Ubuntu-Driven Agentic Collective Intelligence
Multi-agent IT support system with hierarchical orchestration

Entry point for the system with robust configuration management and error handling
"""

import sys
import os

# Force Python to use the local source code
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

from langchain_ollama import ChatOllama

from src.ugentic.config_manager import get_config
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
from src.ugentic.tools.support_tools import set_rag_system


class SystemInitializationError(Exception):
    """Raised when system initialization fails"""
    pass


def initialize_llm(model_name: str, timeout: int = 30) -> ChatOllama:
    """
    Initialize LLM with proper error handling
    
    Args:
        model_name: Name of the model to use
        timeout: Timeout for LLM connections in seconds
        
    Returns:
        Initialized ChatOllama instance
        
    Raises:
        SystemInitializationError: If LLM initialization fails
    """
    try:
        print(f"\n✓ Initializing LLM: {model_name}")
        llm = ChatOllama(model=model_name, temperature=0.7, timeout=timeout)
        print(f"  Model: {model_name}")
        print(f"  Ready for inference\n")
        return llm
    except Exception as e:
        raise SystemInitializationError(
            f"Failed to initialize LLM with model '{model_name}'\n"
            f"Error: {str(e)}\n"
            f"Ensure Ollama is running: ollama serve"
        )


def initialize_embeddings(embedding_model: str) -> Any:
    """
    Initialize embeddings model with graceful fallback
    
    Args:
        embedding_model: Name of the embedding model
        
    Returns:
        Embeddings model or None if initialization fails
    """
    try:
        print(f"✓ Initializing Embeddings: {embedding_model}")
        embeddings = get_ollama_embeddings(embedding_model)
        print(f"  Embeddings ready\n")
        return embeddings
    except Exception as e:
        print(f"⚠ Warning: Failed to initialize embeddings")
        print(f"  Error: {str(e)}")
        print(f"  RAG and memory will be disabled\n")
        return None


def initialize_agents(
    llm: ChatOllama,
    logger: Optional[InvestigationLogger] = None,
    planner: Optional[ExplicitPlanner] = None
) -> Dict[str, Any]:
    """
    Initialize all ReAct agents with orchestration
    
    SESSION 30 FIX: Set orchestrator reference after Infrastructure creation
    Enables upfront triage at IT Manager level
    """
    print("✓ Initializing React Agents")
    print("  Creating specialist agents...")
    
    # Initialize specialist agents first
    agents = {
        'Network Support': NetworkSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'App Support': AppSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'IT Support': ITSupportAgentReAct(llm=llm, logger=logger, planner=planner),
        'Service Desk Manager': ServiceDeskManagerAgentReAct(llm=llm, logger=logger, planner=planner)
    }
    
    # Initialize Infrastructure with orchestration (lead agent)
    print("  Creating orchestrator (Infrastructure)...")
    agents['Infrastructure'] = InfrastructureAgentReAct(
        llm=llm,
        orchestrator=True,
        agents=agents,
        logger=logger,
        planner=planner
    )
    
    # Initialize IT Manager WITHOUT orchestrator reference
    print("  Creating IT Manager...")
    agents['IT Manager'] = ITManagerAgentReAct(llm=llm, agents=agents)
    
    # SESSION 30 FIX: Set orchestrator reference AFTER Infrastructure is created
    # This enables upfront triage at delegation layer
    print("  Linking IT Manager to Orchestrator (SESSION 30 fix)...")
    agents['IT Manager'].set_orchestrator(agents['Infrastructure'])
    
    print(f"✓ {len(agents)} agents initialized")
    print(f"  Ubuntu Orchestration: Enabled")
    print(f"  Upfront Triage: Enabled\n")
    
    return agents


def initialize_rag_system(config, embeddings: Optional[Any]) -> Optional[RAGCore]:
    """
    Initialize RAG system with graceful fallback
    
    Args:
        config: Configuration manager
        embeddings: Embeddings model (may be None)
        
    Returns:
        Initialized RAGCore or None if unavailable
    """
    if embeddings is None:
        print("ℹ RAG system skipped (embeddings unavailable)\n")
        return None
    
    try:
        print("✓ Initializing RAG Knowledge Base")
        splitter = get_text_splitter()
        rag_system = RAGCore(embeddings, splitter, None)
        
        kb_path = Path(config.knowledge_base_dir)
        docs = list(kb_path.glob("*")) if kb_path.exists() else []
        
        if docs:
            rag_system.load_documents_from_directory(str(kb_path))
            print(f"  Loaded {len(docs)} documents")
        else:
            print(f"  No documents found (will use empty knowledge base)")
        
        print(f"  Path: {config.knowledge_base_dir}\n")
        return rag_system
    except Exception as e:
        print(f"⚠ Warning: RAG system initialization failed")
        print(f"  Error: {str(e)}\n")
        return None


def initialize_memory_system(embeddings: Optional[Any]) -> Optional[AgentMemory]:
    """
    Initialize memory system with graceful fallback
    
    Args:
        embeddings: Embeddings model (may be None)
        
    Returns:
        Initialized AgentMemory or None if unavailable
    """
    if embeddings is None:
        print("ℹ Agent Memory skipped (embeddings unavailable)\n")
        return None
    
    try:
        print("✓ Initializing Agent Memory System")
        memory = AgentMemory(embeddings_model=embeddings)
        
        if memory.start():
            print(f"  Cross-session learning: Enabled\n")
            return memory
        else:
            print(f"⚠ Memory system failed to start")
            print(f"  Running with logs only\n")
            return None
    except Exception as e:
        print(f"⚠ Warning: Agent Memory not available")
        print(f"  Error: {str(e)}")
        print(f"  Running with logs only\n")
        return None


def process_user_request(
    user_input: str,
    agents: Dict[str, Any],
    rag_system: Optional[RAGCore],
    logger: InvestigationLogger
) -> Dict[str, Any]:
    """
    Process a user request through the agent system

    ARCHITECTURAL CHANGE (Dec 3, 2025):
    Entry point changed from IT Manager to IT Support (Level 1)
    Flow: IT Support → Escalate if needed → Service Desk routes → Specialist

    Args:
        user_input: User's problem description
        agents: Dictionary of initialized agents
        rag_system: RAG system instance
        logger: Investigation logger

    Returns:
        Investigation result
    """
    print(f"\n{'='*60}")
    print(f"Processing: {user_input}")
    print(f"{'='*60}\n")

    # Add RAG context if available
    rag_context = []
    if rag_system:
        try:
            rag_context = rag_system.retrieve(user_input, top_k=3)
        except Exception as e:
            print(f"⚠ Warning: RAG retrieval failed: {str(e)}")

    context = {
        'user_input': user_input,
        'knowledge_base': rag_context
    }

    # STEP 1: IT Support (Level 1) attempts resolution
    print("🎧 Level 1: IT Support handling request...")
    it_support = agents.get('IT Support')
    result = it_support.investigate(user_input, context)

    # STEP 2: Check if escalation is needed
    if result.get('status') == 'NEEDS_ESCALATION':
        escalation = result.get('escalation_details', {})
        print(f"\n{'⬆'*20} ESCALATION {'⬆'*20}")
        print(f"Reason: {escalation.get('reason', 'Requires specialist expertise')}")
        print(f"{'⬆'*48}\n")

        if escalation.get('type') == 'technical':
            # Service Desk Manager routes to appropriate specialist
            print("📋 Level 2: Service Desk Manager routing to specialist...")
            service_desk = agents.get('Service Desk Manager')

            # Get routing decision from Service Desk Manager
            specialist_name = service_desk.route_escalation(
                issue=user_input,
                level1_findings=result,
                context=context
            )

            print(f"   → Routing to: {specialist_name}\n")

            # Specialist investigates (ReAct + possible orchestration)
            specialist = agents.get(specialist_name)
            if specialist:
                result = specialist.investigate(user_input, context)

                # Check if multi-agent collaboration needed
                if result.get('status') == 'NEEDS_COLLABORATION':
                    print(f"\n{'!'*20} MULTI-AGENT COLLABORATION {'!'*20}")
                    print(f"Escalating to Infrastructure orchestrator...")
                    print(f"{'!'*58}\n")

                    orchestrator = agents.get('Infrastructure')
                    if orchestrator:
                        result = orchestrator.investigate(user_input, context)
                    else:
                        print("⚠ ERROR: Orchestrator agent not found!")
            else:
                print(f"⚠ ERROR: Specialist '{specialist_name}' not found!")

        elif escalation.get('type') == 'strategic':
            # Strategic decision needed - escalate to IT Manager
            print("🎯 Level 3: IT Manager handling strategic decision...")
            it_manager = agents.get('IT Manager')
            if it_manager:
                result = it_manager.handle_strategic_issue(user_input, result, context)
            else:
                print("⚠ ERROR: IT Manager not found!")

    # Display results
    display_results(result, rag_context)

    return result


def display_results(result: Dict[str, Any], rag_docs: list):
    """Display investigation results to user"""
    print(f"\n{'='*60}")
    print(f"INVESTIGATION RESULT")
    print(f"{'='*60}\n")
    
    status = result.get('status')
    
    if status == 'UBUNTU_COLLABORATION_COMPLETE':
        print("✓ UBUNTU ORCHESTRATION EXECUTED")
        print(f"\n  Collaboration ID: {result.get('collaboration_id')}")
        print(f"  Participating Agents: {', '.join(result.get('participating_agents', []))}")
        print(f"\n  Root Cause:")
        print(f"    {result.get('root_cause')}")
        print(f"\n  Solution:")
        print(f"    {result.get('solution')}")
        print(f"\n  Ubuntu Value:")
        print(f"    {result.get('ubuntu_value')}")
    
    elif status == 'RESOLVED':
        print("✓ ISSUE RESOLVED")
        print(f"\n  Root Cause:")
        print(f"    {result.get('root_cause')}")
        print(f"\n  Solution:")
        print(f"    {result.get('solution')}")
        print(f"\n  Iterations: {result.get('iterations', 'N/A')}")
    
    elif status == 'NEEDS_COLLABORATION':
        print("⚠ REQUIRES COLLABORATION")
        print(f"\n  Reason: {result.get('reason')}")
        print(f"  Required Agents: {', '.join(result.get('required_agents', []))}")
    
    else:
        print(f"Status: {status}")
        print(f"Details: {result}")
    
    # Show relevant knowledge base articles
    if rag_docs:
        print(f"\n📚 Relevant Knowledge Base Articles:")
        for doc in rag_docs:
            similarity = doc.get('similarity', 0)
            text = doc.get('chunk_text', 'N/A')[:150]
            print(f"   • ({similarity:.2f}) {text}...")
    
    print(f"\n{'='*60}\n")


def show_welcome_message():
    """Display welcome message and usage information"""
    print(f"\n{'='*60}")
    print(f"UGENTIC - Ubuntu IT Support System")
    print(f"Multi-Agent Orchestration with Ubuntu Philosophy")
    print(f"{'='*60}\n")
    print("Enter IT support requests (or 'quit' to exit)")
    print("\nExample requests:")
    print("  • Users experiencing slow application performance")
    print("  • Server disk space at 95%")
    print("  • VPN connectivity issues for remote users")
    print("  • Application crashes when users log in\n")


def run_demo(fast_mode: bool = False):
    """
    Main demonstration function
    
    Args:
        fast_mode: Use faster model if True
    """
    # Load configuration
    config = get_config()
    print(f"\n{'='*60}")
    print(f"UGENTIC System Initialization")
    print(f"{'='*60}\n")
    print("Configuration Summary:")
    for key, value in config.get_config_summary().items():
        print(f"  {key}: {value}")
    print()
    
    # Setup logging
    try:
        setup_logging()
        print("✓ Logging system initialized\n")
    except Exception as e:
        print(f"⚠ Warning: Logging initialization failed: {str(e)}\n")
    
    # Determine model
    if fast_mode:
        model_name = "gemma:2b"
        print(f"🚀 Fast Mode: Using {model_name}\n")
    else:
        model_name = config.reasoning_model
        print(f"🧠 Standard Mode: Using {model_name}\n")
    
    # Initialize systems
    try:
        # LLM
        llm = initialize_llm(model_name)
        
        # Embeddings
        embeddings = initialize_embeddings(config.embedding_model)
        
        # Investigation Logger
        print("✓ Initializing Investigation Logger")
        logger = InvestigationLogger(base_dir=config.logs_dir)
        print(f"  Path: {config.logs_dir}\n")
        
        # Memory System
        memory = initialize_memory_system(embeddings)
        
        # Explicit Planning
        print("✓ Initializing Explicit Planning System")
        planner = ExplicitPlanner(plans_directory=config.plans_dir)
        print(f"  Path: {config.plans_dir}\n")
        
        # Agents
        agents = initialize_agents(llm, logger=logger, planner=planner)
        
        # RAG System
        rag_system = initialize_rag_system(config, embeddings)
        
        # Connect RAG to tools
        if rag_system:
            set_rag_system(rag_system)
            print("✓ RAG connected to IT Support tools\n")
        
        # Ready
        print(f"{'='*60}")
        print(f"✓ SYSTEM READY")
        print(f"{'='*60}\n")
        
    except SystemInitializationError as e:
        print(f"\n❌ SYSTEM INITIALIZATION FAILED")
        print(f"Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR DURING INITIALIZATION")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Interactive loop
    show_welcome_message()
    
    try:
        while True:
            user_input = input("Your request: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n💾 Saving session summary...")
                logger.save_session_summary()
                
                # Display memory statistics if available
                if memory and logger.memory:
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
                    try:
                        memory.stop()
                    except Exception as e:
                        print(f"Note: Memory server stop failed: {str(e)}")
                
                print("✓ Thank you for using UGENTIC!\n")
                break
            
            if not user_input:
                continue
            
            try:
                process_user_request(user_input, agents, rag_system, logger)
            except Exception as e:
                print(f"\n❌ ERROR PROCESSING REQUEST")
                print(f"Error: {str(e)}\n")
    
    except KeyboardInterrupt:
        print("\n\n⏸ Session interrupted by user")
        logger.save_session_summary()
        if memory:
            try:
                memory.stop()
            except:
                pass
        print("✓ Session saved\n")
    
    except Exception as e:
        print(f"\n❌ FATAL ERROR")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Parse arguments and run"""
    parser = argparse.ArgumentParser(
        description='UGENTIC Ubuntu Multi-Agent IT Support System'
    )
    parser.add_argument(
        '--fast',
        action='store_true',
        help='Use fast model (gemma:2b) instead of configured model'
    )
    
    args = parser.parse_args()
    run_demo(fast_mode=args.fast)


if __name__ == "__main__":
    main()
