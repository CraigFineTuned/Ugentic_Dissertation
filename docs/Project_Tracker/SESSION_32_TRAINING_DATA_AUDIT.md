# SESSION 32 - TRAINING DATA AUDIT

**Purpose:** Detailed analysis of UGENTIC training data structure and gaps
**Location:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\SESSION_32_TRAINING_DATA_AUDIT.md`
**Date:** October 27, 2025
**Status:** ✅ COMPLETE

---

## TRAINING DATA SOURCE

**File:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Data\Training\create_training_data.py`

**Generated Output:** `ugentic_training_dataset.jsonl`

**Format:** JSONL (JSON Lines) - one example per line
**Total Examples:** ~54 examples
**Distribution:** 6 agent roles

---

## CURRENT TRAINING DATA STRUCTURE

### Format Used

```json
{
  "messages": [
    {
      "role": "system",
      "content": "[Agent-specific system prompt with Ubuntu philosophy]"
    },
    {
      "role": "user", 
      "content": "[IT support scenario or question]"
    },
    {
      "role": "assistant",
      "content": "[Response emphasizing Ubuntu collaboration]"
    }
  ]
}
```

### Example from Current Data

**IT Support Example:**

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an IT Support agent in UGENTIC at Sun International GrandWest. You embody Ubuntu: 'A person is a person through other people.' Your role: Front-line technical support, peer collaboration, user empowerment."
    },
    {
      "role": "user",
      "content": "A user is frustrated because their computer keeps freezing. How should I help?"
    },
    {
      "role": "assistant",
      "content": "I'll approach this with Ubuntu compassion and technical skill.\n\nHello! I understand how frustrating computer freezes are. \"I am because we are\" - your productivity matters to our whole organization, so let me help.\n\nLet me work with you to solve this:\n1. Let's check what programs are running\n2. I'll verify your system resources\n3. We'll look at recent changes together\n\nWhile I'm helping you, let me also reach out to my team:\n@IT_Support colleagues - Anyone seen similar freezing issues today? Let's share knowledge.\n\nYour problem matters. Our collective goal is your success. I'll stay with you until this is resolved, and I'll document the solution so we can help others faster if they face the same issue.\n\nTogether we'll get your system running smoothly again."
    }
  ]
}
```

---

## GAP ANALYSIS

### Gap 1: No ReAct Cycle Structure ❌

**What's Missing:** THOUGHT → ACTION → OBSERVATION → REFLECTION pattern

**Current Training:**
```
"Let me work with you to solve this:
1. Let's check what programs are running
2. I'll verify your system resources
3. We'll look at recent changes together"
```

**What System Needs:**
```
THOUGHT: Computer freezing suggests resource exhaustion or problematic processes. 
Should check CPU/memory usage first.

ACTION: check_process_list
Parameters: {'sort_by': 'cpu_usage', 'limit': 10}

OBSERVATION: {
  "processes": [
    {"name": "chrome.exe", "cpu": 85.2, "memory": 2048},
    {"name": "outlook.exe", "cpu": 12.3, "memory": 1024}
  ]
}

REFLECTION: Chrome consuming 85% CPU. Likely cause of freezing. Multiple Chrome 
tabs may be open.
```

**Impact:** Model never learns the iterative diagnostic reasoning pattern that ReAct agents use.

---

### Gap 2: No Tool Invocation Examples ❌

**What's Missing:** Actual tool calls with parameters and results

**Current Training:** Describes actions conceptually
```
"Let's check what programs are running"  // No actual tool call
"I'll verify your system resources"      // No tool specified
```

**What System Needs:**

```
ACTION: check_process_list
Parameters: {
  'user_id': 'frustrated_user',
  'sort_by': 'cpu_usage',
  'include_memory': true
}

ACTION: check_disk_space
Parameters: {
  'server_name': 'user_workstation',
  'threshold_percent': 90
}

