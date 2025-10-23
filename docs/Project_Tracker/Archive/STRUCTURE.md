# UGENTIC PROJECT STRUCTURE

**Last Updated:** October 15, 2025  
**Purpose:** Complete guide to project organization after Session 19 cleanup  
**Status:** Clean, organized, production-ready structure

---

## 🎯 PROJECT OVERVIEW

**Project:** UGENTIC Practical Bridge  
**Purpose:** Multi-agent AI system for IT departments using Ubuntu philosophy  
**Status:** Operational - Phases 1-2 Complete + Enhanced

---

## 📁 ROOT DIRECTORY

```
Ugentic_Dissertation/
├── app.py ⭐ Main application entry point
├── config.json ⭐ System configuration (LLM models, embeddings, etc.)
├── requirements.txt ⭐ Python dependencies
├── .gitignore ⭐ Git exclusions
├── README.md 📘 Project overview and quick start
├── DEVELOPER_GUIDE.md 📘 Development documentation
├── QUICK_START.md 📘 Quick start guide
├── TESTING_GUIDE.md 📘 Testing instructions
├── STRUCTURE.md 📘 This file - project organization guide
├── PHASE2_PIVOT_SUMMARY.md 📘 Important strategic pivot documentation
├── Honours_Research_Proposal_FINAL_Oct6_2025.pdf 📄 Latest research proposal
├── Honours_Research_Proposal_UPDATED_References_Oct11_2025.md 📄 Proposal with updated references
├── run_comprehensive_tests.py 🔧 Comprehensive test runner
├── run_integration_tests.py 🔧 Integration test runner
├── run_tests.bat 🔧 Test launcher (Windows)
├── run_ugentic.bat 🔧 Application launcher (Windows)
├── setup_env.bat 🔧 Environment setup script
├── cleanup_kb.bat 🔧 Knowledge base cleanup utility
├── CLEANUP_SCRIPT.bat 🔧 Cleanup utility
├── .venv/ 📁 Python virtual environment (excluded from git)
├── data/ 📁 Runtime data (memory, cache, etc.)
├── docs/ 📁 Documentation and project tracking
├── knowledge_base/ 📁 RAG knowledge documents
├── logs/ 📁 System logs and investigation records
├── plans/ 📁 Investigation plan files (JSON)
├── src/ 📁 Source code
├── tests/ 📁 Test suite
├── test_results/ 📁 Test output
├── claud_ugentic/ 📁 Claude simulation environment
├── documents/ 📁 Reference documents
├── DISSERTATION_ACADEMIC/ 📁 Academic dissertation (separate project)
└── __pycache__/ 📁 Python cache (excluded from git)
```

---

## 📂 CORE DIRECTORIES

### **1. src/ - Source Code**

```
src/
└── ugentic/
    ├── __init__.py
    ├── agents/ 📁 Agent implementations
    │   ├── base_agent.py
    │   ├── it_manager.py
    │   ├── service_desk_manager.py
    │   ├── it_support.py
    │   ├── infrastructure.py
    │   ├── network_support.py
    │   ├── app_support.py
    │   └── ubuntu_orchestrator.py
    ├── core/ 📁 Core system components
    │   ├── __init__.py
    │   ├── agent_memory.py ⭐ Persistent memory (Phase 2)
    │   ├── explicit_planner.py ⭐ Planning engine (Phase 1)
    │   ├── investigation_logger.py ⭐ Evidence collection
    │   ├── rag_core.py ⭐ RAG knowledge system
    │   └── react_engine.py ⭐ ReAct reasoning
    └── tools/ 📁 MCP tool implementations
        ├── __init__.py
        ├── filesystem_tool.py
        ├── git_tool.py
        ├── research_tool.py
        └── ...
```

**Purpose:** All Python source code for the UGENTIC system

---

### **2. docs/ - Documentation**

```
docs/
├── Technical/ 📁 Technical analysis documents
│   ├── NETWORK_TOOL_VALIDATION_ANALYSIS.md
│   ├── Global_Biased_Test_Analysis_Compilation.md
│   ├── CLAIMS_VS_REALITY.md
│   └── Research_Synthesis_Value_Declared_Strategic_Testing.md
├── misc/ 📁 Miscellaneous documentation
├── Main_Research_Requirements_Checklist.md
├── Honours_Research_Proposal template.md
├── JEMINI_PRESENTATION_RESEARCH_FOCUSED_Oct8_REVISED.md
└── Project_Tracker/ 📁 Session tracking and planning (see detailed structure below)
```

