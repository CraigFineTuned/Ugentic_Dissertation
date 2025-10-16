# SESSION 20: SYSTEM OPTIMIZATION & MODEL RESEARCH

**Date:** October 15, 2025  
**Status:** 🔄 IN PROGRESS  
**Focus:** Fix system issues + Research optimal models for hardware  
**Timeline:** 2-3 hours estimated

---

## 🎯 SESSION OBJECTIVES

### **Primary Goals:**
1. ✅ Fix all identified system issues from testing
2. 🔍 Research optimal Ollama models for user's hardware
3. 🛠️ Implement fixes and optimizations
4. 📝 Document recommendations and changes

---

## 🖥️ HARDWARE SPECIFICATIONS

**System:** Proline V146R716512K  
**CPU:** AMD Ryzen 7 5700U with Radeon Graphics (16 CPUs, ~1.8GHz)  
**RAM:** 16GB (15756MB available)  
**GPU:** AMD Radeon Graphics (8373 MB display, 495 MB dedicated, 7877 MB shared)  
**OS:** Windows 11 Home 64-bit  

**Performance Considerations:**
- Mid-range mobile processor (Zen 2 architecture)
- 16GB RAM sufficient for 7B-8B models
- Integrated GPU (limited VRAM, but can assist)
- Thermal constraints typical of laptops

---

## 🐛 IDENTIFIED ISSUES (From Testing)

### **Issue #1: Missing 'ask_questions' Tool** 🔴 CRITICAL
**Symptom:**
```
Tool ask_questions not found in user_support registry
```

**Impact:**
- IT Support agent fails to gather user information
- Causes Ubuntu collaborations to produce incorrect "root causes"
- Breaks agent reasoning flow

**Location:** `src/ugentic/agents/react_agents/it_support_agent_react.py`

**Root Cause:**
- IT Support agent tries to call 'ask_questions' tool
- Tool not registered in user_support tool registry
- Available tools: get_user_profile, check_user_permissions, reset_user_password, etc.

**Solution Options:**
1. **Option A (Quick):** Remove 'ask_questions' calls, use available tools
2. **Option B (Complete):** Implement 'ask_questions' tool in user_support registry
3. **Option C (Smart):** Modify agent to use get_recent_tickets + search_knowledge_base

**Chosen Solution:** Option C - Use existing tools intelligently

---

### **Issue #2: Ubuntu Collaboration Success Rate = 0%** 🔴 CRITICAL
**Symptom:**
```
Ubuntu Success Rate: 0.0%
Solo Success Rate: 100.0%
Ubuntu Advantage: -100.0%
```

**Impact:**
- Dissertation narrative damaged (Ubuntu looks worse than solo!)
- Evidence collection contradicts hypothesis
- Cannot demonstrate Ubuntu effectiveness

**Possible Root Causes:**
1. Success marking logic in AgentMemory too strict
2. Tool errors flagging collaborations as failures
3. "Root cause found in reflection" incorrectly marks success
4. Collaboration completion logic flawed

**Investigation Needed:**
- Review `src/ugentic/core/agent_memory.py` success calculation
- Check how investigations are marked as successful
- Verify collaboration completion criteria

**Solution:** TBD after investigation

---

### **Issue #3: Slow Response Times** 🟡 MEDIUM
**Symptom:**
- Average response time: 92.41s per investigation
- Second test interrupted (KeyboardInterrupt)
- User waited too long, manually stopped

**Root Cause:**
- qwen2.5:7b might be slow on this hardware
- Large context windows (RAG + planning + Ubuntu)
- Inefficient model for this use case

**Solution:**
- Research faster models that fit hardware
- Consider smaller, optimized models
- Trade-off: speed vs quality

---

## 🔍 MODEL RESEARCH OBJECTIVES

### **Current Configuration:**
- **LLM:** qwen2.5:7b (STANDARD MODE)
- **Embeddings:** embeddinggemma:latest
- **Performance:** 92.41s average response time

### **Research Questions:**
1. What are the fastest Ollama models for 16GB RAM?
2. How do gemma3n:e2b, gemma3n:e4b perform on this hardware?
3. Are granite4 variants (micro, small, tiny) suitable?
4. What's the best speed/quality trade-off?
5. Which models have good IT domain performance?
6. Can we use quantized models for speed?

### **Candidate Models to Research:**

**Gemma 3 Variants:**
- gemma3n:e2b (2B parameters, edge-optimized)
- gemma3n:e4b (4B parameters, edge-optimized)
- gemma3:4b (current used in fast mode)

**Granite 4 Variants:**
- granite4:micro (smallest)
- granite4:micro-h (micro with higher quality)
- granite4:small-h (small with higher quality)
- granite4:tiny-h (tiny with higher quality)

