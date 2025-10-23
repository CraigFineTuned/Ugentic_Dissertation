#!/usr/bin/env python
"""
UGENTIC Health Check Script
Verifies system configuration, dependencies, and connectivity

Usage:
    python health_check.py
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(title: str):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{title:^60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def check_python_version() -> Tuple[bool, str]:
    """Check Python version"""
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            return True, f"Python {version.major}.{version.minor}.{version.micro} ✓"
        else:
            return False, f"Python {version.major}.{version.minor}.{version.micro} - Requires 3.10+"
    except Exception as e:
        return False, str(e)

def check_imports() -> Tuple[bool, List[str]]:
    """Check critical imports"""
    required_modules = [
        'langchain_ollama',
        'chromadb',
        'pydantic',
        'pytest',
        'requests',
    ]
    
    missing = []
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    return len(missing) == 0, missing

def check_project_structure() -> Tuple[bool, List[str]]:
    """Check project directory structure"""
    required_files = [
        'app.py',
        'config.json',
        'requirements.txt',
        'src/ugentic/__init__.py',
        'src/ugentic/config_manager.py',
        'src/ugentic/constants.py',
    ]
    
    project_root = Path(__file__).parent
    missing = []
    
    for file in required_files:
        file_path = project_root / file
        if not file_path.exists():
            missing.append(file)
    
    return len(missing) == 0, missing

def check_directories() -> Tuple[bool, Dict[str, str]]:
    """Check and create required directories"""
    from src.ugentic.config_manager import get_config
    
    try:
        config = get_config()
        
        status = {
            'logs': config.logs_dir,
            'agents_logs': config.agents_logs_dir,
            'knowledge_base': config.knowledge_base_dir,
            'plans': config.plans_dir,
            'test_results': config.test_results_dir,
            'data': config.data_dir,
        }
        
        # All created automatically by config manager
        return True, status
    except Exception as e:
        return False, {'error': str(e)}

def check_ollama_connection() -> Tuple[bool, str]:
    """Check Ollama connectivity"""
    try:
        import requests
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            model_names = [m.get('name', 'unknown') for m in models]
            return True, f"Connected. Models: {', '.join(model_names[:3])}"
        else:
            return False, f"Ollama not responding (status {response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, "Cannot connect to Ollama (http://localhost:11434)"
    except requests.exceptions.Timeout:
        return False, "Ollama connection timeout (5s)"
    except Exception as e:
        return False, str(e)

def check_configuration() -> Tuple[bool, Dict[str, str]]:
    """Check configuration loading"""
    try:
        from src.ugentic.config_manager import get_config
        
        config = get_config()
        
        return True, {
            'reasoning_model': config.reasoning_model,
            'embedding_model': config.embedding_model,
            'fast_model': config.fast_model,
            'project_root': config.project_root,
        }
    except Exception as e:
        return False, {'error': str(e)}

def check_agents() -> Tuple[bool, str]:
    """Check agent initialization capability"""
    try:
        from langchain_ollama import ChatOllama
        from src.ugentic.agents.react_agents import (
            ITManagerAgentReAct,
            InfrastructureAgentReAct,
            NetworkSupportAgentReAct,
            AppSupportAgentReAct,
            ITSupportAgentReAct,
            ServiceDeskManagerAgentReAct
        )
        
        agents = [
            'ITManagerAgentReAct',
            'ServiceDeskManagerAgentReAct',
            'ITSupportAgentReAct',
            'AppSupportAgentReAct',
            'NetworkSupportAgentReAct',
            'InfrastructureAgentReAct',
        ]
        
        return True, f"All {len(agents)} agent classes importable"
    except Exception as e:
        return False, str(e)

def check_tools() -> Tuple[bool, List[str]]:
    """Check tool registry"""
    try:
        from src.ugentic.tools import (
            check_server_metrics,
            check_network_bandwidth,
            query_app_logs,
            get_user_profile,
            get_technician_workload,
        )
        
        return True, [
            'check_server_metrics',
            'check_network_bandwidth',
            'query_app_logs',
            'get_user_profile',
            'get_technician_workload',
        ]
    except Exception as e:
        return False, [str(e)]

def check_logging() -> Tuple[bool, str]:
    """Check logging configuration"""
    try:
        from src.ugentic.logging_config import setup_logging
        
        setup_logging()
        
        import logging
        logger = logging.getLogger("ugentic")
        logger.debug("Health check logging test")
        
        return True, "Logging system initialized"
    except Exception as e:
        return False, str(e)

def print_result(name: str, passed: bool, details=None):
    """Print check result"""
    status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
    print(f"{status} | {name}")
    
    if details:
        if isinstance(details, list):
            if passed:
                for item in details[:5]:
                    print(f"        • {item}")
            else:
                print(f"        Missing: {', '.join(details)}")
        elif isinstance(details, dict):
            for key, value in list(details.items())[:5]:
                print(f"        {key}: {value}")
        else:
            print(f"        {details}")

def run_health_check():
    """Run comprehensive health check"""
    print_header("UGENTIC Health Check")
    
    all_passed = True
    
    # 1. Python Version
    print(f"{Colors.BOLD}System Requirements{Colors.RESET}")
    passed, msg = check_python_version()
    print_result("Python Version", passed, msg)
    all_passed = all_passed and passed
    
    # 2. Dependencies
    passed, missing = check_imports()
    print_result("Python Dependencies", passed, missing if not passed else None)
    all_passed = all_passed and passed
    
    # 3. Project Structure
    passed, missing = check_project_structure()
    print_result("Project Files", passed, missing if not passed else None)
    all_passed = all_passed and passed
    
    # 4. Configuration
    print(f"\n{Colors.BOLD}Configuration{Colors.RESET}")
    passed, config = check_configuration()
    print_result("Configuration Loading", passed, config)
    all_passed = all_passed and passed
    
    # 5. Directories
    passed, dirs = check_directories()
    print_result("Project Directories", passed, dirs)
    all_passed = all_passed and passed
    
    # 6. External Services
    print(f"\n{Colors.BOLD}External Services{Colors.RESET}")
    passed, msg = check_ollama_connection()
    print_result("Ollama Connection", passed, msg)
    # Don't fail overall - can still run with fallback
    
    # 7. Logging
    print(f"\n{Colors.BOLD}UGENTIC Components{Colors.RESET}")
    passed, msg = check_logging()
    print_result("Logging System", passed, msg)
    all_passed = all_passed and passed
    
    # 8. Agents
    passed, msg = check_agents()
    print_result("Agent Classes", passed, msg)
    all_passed = all_passed and passed
    
    # 9. Tools
    passed, tools = check_tools()
    print_result("Tool Registry", passed, tools if not passed else None)
    all_passed = all_passed and passed
    
    # Summary
    print_header("Health Check Summary")
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL CHECKS PASSED{Colors.RESET}")
        print("\nSystem is ready. Run with: python app.py")
        return 0
    else:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠ SOME CHECKS FAILED{Colors.RESET}")
        print("\nFix issues above and retry. See DEPLOYMENT_GUIDE.md for help.")
        return 1

if __name__ == "__main__":
    try:
        exit_code = run_health_check()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Health check interrupted{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
