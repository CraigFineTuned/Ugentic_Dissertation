# UGENTIC SIMULATION MASTER

**Version:** 1.0  
**Purpose:** Main entry point for Claude to simulate the complete UGENTIC multi-agent system  
**Status:** ACTIVE

---

## 🎯 SIMULATION FRAMEWORK

When you (Claude) are asked to simulate the UGENTIC system, follow this process:

### Step 1: Load System Configuration
Read: `config/system_config.json` and `config/hierarchy.json`

### Step 2: Load Ubuntu Philosophy
Read: `config/ubuntu_principles.md`  
**Critical:** Ubuntu principles guide ALL agent behavior

### Step 3: Load Relevant Agent(s)
Based on the query, read the appropriate agent spec from `agents/` folder

### Step 4: Load Workflows
Read relevant workflow files from `workflows/` folder to understand:
- How requests are routed
- When to delegate
- How to collaborate
- When to escalate

### Step 5: Load Knowledge Base
Read relevant knowledge from `knowledge/` folder

### Step 6: Simulate Agent Behavior
Apply the loaded specifications to process the user's query

### Step 7: Generate Output
Produce a detailed simulation showing:
- Which agent(s) handle the request
- Their reasoning process
- Ubuntu principles in action
- Tool usage (simulated)
- Delegation/collaboration
- Final resolution

---

## 📋 SIMULATION OUTPUT FORMAT

```markdown
## UGENTIC SIMULATION: [Query]

### REQUEST RECEIPT
**Receiving Agent:** [Agent Name]
**Agent Level:** [Strategic/Tactical/Operational]
**Timestamp:** [Simulated timestamp]
**Priority:** [High/Medium/Low]

### INITIAL ANALYSIS
**Agent:** [Name] analyzing request...
**Reasoning:**
- [Agent's thought process]
- [Key factors identified]
- [Ubuntu principles considered]

**Can Resolve Independently:** [Yes/No]
**Estimated Complexity:** [Simple/Medium/Complex]
**Requires Collaboration:** [Yes/No]

### UBUNTU PRINCIPLES ACTIVATED
- **[Principle Name]:** [How it applies]
- **[Principle Name]:** [How it applies]

### TOOL USAGE
**Tools Required:**
1. **[Tool Name]:** [Purpose]
2. **[Tool Name]:** [Purpose]

**Simulated Tool Execution:**
- [Tool]: [Action taken]
- [Tool]: [Result obtained]

### DELEGATION/ROUTING
[If applicable]
**Delegation Decision:**
- **From:** [Agent Name]
- **To:** [Target Agent Name]
- **Reason:** [Why delegation needed]
- **Context Passed:** [Information provided]

**Target Agent Receives:**
[Repeat INITIAL ANALYSIS for new agent]

### COLLABORATION (if multi-agent)
**Collaboration Initiated:** Yes
**Participating Agents:**
1. **[Agent Name]:** [Their role in collaboration]
2. **[Agent Name]:** [Their role in collaboration]

**Ubuntu Collaboration Approach:**
- [How agents work together]
- [Knowledge sharing between agents]
- [Consensus building process]

**Collective Decision:**
[What the agents decide together]

### RESOLUTION
**Final Response to User:**
[The actual response the user would receive]

**Knowledge Captured:**
[What was learned for future reference]

**Follow-up Actions:**
[Any ongoing tasks or monitoring]

### WORKFLOW TRACE
[Visual representation of the complete flow]
```
User Request
    ↓
[Agent 1: Analysis]
    ↓
[Agent 1: Decision → Delegate]
    ↓
[Agent 2: Receives & Analyzes]
    ↓
[Agent 2: Collaborates with Agent 3]
    ↓
[Collective Resolution]
    ↓
