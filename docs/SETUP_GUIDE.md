# UGENTIC Setup & Configuration Guide

## 📋 Prerequisites

1.  **Python 3.10+** installed.
2.  **Ollama** installed and running (`ollama serve`).
3.  **Git** installed.

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/CraigFineTuned/Ugentic_Dissertation.git
cd Ugentic_Dissertation
```

### 2. Automated Setup

We provide a cross-platform setup script to create the virtual environment and install dependencies.

**Windows:**
```powershell
python scripts/setup_project.py
```

**Linux/Mac:**
```bash
python3 scripts/setup_project.py
```

### 3. Model Setup

Pull the required models (or configure your own in `config.json`):

```bash
ollama pull deepseek-v3.1:671b-cloud  # Or your preferred reasoning model
ollama pull embeddinggemma:latest     # For RAG/Memory
ollama pull gemma3n:e4b              # Fast model
```

---

## ⚙️ Configuration

### Dynamic Pathing (Core System)

The core system (`src/ugentic`) uses **dynamic path resolution**. It automatically detects the project root relative to the `app.py` file. You do **not** need to configure paths for the main application to work.

### Customizing `config.json`

Create or edit `config.json` in the root directory to override defaults:

```json
{
  "reasoning_model": "llama3",
  "embedding_model": "nomic-embed-text",
  "alternative_models": {
    "fast": "gemma:2b"
  }
}
```

### Environment Variables (Optional)

The system respects standard environment variables:
- `OLLAMA_HOST`: URL of the Ollama server (default: `http://localhost:11434`)

---

## 🛠️ Maintenance & Dissertation Tools

The `scripts/` directory contains maintenance and legacy dissertation generation tools.

### ⚠️ Important: Updating Hardcoded Paths

Some scripts in `scripts/dissertation/` (e.g., `generate_pristine_dissertation.py`) contain **hardcoded paths** specific to the original research environment (e.g., `C:\Users\craig\...`).

**If you intend to use these specific scripts, you MUST update the paths:**

1.  **Open the script** in a text editor.
2.  **Search for** `C:\Users\craig` or `C:\\Users\\craig`.
3.  **Replace** the paths with your local equivalents.

**Example (in `scripts/dissertation/generate_pristine_dissertation.py`):**

*Change this:*
```python
input_md = r"C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Completed\Correction Report.md"
```

*To this (your path):*
```python
# Use relative path or your absolute path
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_md = os.path.join(BASE_DIR, "My_Dissertation", "Correction Report.md")
```

**Note:** The core application (`app.py`) does **not** require this manual fixing. It is fully portable.

---

## 🏃 Running the System

1.  **Activate the environment:**
    *   Windows: `.venv\Scripts\activate`
    *   Linux/Mac: `source .venv/bin/activate`

2.  **Start the application:**
    ```bash
    python app.py
    ```

3.  **Verify System Health:**
    ```bash
    python scripts/maintenance/health_check.py
    ```

---

## 📁 Directory Structure

*   `app.py`: Main entry point.
*   `src/`: Core source code.
*   `scripts/`:
    *   `maintenance/`: Health checks, cleanup scripts.
    *   `dissertation/`: **(Legacy)** Generation scripts for the academic paper.
*   `docs/`: Project documentation.
*   `logs/`: Runtime logs (auto-generated).
*   `knowledge_base/`: Place your RAG documents here (.txt, .md).
*   `config.json`: User configuration.