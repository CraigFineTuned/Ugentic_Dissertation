# UGENTIC Test Prompts - December 3, 2025

**Purpose:** Realistic test scenarios for dynamic system validation after bug fixes
**Status:** Ready to copy-paste into test runner

---

## 🟢 LEVEL 1 RESOLUTION TESTS (Should NOT Escalate)

**Expected:** IT Support resolves directly, <15s, 0 escalations

### Test 1: Password Reset (Simple)
```
Sarah Chen forgot her password and is locked out. She needs access ASAP for the 2pm board meeting.
```
**Expected Behavior:**
- ✅ IT Support uses `reset_user_password(username='Sarah Chen')`
- ✅ Returns temp password + instructions
- ✅ Duration: 5-10s
- ✅ NO escalation

**Success Criteria:**
- Tool returns actual username (not "default_user")
- Status: RESOLVED at Level 1
- No Service Desk involvement

---

### Test 2: Printer Offline (Basic Troubleshooting)
```
I can't print to the 3rd floor printer HP-LaserJet-301. It shows as offline but the power light is on.
```
**Expected Behavior:**
- ✅ IT Support uses `check_printer_status(printer_name='HP-LaserJet-301')`
- ✅ Provides troubleshooting steps
- ✅ Duration: 10-15s
- ✅ NO escalation if basic issue

**Success Criteria:**
- Checks printer status first
- Provides actionable steps
- Only escalates if hardware failure detected

---

### Test 3: Access Request (Permission Check)
```
New employee John Smith needs access to the Finance shared drive to review Q4 reports.
```
**Expected Behavior:**
- ✅ IT Support uses `check_user_permissions(username='John Smith', resource='Finance shared drive')`
- ✅ Grants access OR identifies approval needed
- ✅ Duration: 10-15s
- ✅ May escalate to IT Manager if policy approval needed (strategic path)

**Success Criteria:**
- Checks existing permissions
- If no access: identifies who can approve
- Strategic escalation acceptable (not technical)

---

## 🟡 LEVEL 2 SPECIALIST TESTS (Should Escalate to Specific Specialist)

**Expected:** IT Support → Service Desk Manager → Correct Specialist, <30s

### Test 4: Network Performance (Multiple Users)
```
Our team's VPN connection is extremely slow since yesterday morning. At least 5 people in Marketing are affected.
```
**Expected Behavior:**
- ✅ IT Support detects: network issue + multiple users
- ✅ Escalates to Service Desk Manager
- ✅ Routes to Network Support (not Infrastructure or App Support)
- ✅ Duration: 20-30s

**Success Criteria:**
- Escalation reason: "Requires Network Support specialist tools/expertise"
- Correct routing: Network Support
- Department-wide impact detected

---

### Test 5: Application Timeout (Database Query)
```
The CRM application times out every time we try to export large customer reports. Small exports work fine.
```
**Expected Behavior:**
- ✅ IT Support detects: application-specific issue
- ✅ Escalates to Service Desk Manager
- ✅ Routes to App Support (not Network or Infrastructure)
- ✅ Duration: 20-30s

**Success Criteria:**
- Escalation reason: "Requires App Support specialist tools/expertise"
- Correct routing: App Support
- Recognizes database/query performance issue

---

### Test 6: Server Disk Space Critical
```
Our main file server disk space is at 95% capacity. Backup jobs started failing last night with 'insufficient space' errors.
```
**Expected Behavior:**
- ✅ IT Support detects: infrastructure/storage issue
- ✅ Escalates to Service Desk Manager
- ✅ Routes to Infrastructure (correct)
- ✅ Duration: 20-30s

**Success Criteria:**
- Escalation reason: "Requires Infrastructure specialist tools/expertise"
- Correct routing: Infrastructure
- Recognizes server/storage domain

---

## 🔴 LEVEL 3 ORCHESTRATION TESTS (Multi-Agent Collaboration)

**Expected:** Multiple specialists collaborate, <60s, Ubuntu orchestration

