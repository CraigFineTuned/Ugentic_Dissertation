# UGENTIC System Architecture

**Version:** Session 26 Production Quality  
**Date:** October 16, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture Layers](#architecture-layers)
3. [Component Details](#component-details)
4. [Data Flow](#data-flow)
5. [Configuration System](#configuration-system)
6. [Directory Structure](#directory-structure)
7. [Integration Points](#integration-points)
8. [Error Handling Strategy](#error-handling-strategy)
9. [Deployment Guide](#deployment-guide)

---

## System Overview

UGENTIC is a multi-agent IT support system that integrates Ubuntu philosophy with AI-driven organizational collaboration. The system consists of:

- **6 Hierarchical Agents** mirroring real IT department structure
- **ReAct Engine** for intelligent problem-solving with tool-use
- **Ubuntu Orchestration** for cross-departmental collaboration
- **RAG System** for knowledge-base integration
- **Structured Logging** for transparency and auditability
- **Production-Grade Configuration** for cross-platform deployment

### Key Principles

1. **Hierarchical Structure**: IT Manager → Service Desk Manager → Specialists
2. **Ubuntu Philosophy**: "I am because we are" - collective problem-solving
3. **Tool Diversity**: Smart tool selection prevents investigation loops
4. **Graceful Degradation**: System works even if some components fail
5. **Cross-Platform**: Uses dynamic paths, works on Windows/Mac/Linux

---

## Architecture Layers

### Layer 1: Entry Point (`app.py`)

**Responsibility:** System initialization and user interaction loop

**Key Functions:**
- Parse command-line arguments
- Load configuration
- Initialize all subsystems with error handling
- Maintain user interaction loop
- Handle graceful shutdown

**Best Practices:**
- Comprehensive exception handling with informative messages
- Graceful fallbacks when systems are unavailable
- Clear initialization status reporting

### Layer 2: Configuration Management (`config_manager.py`)

**Responsibility:** Centralized configuration with defaults and validation

**Features:**
- Singleton pattern for single configuration instance
- Dynamic path computation (project-root relative)
- Configuration file loading with fallbacks
- Type-safe configuration access
- Cross-platform path handling

**Usage:**
```python
from src.ugentic.config_manager import get_config

config = get_config()
logs_path = config.logs_dir
model = config.reasoning_model
```

### Layer 3: Core Infrastructure

#### Logging System (`logging_config.py`)
- JSON-structured logging with rotation
- Per-module handler configuration
- Dynamic path management
- 10MB file size limits with 5 backups

#### LLM Integration
- ChatOllama wrapper for local models
- Automatic fallback to fast model
- Connection timeout handling
- Error detection and reporting

#### ReAct Engine (`react_engine.py`)
- General-purpose reasoning + acting pattern
- Tool diversity enforcement (Session 23)
- LLM failure recovery with retry logic (Session 25)
- Reflection every 2 iterations for progress evaluation
- Loop detection and early termination

### Layer 4: Agent Layer

**Six Departmental Agents:**

1. **IT Manager** - Strategic delegation
   - No investigation capability
   - Routes problems to appropriate specialist
   - Authority decisions

2. **Service Desk Manager** - Team coordination
   - Manages IT Support team
   - Escalates to specialists
   - Resource allocation

3. **IT Support** - Front-line support
   - User account issues
   - Password resets
   - Device access
   - Reports to Service Desk Manager

4. **App Support** - Application troubleshooting
   - Application errors
   - Performance issues
   - Database problems
   - Reports to IT Manager

5. **Network Support** - Network infrastructure
   - Connectivity issues
   - Bandwidth problems
   - DNS/firewall
   - Reports to IT Manager

6. **Infrastructure** - Server/system management
   - Server metrics
   - Service status
   - System resources
   - **Orchestrator role**: Coordinates multi-agent investigations

### Layer 5: Knowledge & Memory

#### RAG System (`rag_core.py`)
- Document retrieval for context
- Semantic similarity matching
- Integration with support tools
- Graceful fallback if unavailable

#### Memory System (`agent_memory.py`)
- Cross-session learning
- Pattern recognition
- Statistics tracking
- Server-based for persistence

### Layer 6: Tool Registry

**Categories:**
- Infrastructure Tools (8 tools)
- Network Tools (7 tools)
- Application Tools (7 tools)
- Support Tools (10 tools)
- Manager Tools (7 tools)

**Total: 39 diagnostic and management tools**

---

## Component Details

### ReAct Engine Workflow

```
┌─ Investigation Start
│
├─ Iteration Loop (max 10)
│  │
│  ├─ THOUGHT: LLM reasons about state
│  │  ├─ [Retry Logic: 3 attempts with backoff]
│  │  └─ [Fallback: Smart tool selection on LLM failure]
│  │
│  ├─ ACTION: LLM selects tool
│  │  ├─ [Tool Diversity: Avoid recently used tools]
│  │  └─ [Validation: Ensure tool exists]
│  │
│  ├─ OBSERVATION: Execute tool
│  │  ├─ [Capture: Success/failure/data]
│  │  └─ [Log: Investigation logger]
│  │
│  ├─ REFLECTION: LLM interprets results
│  │  ├─ [Retry Logic: 2 attempts with backoff]
│  │  └─ [Fallback: Simple analysis on failure]
│  │
│  ├─ CHECK: Exit conditions
│  │  ├─ Root cause found? → Return RESOLVED
│  │  ├─ Needs collaboration? → Escalate
│  │  ├─ Tool loop detected? → Return LOOP_DETECTED
│  │  └─ No progress? → Suggest strategy change
│  │
│  └─ PLAN UPDATE: Mark step complete/failed
│
├─ Session Summary
│  ├─ Tool usage statistics
│  ├─ Investigation history
│  ├─ Performance metrics
│  └─ Findings summary
│
└─ Investigation End
```

### Configuration Hierarchy

```
1. ConfigManager (Singleton)
   ├─ Load config.json (if exists)
   ├─ Apply overrides
   ├─ Compute paths
   └─ Provide type-safe access

2. Models
   ├─ Reasoning Model (from config or default)
   ├─ Fast Model (for quick inference)
   ├─ Reasoning Specialist (for complex reasoning)
   └─ Embedding Model (for RAG/Memory)

3. Paths
   ├─ Project Root (auto-detected)
   ├─ Logs Directory (created on startup)
   ├─ Knowledge Base (for RAG documents)
   ├─ Plans Directory (for investigation planning)
   └─ Test Results (for validation runs)
```

### Error Handling Strategy

```
Level 1: System Initialization
├─ LLM Connection Failure
│  └─ STOP: Cannot proceed without LLM
├─ Config Load Failure
│  └─ USE: Defaults and retry
├─ Embeddings Init Failure
│  └─ DEGRADE: Disable RAG/Memory
└─ Agent Init Failure
   └─ RETRY: With exponential backoff

Level 2: Investigation Runtime
├─ Tool Execution Failure
│  └─ LOG: Record failure, try different tool
├─ LLM Response Failure
│  └─ RETRY: 3 attempts, then fallback
├─ Reflection Failure
│  └─ FALLBACK: Simple analysis
└─ Investigation Loop
   └─ TERMINATE: Early with findings

Level 3: Graceful Degradation
├─ No Embeddings
│  └─ Disable: RAG and Memory systems
├─ No RAG
│  └─ Continue: With basic tools only
└─ Memory Failure
   └─ Log-only: Investigation logging continues
```

---

## Data Flow

### Request Processing Flow

```
User Input
    ↓
IT Manager (Delegates)
    ↓
Primary Agent (Investigates with ReAct)
    ├─ LLM Reasoning (with retry/fallback)
    ├─ Tool Selection (diverse, smart)
    ├─ Tool Execution (with logging)
    ├─ Result Reflection (with retry/fallback)
    └─ Progress Evaluation
    │
    └─ Collaboration Needed?
       ├─ YES → Infrastructure (Orchestrator)
       │        └─ Multi-agent coordination
       └─ NO → Return Result

    ↓
Logging & Memory Update
    ├─ Investigation logger
    ├─ Agent memory (if available)
    └─ Test results (if testing)
    
    ↓
Result Display
```

### Context Propagation

```
User Input
    ↓
RAG Retrieval (if available)
    ├─ Semantic similarity search
    └─ Top-3 documents
    ↓
Context Dictionary
    ├─ user_input
    ├─ knowledge_base (retrieved docs)
    ├─ plan_id (if planning)
    └─ [custom context from previous steps]
    ↓
Agent Investigation
    └─ Uses context for informed reasoning
```

---

## Configuration System

### Configuration Manager (`config_manager.py`)

**Features:**
- Singleton pattern (single instance)
- Default values for all settings
- Automatic project root detection
- Path creation on access
- Type-safe properties

**Project Root Detection:**
```
1. Check for marker files: config.json, requirements.txt, .git, app.py
2. Search upward from script location
3. Stop at project root
4. Fallback to script directory
```

**Path Guarantees:**
- All paths are absolute
- Directories created automatically
- Cross-platform compatible
- Works from any working directory

### Configuration File (`config.json`)

```json
{
  "reasoning_model": "deepseek-v3.1:671b-cloud",
  "embedding_model": "embeddinggemma:latest",
  "alternative_models": {
    "fast": "gemma3n:e4b",
    "reasoning": "deepseek-r1:7b",
    "multilingual": "granite4:tiny-h"
  }
}
```

---

## Directory Structure

```
UGENTIC_Dissertation/
├── app.py                          # Entry point
├── config.json                     # Configuration
├── requirements.txt                # Dependencies
│
├── src/ugentic/                   # Main package
│   ├── __init__.py
│   ├── config_manager.py          # [NEW] Configuration system
│   ├── constants.py               # [NEW] Magic string constants
│   ├── config.py                  # Legacy (Brave API key)
│   ├── logging_config.py          # [FIXED] Dynamic paths
│   │
│   ├── core/                      # Core infrastructure
│   │   ├── react_engine.py        # ReAct with Session 25 fixes
│   │   ├── tool_registry.py       # Tool management
│   │   ├── agent_framework.py     # [FIXED] Removed duplicates
│   │   ├── rag_core.py            # RAG system
│   │   ├── agent_memory.py        # Memory system
│   │   ├── reflection_engine.py   # Progress reflection
│   │   └── ... (other core modules)
│   │
│   ├── agents/                    # Agent implementations
│   │   ├── react_agents/
│   │   │   ├── itmanager_agent_react.py
│   │   │   ├── service_desk_manager_react.py
│   │   │   ├── itsupport_agent_react.py
│   │   │   ├── app_support_agent_react.py
│   │   │   ├── network_agent_react.py
│   │   │   └── infrastructure_agent_react.py
│   │   └── __init__.py
│   │
│   ├── tools/                     # Tool implementations
│   │   ├── infrastructure_tools.py
│   │   ├── network_tools.py
│   │   ├── application_tools.py
│   │   ├── support_tools.py
│   │   └── manager_tools.py
│   │
│   └── utils/
│       └── investigation_logger.py
│
├── logs/                          # [DYNAMIC] Created on startup
│   ├── main.jsonl
│   ├── errors.jsonl
│   └── agents/
│       ├── orchestrator.jsonl
│       └── ... (per-agent logs)
│
├── knowledge_base/                # [DYNAMIC] RAG documents
│   └── (place .txt files here)
│
├── plans/                         # [DYNAMIC] Investigation plans
│
├── test_results/                  # [DYNAMIC] Test runs
│
├── docs/                          # Documentation
│   ├── ARCHITECTURE.md            # [NEW] This file
│   └── Project_Tracker/
│       └── SESSION_ENTRY.md
│
└── [other supporting files]
```

---

## Integration Points

### External Systems

1. **Ollama (LLM Service)**
   - Endpoint: `http://localhost:11434`
   - Models: Configurable in config.json
   - Timeout: 30 seconds
   - Fallback: Smart tool selection

2. **File System**
   - Knowledge base documents: `knowledge_base/`
   - Investigation logs: `logs/`
   - Plans: `plans/`

3. **Memory Server** (Optional)
   - Uses in-memory storage
   - Graceful disable if unavailable

### Tool Interface

All tools follow standard interface:
```python
def tool_function(param1, param2) -> Dict[str, Any]:
    return {
        "success": bool,
        "data": object,  # or "result"
        "error": str,    # if success=False
        "message": str   # optional
    }
```

---

## Error Handling Strategy

### Initialization Phase

**Strategy:** Fail fast on critical errors, degrade gracefully on optional components

```python
# Critical - must succeed
config = get_config()          # Exception → Exit
llm = initialize_llm(model)    # Exception → Exit
logger = InvestigationLogger() # Exception → Exit

# Optional - disable on failure
embeddings = initialize_embeddings(model)  # Exception → None → disable RAG/Memory
rag_system = initialize_rag(config)        # Exception → None → disable RAG
memory = initialize_memory()               # Exception → None → disable Memory
```

### Runtime Phase

**Strategy:** Log errors, provide fallbacks, continue operation

```python
# Tool execution failure
try:
    result = tool.execute()
except Exception as e:
    logger.error(f"Tool {tool_name} failed: {e}")
    # Try different tool or escalate

# LLM connection failure
for attempt in range(3):
    try:
        response = llm.invoke(prompt)
        break
    except Exception as e:
        if attempt < 2:
            time.sleep(retry_delay * 2**attempt)  # Exponential backoff
        else:
            # Use fallback tool selection
            return fallback_tool
```

---

## Deployment Guide

### Prerequisites

1. **Python 3.10+**
   ```bash
   python --version  # Must be 3.10 or higher
   ```

2. **Ollama Running**
   ```bash
   ollama serve  # Start in separate terminal
   ```

3. **Models Downloaded**
   ```bash
   ollama pull deepseek-v3.1:671b-cloud
   ollama pull embeddinggemma:latest
   ```

### Installation

1. **Clone/Extract Project**
   ```bash
   cd UGENTIC_Dissertation
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create config.json** (optional)
   ```bash
   cp config.json.example config.json
   # Edit as needed, or use defaults
   ```

### Running

**Standard Mode** (using configured model):
```bash
python app.py
```

**Fast Mode** (using gemma:2b for quick testing):
```bash
python app.py --fast
```

### Troubleshooting

**Issue:** "Connection refused" / "Ollama not running"
```bash
# Solution: Start Ollama in another terminal
ollama serve
```

**Issue:** "Model not found"
```bash
# Solution: Download the model
ollama pull deepseek-v3.1:671b-cloud
```

**Issue:** "No config.json found"
```bash
# Solution: Not critical, system uses defaults
# You can create one to override defaults
```

**Issue:** "Path errors on Windows/Mac"
```bash
# Solution: Already fixed! ConfigManager handles cross-platform paths automatically
```

### Performance Tuning

1. **Use Fast Model for Testing**
   ```bash
   python app.py --fast
   ```

2. **Disable Optional Components**
   - No embeddings model → RAG/Memory disabled automatically
   - System still works with basic tools

3. **Monitor Logs**
   ```bash
   tail -f logs/main.jsonl        # Main activity
   tail -f logs/errors.jsonl      # Errors only
   tail -f logs/agents/*.jsonl    # Per-agent logs
   ```

---

## Performance Characteristics

### Timing (Approximate)

| Operation | Time |
|-----------|------|
| System initialization | 5-10s |
| First investigation | 15-30s |
| Subsequent investigations | 10-20s |
| Tool execution | 0.5-2s each |
| LLM invocation | 2-5s |
| RAG retrieval | 1-3s |

### Resource Usage

| Component | Memory | CPU |
|-----------|--------|-----|
| Python process | 200-500MB | Varies |
| Ollama service | 4-8GB | High during inference |
| Logs (per session) | ~10MB | Minimal |
| Knowledge base | Varies | Minimal |

### Scalability Limits

- **Agents:** 6 agents (hardcoded, can extend)
- **Tools:** 39 tools (easily extensible)
- **Concurrent Requests:** Sequential (by design)
- **Investigation Depth:** Max 10 iterations (configurable)

---

## Maintenance and Monitoring

### Log Files

All logs are JSON-structured for easy parsing:

```bash
# View main log
cat logs/main.jsonl | jq .

# Filter errors
cat logs/errors.jsonl | jq 'select(.level=="ERROR")'

# Check specific agent
cat logs/agents/infrastructure.jsonl | jq .
```

### Memory Statistics

After each session:
```
Total Investigations: N
Ubuntu Collaborations: N
Solo Investigations: N
Ubuntu Success Rate: X%
Solo Success Rate: Y%
Ubuntu Advantage: +Z%
```

### Health Checks

```bash
# Check Ollama connectivity
curl http://localhost:11434/api/tags

# Check project paths
python -c "from src.ugentic.config_manager import get_config; c=get_config(); print(c.get_config_summary())"

# List knowledge base documents
ls -la knowledge_base/
```

---

## Future Enhancements

1. **Dynamic Agent Addition** - Register custom agents at runtime
2. **Tool Marketplace** - Plugin system for new tools
3. **Advanced RAG** - GraphRAG, hierarchical retrieval
4. **Distributed Mode** - Multi-instance orchestration
5. **Web UI** - REST API and web dashboard
6. **Analytics Dashboard** - Real-time metrics
7. **Auto-Recovery** - Automatic retry and resilience patterns

---

## Support and Troubleshooting

For issues:
1. Check logs in `logs/` directory
2. Review error messages (they're descriptive)
3. Verify Ollama is running
4. Check model availability: `ollama list`
5. Review this documentation
6. Check SESSION_ENTRY.md in docs/Project_Tracker/

---

**Document Version:** 1.0  
**Last Updated:** October 16, 2025  
**Maintained By:** Development Team
