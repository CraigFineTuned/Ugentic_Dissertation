# UGENTIC Quick Start Guide

**Version:** 1.0 - With Flexible Model System  
**Date:** October 10, 2025

---

## 🚀 Quick Start

### Running the Main Application

**Fast Mode (Recommended for Development):**
```bash
python app.py --fast
```
- Uses gemma3:4b (fast, efficient)
- Perfect for quick iterations
- ~10 seconds per investigation

**Standard Mode (Recommended for Production):**
```bash
python app.py
```
- Uses qwen2.5:7b (powerful, thorough)
- Better reasoning quality
- ~20 seconds per investigation

---

## 🧪 Running Tests

**Quick Validation (Fast Mode):**
```bash
# Individual tests
python test_react_agent.py --fast      # Sprint 1
python test_all_agents.py --fast       # Sprint 2

# All tests at once
run_sprint_tests.bat --fast
```

**Full Validation (Standard Mode):**
```bash
# Individual tests
python test_react_agent.py             # Sprint 1
python test_all_agents.py              # Sprint 2

# All tests at once
run_sprint_tests.bat
```

---

## 📋 What Each Component Does

### app.py - Main Application
Interactive Ubuntu multi-agent IT support system
- Type IT problems (e.g., "user account locked")
- IT Manager delegates to appropriate agent
- Agent investigates using ReAct pattern
- Tools execute diagnostics
- Ubuntu collaboration when needed

**Example Queries:**
```
"The application server is running slow"
"Users cannot connect to VPN"
"My password needs to be reset"
"Check system performance"
```

### test_react_agent.py - Sprint 1 Test
Tests Infrastructure Agent with 2 scenarios:
1. General system slowness
2. Specific server not responding

**Purpose:** Validates ReAct core with one agent

### test_all_agents.py - Sprint 2 Test
Tests complete system with 3 scenarios:
1. IT Manager delegation to App Support
2. Network Support direct investigation
3. IT Support with context values

**Purpose:** Validates all 6 agents and delegation

---

## 🎯 Common Use Cases

### 1. Development Workflow
```bash
# Morning: Quick iterations
python app.py --fast

# Test changes quickly
python test_all_agents.py --fast

# Final validation
python test_all_agents.py
```

### 2. Demonstration Prep
```bash
# Practice run (fast)
python app.py --fast
# Try: "system performance issues"

# Real demo (powerful)
python app.py
# Show: "investigate slow login times"
```

### 3. Debugging Issues
```bash
# Quick reproduce
python app.py --fast

# Detailed investigation
python app.py
```

---

## ⚙️ System Requirements

**Required:**
- Python 3.12+
- Ollama running
- At least one of: gemma3:4b, qwen2.5:7b

**Check Ollama Models:**
```bash
ollama list
```

**Pull Missing Models:**
```bash
ollama pull gemma3:4b     # Fast model
ollama pull qwen2.5:7b    # Standard model
```

---

## 🛠️ Configuration

### config.json
```json
{
  "reasoning_model": "qwen2.5:7b",
  "embedding_model": "nomic-embed-text:latest",
  ...
}
```

- `reasoning_model`: Default model for standard mode
- Can be changed to any Ollama model
- `--fast` flag always uses gemma3:4b

---

## 📊 System Status

**Current State:**
- ✅ All 6 agents operational
- ✅ 38 diagnostic tools functional
- ✅ 100% test pass rate (5/5 scenarios)
- ✅ Zero critical bugs
- ✅ Production-ready

**Agents Available:**
1. IT Manager (Strategic)
2. Service Desk Manager (Tactical)
3. IT Support (User issues)
4. Infrastructure (Servers)
5. Network Support (Connectivity)
6. App Support (Applications)

---

## 🔍 Troubleshooting

### "No module named 'langchain_ollama'"
```bash
pip install -r requirements.txt
```

### "Connection refused" or "Ollama not found"
```bash
# Start Ollama
ollama serve

# Or check if running
ollama list
```

### "Model not found"
```bash
# Pull the required model
ollama pull gemma3:4b
ollama pull qwen2.5:7b

# Or let app.py show available models
python app.py
```

### Tests fail with errors
```bash
# Check Python environment
python --version  # Should be 3.12+

# Activate virtual environment
.venv\Scripts\activate.bat

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📈 Performance Tips

**For Fast Iterations:**
- Always use `--fast` during development
- gemma3:4b is sufficient for most tasks
- ~50% faster than standard mode

**For Best Quality:**
- Use standard mode (no flag) for demos
- qwen2.5:7b provides better reasoning
- More thorough investigations

**For Testing:**
- Fast mode: Quick validation (~2 min total)
- Standard mode: Thorough testing (~4 min total)

---

## 🎓 For Dissertation

**Quick Demo Setup:**
```bash
# 1. Start with overview
python app.py --fast
# Show: Basic functionality, Ubuntu principles

# 2. Deep dive with powerful model
python app.py
# Show: Complex reasoning, multi-agent coordination

# 3. Run validation tests
run_sprint_tests.bat
# Show: System reliability
```

**Key Points to Highlight:**
- General-purpose LLM-guided investigation
- Flexible tool usage (38 tools across 5 domains)
- Ubuntu collaboration principles
- Production-ready validation
- Flexible deployment options

---

## 📞 Next Steps

After running the system:

1. **Explore Different Scenarios:**
   - User support issues
   - Infrastructure problems
   - Network diagnostics
   - Application performance

2. **Test Ubuntu Collaboration:**
   - Try complex multi-domain issues
   - Observe collaboration detection

3. **Validate System:**
   - Run all tests
   - Verify 100% pass rate

4. **Document Findings:**
   - Capture interesting investigations
   - Note Ubuntu behaviors
   - Record for dissertation

---

## 🚦 Status Indicators

**Console Output:**
- 🚀 = Fast Mode active
- ⚙️ = Standard Mode active
- ✅ = Successful operation
- ⚠️ = Warning (system continues)
- ❌ = Error (requires attention)
- 🤝 = Ubuntu collaboration detected

---

**Quick Start Status:** ✅ READY  
**System Status:** ✅ OPERATIONAL  
**Documentation:** ✅ COMPLETE

**Ready to use! Choose your mode and start investigating.**

---

**For detailed information, see:**
- `docs/FLEXIBLE_MODEL_SYSTEM.md` - Model system details
- `docs/BUG_FIXES_SESSION_9.md` - Recent improvements
- `docs/Project_Tracker/CURRENT_SESSION_CHECKPOINT.md` - Current status