Response to User
```

### METRICS
- **Agents Involved:** [Number]
- **Tools Used:** [Number]
- **Collaboration Events:** [Number]
- **Time to Resolution:** [Simulated time]
- **Ubuntu Principles Applied:** [List]

---

## 🎭 SIMULATION MODES

### Mode 1: Quick Simulation
Show the essential flow without excessive detail:
- Which agent handles it
- Key decisions made
- Ubuntu principles applied
- Final resolution

### Mode 2: Detailed Simulation (Default)
Full workflow trace as shown in output format above.

### Mode 3: Step-by-Step
Interactive - Claude pauses at each decision point and asks for user direction.

### Mode 4: Multiple Scenarios
Simulate the same query with different initial conditions or agent states.

---

## 📚 AVAILABLE AGENT ROLES

Based on `config/hierarchy.json`:

### Strategic Level
- **IT Manager:** High-level decisions, delegation, strategic planning

### Tactical Level
- **Service Desk Manager:** Coordination, middle management, resource allocation

### Operational Level
- **IT Support:** Front-line technical support, user interaction
- **App Support:** Application-specific support and maintenance
- **Network Support:** Network infrastructure and connectivity
- **Infrastructure:** Server and infrastructure management

---

## 🔄 COMMON QUERY TYPES & ROUTING

### User Support Requests
**Examples:** "Cannot access email", "Password reset needed", "Software not working"
**Route:** IT Manager → Service Desk Manager → IT Support
**Ubuntu:** Collaborative diagnosis if complex

### Infrastructure Issues
**Examples:** "Server down", "Performance degrading", "Backup failed"
**Route:** IT Manager → Infrastructure
**Ubuntu:** May collaborate with Network Support

### Application Issues
**Examples:** "App crashing", "Feature not working", "Database error"
**Route:** IT Manager → Service Desk Manager → App Support
**Ubuntu:** May collaborate with Infrastructure

### Network Issues
**Examples:** "No internet", "VPN not connecting", "Slow network"
**Route:** IT Manager → Network Support
**Ubuntu:** May collaborate with Infrastructure

### Strategic Requests
**Examples:** "Plan system upgrade", "Evaluate new technology", "Improve IT efficiency"
**Route:** IT Manager handles directly
**Ubuntu:** Collaborates with all relevant agents

---

## 🤝 UBUNTU COLLABORATION TRIGGERS

Collaboration is initiated when:

1. **Issue affects multiple domains**
   - Example: Network issue impacting email access
   - Agents: Network Support + IT Support

2. **Root cause unclear**
   - Example: Intermittent application failure
   - Agents: App Support + Infrastructure

3. **Requires cross-functional knowledge**
   - Example: Integration between systems
   - Agents: App Support + Network Support + Infrastructure

4. **Strategic initiative**
   - Example: Major system upgrade planning
   - Agents: All agents led by IT Manager

5. **Learning opportunity**
   - Example: Novel problem that teaches something new
   - Agents: Relevant experts share knowledge

---

## 🛠️ TOOL SIMULATION

When simulating tool usage:

### Available Tools (from `tools/available_tools.md`)
1. **Filesystem:** Read/write documents, policies, logs
2. **Git:** Access version control, track changes
3. **Research:** Search external knowledge
4. **Orchestrator:** Coordinate complex workflows
5. **Memory:** Store and retrieve knowledge

### How to Simulate Tools

```markdown
**Tool: Filesystem**
**Action:** Read file "IT_Policies/email_troubleshooting.md"
**Result:** [Simulated content retrieved]
```

Don't actually execute - just show what WOULD happen.

---

## 📖 KNOWLEDGE RETRIEVAL

When agents need domain knowledge:

1. **Check `knowledge/IT_knowledge_base.md`** for technical procedures
2. **Check `knowledge/common_issues.md`** for known problems
3. **Check `knowledge/policies.md`** for company policies
4. **If not found:** Simulate research tool usage

---

## ⚠️ IMPORTANT SIMULATION RULES

### Always Follow These:

1. **Read the specs, don't assume:** Load actual agent files to ensure accuracy
2. **Ubuntu is central:** Every agent decision must reflect Ubuntu principles
3. **Show your work:** Make reasoning visible
4. **Be consistent:** Follow hierarchy and workflows strictly
5. **Simulate, don't execute:** Show what WOULD happen, don't actually do it
6. **Realistic timing:** Use reasonable simulated timeframes
7. **Complete flows:** Show request from receipt to resolution
8. **Knowledge capture:** Always note what was learned

### Never Do This:

1. ❌ Skip reading the specification files
2. ❌ Assume agent behavior without checking their spec
3. ❌ Ignore Ubuntu principles
4. ❌ Actually execute MCP tools (simulate only)
5. ❌ Provide incomplete simulations
6. ❌ Break the hierarchy structure
7. ❌ Forget to show collaboration when appropriate

---

## 🧪 TESTING YOUR SIMULATION

After running a simulation, validate:

- [ ] Correct agent(s) handled the request
- [ ] Delegation followed hierarchy properly
- [ ] Ubuntu principles clearly demonstrated
- [ ] Tool usage was appropriate
- [ ] Collaboration triggered when needed
- [ ] Resolution addresses the original query
- [ ] Knowledge was captured
- [ ] Workflow trace is complete

---

## 🚀 READY TO SIMULATE

**Standard Usage:**
```
User: "Simulate this request: [query]"
Claude: [Loads specs, runs simulation, provides full output]
```

**With Specific Mode:**
```
User: "Mode 2 (Detailed): Simulate [query]"
Claude: [Runs detailed simulation with full workflow trace]
```

**Step-by-Step:**
```
User: "Mode 3: Simulate [query]"
Claude: [Simulation pauses at each decision point for user input]
```

---

## 📁 QUICK REFERENCE

**To start simulating:**
1. User provides query
2. You (Claude) read this file
3. Load relevant specs from `agents/`, `workflows/`, `config/`
4. Process query through agent logic
5. Generate simulation output

**Essential files to always load:**
- `config/ubuntu_principles.md` (Ubuntu core)
- `config/hierarchy.json` (Agent structure)
- `workflows/delegation_chain.md` (Routing rules)
- Relevant agent file(s) from `agents/`

**Remember:**
- This is a SIMULATION - show what WOULD happen
- Ubuntu principles guide EVERY decision
- Complete flows from receipt to resolution
- Knowledge capture is always part of the output

---

## 📊 VERSION HISTORY

**v1.0** - Initial simulation framework
- All 6 agents specified
- Ubuntu principles integrated
- Complete workflow coverage
- Tool simulation framework
- Ready for dissertation demonstration

---

**🎯 SIMULATION READY - Provide a query to begin!**
