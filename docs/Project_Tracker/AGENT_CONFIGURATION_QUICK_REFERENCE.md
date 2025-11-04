# UGENTIC Agent Configuration Quick Reference
**Created:** October 24, 2025  
**Purpose:** Fast reference for understanding how agents work and where configs are located

---

## 📍 WHERE ARE THE CONFIGURATIONS?

### Core Configuration Files

| What | Where | Purpose |
|------|-------|---------|
| **Agent Definitions** | `src/ugentic/agents/react_agents/*.py` | Agent classes with specializations |
| **LLM Models** | `config.json` (root) | Model selection |
| **Tools** | `src/ugentic/tools/*.py` | Diagnostic tool implementations |
| **Knowledge Base** | `knowledge_base/` | Domain documentation (RAG) |
| **Entry Point** | `app.py` (root) | Agent initialization & wiring |
| **Full Analysis** | `docs/Project_Tracker/AGENT_CONFIGURATION_ANALYSIS.md` | Comprehensive deep dive |

---

## 🤖 HOW DO THE AGENTS WORK?

### Architecture Overview

```
USER ISSUE
    ↓
IT Manager (Strategic) - Analyzes & delegates
    ↓
[Service Desk Manager] OR [Specialist Agents]
    ↓
Operational Agents:
- IT Support (users/accounts)
- App Support (applications)  
- Network Support (connectivity)
- Infrastructure (servers) ← ALSO ORCHESTRATOR
    ↓
ReAct Pattern: Think → Act → Observe → Repeat
    ↓
SOLUTION (or Ubuntu Collaboration if complex)
```

---

## 👥 THE 6 AGENTS

### 1. IT Manager (Strategic)
- **File:** `itmanager_agent_react.py`
- **Role:** Delegation only (no hands-on work)
- **Tools:** 0 (uses LLM reasoning to route)
- **Real-Life:** CIO/IT Director
- **Pattern:** Delegation via LLM analysis

### 2. Service Desk Manager (Tactical)
- **File:** `service_desk_manager_react.py`
- **Role:** Team coordination, SLA management
- **Tools:** 7 (workload, availability, skill matching)
- **Real-Life:** Service Desk Manager/Team Lead
- **Pattern:** ReAct (8 iterations)

### 3. IT Support (Operational)
- **File:** `itsupport_agent_react.py`
- **Role:** User accounts, passwords, devices
- **Tools:** 10 (user profile, permissions, resets)
- **Real-Life:** Help Desk Technician (Tier 1/2)
- **Pattern:** ReAct (8 iterations)

### 4. App Support (Operational)
- **File:** `app_support_agent_react.py`
- **Role:** Applications, databases, custom software
- **Tools:** 7 (logs, performance, sessions)
- **Real-Life:** Application Support Specialist
- **Pattern:** ReAct (10 iterations)

### 5. Network Support (Operational)
- **File:** `network_agent_react.py`
- **Role:** Connectivity, DNS, firewalls
- **Tools:** 7 (ping, DNS, traceroute, bandwidth)
- **Real-Life:** Network Administrator
- **Pattern:** ReAct (10 iterations)

### 6. Infrastructure (Operational + Orchestrator)
- **File:** `infrastructure_agent_react.py`
- **Role:** Servers, storage, backups + Multi-agent coordinator
- **Tools:** 8 (real server metrics via psutil)
- **Real-Life:** Systems Administrator + Team Lead
- **Pattern:** ReAct (10 iterations) + Ubuntu Orchestration

---

## 🔧 TOOL DISTRIBUTION (39 Total)

### By Domain

| Agent | Tool Count | Example Tools |
|-------|-----------|--------------|
| IT Support | 10 | `get_user_profile`, `reset_password`, `check_printer` |
| Infrastructure | 8 | `check_server_metrics`, `check_service_status`, `check_disk_space` |
| Service Desk | 7 | `get_team_workload`, `check_skill_match`, `get_sla_status` |
| App Support | 7 | `query_app_logs`, `check_app_performance`, `get_user_sessions` |
| Network | 7 | `ping_test`, `check_dns`, `traceroute`, `check_bandwidth` |
| IT Manager | 0 | (Delegation only) |

### Tool Implementation
- **Location:** `src/ugentic/tools/`
- **Types:** `support_tools.py`, `infrastructure_tools.py`, etc.
- **Behavior:** Deterministic (no randomness after Session 22 fix)
- **Real Data:** Infrastructure tools use `psutil` for actual system metrics

---

## 🧠 THE ReAct PATTERN

### How Each Agent Thinks & Acts

