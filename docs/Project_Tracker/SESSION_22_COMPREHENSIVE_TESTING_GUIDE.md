# SESSION 22 - COMPREHENSIVE VALIDATION & TESTING GUIDE

**Purpose:** Validate that all Session 22 fixes work correctly with realistic, deterministic test scenarios

---

## What Changed

### Code Fixes Applied
1. **Deterministic tool responses** - No randomization, based on hash of user ID
2. **Realistic default data** - John Smith has locked account and no printer access (test scenario)
3. **RAG integration validated** - ask_questions now queries knowledge base with debug output
4. **Logging added** - See [DEBUG] messages when ask_questions uses RAG

### Why Deterministic Data Matters
- Before: Tool returned random results, masked real problems
- After: Same query always returns same answer, allows validation of agent behavior
- Result: Can test if agent actually solves problems or just gets lucky

---

## Test Scenarios (Run These Specific Prompts)

### Test 1: User Permissions Issue (Deterministic - Use ask_questions)
**Prompt:** `User John Smith can't access the printer in Building A`

**What Should Happen:**
- IT Support checks permissions → finds John Smith has NO access
- IT Support should recognize this is the root cause
- Should complete in ~1-2 minutes
- May call ask_questions for additional context about printer access policies
- Look for [DEBUG] messages showing RAG queries

**Expected Outcome:**
- Root cause: User lacks printer access permission
- Solution: Grant permission through IT Manager
- ask_questions used: Yes (validates RAG integration)

---

### Test 2: Account Locked Issue (Forces ask_questions)
**Prompt:** `John Smith's account is locked and he can't log in`

**What Should Happen:**
- IT Support checks profile → finds account_status: locked
- IT Support should ask questions about WHY account is locked
- ask_questions should query RAG for account unlock procedures
- Should complete in ~2-3 minutes
- Multiple [DEBUG] RAG queries expected

**Expected Outcome:**
- Root cause: Account locked (too many failed login attempts)
- Solution: Unlock account
- ask_questions used: Multiple times (validates RAG is providing varied answers)

---

### Test 3: Email Configuration Issue (Validates Fallback)
**Prompt:** `User can't sync email in Outlook`

**What Should Happen:**
- IT Support checks email config → finds issues
- Agent asks questions about sync behavior
- RAG should retrieve email troubleshooting procedures
- Should complete in ~2-3 minutes

**Expected Outcome:**
- Root cause identified from RAG or fallback
- Multiple tools used, diverse responses
- Early termination only on valid solution

---

### Test 4: VPN Connectivity (Simple success case)
**Prompt:** `Remote users are having trouble connecting to the VPN`

**What Should Happen:**
- Infrastructure agent checks VPN/network
- Real diagnostic data returned (not random)
- Completes in ~2-3 minutes
- Clear root cause identified

**Expected Outcome:**
- Deterministic result based on scenario
- No infinite loops
- Good performance

---

## What to Look For in Output

### Good Signs
✅ **[DEBUG] messages** showing RAG queries  
✅ **Consistent tool responses** - same query returns same data  
✅ **Real information gain** - each iteration learns something new  
✅ **Fast completion** - 2-5 minutes for complex scenarios  
✅ **Valid root causes** - Problems actually identified  
✅ **Source attribution** - Responses show "knowledge_base" or "fallback_kb"

### Warning Signs
❌ **No [DEBUG] messages** - ask_questions not being called  
❌ **Random/contradictory data** - Tools returning different answers  
❌ **Immediate termination** - After 3 iterations with no real progress  
❌ **Vague conclusions** - "Findings available for review"  
❌ **Tool loops** - Same tool called 5+ times  
❌ **Long duration** - >10 minutes for simple scenarios

---

## Metrics to Track

For each test, report:

| Metric | Test 1 | Test 2 | Test 3 | Test 4 |
|--------|--------|--------|--------|--------|
| Duration (seconds) | | | | |
| Iterations completed | | | | |
| Tools used | | | | |
| ask_questions calls | | | | |
| Tool diversity score | | | | |
| ask_questions sources | | | | |
| Root cause found | | | | |
| Early termination | | | | |

---

## Expected Performance Benchmarks

