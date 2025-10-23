# SESSION 25 - EMERGENCY DIAGNOSTIC & FIX PROTOCOL
**Date:** October 16, 2025  
**Status:** 🚨 CRITICAL SYSTEM FAILURE IDENTIFIED & READY FOR REPAIR  
**Priority:** IMMEDIATE  

---

## EXECUTIVE SUMMARY

**Problem Found:** Session 25 testing revealed ALL 5 investigations failed at LLM reasoning layer
- **Symptom:** `unauthorized (status code: 401)` errors on every LLM invoke
- **Result:** System falls back to blind tool cycling (2 tools max)
- **Consequence:** 0% actual success despite marking as complete
- **Root Cause:** LLM service (Ollama) cannot be reached or authentication broken

---

## WHAT HAPPENED IN SESSION 25

### Test Scenario
Three identical investigations run on VPN connectivity issues (multi-domain problem)

### Investigation Results
```
Investigation 1: 5 steps completed, 2 tools used (check_server_metrics, check_server_logs)
Investigation 2: 5 steps completed, 2 tools used (same cycle)
Investigation 3: 5 steps completed, 2 tools used (same cycle)

Expected: 4+ tools, 3+ iterations per tool, specific root causes
Actual: 2 tools, repetitive cycling, generic template responses
```

### Error Pattern (CONSISTENT ACROSS ALL ITERATIONS)
```
--- Iteration 1/10 ---
Error generating thought: unauthorized (status code: 401)
ACTION: check_server_metrics
OBSERVATION: [success]
REFLECTION:
Reflection error: unauthorized (status code: 401)
```

**Key Insight:** Tools execute successfully, but LLM reasoning fails

---

## ROOT CAUSE ANALYSIS

### Why Tool Diversity Isn't Working

Session 23 added `_get_tools_to_avoid()` to enforce diversity. But:

```python
# Session 23 fix works IF LLM responds
tools_to_avoid = self._get_tools_to_avoid()  # ✓ Gets list
prompt = f"""... constraint: {constraint_text} ..."""  # ✓ Adds constraint
response = self.llm.invoke(prompt)  # ✗ FAILS WITH 401

# On 401 error, falls back to:
except Exception as e:
    return {
        "next_action": {
            "tool_name": alternative_tools[0]  # ✗ Always first tool
        }
    }
```

**Result:** Falls back to same 2 tools repeatedly

### Why This Causes 0% Success

```
Thought Generation → 401 ERROR
└── Falls back to default action
    └── No reasoning done
        └── No investigation context
            └── Generic template responses
                └── MARKED AS SUCCESS (but wrong)
```

Session marks investigations "complete" but they're actually empty shells.

---

## DIAGNOSTIC STEPS (DO THIS FIRST)

### Step 1: Verify Ollama Status
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Expected: JSON list of models
# If connection refused: Ollama not running
# If 401/403: Authentication issue
```

### Step 2: Check Available Models
```bash
# From PowerShell in project folder
ollama list

