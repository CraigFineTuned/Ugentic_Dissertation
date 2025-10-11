import argparse
import json
from langchain_ollama import ChatOllama
from src.ugentic.core.rag_core import RAGCore, get_ollama_embeddings, get_text_splitter
from app import initialize_react_agents, process_user_request, get_embedding_model_from_config

def run_integration_tests(fast_mode=False):
    """Runs the integration tests for the new app.py"""

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

    # Initialize React agents
    print("2. Initializing React Agents with Ubuntu Orchestration...")
    agents = initialize_react_agents(llm)
    print(f"   {len(agents)} agents initialized\n")

    # Initialize RAG system
    print("3. Initializing RAG Knowledge Base...")
    embedding_model_name = get_embedding_model_from_config()
    ollama_embed = get_ollama_embeddings(embedding_model_name)
    splitter = get_text_splitter()
    rag_system = RAGCore(ollama_embed, splitter, None) # Passing None for unused filesystem_tool
    print("   RAG system ready\n")

    # --- TEST CASES ---
    single_domain_test = "Server disk space at 95%"
    multi_domain_test = "Users experiencing slow application performance"

    print(f"{ '='*60}")
    print("STARTING INTEGRATION TESTS")
    print(f"{ '='*60}\n")

    # --- RUN SINGLE-DOMAIN TEST ---
    print("--- TEST 1: SINGLE-DOMAIN SCENARIO ---")
    process_user_request(single_domain_test, agents, rag_system)

    # --- RUN MULTI-DOMAIN TEST ---
    print("--- TEST 2: MULTI-DOMAIN SCENARIO ---")
    process_user_request(multi_domain_test, agents, rag_system)

    print(f"{ '='*60}")
    print("INTEGRATION TESTS COMPLETE")
    print(f"{ '='*60}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run integration tests for the UGENTIC system.')
    parser.add_argument('--fast', action='store_true', 
                       help='Use fast model (gemma:2b) instead of config.json model')
    args = parser.parse_args()
    run_integration_tests(fast_mode=args.fast)
