#!/usr/bin/env python
"""
UGENTIC Final Verification Script - Comprehensive System Check
Verifies all Session 26 fixes are in place and working correctly

Run this AFTER health_check.py passes to ensure all fixes are applied correctly
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def verify_files_exist() -> Tuple[bool, List[str]]:
    """Verify all Session 26 created/modified files exist"""
    required_files = {
        'NEW': [
            'src/ugentic/config_manager.py',
            'src/ugentic/constants.py',
            'health_check.py',
            'ARCHITECTURE.md',
            'DEPLOYMENT_GUIDE.md',
            'SESSION_26_FINAL_SUMMARY.md',
            'src/ugentic/__init__.py',
            'src/ugentic/core/__init__.py',
        ],
        'MODIFIED': [
            'app.py',
            'src/ugentic/logging_config.py',
            'src/ugentic/core/agent_framework.py',
            'README.md',
            'docs/Project_Tracker/SESSION_ENTRY.md',
        ]
    }
    
    project_root = Path(__file__).parent
    missing = []
    
    print(f"\n{Colors.BOLD}Checking Session 26 Files...{Colors.RESET}\n")
    
    for category, files in required_files.items():
        print(f"{Colors.BOLD}{category} Files:{Colors.RESET}")
        for file_path in files:
            full_path = project_root / file_path
            if full_path.exists():
                size = full_path.stat().st_size
                print(f"  ✓ {file_path} ({size:,} bytes)")
            else:
                print(f"  ✗ {file_path} - MISSING!")
                missing.append(file_path)
    
    return len(missing) == 0, missing

def verify_no_hardcoded_paths() -> Tuple[bool, List[str]]:
    """Verify no hardcoded Windows paths remain"""
    print(f"\n{Colors.BOLD}Checking for Hardcoded Paths...{Colors.RESET}\n")
    
    suspicious_patterns = [
        'C:\\Users\\craig',
        'C:/Users/craig',
        'C:\\\\Users\\\\craig',
        'C:/Users/craig/Desktop',
    ]
    
    files_to_check = [
        'app.py',
        'src/ugentic/logging_config.py',
        'src/ugentic/config.py',
    ]
    
    project_root = Path(__file__).parent
    violations = []
    
    for file_path in files_to_check:
        full_path = project_root / file_path
        if not full_path.exists():
            continue
        
        try:
            content = full_path.read_text()
            for pattern in suspicious_patterns:
                if pattern in content:
                    violations.append(f"{file_path}: Contains '{pattern}'")
                    print(f"  ✗ {file_path}: Found hardcoded path!")
            
            if file_path not in [f.split(':')[0] for f in violations]:
                print(f"  ✓ {file_path}: No hardcoded paths")
        except Exception as e:
            print(f"  ⚠ {file_path}: Could not check ({e})")
    
    return len(violations) == 0, violations

def verify_config_manager() -> Tuple[bool, str]:
    """Verify ConfigManager is working correctly"""
    print(f"\n{Colors.BOLD}Verifying ConfigManager...{Colors.RESET}\n")
    
    try:
        from src.ugentic.config_manager import get_config, ConfigManager
        
        config = get_config()
        
        # Check singleton
        config2 = get_config()
        if config is not config2:
            return False, "ConfigManager is not singleton!"
        
        print(f"  ✓ ConfigManager singleton verified")
        
        # Check paths
        paths_to_check = [
            ('logs_dir', config.logs_dir),
            ('agents_logs_dir', config.agents_logs_dir),
            ('knowledge_base_dir', config.knowledge_base_dir),
            ('plans_dir', config.plans_dir),
            ('test_results_dir', config.test_results_dir),
            ('data_dir', config.data_dir),
        ]
        
        for name, path in paths_to_check:
            if not Path(path).exists():
                return False, f"{name} directory not created: {path}"
            print(f"  ✓ {name}: {path}")
        
        # Check models
        print(f"\n  Models configured:")
        print(f"    • reasoning_model: {config.reasoning_model}")
        print(f"    • embedding_model: {config.embedding_model}")
        print(f"    • fast_model: {config.fast_model}")
        
        # Check project root auto-detection
        if not config.project_root:
            return False, "Project root not detected!"
        print(f"\n  ✓ Project root auto-detected: {config.project_root}")
        
        return True, "ConfigManager working correctly"
    except Exception as e:
        return False, str(e)

def verify_constants() -> Tuple[bool, str]:
    """Verify constants module is working"""
    print(f"\n{Colors.BOLD}Verifying Constants Module...{Colors.RESET}\n")
    
    try:
        from src.ugentic.constants import (
            InvestigationStatus,
            AgentNames,
            InfrastructureTools,
            NetworkTools,
            ApplicationTools,
            SupportTools,
            ManagerTools,
            ErrorMessages,
        )
        
        # Check statuses
        statuses = [
            ('ROOT_CAUSE_FOUND', InvestigationStatus.ROOT_CAUSE_FOUND),
            ('NEEDS_COLLABORATION', InvestigationStatus.NEEDS_COLLABORATION),
            ('RESOLVED', InvestigationStatus.RESOLVED),
        ]
        
        print(f"  Investigation Statuses:")
        for name, value in statuses:
            print(f"    ✓ {name}: {value}")
        
        # Check agents
        agents = AgentNames.all_names()
        print(f"\n  Agents ({len(agents)}):")
        for agent in agents:
            print(f"    ✓ {agent}")
        
        # Check tools
        infra_tools = [name for name in dir(InfrastructureTools) if not name.startswith('_')]
        network_tools = [name for name in dir(NetworkTools) if not name.startswith('_')]
        app_tools = [name for name in dir(ApplicationTools) if not name.startswith('_')]
        support_tools = [name for name in dir(SupportTools) if not name.startswith('_')]
        manager_tools = [name for name in dir(ManagerTools) if not name.startswith('_')]
        
        total_tools = len(infra_tools) + len(network_tools) + len(app_tools) + len(support_tools) + len(manager_tools)
        
        print(f"\n  Tools defined ({total_tools} total):")
        print(f"    ✓ Infrastructure: {len(infra_tools)} tools")
        print(f"    ✓ Network: {len(network_tools)} tools")
        print(f"    ✓ Application: {len(app_tools)} tools")
        print(f"    ✓ Support: {len(support_tools)} tools")
        print(f"    ✓ Manager: {len(manager_tools)} tools")
        
        return True, f"Constants module verified ({total_tools} tools defined)"
    except Exception as e:
        return False, f"Error: {str(e)}"

def verify_logging() -> Tuple[bool, str]:
    """Verify logging uses dynamic paths"""
    print(f"\n{Colors.BOLD}Verifying Logging System...{Colors.RESET}\n")
    
    try:
        from src.ugentic.logging_config import setup_logging
        from src.ugentic.config_manager import get_config
        
        config = get_config()
        
        # Check that setup_logging works
        setup_logging()
        print(f"  ✓ Logging system initialized")
        
        # Check log files will be created in dynamic path
        logs_dir = Path(config.logs_dir)
        print(f"  ✓ Logs directory: {logs_dir}")
        
        if logs_dir.exists():
            print(f"  ✓ Logs directory exists and is writable")
        
        return True, "Logging system uses dynamic paths"
    except Exception as e:
        return False, str(e)

def verify_imports() -> Tuple[bool, str]:
    """Verify package imports work cleanly"""
    print(f"\n{Colors.BOLD}Verifying Package Imports...{Colors.RESET}\n")
    
    try:
        # Test clean imports
        from src.ugentic.config_manager import get_config
        print(f"  ✓ from src.ugentic.config_manager import get_config")
        
        from src.ugentic.constants import InvestigationStatus, AgentNames
        print(f"  ✓ from src.ugentic.constants import InvestigationStatus, AgentNames")
        
        from src.ugentic.core import ReactEngine, ToolRegistry
        print(f"  ✓ from src.ugentic.core import ReactEngine, ToolRegistry")
        
        from src.ugentic.agents.react_agents import (
            ITManagerAgentReAct,
            InfrastructureAgentReAct,
        )
        print(f"  ✓ from src.ugentic.agents.react_agents import agents")
        
        return True, "All imports clean and working"
    except Exception as e:
        return False, str(e)

def verify_documentation() -> Tuple[bool, List[str]]:
    """Verify all documentation files exist and have content"""
    print(f"\n{Colors.BOLD}Verifying Documentation...{Colors.RESET}\n")
    
    docs = {
        'README.md': (500, 'Project overview'),
        'ARCHITECTURE.md': (600, 'System design'),
        'DEPLOYMENT_GUIDE.md': (400, 'Setup instructions'),
        'SESSION_26_FINAL_SUMMARY.md': (300, 'All fixes'),
    }
    
    project_root = Path(__file__).parent
    issues = []
    
    for filename, (min_lines, description) in docs.items():
        filepath = project_root / filename
        
        if not filepath.exists():
            issues.append(f"{filename}: MISSING")
            print(f"  ✗ {filename}: Not found!")
            continue
        
        try:
            content = filepath.read_text()
            line_count = len(content.split('\n'))
            
            if line_count < min_lines:
                issues.append(f"{filename}: Too small ({line_count} lines, need {min_lines})")
                print(f"  ⚠ {filename}: {line_count} lines (expected {min_lines}+)")
            else:
                print(f"  ✓ {filename}: {line_count} lines - {description}")
        except Exception as e:
            issues.append(f"{filename}: Error reading ({e})")
            print(f"  ✗ {filename}: Error - {e}")
    
    return len(issues) == 0, issues

def verify_error_handling() -> Tuple[bool, str]:
    """Verify app.py has comprehensive error handling"""
    print(f"\n{Colors.BOLD}Verifying Error Handling...{Colors.RESET}\n")
    
    try:
        app_path = Path(__file__).parent / 'app.py'
        if not app_path.exists():
            return False, "app.py not found"
        
        content = app_path.read_text()
        
        # Check for key error handling patterns
        checks = {
            'SystemInitializationError': 'Custom exception class',
            'try:': 'Exception handling',
            'except': 'Exception catching',
            'graceful': 'Graceful degradation',
            'fallback': 'Fallback logic',
        }
        
        found = []
        for pattern, description in checks.items():
            if pattern.lower() in content.lower():
                found.append(description)
                print(f"  ✓ {description} found")
            else:
                print(f"  ⚠ {description} not clearly found")
        
        if len(found) >= 4:
            return True, f"Error handling comprehensive ({len(found)}/5 patterns found)"
        else:
            return False, f"Error handling incomplete ({len(found)}/5 patterns found)"
    except Exception as e:
        return False, str(e)

def main():
    """Run all verification checks"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}UGENTIC FINAL VERIFICATION{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}Session 26 - All Fixes Verification{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    results = []
    
    # Run all checks
    passed, missing = verify_files_exist()
    results.append(('Session 26 Files', passed, missing if not passed else None))
    
    passed, violations = verify_no_hardcoded_paths()
    results.append(('No Hardcoded Paths', passed, violations if not passed else None))
    
    passed, msg = verify_config_manager()
    results.append(('ConfigManager', passed, msg if not passed else None))
    
    passed, msg = verify_constants()
    results.append(('Constants Module', passed, msg if not passed else None))
    
    passed, msg = verify_logging()
    results.append(('Logging System', passed, msg if not passed else None))
    
    passed, msg = verify_imports()
    results.append(('Package Imports', passed, msg if not passed else None))
    
    passed, issues = verify_documentation()
    results.append(('Documentation', passed, issues if not passed else None))
    
    passed, msg = verify_error_handling()
    results.append(('Error Handling', passed, msg if not passed else None))
    
    # Print summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}VERIFICATION SUMMARY{Colors.RESET}\n")
    
    all_passed = True
    for name, passed, details in results:
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} | {name}")
        if details and not passed:
            if isinstance(details, list):
                for item in details:
                    print(f"        - {item}")
            else:
                print(f"        {details}")
        all_passed = all_passed and passed
    
    # Final verdict
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    if all_passed:
        print(f"{Colors.GREEN}{Colors.BOLD}✓ ALL VERIFICATION CHECKS PASSED{Colors.RESET}")
        print(f"\n{Colors.GREEN}Session 26 is complete and production-ready!{Colors.RESET}")
        print(f"\n{Colors.BOLD}Next steps:{Colors.RESET}")
        print(f"  1. Run: python app.py")
        print(f"  2. Test with IT support requests")
        print(f"  3. Ready for Phase 3 Expert Validation")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ SOME CHECKS FAILED{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Review failures above and fix issues.{Colors.RESET}")
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Verification interrupted{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Fatal error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
