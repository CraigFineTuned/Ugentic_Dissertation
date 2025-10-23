# SESSION 26 - TESTING & VALIDATION PLAN
**Status:** ⏳ Ready for Implementation  
**Date:** October 16, 2025  
**Objective:** Validate Session 25 fixes and compare against Session 24 findings

---

## SESSION 26 EXECUTIVE SUMMARY

Session 25 fixed the **critical LLM reliability crisis** that caused all 401 errors in Session 24 testing.

**What we're testing:**
1. ✅ Does retry logic prevent 401 errors?
2. ✅ Does fallback tool selection work when LLM unavailable?
3. ✅ Is tool diversity maintained (not just 2 tools)?
4. ✅ Do investigations complete successfully?
5. ✅ Was Session 24's 0% orchestration success partially due to LLM failures?

---

## PRE-TESTING CHECKLIST

### Critical Steps (DO NOT SKIP)
- [ ] Run `CLEAR_PYTHON_CACHE.bat` - **MUST DO THIS FIRST**
- [ ] Run `python diagnose_session25.py` - Verify all fixes in place
- [ ] Verify Ollama running: `curl http://localhost:11434/api/tags`
- [ ] Read SESSION_ENTRY.md for this session's protocol
- [ ] Read SESSION_25_COMPREHENSIVE_FIX_IMPLEMENTATION.md for technical details

### System State Check
```bash
# Verify code changes exist
grep -r "_select_fallback_tool" src/ugentic/core/react_engine.py

# Verify imports work
python -c "from src.ugentic.core.react_engine import ReactEngine; print('OK')"

# Check Ollama
curl http://localhost:11434/api/tags
```

---

## TEST SEQUENCE

### Phase 1: Diagnostic Validation (10 minutes)
**Objective:** Verify Session 25 fixes are installed and working

**Test 1.1: Python Diagnostic**
```bash
python diagnose_session25.py
```
**Expected Output:**
- ✅ React engine code checks: PASS
- ✅ Imports working: PASS  
- ⚠️ or ✅ Ollama status (either is OK)

**Success Criteria:** All checks pass or show "READY FOR TESTING"

---

### Phase 2: Single Investigation Tests (30 minutes)
**Objective:** Verify single-agent investigation works with fixes

**Test 2.1: Simple Problem (5 min)**
```
Problem: "Check current server CPU and memory usage"
Expected: Uses check_server_metrics
Expected Tool Calls: 1-2 tools
Expected Duration: < 30 seconds
Success: Completes without errors
```

**Test 2.2: Moderate Problem with Multiple Tools (10 min)**
```
Problem: "User account locked - what's the status?"
Expected: Uses check_user_permissions and/or check_account_status
Expected Tool Calls: 2-3 tools
Expected Duration: < 2 minutes
Success: Specific root cause (not template text)
```

**Test 2.3: Multi-Layer Problem - CRITICAL (15 min)**
```
Problem: "Network connectivity issue - DNS or firewall?"
Expected: 4+ different tools
Expected Tools: check_network_bandwidth, check_dns_resolution, check_firewall_rules, check_service_status
Expected Duration: < 3 minutes
Success: Tool diversity > 3 unique tools, specific root cause

WATCH FOR:
- NOT just cycling check_server_metrics and check_server_logs
- If LLM fails, fallback tool selection should activate
- Message like "Using fallback tool selection based on problem keywords"
```

---

### Phase 3: Multi-Investigation Session (Optional, 45 minutes)
**Objective:** Full session mimicking real testing conditions

**Setup:** Run 3-5 diverse investigations from SESSION_24 that previously failed

**Test 3.1: Printer Access Problem**
```
Problem: "User John Smith can't access printer in Building A"
Expected: 2-3 tools, specific root cause
Compare: Session 24 success baseline (IT Support agent)
```

**Test 3.2: Finance App Crash Problem**
```
Problem: "Finance application crashing with pattern of errors"
Expected: 2-3 tools, actionable root cause
Compare: Session 24 showed vague diagnosis - should improve now
```

**Test 3.4: VPN Connectivity - THE CRITICAL TEST**
```
Problem: "Remote users intermittent VPN disconnections every 2-3 hours. DNS or firewall suspected."
Expected: 5+ tools from: check_service_status, check_dns_resolution, check_firewall_rules, check_network_bandwidth, check_server_metrics
Expected Root Cause: Multi-domain issue with specific findings
Compare: Session 24 showed 0% success on coordinated investigation

SUCCESS = This investigation now completes with specific findings
```

**Test 3.5: Account Issues**
```
Problem: "Multiple users report intermittent login failures"
Expected: User-level and system-level investigation
Expected Tools: check_user_permissions, check_server_logs, check_service_status
```

---

## METRICS TO COLLECT

### Per Investigation
- Duration (seconds)
- Iterations (number of thought-action-observation cycles)
- Tools used (list all)
- Tool diversity (unique tools / total tools)
- Any LLM errors (401, connection, timeout, etc.)
- Root cause type (specific vs template text)
- Success status (success, needs_collaboration, escalate_to_human)

### Session Summary
- Total investigations: N
- Successful: X
- Avg tool diversity: Y
- Any 401 errors: YES/NO
- Retry logic invoked: YES/NO (check "[Attempt X/3]" messages)
- Fallback tool selection used: YES/NO
- Overall success rate: X%

### Comparison to Session 24
- Session 24: 11 investigations, 2 successful (18.2%)
- Session 26: Y investigations, Z successful (Z%)
- Tool diversity improved: YES/NO
- 401 errors reduced: YES/NO

---

## EXPECTED OUTCOMES

