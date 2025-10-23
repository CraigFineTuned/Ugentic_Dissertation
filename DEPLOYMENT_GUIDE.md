# UGENTIC Deployment & Setup Guide

**Version:** Production-Ready (Session 26)  
**Date:** October 16, 2025

---

## Quick Start (5 minutes)

### 1. Prerequisites

```bash
# Check Python version (3.10+ required)
python --version

# Start Ollama (in separate terminal)
ollama serve

# Download models (one-time)
ollama pull deepseek-v3.1:671b-cloud
ollama pull embeddinggemma:latest
```

### 2. Setup

```bash
# Navigate to project
cd UGENTIC_Dissertation

# Create virtual environment
python -m venv .venv

# Activate it
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run

```bash
# Start system
python app.py

# Or use fast model for testing
python app.py --fast
```

---

## Detailed Installation

### Step 1: System Requirements

**Operating System:**
- Windows 10+ (tested: Windows 11)
- macOS 10.15+ (M1/Intel)
- Linux (Ubuntu 20.04+)

**Python:**
```bash
# Verify Python 3.10 or higher
python --version
# Output should be: Python 3.10.x or higher

# If not installed:
# Windows: https://www.python.org/downloads/
# Mac: brew install python@3.12
# Linux: sudo apt-get install python3.12
```

**Ollama:**
- Download: https://ollama.ai
- Requires 8GB+ RAM (16GB recommended)
- GPU optional (recommended for speed)

### Step 2: Project Setup

```bash
# Clone or extract project
cd path/to/UGENTIC_Dissertation

# Verify structure
ls -la  # or: dir (Windows)
# Should see: app.py, config.json, requirements.txt, src/, etc.
```

### Step 3: Virtual Environment

```bash
# Create
python -m venv .venv

# Activate
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Verify (prompt should show (.venv))
python --version
```

### Step 4: Install Dependencies

```bash
# Install all requirements
pip install -r requirements.txt

# Verify key packages
python -c "import langchain_ollama; import chromadb; print('✓ Dependencies OK')"
```

### Step 5: Configure Models

**Option A: Use Defaults (Recommended)**
```bash
# No action needed - system uses defaults
python app.py
```

**Option B: Custom Configuration**
```bash
# Edit config.json
{
  "reasoning_model": "deepseek-v3.1:671b-cloud",
  "embedding_model": "embeddinggemma:latest",
  "alternative_models": {
    "fast": "gemma3n:e4b",
    "reasoning": "deepseek-r1:7b",
    "multilingual": "granite4:tiny-h"
  }
}
```

### Step 6: Download Models (One Time)

```bash
# Start Ollama service
ollama serve  # Keep this running

# In another terminal, download models:
ollama pull deepseek-v3.1:671b-cloud     # ~40GB
ollama pull embeddinggemma:latest        # ~100MB
ollama pull gemma3n:e4b                  # ~2GB (optional, for --fast mode)

# Verify
ollama list
# Should show models listed
```

### Step 7: Initialize Project Directories

*This happens automatically on first run, but you can pre-create them:*

```bash
mkdir -p logs
mkdir -p logs/agents
mkdir -p knowledge_base
mkdir -p plans
mkdir -p test_results
mkdir -p data
```

---

## Running the System

### Standard Execution

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Activate venv and run
cd UGENTIC_Dissertation
.venv\Scripts\activate  # Windows
python app.py
```

**Startup Output (Expected):**
```
============================================================
UGENTIC System Initialization
============================================================

Configuration Summary:
  project_root: C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation
  reasoning_model: deepseek-v3.1:671b-cloud
  embedding_model: embeddinggemma:latest
  logs_directory: C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\logs
  knowledge_base_directory: ...
  plans_directory: ...

✓ Initializing LLM: deepseek-v3.1:671b-cloud
  Model: deepseek-v3.1:671b-cloud
  Ready for inference

✓ Initializing Embeddings: embeddinggemma:latest
  Embeddings ready

✓ Initializing Investigation Logger
  Path: C:\Users\...\logs

✓ Initializing Explicit Planning System
  Path: C:\Users\...\plans

✓ Initializing React Agents
  Creating specialist agents...
  Creating orchestrator (Infrastructure)...
  Creating IT Manager...
✓ 6 agents initialized
  Ubuntu Orchestration: Enabled

✓ Initializing RAG Knowledge Base
  Loaded 0 documents (will use empty knowledge base)
  Path: C:\Users\...\knowledge_base

✓ RAG connected to IT Support tools

============================================================
✓ SYSTEM READY
============================================================

Your request: 
```

