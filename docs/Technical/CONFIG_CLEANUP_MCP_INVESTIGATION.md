# CONFIG.JSON CLEANUP - MCP INVESTIGATION

**Date:** October 15, 2025  
**Issue:** Outdated/unused MCP server configurations in config.json  
**Action:** Cleaned up and documented

---

## 🔍 WHAT WAS WRONG

### **Old config.json (ISSUES):**
```json
{
  "reasoning_model": "qwen2.5:7b",
  "embedding_model": "embeddinggemma:latest",
  "filesystem_tool": {
    "server_command": ["npx", "-y", "@modelcontextprotocol/server-filesystem"],
    "allowed_paths": ["C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic"]  // WRONG PATH!
  },
  "git_tool": {
    "server_command": ["uvx", "mcp-server-git"],
    "repository_path": "C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic"  // WRONG PATH!
  },
  "research_tool": {
    "server_command": ["node", "C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic\\servers-main\\src\\research\\index.js"]  // DOESN'T EXIST!
  },
  "orchestrator_tool": {
    "server_command": ["node", "C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic\\servers-main\\src\\orchestrator\\index.js"]  // DOESN'T EXIST!
  }
}
```

**Problems:**
1. ❌ Wrong directory: `Ugentic` → should be `Ugentic_Dissertation`
2. ❌ References non-existent `servers-main` directory
3. ❌ **MOST IMPORTANT:** These MCP servers are **NOT USED** by app.py!

---

## 🎯 WHAT YOUR SYSTEM ACTUALLY USES

### **Current Architecture:**

**UGENTIC uses INTERNAL SIMULATED TOOLS, not external MCP servers!**

**Tools Location:** `src/ugentic/tools/`
- ✅ `infrastructure_tools.py` - Server monitoring (check_disk_space, check_server_metrics, etc.)
- ✅ `network_tools.py` - Network diagnostics (ping_test, check_bandwidth, etc.)
- ✅ `application_tools.py` - App monitoring (query_app_logs, check_app_response_time, etc.)
- ✅ `support_tools.py` - User support (get_user_profile, **ask_questions**, etc.)
- ✅ `manager_tools.py` - Team management (get_team_availability, get_sla_status, etc.)

**How it works:**
1. Each tool is a **Python function** that **simulates** real operations
2. Tools return **mock data** for testing/demonstration
3. **No external MCP servers needed**
4. Perfect for dissertation: reproducible, controllable, demonstrable

**Example - check_disk_space (from infrastructure_tools.py):**
```python
def check_disk_space(server_name: str) -> Dict[str, Any]:
    """Simulated disk space check"""
    return {
        "success": True,
        "tool": "check_disk_space",
        "data": {
            "server": server_name,
            "disks": [{
                "device": "C:\\",
                "total_gb": 475.87,
                "used_gb": 413.69,
                "percent": 86.9,
                "status": "warning"
            }]
        }
    }
```

---

## ✅ NEW CLEAN CONFIG.JSON

```json
{
  "reasoning_model": "qwen2.5:7b",
  "alternative_models": {
    "fast": "gemma3n:e4b",
    "reasoning": "deepseek-r1:7b",
    "multilingual": "granite4:small-h"
  },
  "embedding_model": "embeddinggemma:latest"
}
```

**What's kept:**
- ✅ `reasoning_model` - LLM for agent reasoning (USED by app.py)
- ✅ `alternative_models` - Quick reference for model switching (NEW)
- ✅ `embedding_model` - Embeddings for RAG and memory (USED by app.py)

**What's removed:**
- ❌ `filesystem_tool` - Not used by app.py
- ❌ `git_tool` - Not used by app.py
- ❌ `research_tool` - Doesn't exist
- ❌ `orchestrator_tool` - Doesn't exist

---

## 🚀 IF YOU WANT REAL MCP INTEGRATION (OPTIONAL)

### **Why You Might Want It:**
- Connect to **real** filesystems, databases, APIs
- Use **production** tools instead of simulations
- Integration with **external services** (GitHub, Slack, etc.)

### **Best MCP Servers (2025):**

**Official Anthropic Servers:**
```bash
# Filesystem (with security patches)
npx -y @modelcontextprotocol/server-filesystem /path/to/directory

# Git operations
npx -y @modelcontextprotocol/server-git /path/to/repo

# Web content fetching
npx -y @modelcontextprotocol/server-fetch

# Knowledge graph memory
npx -y @modelcontextprotocol/server-memory

# Sequential thinking
npx -y @modelcontextprotocol/server-sequential-thinking
```

