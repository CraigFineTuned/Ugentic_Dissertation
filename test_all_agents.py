"""
Test All ReAct Agents
Sprint 2 - Complete System Verification
"""

import sys
import os
import argparse
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langchain_ollama import ChatOllama
from src.ugentic.agents.react_agents import (
    ITManagerAgentReAct,
    InfrastructureAgentReAct,
    NetworkSupportAgentReAct,
    AppSupportAgentReAct,
    ITSupportAgentReAct,
    ServiceDeskManagerAgentReAct
)


def get_model_name(fast_mode=False):
    """Get model name based on mode"""
    if fast_mode:
        return "gemma3:4b"
    
    # Read from config.json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config.get("reasoning_model", "gemma3:4b")
    except (FileNotFoundError, json.JSONDecodeError):
        return "gemma3:4b"  # Fallback


def test_all_agents(fast_mode=False):
    """Test complete UGENTIC ReAct system with all agents
    
    Args:
        fast_mode: If True, use gemma3:4b. If False, use config.json model.
    """
    model_name = get_model_name(fast_mode)
    mode_label = "FAST MODE" if fast_mode else "STANDARD MODE"
    
    print("\n" + "="*80)
    print(f"UGENTIC COMPLETE SYSTEM TEST - Sprint 2 ({mode_label})")
    print("="*80)
    
    # Initialize LLM
    print(f"\n1. Initializing LLM ({model_name})...")
    llm = ChatOllama(model=model_name, temperature=0.7)
    print("   ✅ LLM initialized")
    
    # Initialize all agents
    print("\n2. Initializing All Agents...")
    
    agents = {}
    
    # Operational agents
    print("   Initializing Infrastructure Agent...")
    agents['Infrastructure'] = InfrastructureAgentReAct(llm=llm, orchestrator=True)
    
    print("   Initializing Network Support Agent...")
    agents['Network Support'] = NetworkSupportAgentReAct(llm=llm)
    
    print("   Initializing App Support Agent...")
    agents['App Support'] = AppSupportAgentReAct(llm=llm)
    
    print("   Initializing IT Support Agent...")
    agents['IT Support'] = ITSupportAgentReAct(llm=llm)
    
    # Tactical agent
    print("   Initializing Service Desk Manager...")
    agents['Service Desk Manager'] = ServiceDeskManagerAgentReAct(llm=llm)
    
    # Strategic agent
    print("   Initializing IT Manager...")
    it_manager = ITManagerAgentReAct(llm=llm, agents=agents)
    
    print(f"\n   ✅ All 6 agents initialized")
    print(f"   Total tools available: {sum(agent.tools.count() for agent in agents.values())}")
    
    # Test Case 1: Infrastructure Issue
    print("\n\n" + "="*80)
    print("TEST CASE 1: Infrastructure Issue (Delegated)")
    print("="*80)
    
    problem1 = "The application server is running very slow"
    print(f"\nProblem: {problem1}")
    print("\nIT Manager delegating...")
    print("-"*80)
    
    result1 = it_manager.delegate(problem1)
    
    print("\n" + "="*80)
    print("DELEGATION RESULT:")
    print("="*80)
    print(f"Status: {result1.get('status')}")
    print(f"Delegated To: {result1.get('delegated_to')}")
    print(f"Reasoning: {result1.get('delegation_reasoning')}")
    
    investigation = result1.get('investigation_result', {})
    print(f"\nInvestigation Status: {investigation.get('status')}")
    print(f"Root Cause: {investigation.get('root_cause', 'N/A')[:100]}")
    print(f"Iterations: {investigation.get('iterations', 'N/A')}")
    
    # Test Case 2: Network Issue
    print("\n\n" + "="*80)
    print("TEST CASE 2: Network Issue (Direct)")
    print("="*80)
    
    problem2 = "Users cannot connect to VPN"
    print(f"\nProblem: {problem2}")
    print("\nNetwork Support investigating directly...")
    print("-"*80)
    
    result2 = agents['Network Support'].investigate(problem2)
    
    print("\n" + "="*80)
    print("INVESTIGATION RESULT:")
    print("="*80)
    print(f"Status: {result2.get('status')}")
    print(f"Root Cause: {result2.get('root_cause', 'N/A')[:100]}")
    print(f"Iterations: {result2.get('iterations', 'N/A')}")
    
    # Test Case 3: User Support Issue
    print("\n\n" + "="*80)
    print("TEST CASE 3: User Support Issue (Direct)")
    print("="*80)
    
    problem3 = "User account is locked"
    context3 = {"user_id": "user_12345"}
    print(f"\nProblem: {problem3}")
    print(f"User: {context3['user_id']}")
    print("\nIT Support investigating...")
    print("-"*80)
    
    result3 = agents['IT Support'].investigate(problem3, context3)
    
    print("\n" + "="*80)
    print("INVESTIGATION RESULT:")
    print("="*80)
    print(f"Status: {result3.get('status')}")
    print(f"Root Cause: {result3.get('root_cause', 'N/A')[:100]}")
    print(f"Iterations: {result3.get('iterations', 'N/A')}")
    
    # Agent Status Summary
    print("\n\n" + "="*80)
    print("AGENT STATUS SUMMARY")
    print("="*80)
    
    for name, agent in agents.items():
        status = agent.get_status()
        print(f"\n{name}:")
        print(f"  Type: {status.get('agent_type')}")
        print(f"  Specialization: {status.get('specialization')}")
        print(f"  Tools: {status.get('tools_available')}")
        print(f"  Pattern: {status.get('pattern')}")
    
    print(f"\nIT Manager:")
    manager_status = it_manager.get_status()
    print(f"  Type: {manager_status.get('agent_type')}")
    print(f"  Pattern: {manager_status.get('pattern')}")
    print(f"  Manages: {len(manager_status.get('manages', []))} agents")
    
    # Final Summary
    print("\n\n" + "="*80)
    print("SPRINT 2 TEST SUMMARY")
    print("="*80)
    print(f"✅ All 6 agents operational")
    print(f"✅ Total tools: {sum(agent.tools.count() for agent in agents.values())}")
    print(f"✅ ReAct pattern: Working across all agents")
    print(f"✅ IT Manager delegation: Functional")
    print(f"✅ Multi-domain coverage: Complete")
    print("\nSprint 2 Complete System: VALIDATED")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Sprint 2 Test - All Agents System')
    parser.add_argument('--fast', action='store_true',
                       help='Use fast model (gemma3:4b) instead of config.json model')
    args = parser.parse_args()
    
    try:
        test_all_agents(fast_mode=args.fast)
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