```
1. THOUGHT: "I need to check the user's account status"
   ↓
2. ACTION: Call tool `get_user_profile("john.smith")`
   ↓
3. OBSERVATION: "Account locked due to failed login attempts"
   ↓
4. THOUGHT: "I should unlock the account"
   ↓
5. ACTION: Call tool `unlock_user_account("john.smith")`
   ↓
6. OBSERVATION: "Account successfully unlocked"
   ↓
7. ANSWER: "I've unlocked John Smith's account..."
```

**Iterations:** 
- IT Support, Service Desk: 8 max
- Infrastructure, App, Network: 10 max
- Prevents infinite loops

---

## 🤝 UBUNTU ORCHESTRATION

### When & How Multi-Agent Collaboration Happens

**Trigger:** Infrastructure agent detects complexity during solo investigation

**Process:**

1. **Solo Investigation First** (Infrastructure agent)
   ```
   User: "Finance app crashing"
   Infrastructure: [ReAct investigation...]
   Result: "This seems multi-domain..."
   ```

2. **Collaboration Detection** (`CollaborationDetector`)
   - Analyzes investigation history
   - Identifies patterns (app + network + infrastructure keywords)
   - Scores confidence: should we collaborate?

3. **Ubuntu Orchestration** (`UbuntuOrchestrator`)
   ```
   Step 1: Invite relevant agents (App, IT Support, Infrastructure)
   Step 2: Each agent investigates from their perspective
   Step 3: Synthesize findings into unified solution
   Step 4: Generate Ubuntu value statement
   ```

4. **Example from Session 29:**
   - **Infrastructure:** "Domain trust issue"
   - **IT Support:** "User profile corruption"
   - **App Support:** "Permission errors"
   - **Synthesis:** "HR system integration issue causing corrupted profiles"

---

## 📚 KNOWLEDGE BASE (RAG)

### How Agents Access Documentation

**Structure:**
```
knowledge_base/
├── 00_IT_Policies_and_Procedures.md
├── 01_Ubuntu_Collaboration_Framework.md
├── 02_Application_Support/
│   ├── 02-01_App_Support_Playbook.md
│   ├── 02-02_Application_Architecture.md
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

**Access Method:**
- Tool: `ask_questions(question)` (available to IT Support)
- Backend: RAG system with vector embeddings
- Model: `embeddinggemma:latest` (from `config.json`)
- Returns: Relevant documentation sections

**Example:**
```python
# Agent calls
ask_questions("How do I reset a password for a locked account?")

# RAG returns relevant section from:
knowledge_base/00_IT_Policies_and_Procedures.md
```

---

## ⚙️ AGENT INITIALIZATION (How Agents Are Created)

### Startup Flow (`app.py`)

```python
# 1. Load configuration
config = load_config("config.json")

# 2. Initialize LLM
llm = ChatOllama(
    model=config.reasoning_model,  # "deepseek-v3.1:671b-cloud"
    temperature=0.0
)

# 3. Create operational agents
it_support = ITSupportAgentReAct(llm=llm, name="IT Support")
app_support = AppSupportAgentReAct(llm=llm, name="App Support")
network = NetworkAgentReAct(llm=llm, name="Network Support")

# 4. Create Infrastructure with orchestration
infrastructure = InfrastructureAgentReAct(
    llm=llm,
    name="Infrastructure",
    orchestrator=True,  # Enable Ubuntu orchestration
    agents={
        "IT Support": it_support,
        "App Support": app_support,
        "Network Support": network
    }
)

# 5. Create managers
service_desk_manager = ServiceDeskManagerAgentReAct(llm=llm)
it_manager = ITManagerAgentReAct(
    llm=llm,
    agents={
        "Service Desk Manager": service_desk_manager,
        "Infrastructure": infrastructure,
        "App Support": app_support,
        "Network Support": network
    }
)
```

---

## 🎯 AGENT CONFIGURATION PATTERN (Code Example)

### From `infrastructure_agent_react.py`

```python
class InfrastructureAgentReAct:
    def __init__(self, llm, name="Infrastructure", orchestrator=True, 
                 agents=None, logger=None, planner=None):
        # 1. Identity
        self.name = name
        self.agent_type = "Operational"
        self.specialization = "Servers, Storage, Backups, Virtualization"
        self.is_orchestrator = orchestrator
        
        # 2. Tool Registry
        self.tools = ToolRegistry("infrastructure")
        self._register_tools()
        
        # 3. ReAct Engine
        self.react_engine = ReactEngine(
            agent_name=self.name,
            tools=self.tools,
            llm=self.llm,
            max_iterations=10
        )
        
        # 4. Ubuntu Orchestration (if enabled)
        if orchestrator and agents:
            self.ubuntu_orchestrator = UbuntuOrchestrator(
                llm=llm, 
                agents=agents
            )
            self.collaboration_detector = CollaborationDetector(llm=llm)
        
        # 5. Ubuntu Principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
    
    def _register_tools(self):
        """Register infrastructure tools"""
        self.tools.register(
            check_server_metrics,
            "Checks actual server CPU, memory, disk usage"
        )
        # ... 7 more tools