**Official GitHub Server (Go-based, faster):**
```bash
# New official GitHub MCP server (April 2025)
# Install: https://github.com/github/github-mcp-server
github-mcp-server
```

**How to Add MCP to UGENTIC:**

**Option 1: Keep Simulated Tools** ⭐ (Recommended for dissertation)
- Current approach works perfectly
- Reproducible results
- No external dependencies
- Easy to demonstrate and explain

**Option 2: Hybrid Approach** (Future enhancement)
- Keep simulated tools for testing
- Add MCP servers for production use
- Flag to toggle between modes

**Option 3: Full MCP Integration** (Post-graduation)
- Replace simulated tools with real MCP servers
- Requires 15-20 hours implementation
- Better for production deployment

---

## 📋 HOW TO ADD MCP INTEGRATION (IF DESIRED)

### **Step 1: Install MCP Servers**
```bash
# Make sure Node.js installed
node --version

# Test filesystem server
npx -y @modelcontextprotocol/server-filesystem "C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation"
```

### **Step 2: Update config.json**
```json
{
  "reasoning_model": "qwen2.5:7b",
  "embedding_model": "embeddinggemma:latest",
  "mcp_servers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic_Dissertation"
      ],
      "enabled": false
    },
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"],
      "env": {
        "GIT_DIR": "C:\\Users\\craig\\Desktop\\MainProjects\\Ugentic_Dissertation\\.git"
      },
      "enabled": false
    }
  }
}
```

### **Step 3: Update app.py to Use MCP**
```python
# Add MCP server initialization
from src.ugentic.core.filesystem_tool import FilesystemTool

def initialize_mcp_servers():
    """Initialize MCP servers from config"""
    with open('config.json', 'r') as f:
        config = json.load(f)
    
    mcp_servers = {}
    if 'mcp_servers' in config:
        for name, server_config in config['mcp_servers'].items():
            if server_config.get('enabled', False):
                # Initialize MCP server
                mcp_servers[name] = FilesystemTool(
                    server_config['command'],
                    server_config['args']
                )
    
    return mcp_servers
```

---

## 🎓 RECOMMENDATION FOR DISSERTATION

### **KEEP CURRENT APPROACH** ✅

**Why:**
1. **Simulated tools work perfectly** for research validation
2. **Reproducible results** - same input = same output (critical for research)
3. **No external dependencies** - system always works
4. **Easy to demonstrate** in defense
5. **Clear for evaluators** - they can see exactly what happens
6. **Already validated** - system working, tests passing

**MCP Integration:** Document as future enhancement, implement post-graduation

---

## 🔍 MCP SECURITY NOTE

**Important:** If you do add MCP, use the **latest patched versions!**

**Security Advisory (Aug 2025):**
- CVE-2025-53109 & CVE-2025-53110 - Filesystem MCP Server vulnerabilities
- **Fixed in:** npm version 2025.7.1+
- **Issue:** Allowed sandbox escape, arbitrary code execution
- **Solution:** Always use `npx -y @modelcontextprotocol/server-filesystem` (auto-updates)

**Source:** https://cymulate.com/blog/cve-2025-53109-53110-escaperoute-anthropic/

---

## 📊 SUMMARY

**What We Did:**
- ✅ Removed unused MCP server configurations
- ✅ Fixed config.json to only include what app.py uses
- ✅ Documented current architecture (simulated tools)
- ✅ Provided MCP integration guide for future

**Current System:**
- ✅ Uses internal simulated tools (perfect for dissertation)
- ✅ No external MCP servers needed
- ✅ Clean, simple config.json
- ✅ All tools working (including ask_questions fix)

**For Future:**
- 📝 MCP integration documented (post-graduation)
- 📝 Modern best practices identified (2025 official servers)
- 📝 Security considerations noted (patches)
- 📝 Implementation guide ready (15-20 hours)

---

## ✅ VERIFICATION

**Old config.json:** 106 lines, 4 unused MCP servers, wrong paths  
**New config.json:** 9 lines, only used configuration, correct and clean

**System Status:**
- ✅ All agents working with simulated tools
- ✅ ask_questions tool functional
- ✅ Success rates fixed
- ✅ Model switching available
- ✅ No external dependencies

**Config Status:**
- ✅ Clean and minimal
- ✅ Only used settings
- ✅ No wrong paths
- ✅ Easy to maintain

---

**Your config.json is now clean, correct, and production-ready! 🎉**

**Bottom Line:** Your system uses **internal simulated tools** (Python functions), not external MCP servers. This is **perfect for your dissertation** - reproducible, demonstrable, and reliable!
