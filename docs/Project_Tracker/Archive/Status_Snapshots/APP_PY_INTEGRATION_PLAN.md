# App.py Sprint 3 Integration Plan

**Date:** October 10, 2025  
**Objective:** Integrate Ubuntu Orchestration into main demonstration system (app.py)  
**Priority:** HIGH - This is what will be demonstrated for dissertation

---

## Current vs. Target State

### Current app.py (OLD)
- ❌ Uses old departmental agents (no ReAct pattern)
- ❌ Manual routing functions for each agent
- ❌ No Ubuntu Orchestrator
- ❌ No Collaboration Detector
- ❌ No automatic multi-agent coordination
- ✅ Has RAG system
- ✅ Has --fast flag support

### Target app.py (NEW - Sprint 3 Integrated)
- ✅ Uses React agents with ReAct pattern
- ✅ IT Manager delegates to appropriate agent
- ✅ Ubuntu Orchestrator integrated
- ✅ Collaboration Detector integrated
- ✅ Automatic multi-agent coordination
- ✅ All Session 9 bug fixes applied
- ✅ Simple, demonstrable user experience
- ✅ RAG system integrated
- ✅ Model flexibility (--fast and standard)

---

## Integration Strategy

### Phase 1: Core Agent Replacement (30 min)
**Goal:** Replace old agents with React agents

**Changes:**
1. Import React agents from `src.ugentic.agents.react_agents`
2. Initialize React agents with LLM
3. Create agents dictionary for orchestration
4. Initialize Infrastructure agent with orchestration=True

**Files Modified:**
- `app.py` - Core changes

### Phase 2: Simplify Routing (15 min)
**Goal:** Remove manual routing, use ReAct investigation

**Changes:**
1. Remove individual route_to_X functions
2. IT Manager delegates → agent.investigate()
3. Agent uses ReAct pattern automatically
4. Ubuntu Orchestration triggers when needed

**Old Flow:**
```
User Input → IT Manager → Manual routing function → Simulated response
```

**New Flow:**
```
User Input → IT Manager → Agent.investigate() → ReAct loop → [Ubuntu Orchestration if multi-domain] → Solution
```

### Phase 3: User Experience Enhancement (15 min)
**Goal:** Show orchestration to user

**Changes:**
1. Display when orchestration triggered
2. Show participating agents
3. Display collective findings
4. Present Ubuntu value to user

**User Sees:**
```
🔍 Infrastructure investigating...
💭 Iteration 1: Checking server metrics...
🤝 Multi-domain issue detected - Initiating Ubuntu Orchestration
   └─ Network Support investigating...
   └─ App Support investigating...
🧠 Synthesizing collective findings...
✅ Solution found through Ubuntu collaboration!
```

### Phase 4: RAG Integration (10 min)
**Goal:** Connect RAG to React agents

**Changes:**
1. Pass RAG context to agent.investigate()
2. Agents can query knowledge base
3. Display relevant documentation to user

---

## Implementation Code Structure

### New app.py Structure