### ✅ SUCCESS SCENARIO
```
Retry logic prevents most 401 errors
Tool diversity increases to 3+ per investigation
VPN problem solved with 5+ tools
Overall success rate improves to 50%+ from 18.2%
Conclusion: Session 25 fixes were effective
Next: Return to Session 24 findings and retest orchestration
```

### ⚠️ PARTIAL SUCCESS SCENARIO
```
Some 401 errors but retries help
Tool diversity improves but still mostly 2 tools
VPN problem partially solved (2-3 tools used)
Success rate improves to 30-40%
Conclusion: Fixes help but other issues remain
Next: Investigate remaining tool selection gaps
```

### ❌ FAILURE SCENARIO
```
Still seeing 401 errors with no fallback
Tool diversity unchanged (still just 2 tools)
Fallback tool selection not triggering
Success rate unchanged at 18.2%
Conclusion: Session 25 fixes didn't fully implement
Next: Debug react_engine.py code path
```

---

## TROUBLESHOOTING

### If Seeing 401 Errors
**This is OK if:**
- All 3 attempts shown: "[Attempt 1/3]", "[Attempt 2/3]", "[Attempt 3/3]"
- Followed by "Using fallback tool selection"
- Investigation completes with fallback tools

**This is BAD if:**
- Only 1 error shown, no retry logic
- No fallback tool selection
- Investigation fails or crashes

**Action:** Check that react_engine.py _generate_thought() has retry loop

### If Only 2 Tools Used
**This could mean:**
1. Tool diversity constraint working but 401 errors causing fallback
2. Tool selection logic not working (cache not cleared)
3. Fallback always choosing first available tool

**Check:** Was "Using fallback tool selection" message shown?
- If YES: Tool diversity is expected to be lower (keyword match)
- If NO: Something wrong with tool selection

**Action:** 
- Run `CLEAR_PYTHON_CACHE.bat` again
- Verify _get_tools_to_avoid() is being called

### If Fallback Never Triggers
**Likely:** Ollama is running fine, LLM working
**Expected:** 0 "Using fallback" messages, 3+ tools per investigation

### If Crashes/Exceptions Occur
**Action:**
1. Save full output
2. Check exact exception message
3. Verify retry logic has proper try/except blocks
4. Review SESSION_25_COMPREHENSIVE_FIX_IMPLEMENTATION.md error handling section

---

## DOCUMENTATION

### Log Everything
- Copy investigation output to file
- Note any error messages
- Record tools used
- Document root cause quality

### Update SESSION_ENTRY.md
After testing completes, add:
```markdown
## SESSION 26 - RESULTS

**Date:** [DATE]
**Tests Run:** [NUMBER] investigations
**Success Rate:** [X]%
**Avg Tool Diversity:** [X] tools
**Retry Logic Invoked:** [YES/NO] times
**Fallback Selection Used:** [YES/NO] times

### Key Findings
- [Finding 1]
- [Finding 2]
- [Finding 3]

### Impact vs Session 24
- Success rate: 18.2% → [X]%
- Tool diversity: 2 tools → [X] tools
- 401 errors: All → [X] remaining

### Next Phase
- [Next session priority]
```

---

## SESSION 26 DECISION TREE

```
START Session 26 Testing
    ↓
Run diagnose_session25.py
    ↓
    All checks pass?
    ├─ NO → Fix issues, rerun diagnose
    └─ YES ↓
      Run Test 2.1 (Simple)
          ↓
          Success?
          ├─ NO → Debug and repeat
          └─ YES ↓
            Run Test 2.3 (Multi-Layer/VPN)
                ↓
                Success?
                ├─ NO → Analyze tool selection
                └─ YES ↓
                  If time available:
                  Run Phase 3 (Multi-Investigation)
                      ↓
                      SUCCESS → Document findings
                      PARTIAL → Note gaps
                      FAILURE → Debug
    ↓
Update SESSION_ENTRY.md with results
    ↓
Determine next session's priorities:
    - If success rate improved: Return to Session 24 orchestration testing
    - If partial success: Investigate remaining tool gaps
    - If failure: Debug retry logic implementation
```

---

## TIMELINE ESTIMATE

| Phase | Task | Duration | Notes |
|---|---|---|---|
| Pre-Testing | Cache clear + diagnostics | 5 min | MUST DO FIRST |
| Phase 1 | Diagnostic validation | 10 min | Quick check |
| Phase 2 | Single investigations (3 tests) | 30 min | Core validation |
| Phase 3 | Multi-investigation session | 45 min | Optional, if time |
| Documentation | Log results, update files | 15 min | Important for dissertation |
| **TOTAL** | **Complete session** | **60-105 min** | Depends on Phase 3 |

---

## CRITICAL REMINDERS

✅ **YOU RUN ALL TESTS MANUALLY** - Never automated
✅ **CLEAR CACHE FIRST** - `CLEAR_PYTHON_CACHE.bat` is essential
✅ **CHECK DIAGNOSE OUTPUT** - `python diagnose_session25.py`
✅ **DOCUMENT EVERYTHING** - Logs are needed for analysis
✅ **UPDATE SESSION_ENTRY.MD** - Master continuity file

---

## SESSION 27 PREVIEW

Based on Session 26 results:

**If success rate improves significantly:**
→ Session 27: Retest orchestration/multi-agent scenarios from Session 24

**If tool diversity improves but success limited:**
→ Session 27: Deep dive into tool selection logic, investigate gaps

**If retry logic works but synthesis still fails:**
→ Session 27: Focus on JSON synthesis layer and root cause generation

**If all fails:**
→ Session 27: Debug retry implementation, verify code was actually deployed

---

This is your complete testing blueprint for Session 26. Follow the sequence, document results, and update SESSION_ENTRY.md.

**You've got this! The system is now robust enough to handle Ollama unavailability - let's see if the fixes solved the 18% success rate problem.**