# Should see:
# - deepseek-v3.1:671b-cloud
# - gemma3n:e4b
# - granite4:tiny-h
# - embeddinggemma:latest
```

### Step 3: Test LLM Invocation
```bash
# Interactive test
ollama run deepseek-v3.1:671b-cloud
# Type: What is 2+2?
# Should respond with: 4
```

### Step 4: Check Python Dependencies
```bash
.venv\Scripts\activate
pip list | findstr langchain
# Should show: langchain, langchain-ollama
```

---

## FIXING THE SYSTEM

### Fix 1: Update ReactEngine Error Handling
**File:** `src/ugentic/core/react_engine.py`

**Change 1:** Add LLM retry logic in `_generate_thought()`

Replace the entire try-except block in `_generate_thought()` method:

```python
def _generate_thought(self, problem_report: str, context: Dict) -> Dict[str, Any]:
    """Generate thought WITH retry logic"""
    tools_to_avoid = self._get_tools_to_avoid()
    all_tools = [t['name'] for t in self.tools.list()]
    alternative_tools = [t for t in all_tools if t not in tools_to_avoid]
    
    recent_tools_str = " → ".join(self.tool_usage_history[-4:]) if self.tool_usage_history else "None"
    
    constraint_text = ""
    if tools_to_avoid:
        constraint_text = f"""
TOOL CONSTRAINTS (Session 23 - Tool Diversity Fix):
- DO NOT use: {', '.join(tools_to_avoid)}
- MUST use alternatives: {', '.join(alternative_tools[:4])}
"""
    
    prompt = f"""You are {self.agent_name}, investigating this problem:
Problem: {problem_report}

Context: {json.dumps(context, indent=2)}

Investigation History: {self._format_history()}
{constraint_text}

Available Tools: {self._format_tools()}

STRATEGIC INVESTIGATION:
1. What have I discovered so far?
2. What angles remain unexplored?
3. What is my hypothesis?
4. What DIFFERENT tool would help?

MANDATORY JSON Response:
{{
    "reasoning": "Your reasoning",
    "next_action": {{
        "tool_name": "tool_name_here",
        "parameters": {{}},
        "expectation": "What you expect"
    }},
    "status": "INVESTIGATING" or "ROOT_CAUSE_FOUND"
}}"""
    
    # NEW: Retry logic with exponential backoff
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                thought = json.loads(json_str)
                
                # Validate tool selection
                tool_name = thought.get('next_action', {}).get('tool_name', '')
                if tool_name in tools_to_avoid and alternative_tools:
                    thought['next_action']['tool_name'] = alternative_tools[0]
                
                return thought
            else:
                # No JSON in response, return structured response
                return {
                    "reasoning": response_text,
                    "next_action": {
                        "tool_name": alternative_tools[0] if alternative_tools else self._select_default_tool(),
                        "parameters": {},
                        "expectation": "Gather information"
                    },
                    "status": "INVESTIGATING"
                }
        
        except Exception as e:
            error_msg = str(e)
            is_auth_error = "401" in error_msg or "unauthorized" in error_msg.lower()
            is_connection_error = "connection" in error_msg.lower() or "refused" in error_msg.lower()
            
            print(f" [Attempt {attempt + 1}/{max_retries}] LLM Error: {type(e).__name__}")
            
            if is_auth_error:
                print(f" ✗ AUTHENTICATION ERROR (401): Check Ollama service")
            elif is_connection_error:
                print(f" ✗ CONNECTION ERROR: Ollama not responding")
            else:
                print(f" ✗ ERROR: {error_msg[:100]}")
            
            if attempt < max_retries - 1:
                print(f" ⏳ Retrying in {retry_delay}s...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f" ✗ All {max_retries} attempts failed. Using fallback.")
                
                # Fallback: Smart tool selection without LLM
                fallback_tool = self._select_fallback_tool(problem_report)
                
                return {
                    "reasoning": f"Error: {error_msg[:50]}. Using fallback tool.",
                    "next_action": {
                        "tool_name": fallback_tool,
                        "parameters": {},
                        "expectation": "Basic check"
                    },
                    "status": "INVESTIGATING",
                    "fallback_mode": True
                }
    
    # Should not reach here, but just in case
    return {
        "reasoning": "Critical error in thought generation",
        "next_action": {"tool_name": self._select_default_tool(), "parameters": {}},
        "status": "INVESTIGATING"
    }
```

**Change 2:** Add import at top of file

Add to imports:
```python
import time
```

**Change 3:** Add fallback tool selection method

Add this new method to ReactEngine class:

```python
def _select_fallback_tool(self, problem_report: str) -> str:
    """Smart tool selection when LLM fails"""
    problem_lower = problem_report.lower()
    
    # Keyword-based tool selection
    keywords_to_tools = {
        'printer': 'check_printer_status',
        'network': 'check_network_bandwidth',
        'dns': 'check_dns_resolution',
        'firewall': 'check_firewall_rules',
        'vpn': 'check_service_status',
        'permission': 'check_user_permissions',
        'cpu': 'check_server_metrics',
        'memory': 'check_server_metrics',
        'disk': 'check_disk_space',
        'error': 'check_server_logs',
        'crash': 'check_server_logs',
        'service': 'check_service_status',
        'process': 'check_process_list',
        'response': 'measure_server_response_time'
    }
    
    # Find best matching tool
    available_tools = [t['name'] for t in self.tools.list()]
    tools_to_avoid = self._get_tools_to_avoid()
    available_tools = [t for t in available_tools if t not in tools_to_avoid]
    
    for keyword, tool in keywords_to_tools.items():
        if keyword in problem_lower and tool in available_tools:
            return tool
    
    # Fallback: return first available tool not in avoid list
    return available_tools[0] if available_tools else self._select_default_tool()
```

---

### Fix 2: Enhance Reflection Engine
**File:** `src/ugentic/core/react_engine.py`

Update `_generate_reflection()` with same retry logic:

```python
def _generate_reflection(self, thought: Dict, observation: Dict) -> Dict[str, Any]:
    """LLM reflects on observation vs expectation WITH RETRY"""
    
    prompt = f"""Analyze this finding:
Expected: {thought.get('next_action', {}).get('expectation', 'Unknown')}
Observed: {json.dumps(observation, indent=2)}

JSON Response:
{{
    "interpretation": "What this means",
    "hypothesis_confirmed": true/false,
    "hypothesis_refuted": true/false,
    "root_cause_found": true/false,
    "needs_collaboration": true/false
}}"""
    
    max_retries = 2
    for attempt in range(max_retries):
        try:
            response = self.llm.invoke(prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_str = response_text[start:end]
                return json.loads(json_str)
            else:
                return {
                    "interpretation": response_text,
                    "hypothesis_confirmed": False,
                    "hypothesis_refuted": False,
                    "root_cause_found": False,
                    "needs_collaboration": False
                }
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(1)
            else:
                # Fallback reflection
                return {
                    "interpretation": f"Unable to analyze: {str(e)[:50]}",
                    "hypothesis_confirmed": observation.get('success', False),
                    "hypothesis_refuted": False,
                    "root_cause_found": False,
                    "needs_collaboration": False,
                    "fallback_mode": True
                }
```

---

### Fix 3: Clear Python Cache
**Run:** `CLEAR_PYTHON_CACHE.bat`

This resets bytecode and ensures fresh imports.

---

## TESTING SEQUENCE (DO THIS AFTER FIXES)

### Test 1: Quick LLM Test
```bash
# Verify Ollama is working first
curl http://localhost:11434/api/tags

# Then run Python diagnostic
python diagnose_session25.py
```

### Test 2: Single Investigation
```
Problem: "Check current server CPU and memory usage"
Expected: At least 1 LLM invocation succeeds, gets back tool recommendation
Expected Tools: check_server_metrics
Duration: ~10 seconds
```

### Test 3: Multi-Tool Investigation  
```
Problem: "Network connectivity issue - users can't reach DNS"
Expected: 3+ different tools used
Expected Tools: check_server_metrics, check_dns_resolution, check_network_bandwidth
Duration: ~30 seconds
Success Criteria: At least 2 different tools used
```

### Test 4: Full Session (3 Investigations)
```
Problem 1: Server memory high
Problem 2: Service not responding  
Problem 3: Backup failed

Expected: 
- All 3 complete
- Average 3+ tools per investigation
- Specific root causes (not templates)
- No 401 errors in output
```

---

## SUCCESS CRITERIA FOR SESSION 25 FIX

### Must Have ✓
- [ ] No 401 errors in console output
- [ ] At least 2 different tools used per investigation (not cycling same 2)
- [ ] Root causes are specific (not template text)
- [ ] Python cache cleared
- [ ] Session completes without errors

### Nice to Have
- [ ] 3+ tools per investigation
- [ ] Tool reasoning is visible
- [ ] Reflection engine working
- [ ] Success rate > 50%

---

## IF OLLAMA ISN'T RUNNING

### Quick Start Ollama
```bash
# PowerShell as Administrator
ollama serve

# In new terminal
ollama pull deepseek-v3.1:671b-cloud
ollama pull gemma3n:e4b
```

### If Models Missing
```bash
ollama pull deepseek-v3.1:671b-cloud
ollama pull gemma3n:e4b
ollama pull granite4:tiny-h
ollama pull embeddinggemma:latest
```

---

## IF AUTHENTICATION ERROR PERSISTS

### Option 1: Check Ollama Port
Ollama runs on port 11434 by default. If getting 401:
- Check if different port: `netstat -ano | findstr 11434`
- Check Ollama logs for errors

### Option 2: Use Alternative Model
Edit `config.json`:
```json
{
  "reasoning_model": "gemma3n:e4b",
  "alternative_models": {
    "fast": "granite4:tiny-h"
  }
}
```

### Option 3: Restart System
```bash
# Kill Ollama
taskkill /IM ollama.exe

# Clear cache
CLEAR_PYTHON_CACHE.bat

# Restart Ollama
ollama serve
```

---

## FILES MODIFIED IN THIS SESSION

- `src/ugentic/core/react_engine.py` - Added retry logic and fallback tool selection
- `docs/Project_Tracker/SESSION_25_EMERGENCY_FIX.md` - This file

---

## NEXT SESSION (26) PROTOCOL

### If Session 25 Fix Succeeds
1. Document success criteria met
2. Run comprehensive tests (5+ investigations)
3. Analyze tool diversity metrics
4. Update SESSION_ENTRY.md with results

### If Session 25 Fix Partially Works
1. Identify remaining 401 errors
2. Try alternative models
3. Check Ollama service health
4. Implement fallback to gradient model

### If Session 25 Fix Fails
1. Run `python diagnose_session25.py` for detailed diagnostics
2. Check Ollama service status
3. Review Ollama error logs
4. Verify all required models are loaded
5. Consider running from fresh Ollama instance

---

## CRITICAL REMINDERS
- ✅ Always run `CLEAR_PYTHON_CACHE.bat` after code changes
- ✅ User runs tests manually (never automated)
- ✅ Check SESSION_ENTRY.md before each session
- ✅ Update this file with results
- ✅ Log all errors for dissertation analysis