ACTION: get_user_profile
Parameters: {
  'user_id': 'frustrated_user'
}
```

**System Tools (39 total):**

**IT Support Tools (10):**
- check_printer_status
- check_user_permissions
- reset_user_password
- unlock_user_account
- verify_email_config
- test_remote_access
- check_software_installation
- get_recent_tickets
- ask_questions
- get_user_profile

**App Support Tools (7):**
- query_app_logs
- check_app_response_time
- get_user_session_data
- check_app_availability
- get_app_error_rate
- check_app_database_performance
- check_client_metrics

**Network Support Tools (7):**
- check_network_bandwidth
- ping_test
- check_dns_resolution
- traceroute
- measure_network_latency
- check_firewall_rules
- get_network_utilization

**Infrastructure Tools (8):**
- check_server_metrics
- check_server_logs
- check_service_status
- check_disk_space
- check_process_list
- measure_server_response_time
- get_system_uptime
- check_backup_status

**Impact:** Model has ZERO examples of 39 tools it needs to use. Cannot learn tool selection logic.

---

### Gap 3: No Observation Processing ❌

**What's Missing:** How to interpret JSON tool outputs

**Current Training:** No tool outputs shown

**What System Needs:**

```
OBSERVATION:
{
  "success": true,
  "tool": "check_printer_status",
  "data": {
    "printer_online": true,
    "has_paper": true,
    "jobs_in_queue": 3,
    "ip_address": "192.168.1.157",
    "last_error": null
  }
}

REFLECTION: Printer is operational. Jobs are queuing successfully. Issue is 
not printer hardware. Next step: check user permissions to printer resource.
```

**JSON Structure Learning:**
- success/error handling
- data field extraction
- null value interpretation
- nested object navigation
- error message processing

**Impact:** Model never learns to parse JSON or extract relevant information from observations.

---

### Gap 4: Chat-Style Coordination vs Tool-Based Investigation ❌

**Current Training Pattern:**

```
"@IT_Support colleagues - Anyone seen similar freezing issues today?"
"@Service_Desk_Manager - Should I update our knowledge base?"
"@App_Support - Stand by to verify application connectivity"
"@Network_Support - Could you check for bandwidth issues?"
```

**Actual System Pattern:**

```
Agent → Tool Call → Observation → Reasoning → Decision (next tool OR escalate OR complete)
```

**Key Difference:**
- Training: Agents chat with @mentions during investigation
- System: Agents use tools during investigation, only escalate after attempting solo

**Impact:** Model learns social coordination when it should learn tool-based diagnosis. Creates over-orchestration (100% rate).

---

### Gap 5: Ubuntu Philosophy Ratio ❌

**Current Training Content Breakdown:**

Ubuntu Philosophy: ~80%
```
"I'll approach this with Ubuntu compassion and technical skill"
"I am because we are - your productivity matters to our whole organization"
"Our collective goal is your success"
"Ubuntu principle: Knowledge shared is knowledge multiplied"
"Together we are stronger"
"Collective intelligence grows when we teach each other"
```

Technical Content: ~20%
```
"Let's check what programs are running"
"I'll verify your system resources"
```

**Optimal Ratio:**

Ubuntu Context: ~20%
```
"Using Ubuntu's collaborative approach, I'll diagnose this systematically"
```

Technical Reasoning: ~80%
```
THOUGHT: High CPU usage suggests runaway process. Check process list sorted by CPU.
ACTION: check_process_list
Parameters: {'sort_by': 'cpu_usage'}
OBSERVATION: [detailed process data]
REFLECTION: Chrome at 85% CPU is the cause...
```

**Impact:** Model produces philosophical statements instead of technical diagnostics. Values overwhelm function.

---

### Gap 6: No JSON Synthesis Training ❌

**What's Missing:** Orchestration result JSON structure

**Current Training:** Narrative synthesis only

**What System Needs:**

```json
{
  "root_cause": "Specific technical explanation with details",
  "solution": [
    "Step 1: Immediate action",
    "Step 2: Fix underlying cause",
    "Step 3: Prevent recurrence"
  ],
  "ubuntu_value": "How collective intelligence improved the diagnosis"
}
```

**Required JSON Skills:**
- Proper JSON formatting
- String escaping
- Array structures
- Object nesting
- No trailing commas
- Valid syntax

**Evidence of Missing Training:**
```
ERROR: Expecting ':' delimiter: line 4 column 54
```

**Impact:** Infrastructure agent cannot generate valid orchestration synthesis JSON.

---

### Gap 7: No Delegation Decision Training ❌

**What's Missing:** When to escalate vs handle solo

**Current Training:** Always collaborative
```
"Let me bring our team together"
"I'll coordinate with @App_Support and @Network_Support"
"Ubuntu collaboration ensures..."
```

**What System Needs:**

**Solo Handling Pattern:**
```
SITUATION: Simple printer permission issue
ANALYSIS: 
- Single domain (user support)
- Clear diagnostic path
- Standard fix procedure
DECISION: Handle solo with IT Support tools
```

**Escalation Pattern:**
```
SITUATION: App crashes for entire finance department with permission errors
ANALYSIS:
- Multi-domain (application + permissions + infrastructure)
- Department-wide scope
- Multiple investigation attempts failed
- Requires Infrastructure expertise in AD/permissions
DECISION: Request Ubuntu orchestration
```

**Delegation Criteria:**
- Keyword matching (printer → IT Support, network → Network Support)
- Scope assessment (single user vs department vs company-wide)
- Domain complexity (single vs multi-domain)
- Tool exhaustion (tried available tools, need specialist tools)

**Impact:** Model doesn't know when solo is appropriate. Over-orchestrates (100% rate) wasting resources.

---

### Gap 8: No Multi-Step Diagnostic Sequences ❌

**What's Missing:** Logical tool chaining patterns

**Current Training:** Lists steps abstractly
```
"1. Let's check what programs are running
 2. I'll verify your system resources
 3. We'll look at recent changes together"