```python
# Imports
from langchain_ollama import ChatOllama
from src.ugentic.agents.react_agents import (
    ITManagerAgentReAct,
    InfrastructureAgentReAct,
    NetworkSupportAgentReAct,
    AppSupportAgentReAct,
    ITSupportAgentReAct,
    ServiceDeskManagerReAct
)
from src.ugentic.core.rag_core import RAGCore

def initialize_react_agents(llm):
    """Initialize all React agents with orchestration"""
    
    # Initialize specialist agents first
    agents = {
        'Network Support': NetworkSupportAgentReAct(llm=llm),
        'App Support': AppSupportAgentReAct(llm=llm),
        'IT Support': ITSupportAgentReAct(llm=llm),
        'Service Desk Manager': ServiceDeskManagerReAct(llm=llm)
    }
    
    # Initialize Infrastructure with orchestration (lead agent)
    agents['Infrastructure'] = InfrastructureAgentReAct(
        llm=llm,
        orchestrator=True,
        agents=agents
    )
    
    # Initialize IT Manager (delegates only, no investigation)
    agents['IT Manager'] = ITManagerAgentReAct(llm=llm, agents=agents)
    
    return agents

def process_user_request(user_input, agents, rag_system):
    """Process user request through React agents with orchestration"""
    
    print(f"\n{'='*60}")
    print(f"🎯 Processing: {user_input}")
    print(f"{'='*60}\n")
    
    # Step 1: IT Manager delegates
    print("📋 IT Manager analyzing request...")
    it_manager = agents.get('IT Manager')
    delegation = it_manager.delegate(user_input)
    
    target_agent_name = delegation['agent']
    print(f"   → Delegating to: {target_agent_name}\n")
    
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
    
    # Step 3: Display results
    display_results(result, rag_context)
    
    return result

def display_results(result, rag_docs):
    """Display investigation results to user"""
    
    print(f"\n{'='*60}")
    print(f"INVESTIGATION RESULT")
    print(f"{'='*60}\n")
    
    status = result.get('status')
    
    if status == 'UBUNTU_COLLABORATION_COMPLETE':
        print("✅ UBUNTU ORCHESTRATION EXECUTED")
        print(f"\nCollaboration ID: {result.get('collaboration_id')}")
        print(f"Participating Agents: {', '.join(result.get('participating_agents', []))}")
        print(f"\n🎯 Root Cause:")
        print(f"   {result.get('root_cause')}")
        print(f"\n💡 Solution:")
        print(f"   {result.get('solution')}")
        print(f"\n🤝 Ubuntu Value:")
        print(f"   {result.get('ubuntu_value')}")
    elif status == 'RESOLVED':
        print("✅ ISSUE RESOLVED")
        print(f"\n🎯 Root Cause:")
        print(f"   {result.get('root_cause')}")
        print(f"\n💡 Solution:")
        print(f"   {result.get('solution')}")
        print(f"\nIterations: {result.get('iterations', 'N/A')}")
    elif status == 'NEEDS_COLLABORATION':
        print("🤝 REQUIRES COLLABORATION")
        print(f"\nReason: {result.get('reason')}")
        print(f"Required Agents: {', '.join(result.get('required_agents', []))}")
    else:
        print(f"Status: {status}")
        print(f"Details: {result}")
    
    # Show relevant knowledge base articles
    if rag_docs:
        print(f"\n📚 Relevant Knowledge Base Articles:")
        for doc in rag_docs:
            print(f"   • ({doc['similarity']:.2f}) {doc['chunk_text'][:150]}...")
    
    print(f"\n{'='*60}\n")

def run_demo(fast_mode=False):
    """Main demonstration function"""
    
    # Get model
    if fast_mode:
        model_name = "gemma3:4b"
        print("\n🚀 Running in FAST MODE (gemma3:4b)")
    else:
        with open('config.json', 'r') as f:
            config = json.load(f)
        model_name = config.get('reasoning_model', 'qwen2.5:7b')
        print(f"\n🚀 Running in STANDARD MODE ({model_name})")
    
    print(f"{'='*60}\n")
    
    # Initialize LLM
    print("1. Initializing LLM...")
    llm = ChatOllama(model=model_name, temperature=0.7)
    print("   ✅ LLM initialized\n")
    
    # Initialize React agents with orchestration
    print("2. Initializing React Agents with Ubuntu Orchestration...")
    agents = initialize_react_agents(llm)
    print(f"   ✅ {len(agents)} agents initialized")
    print(f"   ✅ Ubuntu Orchestration: Enabled\n")
    
    # Initialize RAG system
    print("3. Initializing RAG Knowledge Base...")
    rag_system = RAGCore(embedding_model_name=get_embedding_model_from_config())
    doc_path = "documents/policies"
    if os.path.exists(doc_path):
        rag_system.ingest_documents(doc_path)
        print(f"   ✅ RAG system ready with {len(os.listdir(doc_path))} documents\n")
    else:
        print("   ⚠️ No documents found, RAG system initialized empty\n")
    
    # Interactive loop
    print(f"{'='*60}")
    print("UGENTIC UBUNTU IT SUPPORT SYSTEM")
    print(f"{'='*60}\n")
    print("Enter IT support requests (or 'quit' to exit)")
    print("Examples:")
    print("  - Users experiencing slow application performance")
    print("  - Server disk space at 95%")
    print("  - VPN connectivity issues for remote users")
    print("  - Application crashes when users log in\n")
    
    while True:
        user_input = input("🎯 Your request: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thank you for using UGENTIC!")
            break
        
        if not user_input:
            continue
        
        # Process request
        process_user_request(user_input, agents, rag_system)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='UGENTIC Ubuntu Multi-Agent IT Support System')
    parser.add_argument('--fast', action='store_true', 
                       help='Use fast model (gemma3:4b) instead of config.json model')
    args = parser.parse_args()
    
    run_demo(fast_mode=args.fast)
```

---

## Key Improvements

### 1. Simplicity
- Clear 3-step process: Delegate → Investigate → Display
- No manual routing functions
- Automatic orchestration when needed

### 2. User Experience
- Clear status messages
- Shows orchestration when it happens
- Displays Ubuntu value
- Shows relevant knowledge base

### 3. Production Quality
- All Session 9 bug fixes included
- Parameter validation working
- Context awareness operational
- Model flexibility maintained

### 4. Demonstrability
- Perfect for dissertation defense
- Shows all system capabilities
- Ubuntu principles visible
- Multi-agent coordination clear

---

## Testing After Integration

### Test Cases for New app.py

**Single-Domain Test:**
```
Input: "Server disk space at 95%"
Expected: Infrastructure investigates alone, no orchestration
```

**Multi-Domain Test:**
```
Input: "Users experiencing intermittent application timeouts"
Expected: Infrastructure → detects multi-domain → orchestration with Network + App
```

**User Support Test:**
```
Input: "User locked out of their account"
Expected: IT Support handles directly
```

---

## Timeline

**Phase 1 (Core Replacement):** 30 minutes  
**Phase 2 (Simplify Routing):** 15 minutes  
**Phase 3 (User Experience):** 15 minutes  
**Phase 4 (RAG Integration):** 10 minutes  
**Testing:** 20 minutes  

**Total:** ~90 minutes (1.5 hours)

---

## Success Criteria

✅ app.py uses React agents  
✅ Ubuntu Orchestration visible to user  
✅ Single-domain issues handled efficiently  
✅ Multi-domain issues trigger orchestration  
✅ All Session 9 fixes applied  
✅ Model flexibility works  
✅ RAG integration functional  
✅ Clean, demonstrable user experience

---

**Status:** READY TO IMPLEMENT  
**Priority:** HIGHEST - This is the dissertation demonstration system  
**Next Action:** Implement new app.py with Sprint 3 integration

**Craig, shall I proceed with implementing this new app.py?**
