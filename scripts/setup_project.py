#!/usr/bin/env python3
"""
UGENTIC Setup Helper
Cross-platform script to set up the development environment.
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

def setup_environment():
    print("="*60)
    print("UGENTIC Development Environment Setup")
    print("="*60)

    project_root = Path(__file__).resolve().parent.parent
    venv_dir = project_root / ".venv"
    
    print(f"Project Root: {project_root}")
    
    # 1. Create Virtual Environment
    if not venv_dir.exists():
        print(f"\nCreating virtual environment at {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
        print("✓ Virtual environment created")
    else:
        print(f"\n✓ Virtual environment already exists at {venv_dir}")

    # 2. Determine pip path
    if platform.system() == "Windows":
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        pip_path = venv_dir / "bin" / "pip"

    # 3. Install Dependencies
    requirements_path = project_root / "requirements.txt"
    if requirements_path.exists():
        print(f"\nInstalling dependencies from {requirements_path}...")
        try:
            subprocess.check_call([str(pip_path), "install", "-r", str(requirements_path)])
            print("✓ Dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            sys.exit(1)
    else:
        print(f"\n⚠ Warning: requirements.txt not found at {requirements_path}")

    # 4. Create Directories
    dirs_to_create = [
        project_root / "logs",
        project_root / "logs" / "agents",
        project_root / "plans",
        project_root / "knowledge_base",
        project_root / "data"
    ]
    
    print("\nEnsuring required directories exist...")
    for d in dirs_to_create:
        if not d.exists():
            d.mkdir(parents=True)
            print(f"  Created: {d}")
        else:
            print(f"  Exists: {d}")

    print("\n" + "="*60)
    print("✓ Setup Complete!")
    print("="*60)
    print("\nTo activate the environment:")
    if platform.system() == "Windows":
        print(f"  {venv_dir}\\Scripts\\activate")
    else:
        print(f"  source {venv_dir}/bin/activate")
    print("\nThen run the application:")
    print("  python app.py")

if __name__ == "__main__":
    setup_environment()