**Purpose:** All project documentation, organized by type

---

### **3. docs/Project_Tracker/ - Planning & Session Tracking** ⭐

```
Project_Tracker/
├── SESSION_ENTRY.md ⭐⭐⭐ ENTRY POINT - Start here every session
├── CURRENT_SESSION_CHECKPOINT.md ⭐⭐⭐ Current state and progress
├── SESSION_COMPLETION_SUMMARY.md ⭐⭐⭐ Historical session record
├── PROJECT_CONTEXT.md ⭐⭐⭐ Static project context (never-changing)
├── SESSION_17_COMPLETION_SUMMARY.md 📋 Session 17 summary
├── SESSION_18_COMPLETION_SUMMARY.md 📋 Session 18 summary
├── SESSION_19_COMPLETION_SUMMARY.md 📋 Session 19 summary
├── DISSERTATION_COMPLETION_ROADMAP.md 📋 Graduation plan
├── CLEANUP_ANALYSIS_AND_PLAN.md 📋 This cleanup plan
├── Implementation_Tracker/ 📁 Implementation tracking
└── Archive/ 📁 Historical documents (organized)
    ├── Legacy_Sessions/ 📁 Old sessions (5-13)
    ├── Legacy_Sprints/ 📁 Old sprint system (1-4)
    ├── Status_Snapshots/ 📁 Point-in-time status docs
    ├── Cancelled_Work/ 📁 TRM and cancelled features
    ├── Phase_Guides/ 📁 Redundant Phase 2 guides
    ├── Historical_Proposals/ 📁 Superseded proposals
    ├── Legacy_Protocols/ 📁 Old protocol files
    └── Analysis_Documents/ 📁 Historical analysis docs
```

**Purpose:** Project tracking and planning system
**Critical Files:** SESSION_ENTRY.md is the single entry point for every session

---

### **4. knowledge_base/ - RAG Documents**

```
knowledge_base/
├── 00_IT_Policies_and_Procedures.md
├── 01_Ubuntu_Collaboration_Framework.md
├── 02_Application_Support/
│   ├── 02-01_App_Support_Playbook.md
│   ├── 02-02_Application_Architecture_Diagrams.md
│   └── 02-03_Vendor_Escalation_Contacts.md
├── 03_Network_Support/
│   ├── 03-01_Network_Support_Manual.md
│   ├── 03-02_Network_Topology_Diagram.md
│   └── 03-03_Firewall_Rule_Matrix.md
├── 04_Infrastructure_Support/
│   ├── 04-01_Infrastructure_Handbook.md
│   ├── 04-02_Server_Configuration_Database.md
│   └── 04-03_Disaster_Recovery_Plan.md
└── 05_Strategic_and_Tactical/
    └── 05-01_IT_Management_Framework.md
```

**Purpose:** Knowledge documents for RAG system (semantic search)
**Status:** 6 documents loaded, embeddings: embeddinggemma:latest

---

### **5. data/ - Runtime Data**

```
data/
└── memory/ 📁 Persistent memory storage (Phase 2)
    ├── investigations.json ⭐ Investigation records
    ├── metadata.json ⭐ Session metadata
    └── backups/ 📁 Automatic backups
```

**Purpose:** System runtime data (excluded from git)
**Key Feature:** Cross-session learning with semantic similarity

---

### **6. logs/ - System Logs**

```
logs/
├── session_YYYYMMDD_HHMMSS/ 📁 Session-specific logs
│   ├── summary.json
│   ├── summary.md
│   └── investigations/
│       ├── inv_YYYYMMDD_HHMMSS_problem.json
│       └── inv_YYYYMMDD_HHMMSS_problem.md
└── orchestration/ 📁 Ubuntu collaboration logs
    └── ubuntu_collab_YYYYMMDD_HHMMSS.json
```

**Purpose:** Investigation logging and evidence collection
**Status:** Operational, integrated with memory system

---

### **7. plans/ - Investigation Plans**

```
plans/
├── Agent_YYYYMMDD_HHMMSS.json 📁 Individual investigation plans
└── test/ 📁 Test plans
```

**Purpose:** Explicit planning records (Phase 1)
**Status:** Operational, plans created for every investigation

---

### **8. tests/ - Test Suite**