### Fast Mode (For Testing)

```bash
# Uses gemma3n:e4b (fast, smaller model)
python app.py --fast

# Expected: Faster startup and response time
# Good for: Testing, learning, resource-constrained systems
```

### Interactive Usage

```bash
Your request: User can't access network printer

============================================================
Processing: User can't access network printer
============================================================

🎯 IT Manager analyzing request...
   → Delegating to: Network Support

--- Iteration 1/10 ---

 THOUGHT:
 The user has a network printer access issue. I need to diagnose
 the problem systematically...

 ACTION: check_printer_status
   Parameters: {}

 OBSERVATION:
   {"success": true, "status": "online", "available_ports": [...]}

... [continues investigation] ...

============================================================
INVESTIGATION RESULT
============================================================

✓ ISSUE RESOLVED

  Root Cause:
    Network printer driver not installed on user's workstation

  Solution:
    Install network printer driver from \\server\printers\drivers

  Iterations: 3

============================================================

Your request: 
```

### Exit Session

```bash
Your request: quit

💾 Saving session summary...

==================================================
AGENT MEMORY STATISTICS
==================================================
Total Investigations: 5
Ubuntu Collaborations: 1
Solo Investigations: 4
Ubuntu Success Rate: 100.0%
Solo Success Rate: 75.0%
Ubuntu Advantage: +25.0%
==================================================

✓ Thank you for using UGENTIC!
```

---

## Adding Knowledge Base Documents

### Supported Formats
- Text files (`.txt`)
- Markdown (`.md`)
- Any text-based format

### Process

1. **Create text files** with IT procedures, policies, or documentation

2. **Place in `knowledge_base/` directory**
   ```bash
   knowledge_base/
   ├── network_policies.txt
   ├── password_procedures.md
   ├── printer_setup.txt
   └── vlan_configuration.md
   ```

3. **System loads automatically** on next run
   ```
   ✓ Initializing RAG Knowledge Base
     Loaded 4 documents
   ```

### Example Document

**File:** `knowledge_base/password_reset.txt`
```
Password Reset Procedure

When a user reports a forgotten password:

1. Verify user identity (display name, employee ID, department)
2. Check account status in AD (should be Active)
3. Perform password reset in Active Directory
4. Generate temporary password: 8+ chars, alphanumeric + symbols
5. Deliver via secure channel (not email)
6. Require change on next login
7. Document in ticket system
8. Follow up within 24 hours

Common Issues:
- Account locked: Unlock before reset
- Account disabled: Coordinate with HR
- Remote users: Ensure VPN access first
```

---

## Troubleshooting

### Issue: "Connection refused" or "Ollama not responding"

**Cause:** Ollama service not running

**Solution:**
```bash
# Terminal 1
ollama serve

# Then run app in Terminal 2
python app.py
```

**Verify Ollama:**
```bash
curl http://localhost:11434/api/tags
# Should return list of models
```

### Issue: "Model not found"

**Cause:** Model not downloaded

**Solution:**
```bash
# Download the model
ollama pull deepseek-v3.1:671b-cloud

# Verify
ollama list
```

### Issue: "ModuleNotFoundError: No module named 'langchain_ollama'"

**Cause:** Dependencies not installed

**Solution:**
```bash
# Ensure venv is activated
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux

# Reinstall
pip install -r requirements.txt

# Verify
python -c "import langchain_ollama; print('✓')"
```

### Issue: "Permission denied" on logs directory

**Cause:** Directory permissions

**Solution:**
```bash
# Windows
icacls logs /grant "%USERNAME%":F

# Mac/Linux
chmod 755 logs
chmod 755 logs/agents
```

### Issue: "Out of memory" errors

**Cause:** Model too large or insufficient RAM

**Solution:**
```bash
# Option 1: Use fast model
python app.py --fast

# Option 2: Close other applications
# Option 3: Increase virtual memory (not recommended)
```

### Issue: Slow performance

**Cause:** Model inference is computationally intensive

**Solutions:**
```bash
# Option 1: Use GPU (if available)
# Reinstall Ollama with GPU support
# Download from https://ollama.ai

# Option 2: Use faster model
python app.py --fast

# Option 3: Reduce max iterations
# Edit src/ugentic/core/react_engine.py
# Change: max_iterations from 10 to 5
```