### Test 7: Multi-Domain Issue (Network + Storage + Permissions)
```
Half the Marketing department can't access the shared drive. When they do connect, files take forever to load. This started this morning around 9am.
```
**Expected Behavior:**
- ✅ IT Support detects: multi-domain (network + infrastructure + possibly permissions)
- ✅ Escalates for orchestration
- ✅ Multiple specialists investigate:
  - Network Support: connectivity issues
  - Infrastructure: storage performance
  - Possibly IT Support: permissions
- ✅ Duration: 45-60s
- ✅ Ubuntu orchestration event logged

**Success Criteria:**
- 2-3 agents collaborate
- Root cause identified through collective investigation
- logs/orchestration/ contains event record

---

### Test 8: Large Migration Planning (Strategic + Multi-Specialist)
```
We're planning to migrate 500 users to Microsoft Teams from our current system. Need to ensure our network can handle the traffic, applications are compatible, and we have sufficient storage. Budget is $50k.
```
**Expected Behavior:**
- ✅ IT Support detects: strategic decision + multi-domain
- ✅ Routes to IT Manager (strategic approval)
- ✅ IT Manager orchestrates specialists:
  - Network Support: bandwidth assessment
  - Infrastructure: storage capacity
  - App Support: compatibility testing
- ✅ Duration: 60-90s
- ✅ Strategic + technical orchestration

**Success Criteria:**
- IT Manager involved (strategic decision)
- 3+ specialists provide input
- Budget approval path included
- Comprehensive migration plan

---

## 🟣 STRATEGIC DECISION TESTS (IT Manager Approval Required)

**Expected:** IT Support → IT Manager (strategic path), <25s

### Test 9: Software License Purchase
```
Our department needs Microsoft 365 E5 licenses for 50 users to enable advanced security features. Annual cost is approximately $15,000.
```
**Expected Behavior:**
- ✅ IT Support detects: budget approval needed
- ✅ Strategic escalation to IT Manager
- ✅ IT Manager evaluates: budget, policy, vendor
- ✅ Duration: 15-25s
- ✅ NO technical specialist needed (purely strategic)

**Success Criteria:**
- Direct path: IT Support → IT Manager
- Escalation type: "strategic" (not "technical")
- Budget approval process invoked

---

### Test 10: Policy Change (Compliance)
```
Our current backup retention policy is 30 days but new compliance regulations require 7 years retention for financial records. What are our options and costs?
```
**Expected Behavior:**
- ✅ IT Support detects: policy decision
- ✅ Routes to IT Manager (strategic)
- ✅ IT Manager may consult Infrastructure for technical options
- ✅ Duration: 20-30s

**Success Criteria:**
- Strategic escalation identified
- Policy implications recognized
- Infrastructure consulted for technical feasibility

---

## 🎯 EDGE CASE TESTS (Dynamic Reasoning Required)

**Expected:** Adaptive investigation, system demonstrates reasoning

### Test 11: Everything Slow (Diagnostic Pivot Required)
```
Everything suddenly became slow 10 minutes ago - email, file shares, internal websites, even our applications. Nothing specific, just everything is crawling.
```
**Expected Behavior:**
- ✅ IT Support begins investigation
- ✅ Tests multiple hypotheses:
  - Network connectivity check
  - Server resource check
  - Could be ISP/external issue
- ✅ **Dynamic:** May pivot between hypotheses
- ✅ Duration: 30-60s
- ✅ Escalates to appropriate specialist once hypothesis confirmed

**Success Criteria:**
- Shows investigative reasoning (not jumping to conclusion)
- Tests multiple domains
- Escalates only after narrowing scope
- Demonstrates adaptive thinking

---

### Test 12: Permission Comparison (Analytical Task)
```
Can you compare permissions between users 'jdoe' and 'jsmith'? They're supposed to have the same access since they're both Financial Analysts, but jdoe can't access certain folders that jsmith can.
```
**Expected Behavior:**
- ✅ IT Support performs comparative analysis:
  - `check_user_permissions(username='jdoe', resource='folders')`
  - `check_user_permissions(username='jsmith', resource='folders')`
  - Identifies differences