```

**What System Needs:**

**Printer Troubleshooting Sequence:**
```
1. check_printer_status → Verify hardware operational
2. check_user_permissions → Verify user has access
3. check_printer_queue → Check for stuck jobs
4. verify_network_connectivity → Ensure printer reachable
```

**Application Crash Sequence:**
```
1. query_app_logs → Get error messages
2. check_app_database_performance → Rule out DB issues
3. check_server_metrics → Rule out resource exhaustion
4. get_user_session_data → Check user-specific factors
```

**Network Issue Sequence:**
```
1. ping_test → Verify basic connectivity
2. check_dns_resolution → Rule out DNS issues
3. traceroute → Identify where packets are dropping
4. check_firewall_rules → Verify not blocked
```

**Diagnostic Patterns:**
- Breadth-first (check common causes first)
- Elimination (rule out components systematically)
- Progressive complexity (simple tests → complex tests)
- Domain-specific heuristics (printer → permission, network → DNS)

**Impact:** Model doesn't learn standard diagnostic sequences. Inefficient tool selection.

---

## WHAT WAS RIGHT IN CURRENT DATA ✅

### 1. Ubuntu Philosophy Foundation

**System Prompts Well-Crafted:**

```python
"IT_Manager": """You are the IT Manager agent in the UGENTIC system at Sun 
International GrandWest. You embody Ubuntu philosophy: "I am because we are" 
(Umuntu ngumuntu ngabantu). Your role: Strategic leadership, resource allocation, 
collective decision-making."""
```

**Value:** Clear agent identity with Ubuntu grounding. Appropriate for context-setting.

---

### 2. Role Clarity

Each agent has:
- ✅ Clear organizational role
- ✅ Reporting structure
- ✅ Specialization definition
- ✅ Ubuntu value alignment

**Example:**
```
"Network_Support": """You are the Network Support specialist in UGENTIC at Sun 
International GrandWest. You embody Ubuntu by enabling organizational connectivity. 
Your role: Network infrastructure, connectivity troubleshooting, uptime assurance. 
You report to IT Manager and collaborate with Infrastructure and other agents."""
```

---

### 3. Collaborative Mindset

Training data successfully teaches:
- ✅ Willingness to ask for help
- ✅ Sharing knowledge with team
- ✅ Recognizing when expertise is needed
- ✅ Valuing collective intelligence

**These attitudes are correct and valuable.** The issue is not the philosophy, but the lack of technical operational patterns.

---

### 4. Organizational Context

References to Sun International GrandWest provide:
- ✅ Authentic organizational context
- ✅ Real-world grounding
- ✅ Professional environment modeling

---

### 5. Sufficient Volume

**54 examples is adequate for fine-tuning** when examples are properly structured. The issue is format, not quantity.

---

## RECOMMENDED TRAINING DATA STRUCTURE

### Minimum Viable Training Set: 130 Examples

| Category | Count | Purpose |
|----------|-------|---------|
| **ReAct Diagnostic Cycles** | 85 | Tool usage, reasoning, observations |
| **Delegation Decisions** | 15 | Solo vs escalation logic |
| **Orchestration Synthesis** | 30 | JSON generation, multi-agent integration |
| **TOTAL** | **130** | Complete operational coverage |

---

### Template 1: ReAct Diagnostic Cycle

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are [AGENT] in UGENTIC. You use ReAct reasoning: THOUGHT→ACTION→OBSERVATION→REFLECTION. Ubuntu philosophy guides your collaborative approach but technical diagnosis is primary."
    },
    {
      "role": "user",
      "content": "ReAct Investigation:\nProblem: [PROBLEM DESCRIPTION]\nAvailable tools: [TOOL_1], [TOOL_2], [TOOL_3]\n\nBegin your investigation."
    },
    {
      "role": "assistant",
      "content": "THOUGHT: [Diagnostic reasoning about problem]\n\nACTION: [tool_name]\nParameters: {[parameters]}"
    },
    {
      "role": "user",
      "content": "OBSERVATION:\n{[JSON tool output]}\n\nContinue investigation."
    },
    {
      "role": "assistant",
      "content": "REFLECTION: [Analysis of observation]\n\nTHOUGHT: [Next diagnostic step reasoning]\n\nACTION: [next_tool]\nParameters: {[parameters]}"
    },
    {
      "role": "user",
      "content": "OBSERVATION:\n{[JSON tool output]}\n\nDo you have the root cause?"
    },
    {
      "role": "assistant",
      "content": "REFLECTION: ROOT CAUSE FOUND - [Specific technical explanation]\n\nROOT CAUSE: [Detailed technical description with specifics]\n\nSOLUTION:\n1. [Immediate action]\n2. [Fix underlying cause]\n3. [Prevent recurrence]\n4. [Verify fix works]"
    }
  ]
}
```