```
tests/
├── integration/ 📁 Integration tests
├── system_integration_test.py
├── test_agent_framework.py
├── test_all_agents.py
├── test_analysis_tool.py
├── test_brave_api.py
├── test_decision_tool.py
├── test_departmental_agents.py
├── test_explicit_planning.py
├── test_fetch_tool.py
├── test_filesystem_tool.py
├── test_git_tool.py
├── test_memory_tool.py
├── test_phase2_memory.py ⭐ Memory system tests
├── test_rag_core.py
├── test_research_tool.py
├── test_sequential_thinking_tool.py
├── test_time_tool.py
├── test_react_agent.py
├── test_refactored_integration.py
├── test_ubuntu_orchestration.py
├── test_orchestrator_prompt.txt
└── __pycache__/
```

**Purpose:** Comprehensive test suite
**Status:** Phase 2 tests: 6/6 passing (100%)

---

### **9. claud_ugentic/ - Claude Simulation Environment**

```
claud_ugentic/
├── SIMULATION_MASTER.md 📘 Simulation entry point
├── config/ 📁 System configuration
├── agents/ 📁 All 6 agent specifications
├── workflows/ 📁 Workflow definitions
└── simulations/ 📁 Test scenarios
```

**Purpose:** Specification-driven simulation system
**Status:** Complete, ready for demonstration

---

### **10. DISSERTATION_ACADEMIC/ - Academic Project** 🚫

```
DISSERTATION_ACADEMIC/
└── [Separate academic dissertation project]
```

**⚠️ IMPORTANT:** This directory is SEPARATE and AVOIDED by system work
**Purpose:** Academic dissertation writing only
**Status:** 87% complete, Chapter 5 pending interviews

---

## 🎯 KEY FILES EXPLAINED

### **Critical System Files**

1. **app.py** - Main application entry point
   - Initializes all system components
   - Loads configuration
   - Starts the UGENTIC system

2. **config.json** - System configuration
   - LLM models (qwen2.5:7b primary, deepseek-r1:8b advanced)
   - Embeddings model (embeddinggemma:latest)
   - Agent definitions
   - Tool configurations

3. **requirements.txt** - Python dependencies
   - LangChain, Ollama, ChromaDB, etc.
   - All required packages with versions

### **Critical Planning Files** ⭐

4. **docs/Project_Tracker/SESSION_ENTRY.md** - **ENTRY POINT**
   - Single file to start every session
   - Loads context automatically
   - Defines session protocol

5. **docs/Project_Tracker/CURRENT_SESSION_CHECKPOINT.md** - Current state
   - What's happening now
   - Progress tracking
   - Next actions

6. **docs/Project_Tracker/PROJECT_CONTEXT.md** - Static context
   - Project vision and goals
   - Ubuntu philosophy
   - Architecture overview

7. **docs/Project_Tracker/SESSION_COMPLETION_SUMMARY.md** - History
   - All completed sessions
   - Cumulative progress
   - Historical record

### **Core System Components** ⭐

8. **src/ugentic/core/agent_memory.py** - Persistent Memory (Phase 2)
   - Cross-session learning
   - Semantic similarity (embeddinggemma:latest)
   - Investigation storage

9. **src/ugentic/core/explicit_planner.py** - Planning Engine (Phase 1)
   - Structured plan creation
   - Progress tracking
   - Evidence collection

10. **src/ugentic/core/investigation_logger.py** - Evidence Collection
    - JSON and Markdown logs
    - Session summaries
    - Investigation records

11. **src/ugentic/core/rag_core.py** - RAG Knowledge System
    - Semantic search
    - Document embedding
    - Knowledge retrieval

12. **src/ugentic/core/react_engine.py** - ReAct Reasoning
    - Thought-action-observation loop
    - Tool usage
    - Reflection

---

## 🔄 WORKFLOW: HOW FILES WORK TOGETHER

### **Session Start Workflow:**

```
1. Read SESSION_ENTRY.md (entry point)
   ↓
2. Load CURRENT_SESSION_CHECKPOINT.md (current state)
   ↓
3. Load PROJECT_CONTEXT.md (static context)
   ↓
4. Load SESSION_COMPLETION_SUMMARY.md (history)
   ↓
5. Execute next action from checkpoint
```

### **Investigation Workflow:**

```
1. User provides IT support request via app.py
   ↓
2. IT Manager analyzes (planning engine creates plan)
   ↓
3. Delegates to appropriate agent(s)
   ↓
4. Agent investigates (ReAct reasoning)
   ↓
5. Ubuntu collaboration if needed (orchestrator)
   ↓
6. Memory recalls similar problems (semantic similarity)
   ↓
7. RAG retrieves relevant knowledge
   ↓
8. Solution implemented
   ↓
9. Investigation logged (JSON + Markdown)
   ↓
10. Memory stores investigation
    ↓
11. Plan updated (progress tracked)
```