```

---

## 🔑 KEY CONFIGURATION PARAMETERS

### From `config.json`

```json
{
  "reasoning_model": "deepseek-v3.1:671b-cloud",
  "embedding_model": "embeddinggemma:latest",
  "fast_model": "gemma3n:e4b"
}
```

**Verified Working:** Session 29 testing (100% success rate)

### Agent Parameters

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `name` | String | Agent display name |
| `agent_type` | Strategic/Tactical/Operational | Hierarchy level |
| `specialization` | Domain description | What agent focuses on |
| `orchestrator` | Boolean | Can coordinate multi-agent? |
| `max_iterations` | 8-10 | ReAct loop limit |
| `tools` | ToolRegistry | Available diagnostics |
| `ubuntu_principles` | Dict | Cultural values |

---

## 📊 VALIDATION STATUS

### From Session 29 (October 17, 2025)

| Test Case | Agent | Result | Ubuntu? |
|-----------|-------|--------|---------|
| Printer Issue | IT Support | ✅ Success | No (simple) |
| Finance App Crash | Infrastructure (lead) + App + IT Support | ✅ Success | Yes (complex) |

**Performance:** 9.62s average response time  
**Completion:** 100% success rate  
**Status:** ✅ Dissertation-ready

---

## 🎓 FOR DISSERTATION ANALYSIS

### What Makes This Configuration Authentic?

1. **Real IT Roles** → 6 agents match actual job functions
2. **Real Tools** → 39 tools mirror actual diagnostics
3. **Real Hierarchy** → Strategic → Tactical → Operational
4. **Real Documentation** → Knowledge base = SOPs/playbooks
5. **Real Proficiencies** → Tools match what techs actually use

### Ubuntu Integration Points

1. **Embedded Principles** → Every agent has Ubuntu values
2. **Orchestration System** → `UbuntuOrchestrator` class
3. **Collaboration Detection** → `CollaborationDetector` class
4. **Knowledge Framework** → `01_Ubuntu_Collaboration_Framework.md`
5. **Value Statements** → Generated after each collaboration

---

## 🚀 QUICK START FOR ANALYSIS

**Want to understand the agents?**

1. **Read this doc** ✅ You're here!
2. **Check full analysis:** `AGENT_CONFIGURATION_ANALYSIS.md`
3. **View agent code:** `src/ugentic/agents/react_agents/`
4. **Inspect tools:** `src/ugentic/tools/`
5. **See testing:** `SESSION_29_SYSTEM_ANALYSIS.md`

**Want to modify an agent?**

1. Edit agent file in `src/ugentic/agents/react_agents/`
2. Modify tools in `src/ugentic/tools/`
3. Update knowledge base in `knowledge_base/`
4. Test using test cases in `docs/Project_Tracker/`

---

## 📞 COMMON QUESTIONS

**Q: Where do I change which LLM the agents use?**  
A: Edit `config.json` → `reasoning_model`

**Q: How do I add a new tool to an agent?**  
A: 
1. Create function in `src/ugentic/tools/`
2. Register in agent's `_register_tools()` method

**Q: Can I disable Ubuntu orchestration?**  
A: Yes, set `orchestrator=False` in Infrastructure agent init

**Q: Where are the agent prompts?**  
A: In each agent's class (see `self.specialization`, `ubuntu_principles`)

**Q: How does the ReAct pattern work?**  
A: See `src/ugentic/core/react_engine.py`

**Q: Where is the collaboration logic?**  
A: `src/ugentic/core/ubuntu_orchestrator.py` and `collaboration_detector.py`

---

## ✅ VERIFICATION CHECKLIST

For analyzing agent configurations, check:

- [ ] Read `AGENT_CONFIGURATION_ANALYSIS.md` (full deep dive)
- [ ] Reviewed all 6 agent files in `src/ugentic/agents/react_agents/`
- [ ] Examined tool implementations in `src/ugentic/tools/`
- [ ] Understood knowledge base structure in `knowledge_base/`
- [ ] Read Session 29 testing results
- [ ] Traced agent initialization in `app.py`
- [ ] Reviewed Ubuntu orchestration in `core/ubuntu_orchestrator.py`

---

**Document Status:** ✅ COMPLETE  
**For:** Quick reference and onboarding  
**Updated:** October 24, 2025  
**Related Docs:** 
- `AGENT_CONFIGURATION_ANALYSIS.md` (comprehensive)
- `SESSION_29_SYSTEM_ANALYSIS.md` (testing)
- `ARCHITECTURE.md` (system design)