**Other Possibilities:**
- phi4:latest (Microsoft's efficient model)
- qwen2.5:3b (smaller Qwen)
- llama3.2:3b (Meta's lightweight)
- mistral-small:latest (optimized Mistral)

### **Evaluation Criteria:**
1. **Speed:** Response time < 30s on this hardware
2. **Quality:** Maintains reasoning quality for IT support
3. **Context:** Handles 8K+ context windows
4. **Memory:** Runs smoothly on 16GB RAM
5. **Reliability:** Stable, doesn't crash or hang

---

## 🛠️ IMPLEMENTATION PLAN

### **Phase 1: Research & Analysis** (30 minutes)
**Tasks:**
1. ✅ Create this planning document
2. 🔍 Search web for Ollama model benchmarks
3. 🔍 Research gemma3n performance on AMD Ryzen
4. 🔍 Research granite4 model capabilities
5. 🔍 Find community recommendations for 16GB systems
6. 📊 Compile findings into recommendations table

**Deliverable:** Model recommendations document

---

### **Phase 2: Fix Issue #1 - Missing Tool** (30 minutes)
**Tasks:**
1. 🔍 Read IT Support agent code
2. 🔍 Identify all 'ask_questions' calls
3. 🛠️ Replace with existing tools:
   - Use get_recent_tickets to understand user history
   - Use search_knowledge_base for solutions
   - Use get_user_profile for user context
4. ✅ Test fix with "disk space low" scenario
5. ✅ Verify agent completes without tool errors

**Deliverable:** Fixed IT Support agent

---

### **Phase 3: Fix Issue #2 - Success Rate** (45 minutes)
**Tasks:**
1. 🔍 Read AgentMemory success calculation logic
2. 🔍 Understand how investigations are marked successful
3. 🔍 Review collaboration completion criteria
4. 🛠️ Fix success marking logic
5. ✅ Test with multiple scenarios
6. ✅ Verify Ubuntu success rate > 0%

**Deliverable:** Fixed success rate calculation

---

### **Phase 4: Model Optimization** (30 minutes)
**Tasks:**
1. 📝 Document recommended models
2. 🛠️ Update config.json with optimal model(s)
3. 📝 Create model switching guide
4. 📝 Document speed/quality trade-offs
5. ✅ Prepare for user testing

**Deliverable:** Optimized configuration + documentation

---

### **Phase 5: Testing & Validation** (15 minutes - USER RUNS)
**Tasks:**
1. 📝 Create test scenarios for user
2. 📝 Document expected outcomes
3. 📝 Provide testing instructions
4. ⏳ User runs tests and reports results

**Deliverable:** Test plan for user execution

---

## 📊 SUCCESS CRITERIA

**System Fixes:**
- ✅ IT Support agent completes investigations without tool errors
- ✅ Ubuntu collaboration success rate > 50%
- ✅ Average response time < 45s (50% improvement)

**Model Research:**
- ✅ Comprehensive model comparison table created
- ✅ Top 3 model recommendations documented
- ✅ Clear speed/quality trade-offs explained
- ✅ Hardware compatibility verified

**Documentation:**
- ✅ All changes documented in planning files
- ✅ User testing instructions provided
- ✅ Model switching guide created
- ✅ Session summary completed

---

## 🚨 CONSTRAINTS & REMINDERS

**Hard Rules:**
1. ❌ **AVOID:** All files in `DISSERTATION_ACADEMIC/` (separate academic project)
2. ✅ **USE:** Planning files in `docs/Project_Tracker/` only
3. 🧪 **TESTING:** User runs all tests manually - never assume or suggest automation
4. 🔄 **DYNAMIC:** Update checkpoint files as work progresses

**Planning Hierarchy:**
```
SESSION_ENTRY.md (entry point)
  ↓
CURRENT_SESSION_CHECKPOINT.md (what's happening now)
  ↓
PROJECT_CONTEXT.md (static context)
  ↓
SESSION_COMPLETION_SUMMARY.md (history)
```

---

## 📝 WORK LOG

### **Activity 1: Planning Document Creation** ✅
**Time:** 10 minutes  
**Status:** COMPLETE  
**Output:** This document

### **Activity 2: Model Research** 🔄
**Time:** TBD  
**Status:** NEXT  
**Output:** TBD

---

## 🎯 NEXT STEPS

**Immediate:**
1. Search web for Ollama model benchmarks
2. Research gemma3n and granite4 performance
3. Compile recommendations

**After Research:**
1. Fix IT Support agent (Issue #1)
2. Fix success rate calculation (Issue #2)
3. Update model configuration

**Final:**
1. Update checkpoint files
2. Create user testing guide
3. Session completion summary

---

**Status:** Phase 1 starting - Model research  
**ETA:** 2-3 hours total session time  
**Confidence:** HIGH - Clear plan, actionable steps
