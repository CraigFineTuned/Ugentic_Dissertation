# PLATFORM-INDEPENDENT PATH SYSTEM

**Created:** November 17, 2025 - Session 33
**Purpose:** Normalize file references across Windows/Linux environments
**Status:** ✅ ACTIVE - Use this for all file references

---

## 🌐 ENVIRONMENT DETECTION

### Current Environment
- **Platform:** Linux
- **User:** user
- **Project Root:** `/home/user/Ugentic_Dissertation`

### Historical Environment (Windows)
- **Platform:** Windows 11
- **User:** craig
- **Project Root:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation`

---

## 📁 CANONICAL PATH CONVENTION

### Always Use Relative Paths from Project Root

**Format:** `{PROJECT_ROOT}/relative/path/to/file`

**Examples:**
```
# Source Code
{PROJECT_ROOT}/src/ugentic/agents/react_agents/itmanager_agent_react.py
{PROJECT_ROOT}/src/ugentic/core/react_engine.py
{PROJECT_ROOT}/app.py

# Documentation
{PROJECT_ROOT}/docs/Project_Tracker/SESSION_ENTRY.md
{PROJECT_ROOT}/docs/Project_Tracker/PROJECT_CONTEXT.md
{PROJECT_ROOT}/README.md

# Configuration
{PROJECT_ROOT}/config.json
{PROJECT_ROOT}/requirements.txt

# Knowledge Base
{PROJECT_ROOT}/knowledge_base/00_IT_Policies_and_Procedures.md
{PROJECT_ROOT}/knowledge_base/02_Application_Support/02-01_App_Support_Playbook.md

# Data & Memory
{PROJECT_ROOT}/data/memory/investigations.json
{PROJECT_ROOT}/data/logs/
```

---

## 🔄 PATH TRANSLATION TABLE

### Critical File Paths

| Component | Relative Path | Linux (Current) | Windows (Historical) |
|-----------|---------------|-----------------|----------------------|
| **Master Entry** | `docs/Project_Tracker/SESSION_ENTRY.md` | `/home/user/Ugentic_Dissertation/docs/Project_Tracker/SESSION_ENTRY.md` | `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\SESSION_ENTRY.md` |
| **Project Context** | `docs/Project_Tracker/PROJECT_CONTEXT.md` | `/home/user/Ugentic_Dissertation/docs/Project_Tracker/PROJECT_CONTEXT.md` | `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\PROJECT_CONTEXT.md` |
| **Checkpoint** | `docs/Project_Tracker/CURRENT_SESSION_CHECKPOINT.md` | `/home/user/Ugentic_Dissertation/docs/Project_Tracker/CURRENT_SESSION_CHECKPOINT.md` | `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\Project_Tracker\CURRENT_SESSION_CHECKPOINT.md` |
| **Main App** | `app.py` | `/home/user/Ugentic_Dissertation/app.py` | `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\app.py` |
| **Config** | `config.json` | `/home/user/Ugentic_Dissertation/config.json` | `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\config.json` |

### Agent Files

| Agent | Relative Path |
|-------|---------------|
| IT Manager | `src/ugentic/agents/react_agents/itmanager_agent_react.py` |
| Service Desk Manager | `src/ugentic/agents/react_agents/service_desk_manager_react.py` |
| IT Support | `src/ugentic/agents/react_agents/itsupport_agent_react.py` |
| App Support | `src/ugentic/agents/react_agents/app_support_agent_react.py` |
| Network Support | `src/ugentic/agents/react_agents/network_agent_react.py` |
| Infrastructure | `src/ugentic/agents/react_agents/infrastructure_agent_react.py` |

### Core Engine Files

| Component | Relative Path |
|-----------|---------------|
| ReAct Engine | `src/ugentic/core/react_engine.py` |
| Agent Memory | `src/ugentic/core/agent_memory.py` |
| Collaboration Triage | `src/ugentic/core/collaboration_triage_engine.py` |
| Diagnostic Trees | `src/ugentic/core/diagnostic_trees.py` |
| Config Manager | `src/ugentic/core/config_manager.py` |

---

## 🛠️ USAGE GUIDELINES

### When Documenting File Changes

**❌ DON'T:**
```markdown
Modified: C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\src\ugentic\core\react_engine.py
```

**✅ DO:**
```markdown
Modified: `src/ugentic/core/react_engine.py`
```

### When Referencing in Code Comments

**❌ DON'T:**
```python
# See C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\docs\...
```

**✅ DO:**
```python
# See {PROJECT_ROOT}/docs/Project_Tracker/SESSION_ENTRY.md
# Or use relative path: ../../../docs/Project_Tracker/SESSION_ENTRY.md
```

### When Writing Instructions

**❌ DON'T:**
```
Run: python C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\app.py
```

**✅ DO:**
```bash
# From project root:
python app.py