### Issue: "Path not found" or file permissions

**Cause:** Path handling on different OS

**Solution:**
```bash
# Verify configuration
python -c "from src.ugentic.config_manager import get_config; c=get_config(); import json; print(json.dumps(c.get_config_summary(), indent=2))"

# Should show all paths as absolute and correct
```

---

## Monitoring and Debugging

### View Logs

```bash
# Main activity log
cat logs/main.jsonl | python -m json.tool

# Errors only
cat logs/errors.jsonl | python -m json.tool

# Agent logs
cat logs/agents/infrastructure.jsonl | python -m json.tool
```

### Check System State

```bash
# Python check
python -c "
from src.ugentic.config_manager import get_config
from pathlib import Path

config = get_config()
print(f'Project Root: {config.project_root}')
print(f'Config File: {Path(config.project_root) / \"config.json\" }')
print(f'Logs Dir: {config.logs_dir}')
print(f'KB Dir: {config.knowledge_base_dir}')
"

# File system check
ls -la logs/
ls -la knowledge_base/
ls -la plans/
```

### Performance Monitoring

```bash
# Watch logs in real-time
tail -f logs/main.jsonl | jq '.message'

# Filter by severity
tail -f logs/main.jsonl | jq 'select(.level=="ERROR")'

# Count investigations
wc -l logs/main.jsonl
```

---

## Maintenance

### Backup

```bash
# Backup investigation logs
cp -r logs logs.backup.$(date +%Y%m%d)

# Backup knowledge base
cp -r knowledge_base knowledge_base.backup.$(date +%Y%m%d)

# Backup plans
cp -r plans plans.backup.$(date +%Y%m%d)
```

### Cleanup

```bash
# Remove old logs (keep recent)
find logs -name "*.jsonl.*" -mtime +7 -delete  # Delete backups >7 days

# Clear memory
rm -rf logs/agents/*.jsonl

# Keep knowledge base (don't delete)
```

### Update

```bash
# Get latest code
git pull origin main

# Reinstall dependencies (if changed)
pip install -r requirements.txt

# Restart
python app.py
```

---

## Performance Tuning

### For Development/Testing

```bash
# Use fast model
python app.py --fast

# Reduced iterations
# Edit src/ugentic/core/react_engine.py
# Change max_iterations = 10 to max_iterations = 5

# Small test knowledge base
# Keep only essential docs in knowledge_base/
```

### For Production

```bash
# Use full reasoning model (already configured)
python app.py

# Full max iterations (10)
# Keep as is

# Comprehensive knowledge base
# Add all relevant docs to knowledge_base/

# Monitor logs regularly
tail -f logs/errors.jsonl
```

### For Resource-Constrained Systems

```bash
# Minimal configuration
python app.py --fast

# Remove embeddings model from config (disables RAG/Memory)
# Edit config.json, remove embedding_model

# Restart
python app.py
```

---

## Environment Variables

*Currently not used, but can be added:*

```bash
# Future enhancements
export OLLAMA_HOST=http://localhost:11434
export LOG_LEVEL=INFO
export MAX_ITERATIONS=10
export REASONING_MODEL=deepseek-v3.1:671b-cloud
```

---

## Accessing Logs from Different Locations

### Ensure You Can Run From Anywhere

```bash
# This works from project root
cd UGENTIC_Dissertation
python app.py

# This should ALSO work (uses dynamic paths)
cd /tmp
python /path/to/UGENTIC_Dissertation/app.py

# This should work too
cd ~
python /path/to/UGENTIC_Dissertation/app.py
```

**Why:** ConfigManager automatically detects project root and creates paths relative to it, regardless of working directory.

---

## Getting Help

1. **Check logs:** `cat logs/errors.jsonl`
2. **Read output:** Error messages are descriptive
3. **Verify setup:** Ollama running? Models downloaded?
4. **Review documentation:** See ARCHITECTURE.md
5. **Check session tracker:** docs/Project_Tracker/SESSION_ENTRY.md

---

## Success Indicators

After running `python app.py`, you should see:

✓ Configuration loaded  
✓ LLM initialized  
✓ Embeddings ready (or skipped)  
✓ Investigation Logger ready  
✓ Explicit Planner ready  
✓ Agents initialized  
✓ RAG system ready (or skipped)  
✓ SYSTEM READY  

Then:
```
Your request: _
```

Ready for input!

---

**Document Version:** 1.0  
**Updated:** October 16, 2025  
**Status:** Production Ready