### Baseline (Session 21)
- Test 1: 6.0 min
- Average: 8.3 min
- Tool diversity: Low/invalid
- ask_questions: Not used (template loops)

### Session 22 Expected (After Fixes)
- Test 1: 2-3 min (printer access is straightforward)
- Test 2: 2-4 min (account unlock is straightforward)  
- Test 3: 3-5 min (email config requires some investigation)
- Test 4: 2-3 min (VPN is network-focused)
- Average: 2-4 min
- Tool diversity: 0.5-1.0 (valid range)
- ask_questions: Used when needed, shows RAG integration

---

## Critical Success Criteria

**ALL of these must be true:**

1. ✓ No test takes >5 minutes (if so, loop detected)
2. ✓ Tool diversity scores are 0.0-1.0 (not negative, not failing)
3. ✓ Each test identifies a real root cause
4. ✓ ask_questions produces varied answers (not templates)
5. ✓ [DEBUG] messages show RAG being queried
6. ✓ No contradictory data from same tool (deterministic)
7. ✓ Conclusions are actionable (not vague)

---

## How to Run Tests

1. **Start application:**
   ```bash
   cd C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation
   python app.py
   ```

2. **Enter test prompt** exactly as specified above

3. **Record:**
   - Duration (from "Processing:" to final result)
   - Number of iterations
   - Tools used
   - Any [DEBUG] messages
   - Final root cause and solution

4. **Copy output** for analysis

5. **Move to next test** or 'quit' to exit

---

## What Each Test Validates

**Test 1:** Basic permission checking + potential ask_questions usage  
**Test 2:** Forced ask_questions usage for account procedures  
**Test 3:** RAG integration with varied questions  
**Test 4:** Simple network/infrastructure scenario (baseline)

---

## If Issues Occur

**Issue: Duration > 5 minutes**
- Check for [DEBUG] messages
- Look for repeated tool calls
- Verify tool responses are deterministic
- May indicate early termination threshold not working

**Issue: Tool diversity = 0.0**
- Agent using only one tool
- Agent may have solved problem but marked as "low diversity"
- Is valid if only one tool was needed

**Issue: No [DEBUG] messages**
- ask_questions not being called
- Agent finding other tools first
- Not necessarily a problem if agent solves anyway

**Issue: [DEBUG] shows "RAG returned no match"**
- Question too specific or obscure
- Fallback logic providing answer
- This is expected - fallback system working

**Issue: Contradictory responses from same tool**
- Means randomization still active
- Check that support_tools.py was updated
- May need to restart application

---

## Success Scenario

**Expected session output for Test 1:**
```
Processing: User John Smith can't access the printer in Building A

IT Manager analyzing request...
   -> Delegating to: IT Support

📋 Investigation Plan Created: IT_Support_TIMESTAMP
   Objective: User John Smith can't access the printer in Building A
   Total Steps: 5
   Next Step: Gather initial information about the issue

============================================================
 IT Support - ReAct Investigation Starting
============================================================

--- Iteration 1/8 ---

📊 Plan Progress: 0/5 (0%)

 ACTION: check_user_permissions
   Parameters: {'user_id': 'John Smith', 'resource': 'printer in Building A'}

 OBSERVATION:
   {
  "success": true,
  "data": {
    "user_id": "John Smith",
    "has_access": false,  ← CONSISTENT
    "reason": "Not in printer access group"
  }
}

--- Iteration 2/8 ---

 ACTION: ask_questions
   Parameters: {'questions': ['What printer access groups does John Smith belong to?']}

   [DEBUG] ask_questions querying RAG for: 'What printer access groups...'
   [DEBUG] RAG returned match (similarity: 0.72)

 OBSERVATION:
   {
  "success": true,
  "data": {
    "responses": [{
      "answer": "[Real knowledge base content about printer access groups]",
      "source": "knowledge_base",
      "confidence": "high"
    }]
  }
}

✅ ROOT CAUSE FOUND
- John Smith has no printer access permission
- Solution: Grant permission through IT Manager

Duration: ~2 minutes
Tool diversity: 0.67
ask_questions: YES (RAG integrated)
```

---

**Status:** Ready for comprehensive testing  
**Next:** Run all four test scenarios with exact prompts provided above
