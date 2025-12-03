# UGENTIC: Ubuntu-Driven Agentic Collective Intelligence

**Multi-agent AI system integrating Ubuntu philosophy with organizational IT support**

![Status](https://img.shields.io/badge/status-project--closure-blue)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-research-orange)

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/CraigFineTuned/Ugentic_Dissertation.git
cd Ugentic_Dissertation

# 2. Run Setup (Creates venv & installs dependencies)
# Windows:
python scripts/setup_project.py
# Linux/Mac:
python3 scripts/setup_project.py

# 3. Start Ollama (in a separate terminal)
ollama serve

# 4. Activate & Run
# Windows:
.venv\Scripts\activate
python app.py
```

See **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** for detailed configuration instructions.

---

## 📋 Overview

UGENTIC is a research prototype demonstrating how **Ubuntu philosophy** (collective humanity, "I am because we are") can enhance **multi-agent AI systems** for organizational collaboration.

It features a hierarchical team of 6 autonomous agents that collaborate to solve IT support issues, switching between "Solo" (efficient) and "Ubuntu" (collaborative) modes based on problem complexity.

---

## 📁 Repository Structure

| Directory | Purpose |
|-----------|---------|
| `src/ugentic` | **Core System Code**. Contains the ReAct engine, agents, and orchestration logic. |
| `scripts/` | **Tools**. Includes setup helpers, maintenance scripts, and legacy dissertation generators. |
| `docs/` | **Documentation**. Architecture guides, project tracking, and setup instructions. |
| `knowledge_base/` | **RAG Data**. Place text files here for the agents to ingest. |
| `logs/` | **Runtime Data**. Structured JSON logs of all agent investigations. |

---

## 📚 Key Documentation

*   **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)**: Detailed installation, configuration, and troubleshooting.
*   **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**: System design, agent roles, and the Ubuntu orchestration protocol.
*   **[docs/AGENTS.md](docs/AGENTS.md)**: Detailed profiles of the 6 agent personas.

---

## ⚠️ Note on Legacy Scripts

The `scripts/dissertation/` directory contains python scripts used to generate the specific academic dissertation text. These scripts may contain **hardcoded paths** specific to the original research environment. If you wish to use them, please refer to the "Updating Hardcoded Paths" section in the [Setup Guide](docs/SETUP_GUIDE.md).

**The core system (`app.py`) is fully portable and does not require path modification.**

---

## 📄 License & Citation

**Title:** Investigating Ubuntu Philosophy in Multi-Agent AI Systems for Organizational Support  
**Researcher:** Craig Vraagom (402415017)  
**Institution:** Richfield Graduate Institute of Technology  
**Date:** October 2025