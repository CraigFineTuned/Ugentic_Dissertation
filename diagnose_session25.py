#!/usr/bin/env python3
"""
Session 25 Diagnostic Test
Quick verification that retry logic and fallback mechanisms are working
Run this BEFORE comprehensive testing
"""

import sys
import json
from pathlib import Path

def check_react_engine_code():
    """Verify react_engine.py has Session 25 fixes"""
    print("\n" + "="*60)
    print(" CHECKING REACT ENGINE CODE")
    print("="*60)
    
    react_path = Path("src/ugentic/core/react_engine.py")
    
    if not react_path.exists():
        print("❌ react_engine.py not found!")
        return False
    
    content = react_path.read_text()
    
    checks = {
        "import time": "Time module import (needed for backoff delays)",
        "_select_fallback_tool": "Fallback tool selection method",
        "max_retries = 3": "3-attempt retry logic in _generate_thought",
        "retry_delay *= 2": "Exponential backoff (1s, 2s, 4s)",
        "SESSION 25 FIX": "Session 25 documentation in docstring",
        "fallback_mode": "Fallback mode indicator",
        "exponential backoff": "Retry strategy documentation"
    }
    
    all_good = True
    for check_str, description in checks.items():
        if check_str in content:
            print(f"✅ {description}")
        else:
            print(f"❌ {description} - NOT FOUND")
            all_good = False
    
    return all_good


def check_ollama_availability():
    """Check if Ollama is running"""
    print("\n" + "="*60)
    print(" CHECKING OLLAMA AVAILABILITY")
    print("="*60)
    
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=2)
        
        if response.status_code == 200:
            print("✅ Ollama is running on port 11434")
            try:
                models = response.json().get('models', [])
                print(f"   Found {len(models)} model(s):")
                for model in models[:5]:
                    print(f"   - {model.get('name', 'unknown')}")
                if len(models) > 5:
                    print(f"   ... and {len(models) - 5} more")
                return True
            except:
                print("⚠️ Ollama responding but couldn't parse models")
                return True
        else:
            print(f"❌ Ollama responded with status {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️ Ollama NOT running (connection refused)")
        print("   This is OK - Session 25 fixes allow fallback tool selection")
        print("   System will still work, just without LLM reasoning")
        return False
    except Exception as e:
        print(f"⚠️ Could not check Ollama: {e}")
        print("   Make sure requests library is installed")
        return False


def check_python_cache():
    """Check if Python cache might be stale"""
    print("\n" + "="*60)
    print(" CHECKING PYTHON CACHE")
    print("="*60)
    
    pycache_dir = Path("src/ugentic/core/__pycache__")
    
    if pycache_dir.exists():
        files = list(pycache_dir.glob("*.pyc"))
        print(f"⚠️ Found {len(files)} .pyc files in __pycache__")
        print("   Run CLEAR_PYTHON_CACHE.bat before testing!")
        return False
    else:
        print("✅ No stale cache files found")
        return True


def check_imports():
    """Test if modules can be imported"""
    print("\n" + "="*60)
    print(" CHECKING IMPORTS")
    print("="*60)
    
    try:
        print("Testing: import time")
        import time
        print("✅ time module imported")
        
        print("Testing: from src.ugentic.core.react_engine import ReactEngine")
        from src.ugentic.core.react_engine import ReactEngine
        print("✅ ReactEngine imported")
        
        # Check if new method exists
        if hasattr(ReactEngine, '_select_fallback_tool'):
            print("✅ _select_fallback_tool method exists")
        else:
            print("❌ _select_fallback_tool method NOT FOUND - cache might be stale")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False


def run_diagnostics():
    """Run all diagnostic checks"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  SESSION 25 DIAGNOSTIC TEST".center(58) + "║")
    print("║" + "  Verify fixes are in place before testing".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    results = {}
    
    results['react_engine'] = check_react_engine_code()
    results['ollama'] = check_ollama_availability()
    results['cache'] = check_python_cache()
    results['imports'] = check_imports()
    
    print("\n" + "="*60)
    print(" DIAGNOSTIC SUMMARY")
    print("="*60)
    
    print(f"\nCode Fixes Present:      {'✅ YES' if results['react_engine'] else '❌ NO'}")
    print(f"Ollama Status:           {'✅ Running' if results['ollama'] else '⚠️ Not running (OK)'}")
    print(f"Cache Status:            {'✅ Clean' if results['cache'] else '⚠️ Stale'}")
    print(f"Imports Working:         {'✅ YES' if results['imports'] else '❌ NO'}")
    
    print("\n" + "="*60)
    print(" NEXT STEPS")
    print("="*60)
    
    if not results['react_engine']:
        print("\n❌ CRITICAL: React engine fixes not found!")
        print("   Make sure react_engine.py was updated with Session 25 fixes")
        return False
    
    if not results['cache']:
        print("\n⚠️ BEFORE TESTING: Run CLEAR_PYTHON_CACHE.bat")
        print("   This ensures Python loads the new react_engine.py code")
        return False
    
    if not results['imports']:
        print("\n❌ CRITICAL: Cannot import modules!")
        print("   Check that _select_fallback_tool method exists in ReactEngine")
        return False
    
    if not results['ollama']:
        print("\n✅ Ollama not running, but that's OK!")
        print("   Session 25 fixes include fallback tool selection")
        print("   You can still run tests - system will use keyword-based tools")
        print("\n   Optional: Start Ollama for full LLM-driven investigation:")
        print("   > ollama serve")
    
    print("\n✅ ALL CHECKS PASSED - READY FOR TESTING")
    print("\nFirst test to run:")
    print("  Problem: 'Check server CPU usage'")
    print("  Expected: Uses check_server_metrics tool")
    print("  Expected Result: Specific CPU percentage (not template text)")
    
    return True


if __name__ == "__main__":
    success = run_diagnostics()
    sys.exit(0 if success else 1)