# Or with explicit path:
cd {PROJECT_ROOT}
python app.py
```

---

## 🔍 ENVIRONMENT AUTO-DETECTION SCRIPT

For scripts that need to detect environment:

```python
import os
import platform

def get_project_root():
    """Auto-detect project root based on current platform"""
    current_platform = platform.system()

    if current_platform == "Linux":
        return "/home/user/Ugentic_Dissertation"
    elif current_platform == "Windows":
        return r"C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation"
    else:
        # Fallback: Find project root by looking for config.json
        current_dir = os.path.dirname(os.path.abspath(__file__))
        while current_dir != os.path.dirname(current_dir):
            if os.path.exists(os.path.join(current_dir, "config.json")):
                return current_dir
            current_dir = os.path.dirname(current_dir)
        raise RuntimeError("Could not find project root")

# Usage:
PROJECT_ROOT = get_project_root()
session_entry = os.path.join(PROJECT_ROOT, "docs", "Project_Tracker", "SESSION_ENTRY.md")
```

---

## 📋 QUICK REFERENCE GUIDE

### File Reference Checklist

When writing documentation:
- [ ] Use relative paths from project root
- [ ] Use forward slashes (/) not backslashes (\)
- [ ] Use `{PROJECT_ROOT}/` prefix or bare relative path
- [ ] Never hardcode `C:\Users\craig\...`
- [ ] Never hardcode `/home/user/...`
- [ ] Test paths work on both platforms

### Platform Differences

| Aspect | Linux | Windows |
|--------|-------|---------|
| Path Separator | `/` | `\` (but `/` works too) |
| Line Endings | LF (`\n`) | CRLF (`\r\n`) |
| Case Sensitivity | Yes | No |
| Python venv activation | `source .venv/bin/activate` | `.venv\Scripts\activate` |
| Shell | bash | cmd/PowerShell |

---

## 🚨 MIGRATION STATUS

### Files Needing Path Updates

**High Priority (Session 33):**
- [ ] SESSION_ENTRY.md (1,297 lines with Windows paths)
- [ ] SESSION_COMPLETION_SUMMARY.md
- [ ] CURRENT_SESSION_CHECKPOINT.md
- [ ] PROJECT_CONTEXT.md

**Medium Priority:**
- [ ] All SESSION_XX_*.md files
- [ ] ARCHITECTURE.md
- [ ] DEPLOYMENT_GUIDE.md

**Low Priority (Reference only):**
- [ ] Archived session summaries (historical record)

### Migration Strategy

**Phase 1 (Now):** Update active nucleus files (SESSION_ENTRY, CHECKPOINT, CONTEXT)
**Phase 2 (Next session):** Update recent session files (30-32)
**Phase 3 (Future):** Archive historical files with note about Windows paths

---

## ✅ VERIFICATION

To verify path references work:

```bash
# From project root
cd /home/user/Ugentic_Dissertation

# Test file exists
test -f docs/Project_Tracker/SESSION_ENTRY.md && echo "✅ Path works"

# Test Python can find it
python -c "import os; print('✅ App exists' if os.path.exists('app.py') else '❌ Not found')"

# Test config loads
python -c "import json; json.load(open('config.json')); print('✅ Config valid')"
```

---

## 🎯 BENEFITS

**Before (Broken):**
- Windows paths don't work on Linux
- Copy-paste errors
- Documentation feels foreign
- Can't test on different platforms

**After (Fixed):**
- ✅ Paths work on any platform
- ✅ Accurate documentation
- ✅ Copy-paste works correctly
- ✅ Cross-platform compatibility
- ✅ Future-proof for deployment

---

**Document:** PATH_MAPPINGS.md
**Location:** `docs/Project_Tracker/`
**Status:** ✅ ACTIVE - Reference this for ALL path usage
**Created:** November 17, 2025 - Session 33
**Maintained By:** All sessions going forward
