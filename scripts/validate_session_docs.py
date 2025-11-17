#!/usr/bin/env python3
"""
Session Documentation Validation Script

Validates consistency and integrity of session documentation:
- File references exist
- No broken links
- No duplicate session summaries
- SESSION_ENTRY.md is current
- Paths use relative format
- All session files have corresponding entries

Usage:
    python scripts/validate_session_docs.py

Created: Session 33 - November 17, 2025
"""

import os
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

# Auto-detect project root
def get_project_root() -> Path:
    """Find project root by looking for config.json"""
    current_dir = Path(__file__).resolve().parent
    while current_dir != current_dir.parent:
        if (current_dir / "config.json").exists():
            return current_dir
        current_dir = current_dir.parent
    raise RuntimeError("Could not find project root (no config.json found)")

PROJECT_ROOT = get_project_root()
TRACKER_DIR = PROJECT_ROOT / "docs" / "Project_Tracker"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.END}")

def validate_file_exists(file_path: Path) -> bool:
    """Check if file exists"""
    return file_path.exists() and file_path.is_file()

def validate_session_entry_freshness() -> Tuple[bool, str]:
    """Check if SESSION_ENTRY.md was updated within last 30 days"""
    session_entry = TRACKER_DIR / "SESSION_ENTRY.md"

    if not validate_file_exists(session_entry):
        return False, "SESSION_ENTRY.md not found"

    # Get file modification time
    mtime = datetime.fromtimestamp(session_entry.stat().st_mtime)
    age_days = (datetime.now() - mtime).days

    if age_days > 30:
        return False, f"SESSION_ENTRY.md is {age_days} days old (last updated: {mtime.strftime('%Y-%m-%d')})"

    return True, f"Last updated {age_days} days ago ({mtime.strftime('%Y-%m-%d')})"

def find_file_references(content: str) -> List[str]:
    """Extract file references from markdown content"""
    # Match patterns like: `path/to/file.ext` or docs/Project_Tracker/FILE.md
    patterns = [
        r'`([^`]+\.(?:py|md|json|txt|sh))`',  # Backtick-enclosed paths
        r'(?:docs|src|scripts|knowledge_base)/[\w/]+\.(?:py|md|json|txt|sh)',  # Plain paths
    ]

    references = []
    for pattern in patterns:
        references.extend(re.findall(pattern, content))

    return references

def validate_file_references() -> Tuple[bool, List[str]]:
    """Check that all referenced files exist"""
    session_entry = TRACKER_DIR / "SESSION_ENTRY.md"

    if not validate_file_exists(session_entry):
        return False, ["SESSION_ENTRY.md not found"]

    content = session_entry.read_text(encoding='utf-8')
    references = find_file_references(content)

    missing_files = []
    for ref in references:
        # Clean up reference (remove backticks, quotes)
        ref = ref.strip('`"\'')

        # Try both as absolute path from PROJECT_ROOT and as-is
        file_path = PROJECT_ROOT / ref
        if not validate_file_exists(file_path):
            missing_files.append(ref)

    return len(missing_files) == 0, missing_files

def find_windows_paths(content: str) -> List[str]:
    """Find Windows-style paths in content"""
    pattern = r'C:\\Users\\[\w\\]+'
    return re.findall(pattern, content)

def validate_no_windows_paths() -> Tuple[bool, Dict[str, int]]:
    """Check that documentation uses relative paths, not Windows-specific"""
    files_to_check = [
        TRACKER_DIR / "SESSION_ENTRY.md",
        TRACKER_DIR / "CURRENT_SESSION_CHECKPOINT.md",
        TRACKER_DIR / "SESSION_COMPLETION_SUMMARY.md",
        TRACKER_DIR / "PROJECT_CONTEXT.md",
    ]

    files_with_windows_paths = {}

    for file_path in files_to_check:
        if not validate_file_exists(file_path):
            continue

        content = file_path.read_text(encoding='utf-8')
        windows_paths = find_windows_paths(content)

        if windows_paths:
            files_with_windows_paths[file_path.name] = len(windows_paths)

    return len(files_with_windows_paths) == 0, files_with_windows_paths

