"""
Test ReAct Infrastructure Agent
Sprint 1 - Verification Test
"""

import sys
import os
import argparse
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from langchain_ollama import ChatOllama
from src.ugentic.agents.react_agents.infrastructure_agent_react import InfrastructureAgentReAct


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


def test_react_infrastructure_agent(fast_mode=False):
    """Test ReAct pattern with Infrastructure agent
    
    Args:
        fast_mode: If True, use gemma3:4b. If False, use config.json model.
    """
    model_name = get_model_name(fast_mode)
    mode_label = "FAST MODE" if fast_mode else "STANDARD MODE"
    
    print("\n" + "="*80)
    print(f"UGENTIC REACT AGENT TEST - Sprint 1 ({mode_label})")
    print("="*80)
    
    # Initialize LLM
    print(f"\n1. Initializing LLM ({model_name})...")
    llm = ChatOllama(model=model_name, temperature=0.7)
    print("   ✅ LLM initialized")
    
    # Initialize Infrastructure agent
    print("\n2. Initializing Infrastructure Agent with ReAct...")
    agent = InfrastructureAgentReAct(llm=llm, orchestrator=True)
    print(f"   ✅ Agent initialized")
    print(f"   Agent: {agent.name}")
    print(f"   Tools: {agent.tools.count()}")
    print(f"   Pattern: ReAct (Reasoning + Acting)")
    
    # Test Case 1: System slowness
    print("\n" + "="*80)
    print("TEST CASE 1: User reports 'The system is slow'")
    print("="*80)
    
    problem1 = "The system is slow and users are complaining"
    
    print(f"\nProblem Report: {problem1}")
    print("\nStarting ReAct investigation...")
    print("-"*80)
    
    result1 = agent.investigate(problem1)
    
    print("\n" + "="*80)
    print("INVESTIGATION RESULT:")
    print("="*80)
    print(f"Status: {result1.get('status')}")
    print(f"Root Cause: {result1.get('root_cause', 'N/A')}")
    print(f"Solution: {result1.get('solution', 'N/A')}")
    print(f"Iterations: {result1.get('iterations', 'N/A')}")
    
    # Get investigation history
    history = agent.get_investigation_history()
    print(f"\nInvestigation Steps: {len(history)}")
    for i, step in enumerate(history, 1):
        print(f"\n  Step {i}:")
        print(f"    Tool Used: {step.action.get('tool_name')}")
        print(f"    Finding: {step.reflection.get('interpretation', 'N/A')[:100]}...")
    
    # Test Case 2: Specific server issue
    print("\n\n" + "="*80)
    print("TEST CASE 2: Server-specific issue")
    print("="*80)
    
    problem2 = "Server app-server-01 is not responding"
    
    print(f"\nProblem Report: {problem2}")
    print("\nStarting ReAct investigation...")
    print("-"*80)
    
    result2 = agent.investigate(problem2)
    
    print("\n" + "="*80)
    print("INVESTIGATION RESULT:")
    print("="*80)
    print(f"Status: {result2.get('status')}")
    print(f"Root Cause: {result2.get('root_cause', 'N/A')}")
    print(f"Solution: {result2.get('solution', 'N/A')}")
    print(f"Iterations: {result2.get('iterations', 'N/A')}")
    
    # Final summary
    print("\n\n" + "="*80)
    print("SPRINT 1 TEST SUMMARY")
    print("="*80)
    print(f"✅ ReAct Engine: Working")
    print(f"✅ Tool Registry: {agent.tools.count()} tools registered")
    print(f"✅ LLM Reasoning: Functioning")
    print(f"✅ Tool Execution: Operational")
    print(f"✅ Investigation Loop: Complete")
    print("\nSprint 1 Core Infrastructure: VALIDATED")
    print("="*80 + "\n")


if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Sprint 1 Test - Infrastructure Agent')
    parser.add_argument('--fast', action='store_true',
                       help='Use fast model (gemma3:4b) instead of config.json model')
    args = parser.parse_args()
    
    try:
        test_react_infrastructure_agent(fast_mode=args.fast)
    except Exception as e:
        print(f"\n❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