---

## 📊 SYSTEM STATUS

### **Phase 1: Explicit Planning** ✅ COMPLETE
- **Files:** `src/ugentic/core/explicit_planner.py`
- **Status:** Operational, all agents integrated
- **Evidence:** Plans in `plans/` directory

### **Phase 2: Persistent Memory** ✅ COMPLETE + ENHANCED
- **Files:** `src/ugentic/core/agent_memory.py`
- **Status:** Operational with semantic similarity
- **Storage:** `data/memory/`
- **Enhancement:** embeddinggemma:latest embeddings (Session 19)
- **Tests:** 6/6 passing (100%)

### **Phase 3: Sequential Thinking** ⏸️ OPTIONAL
- **Status:** Not started
- **Estimate:** ~4 hours
- **Priority:** Optional enhancement

---

## 🎓 DISSERTATION STATUS

**Overall:** 87% complete (6 of 7 chapters)
**Blocked:** Chapter 5 (needs expert interviews)
**Deadline:** December 5, 2025 (51 days remaining)

**Chapter Status:**
- ✅ Chapter 1: Introduction
- ✅ Chapter 2: Literature Review
- ✅ Chapter 3: Methodology
- ✅ Chapter 4: System Design and Implementation
- ⏳ Chapter 5: Design Validation Findings (blocked)
- ✅ Chapter 6: Discussion
- ✅ Chapter 7: Conclusion

---

## 🚀 QUICK START

### **To Run the System:**
```bash
# Windows
run_ugentic.bat

# Or manually
python app.py
```

### **To Run Tests:**
```bash
# Windows
run_tests.bat

# Or manually
python run_comprehensive_tests.py
```

### **To Start a New Session:**
1. Open `docs/Project_Tracker/SESSION_ENTRY.md`
2. Follow instructions to load context
3. Execute next action from checkpoint

---

## 📝 MAINTENANCE

### **Adding New Knowledge:**
1. Add markdown file to `knowledge_base/` in appropriate subfolder
2. System auto-loads on next startup
3. Embeddings generated automatically

### **Viewing Investigation Logs:**
1. Check `logs/session_YYYYMMDD_HHMMSS/`
2. JSON for structured data
3. Markdown for readable reports

### **Accessing Memory Data:**
1. `data/memory/investigations.json` - All investigations
2. `data/memory/metadata.json` - Session metadata
3. Backup files in `data/memory/backups/`

---

## 🔒 WHAT'S EXCLUDED (Git)

**Excluded from version control:**
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `data/` - Runtime data
- `logs/` - System logs
- `test_results/` - Test outputs
- `*.pyc` - Compiled Python files

**See `.gitignore` for complete list**

---

## 📚 DOCUMENTATION HIERARCHY

```
README.md (Overview)
  ↓
STRUCTURE.md (This file - Organization)
  ↓
DEVELOPER_GUIDE.md (Development)
  ↓
QUICK_START.md (Quick start)
  ↓
TESTING_GUIDE.md (Testing)
  ↓
docs/Project_Tracker/SESSION_ENTRY.md (Session start)
```

---

## ✅ POST-CLEANUP STATUS

**Files Archived:** 49 files  
**Files Moved:** 16 files  
**Structure:** Clean and organized  
**Documentation:** Comprehensive  
**Status:** Production-ready  

**Archive Breakdown:**
- Legacy Sessions: 9 files
- Legacy Sprints: 5 files
- Status Snapshots: 12 files
- Cancelled Work: 3 files
- Phase Guides: 7 files
- Historical Proposals: 6 files
- Legacy Protocols: 3 files
- Analysis Documents: 4 files

---

## 🎯 BEST PRACTICES

### **For Development:**
1. Always start with SESSION_ENTRY.md
2. Update checkpoint after significant work
3. Document everything
4. Test before committing
5. Follow Ubuntu principles

### **For Sessions:**
1. Read context files first
2. Execute actions from checkpoint
3. Update planning files
4. Track progress
5. Create completion summary

### **For Maintenance:**
1. Keep knowledge_base updated
2. Review logs regularly
3. Backup memory data
4. Archive old sessions
5. Update documentation

---

**Last Cleanup:** Session 19 (October 15, 2025)  
**Next Review:** As needed  
**Status:** ✅ Clean, organized, production-ready

---

**For questions about project structure, consult this file first.**  
**For session workflow, start with SESSION_ENTRY.md.**