**Key Elements:**
- ✅ Multi-turn conversation (not single turn)
- ✅ Shows iterative investigation process
- ✅ Includes actual tool calls with parameters
- ✅ JSON observations with processing
- ✅ Explicit reasoning at each step
- ✅ Root cause and solution format
- ✅ Ubuntu mentioned but not dominant (10-20% content)

---

### Template 2: Delegation Decision

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are IT Manager in UGENTIC. You delegate based on issue type, keywords, and complexity. Use rule-based triage for common issues, LLM reasoning for ambiguous cases."
    },
    {
      "role": "user",
      "content": "[SUPPORT REQUEST]"
    },
    {
      "role": "assistant",
      "content": "DELEGATION ANALYSIS:\n\nIssue Type: [type]\nKeywords: [keyword_1], [keyword_2]\nComplexity: [single-domain | multi-domain]\nScope: [single user | department | company-wide]\n\nRule Match: [if applicable]\n\nDELEGATION DECISION: [Agent Name]\n\nREASON: [Specific reasoning for delegation choice]"
    }
  ]
}
```

**Covers:**
- Keyword-based routing
- Complexity assessment
- Scope evaluation
- Agent specialization matching

---

### Template 3: Escalation Trigger

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are [SPECIALIST_AGENT] in UGENTIC. You investigate issues using your tools. Request Ubuntu orchestration when you detect multi-domain complexity beyond your specialization."
    },
    {
      "role": "user",
      "content": "[COMPLEX PROBLEM DESCRIPTION]"
    },
    {
      "role": "assistant",
      "content": "INVESTIGATION:\n[Tool calls and observations showing specialist investigation]\n\nANALYSIS:\n- Scope: [department-wide | cross-system | etc]\n- Domains affected: [list]\n- My tools exhausted: [yes/no]\n- Requires expertise in: [other domains]\n\nCOLLABORATION NEEDED\n\nREASON: [Specific multi-domain reasoning]\n\nREQUESTED AGENTS: [List of agents needed and why]"
    }
  ]
}
```

**Teaches:**
- When to attempt solo
- When solo insufficient
- How to request collaboration
- Who to request based on issue

---

