# UGENTIC

**Ubuntu-Driven Multi-Agent IT Support System**

![Status](https://img.shields.io/badge/status-research--complete-green)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Agents](https://img.shields.io/badge/agents-6-purple)
![Tools](https://img.shields.io/badge/tools-46-orange)

---

## About

UGENTIC is a research prototype demonstrating how **Ubuntu philosophy** ("I am because we are") enhances multi-agent AI collaboration. It features 6 autonomous agents that work together to solve IT support issues, switching between Solo and Ubuntu (collaborative) modes based on problem complexity.

**Key Innovation:** Agents embody collective problem-solving - recognizing when to collaborate rather than work alone, resulting in **92% performance improvement** on complex multi-domain issues.

---

## Agent Architecture

```
                         ┌─────────────────────┐
                         │     IT Manager      │ Strategic
                         │   (Hybrid Triage)   │ Delegation
                         └──────────┬──────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼                         ▼                         ▼
┌─────────────────┐     ┌─────────────────────┐     ┌─────────────────┐
│ Service Desk    │     │   Infrastructure    │     │ Network Support │
│    Manager      │     │   (Orchestrator)    │     │                 │
│    Tactical     │     │    Operational      │     │   Operational   │
└────────┬────────┘     └──────────┬──────────┘     └─────────────────┘
         │                         │
         ▼                         │              ┌─────────────────┐
┌─────────────────┐                │              │   App Support   │
│   IT Support    │                │              │                 │
│  (Front-line)   │◄───────────────┼──────────────│   Operational   │
│   Operational   │   Ubuntu       │              └─────────────────┘
└─────────────────┘   Orchestration│
                                   ▼
                         ┌─────────────────────┐
                         │  Multi-Agent        │
                         │  Collaboration      │
                         │  (Complex Issues)   │
                         └─────────────────────┘
```

---

## Agents Overview

| Agent | Type | Role | Tools |
|-------|------|------|-------|
| **IT Manager** | Strategic | Triage & delegation (does NOT investigate) | 7 |
| **Infrastructure** | Operational + Orchestrator | Servers, storage + multi-agent coordination | 8 |
| **Network Support** | Operational | Connectivity, security, performance | 7 |
| **App Support** | Operational | Applications, databases, errors | 7 |
| **IT Support** | Operational | Front-line user support, accounts | 10 |
| **Service Desk Manager** | Tactical | Team coordination, SLA management | 7 |

**Total:** 6 agents, 46 diagnostic tools

---

## How It Works

### Triage Flow

```
User Request
     │
     ▼
┌─────────────────────────────────────────────┐
│              IT Manager Triage              │
├─────────────────────────────────────────────┤
│  Upfront (5-10%)    → Multi-domain detected │───► Infrastructure Orchestrator
│  Rule-based (70-80%) → Clear keywords       │───► Direct to Specialist
│  LLM (10-20%)       → Ambiguous cases       │───► Reasoned Delegation
└─────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────┐
│         Specialist Investigation            │
│              (ReAct Pattern)                │
├─────────────────────────────────────────────┤
│  Thought → What do I need to know?          │
│  Action  → Execute diagnostic tool          │
│  Observe → Analyze results                  │
│  Repeat  → Until solved or needs help       │
└─────────────────────────────────────────────┘
     │
     ▼ (if multi-domain)
┌─────────────────────────────────────────────┐
│         Ubuntu Orchestration                │
│    "I am because we are"                    │
├─────────────────────────────────────────────┤
│  Coordinate multiple specialists            │
│  Synthesize findings                        │
│  Unified solution                           │
└─────────────────────────────────────────────┘
```

### Ubuntu Philosophy in Practice

- **Collective Problem-Solving:** Agents recognize when collaboration beats solo work
- **Knowledge Sharing:** Solutions documented for team learning
- **Mutual Support:** Specialists help each other on complex issues
- **Consensus Building:** Multi-agent decisions involve all relevant expertise

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/CraigFineTuned/Ugentic_Dissertation.git
cd Ugentic_Dissertation

# 2. Setup environment
python scripts/setup_project.py

# 3. Start Ollama (separate terminal)
ollama serve

# 4. Run the system
.venv\Scripts\activate   # Windows
python app.py
```

---

## Project Structure

```
Ugentic_Dissertation/
├── app.py                    # Main entry point
├── src/ugentic/
│   ├── agents/
│   │   └── react_agents/     # 6 ReAct pattern agents
│   ├── core/
│   │   ├── react_engine.py   # ReAct reasoning engine
│   │   ├── ubuntu_orchestrator.py  # Multi-agent coordination
│   │   └── collaboration_detector.py
│   └── tools/                # 46 diagnostic tools
├── docs/
│   ├── ARCHITECTURE.md       # System design
│   ├── AGENTS.md             # Detailed agent profiles
│   └── SETUP_GUIDE.md        # Installation guide
└── knowledge_base/           # RAG documents
```

---

## Performance

| Metric | Value |
|--------|-------|
| Level 1 Resolution (IT Support) | 5-15 seconds |
| Level 2 Resolution (Specialist) | 10-20 seconds |
| Level 3 Resolution (Orchestration) | 20-40 seconds |
| Ubuntu Collaboration Improvement | **92%** |
| Tool Count | 46 |
| Max Investigation Iterations | 8-10 |

---

## Key Features

| Feature | Description |
|---------|-------------|
| **ReAct Pattern** | Reasoning + Acting for intelligent investigation |
| **Hybrid Triage** | Rule-based (fast) + LLM (smart) delegation |
| **Ubuntu Orchestration** | Multi-agent collaboration for complex issues |
| **Diagnostic Trees** | Pre-built decision trees for common problems |
| **Automatic Escalation** | Detects when to involve other specialists |
| **RAG Integration** | Knowledge base queries for solutions |

---

## Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) | Installation and configuration |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design and patterns |
| [AGENTS.md](docs/AGENTS.md) | Detailed agent profiles and tools |

---

## Research Context

**Title:** Ubuntu-Driven Multi-Agent AI Systems for Organisational IT Departments: A Design Science Investigation

**Researcher:** Craig Vraagom (402415017)

**Institution:** Richfield Graduate Institute of Technology

**Date:** November 2025

---

## Related Projects

- [Ugentic_Unlimited](https://github.com/CraigFineTuned/Ugentic_Unlimited) - Evolution into organizational simulation platform

---

## License

Research project. See documentation for academic citation requirements.