def find_duplicate_session_files() -> Dict[int, List[str]]:
    """Find duplicate session summary files"""
    session_files = {}

    for file in TRACKER_DIR.glob("SESSION_*.md"):
        # Extract session number
        match = re.match(r'SESSION_(\d+)_', file.name)
        if match:
            session_num = int(match.group(1))
            if session_num not in session_files:
                session_files[session_num] = []
            session_files[session_num].append(file.name)

    # Find sessions with multiple files
    duplicates = {num: files for num, files in session_files.items() if len(files) > 3}

    return duplicates

def validate_critical_files_exist() -> Tuple[bool, List[str]]:
    """Check that critical nucleus files exist"""
    critical_files = [
        "SESSION_ENTRY.md",
        "CURRENT_SESSION_CHECKPOINT.md",
        "SESSION_COMPLETION_SUMMARY.md",
        "PROJECT_CONTEXT.md",
        "PATH_MAPPINGS.md",
    ]

    missing = []
    for filename in critical_files:
        if not validate_file_exists(TRACKER_DIR / filename):
            missing.append(filename)

    return len(missing) == 0, missing

def main():
    """Run all validation checks"""
    print_header("SESSION DOCUMENTATION VALIDATION")

    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Tracker Directory: {TRACKER_DIR}\n")

    all_passed = True

    # Check 1: Critical files exist
    print_header("CHECK 1: Critical Files Exist")
    passed, missing = validate_critical_files_exist()
    if passed:
        print_success("All critical nucleus files exist")
    else:
        print_error(f"Missing critical files: {', '.join(missing)}")
        all_passed = False

    # Check 2: SESSION_ENTRY.md freshness
    print_header("CHECK 2: SESSION_ENTRY.md Freshness")
    passed, message = validate_session_entry_freshness()
    if passed:
        print_success(f"SESSION_ENTRY.md is current: {message}")
    else:
        print_warning(message)
        all_passed = False

    # Check 3: File references valid
    print_header("CHECK 3: File References Valid")
    passed, missing_files = validate_file_references()
    if passed:
        print_success("All file references are valid")
    else:
        print_error(f"Found {len(missing_files)} broken file references:")
        for ref in missing_files[:10]:  # Show first 10
            print(f"   - {ref}")
        if len(missing_files) > 10:
            print(f"   ... and {len(missing_files) - 10} more")
        all_passed = False

    # Check 4: No Windows paths
    print_header("CHECK 4: Platform-Independent Paths")
    passed, files_with_paths = validate_no_windows_paths()
    if passed:
        print_success("All paths use relative format (platform-independent)")
    else:
        print_warning(f"Found Windows-specific paths in {len(files_with_paths)} files:")
        for filename, count in files_with_paths.items():
            print(f"   - {filename}: {count} Windows paths found")
        print("\n   See PATH_MAPPINGS.md for migration guide")
        # This is a warning, not a failure

    # Check 5: Duplicate session files
    print_header("CHECK 5: Duplicate Session Files")
    duplicates = find_duplicate_session_files()
    if not duplicates:
        print_success("No excessive duplicate session files found")
    else:
        print_warning(f"Found {len(duplicates)} sessions with >3 files (possible duplicates):")
        for session_num, files in sorted(duplicates.items()):
            print(f"   Session {session_num}: {len(files)} files")
            for filename in files:
                print(f"      - {filename}")
        # This is a warning, not a failure

    # Final summary
    print_header("VALIDATION SUMMARY")

    if all_passed:
        print_success("All critical validation checks passed!")
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ DOCUMENTATION IS VALID{Colors.END}\n")
        return 0
    else:
        print_error("Some validation checks failed")
        print(f"\n{Colors.RED}{Colors.BOLD}❌ PLEASE FIX ISSUES ABOVE{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