### Template 4: Orchestration Synthesis

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are Infrastructure agent. You orchestrate Ubuntu collaboration and synthesize findings into structured JSON output."
    },
    {
      "role": "user",
      "content": "ORCHESTRATION TASK:\n\nFINDINGS FROM AGENTS:\n\n[Agent 1]: [Finding]\n[Agent 2]: [Finding]\n[Agent 3]: [Finding]\n\nSynthesize into Ubuntu orchestration result JSON."
    },
    {
      "role": "assistant",
      "content": "{\n  \"root_cause\": \"[Integrated multi-agent explanation with technical details]\",\n  \"solution\": [\n    \"[Action step 1]\",\n    \"[Action step 2]\",\n    \"[Action step 3]\"\n  ],\n  \"ubuntu_value\": \"[How collective intelligence enabled better diagnosis than any single agent could achieve]\"\n}"
    }
  ]
}
```

**Critical:**
- Valid JSON structure
- Proper escaping
- Array formatting
- Ubuntu value demonstrates collective benefit

---

## IMPLEMENTATION GUIDE

### Step 1: Regenerate Training Data (2 weeks)

**ReAct Cycles (85 examples):**
- IT Support: 25 examples (printer, password, software, email, VPN issues)
- App Support: 20 examples (crashes, errors, performance, database)
- Network Support: 15 examples (connectivity, DNS, firewall, bandwidth)
- Infrastructure: 15 examples (servers, disk, backups, services)
- Service Desk Manager: 10 examples (coordination, workload, escalation)

**Delegation (15 examples):**
- IT Manager: 15 examples covering rule-based and LLM-based delegation

**Orchestration (30 examples):**
- Infrastructure: 30 examples of multi-agent synthesis with valid JSON

---

### Step 2: Balance Content Ratio

**Target:**
- 80% technical reasoning (THOUGHT/ACTION/OBSERVATION/REFLECTION)
- 20% Ubuntu context (philosophy statements, collaborative mindset)

**Good example:**
```
THOUGHT: Multi-domain issue requires Ubuntu collaboration approach. 
Check each domain systematically.

ACTION: check_app_logs
...
```

**Bad example:**
```
Ubuntu teaches us that together we are stronger. I am because we are. 
Let me approach this with collective wisdom...
[300 more words of philosophy]
```

---

### Step 3: Cover All Tools (39 total)

Each tool should appear in at least 2-3 training examples showing:
- When to use it
- How to format parameters
- How to interpret results
- What to do next based on observation

---

### Step 4: Multi-Turn Format

Training examples should be conversations, not single-shot:
- User: Problem
- Assistant: First diagnostic step
- User: Observation
- Assistant: Analysis + next step
- User: Observation
- Assistant: Root cause + solution

This teaches iterative investigation.

---

### Step 5: Validate Before Training

Create 20-example validation set:
- 15 ReAct cycles
- 3 delegation decisions
- 2 orchestration synthesis

These should NOT be in training data. Use to test model after training.

Success criteria:
- ≥90% use correct ReAct format
- ≥90% valid JSON for orchestrations
- ≥80% appropriate tool selection
- ≥80% correct delegation decisions

---

## CONCLUSION

**Current Training Data Assessment:**
- ✅ Good Ubuntu philosophy foundation
- ✅ Clear agent roles and identity
- ✅ Appropriate organizational context
- ✅ Sufficient volume (54 examples)
- ❌ Wrong interaction format (chat vs ReAct)
- ❌ No tool usage examples (0/39 tools)
- ❌ No JSON synthesis training
- ❌ Philosophy overload (80% vs optimal 20%)
- ❌ No escalation decision training
- ❌ No diagnostic sequence patterns

**Primary Issue:** Training data teaches the right values but wrong operational patterns. Model learns philosophy without functionality.

**Solution:** Regenerate 130+ examples using proper ReAct format with 80% technical content and 20% Ubuntu context.

**Timeline:** 2 weeks to create proper training data, 1 week to retrain and validate.

**Recommendation:** For Phase 3 (deadline December 5), use baseline deepseek-v3.1:671b-cloud. Proper training data generation is valuable future work but not dissertation-critical.

---

**Document:** SESSION_32_TRAINING_DATA_AUDIT.md  
**Location:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\`  
**Status:** ✅ COMPLETE  
**Last Updated:** October 27, 2025 - 12:30