- ✅ Duration: 15-25s
- ✅ Should resolve at Level 1 (permission check capability exists)

**Success Criteria:**
- Comparative analysis performed
- Differences identified
- Resolution or escalation path clear
- No unnecessary escalation

---

## 📊 EXPECTED METRICS AFTER FIXES

### Before Fixes (Test Results Dec 3 AM):
- Level 1 Resolution Rate: 0% (0/2 tests resolved)
- Service Desk Routing Accuracy: 50% (1/2 correct)
- Tool Data Accuracy: 0% (returned "default_user")
- Average Response Time: 26s (too slow for simple issues)

### After Fixes (Expected):
- Level 1 Resolution Rate: **80%+** (Tests 1-3, 12 should resolve at Level 1)
- Service Desk Routing Accuracy: **90%+** (Tests 4-6 correctly routed)
- Tool Data Accuracy: **100%** (returns actual usernames)
- Average Response Time:
  - Simple (Level 1): **<15s**
  - Specialist: **<30s**
  - Orchestration: **<60s**

---

## 🧪 HOW TO RUN TESTS

### Option 1: Interactive Testing
```bash
python app.py
# Enter each prompt manually, observe behavior
```

### Option 2: Automated Test Suite
```python
# Create test_suite.py
test_prompts = [
    "Sarah Chen forgot her password...",  # Test 1
    "I can't print to the 3rd floor...",  # Test 2
    # ... add all tests
]

for i, prompt in enumerate(test_prompts, 1):
    print(f"\n{'='*60}")
    print(f"TEST {i}")
    print(f"{'='*60}")
    result = process_user_request(prompt)
    # Log results
```

### Option 3: Batch Testing with Metrics
```bash
python scripts/maintenance/health_check.py
# Run comprehensive test suite with automatic metrics collection
```

---

## 📁 WHERE TO FIND RESULTS

### Terminal Output:
- Real-time investigation flow
- Agent reasoning (thoughts)
- Tool calls and observations
- Escalation decisions

### Log Files (Persistent):

1. **Individual Investigations:**
   - `logs/investigations/inv_YYYYMMDD_HHMMSS_query.json`
   - `logs/investigations/inv_YYYYMMDD_HHMMSS_query.md`

2. **Session Summary:**
   - `logs/sessions/session_YYYYMMDD_HHMMSS.json`
   - Contains: Total investigations, success rate, avg response time

3. **Orchestration Events:**
   - `logs/orchestration/collab_YYYYMMDD_HHMMSS.json`
   - `logs/orchestration/collab_YYYYMMDD_HHMMSS.md`

4. **Daily Metrics:**
   - `logs/metrics/daily_summary_YYYYMMDD.json`

### Key Metrics to Check:
```json
{
  "total_investigations": 12,
  "successful_investigations": 10,
  "orchestration_count": 2,
  "avg_response_time": 18.5,
  "agent_usage": {
    "IT Support": 12,
    "Network Support": 2,
    "App Support": 1,
    "Infrastructure": 1
  }
}
```

---

## ✅ SUCCESS INDICATORS

**Test suite successful if:**
- ✅ Tests 1-3: Resolve at Level 1 (no unnecessary escalation)
- ✅ Tests 4-6: Correct specialist routing (Network, App, Infrastructure)
- ✅ Tests 7-8: Multi-agent orchestration with Ubuntu collaboration
- ✅ Tests 9-10: Strategic path to IT Manager (budget/policy)
- ✅ Tests 11-12: Adaptive reasoning demonstrated
- ✅ Level 1 Resolution Rate: 80%+
- ✅ Tool data: No "default_user" (returns actual usernames)
- ✅ Avg response time <20s for simple issues

---

**Last Updated:** December 3, 2025
**Status:** Ready for testing
**Related Docs:** TEST_RESULTS_DEC3.md, REFACTORING_SUMMARY_DEC3.md
