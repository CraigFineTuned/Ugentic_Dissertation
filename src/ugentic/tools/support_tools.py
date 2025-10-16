"""
IT Support Diagnostic Tools
Front-line user support and basic troubleshooting

Session 22 Fix: 
- ask_questions now connects to RAG system for real answers
- All tools now return DETERMINISTIC data (no randomization)
- Added logging for debugging and validation
"""

import hashlib
from datetime import datetime
from typing import Dict, Any, Optional

# Global RAG system reference (set by initialize_support_tools)
_RAG_SYSTEM = None
_DEBUG_MODE = True  # Enable to see RAG queries

def set_rag_system(rag_system):
    """Set the RAG system for ask_questions tool to use"""
    global _RAG_SYSTEM
    _RAG_SYSTEM = rag_system

def get_rag_system():
    """Get the current RAG system"""
    return _RAG_SYSTEM

def _hash_user_id(user_id: str) -> int:
    """Generate deterministic integer from user ID"""
    return int(hashlib.md5(user_id.encode()).hexdigest(), 16) % 100

def get_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Gets user profile information
    FIXED Session 22: Now deterministic based on user_id
    """
    hash_val = _hash_user_id(user_id)
    departments = ["IT", "HR", "Finance", "Operations", "Marketing"]
    statuses = ["active", "locked", "disabled"]
    
    # Deterministic based on hash
    dept_idx = hash_val % len(departments)
    status_idx = (hash_val // len(departments)) % len(statuses)
    
    # John Smith specific: locked account (realistic for test scenario)
    if "john" in user_id.lower() and "smith" in user_id.lower():
        account_status = "locked"
    else:
        account_status = statuses[status_idx]
    
    return {
        "user_id": user_id,
        "username": f"user_{user_id}",
        "email": f"{user_id}@company.com",
        "department": departments[dept_idx],
        "account_status": account_status,
        "last_login": "2025-10-16T08:30:00",
        "password_expires_days": 45 + (hash_val % 45),
        "groups": ["Domain Users", "VPN Users"]
    }


def check_user_permissions(user_id: str, resource: str) -> Dict[str, Any]:
    """
    Checks user permissions for a specific resource
    FIXED Session 22: Now deterministic based on user_id and resource
    """
    hash_val = _hash_user_id(user_id)
    
    # John Smith specific: no printer access in Building A (realistic for test)
    if "john" in user_id.lower() and "smith" in user_id.lower():
        if "printer" in resource.lower() and "building a" in resource.lower():
            has_access = False
        else:
            has_access = hash_val % 2 == 0
    else:
        has_access = hash_val % 3 == 0
    
    return {
        "user_id": user_id,
        "resource": resource,
        "has_access": has_access,
        "permission_level": ["read", "write", "admin"][hash_val % 3] if has_access else None,
        "granted_by": "IT Manager" if has_access else None,
        "expires": "2025-12-31" if has_access else None
    }


def reset_user_password(user_id: str) -> Dict[str, Any]:
    """
    Resets user password
    FIXED Session 22: Deterministic 85% success rate
    """
    hash_val = _hash_user_id(user_id)
    success = hash_val % 100 < 85  # 85% success rate
    
    return {
        "user_id": user_id,
        "success": success,
        "temporary_password": "TempPass@2025!" if success else None,
        "must_change_on_login": True if success else None,
        "error": None if success else "Password policy violation",
        "timestamp": datetime.now().isoformat()
    }


def unlock_user_account(user_id: str) -> Dict[str, Any]:
    """
    Unlocks user account
    FIXED Session 22: Deterministic 90% success rate
    """
    hash_val = _hash_user_id(user_id)
    success = hash_val % 100 < 90  # 90% success rate
    
    return {
        "user_id": user_id,
        "success": success,
        "previous_status": "locked",
        "new_status": "active" if success else "locked",
        "locked_reason": "Too many failed login attempts",
        "unlocked_by": "IT Support",
        "timestamp": datetime.now().isoformat()
    }


def check_printer_status(printer_name: str) -> Dict[str, Any]:
    """
    Checks printer status
    FIXED Session 22: Deterministic based on printer name
    """
    hash_val = int(hashlib.md5(printer_name.encode()).hexdigest(), 16) % 100
    statuses = ["online", "offline", "paper_jam"]
    
    # Building A printers mostly offline (realistic for test scenario)
    if "building a" in printer_name.lower():
        status = statuses[hash_val % 3]  # Mix of statuses
    else:
        status = "online"
    
    return {
        "printer_name": printer_name,
        "status": status,
        "ip_address": f"192.168.1.{100 + (hash_val % 100)}",
        "jobs_in_queue": hash_val % 5,
        "paper_level": f"{80 + (hash_val % 20)}%",
        "toner_level": f"{70 + (hash_val % 30)}%",
        "last_job": "5 minutes ago" if status == "online" else "2 hours ago"
    }


def verify_email_config(user_id: str) -> Dict[str, Any]:
    """
    Verifies email configuration for user
    FIXED Session 22: Deterministic
    """
    hash_val = _hash_user_id(user_id)
    config_ok = hash_val % 100 > 20  # 80% config ok
    
    issues = []
    if not config_ok:
        issue_types = [
            "Incorrect server settings",
            "Authentication failure",
            "Port blocked",
            "SSL certificate issue"
        ]
        issues = [issue_types[hash_val % len(issue_types)]]
    
    return {
        "user_id": user_id,
        "email": f"{user_id}@company.com",
        "configuration_ok": config_ok,
        "server": "mail.company.com",
        "port": 587,
        "ssl_enabled": True,
        "authentication": "working" if config_ok else "failed",
        "issues": issues if issues else None,
        "last_sync": datetime.now().isoformat() if config_ok else "Failed"
    }


def test_remote_access(user_id: str) -> Dict[str, Any]:
    """
    Tests remote access (VPN) for user
    FIXED Session 22: Deterministic 80% success
    """
    hash_val = _hash_user_id(user_id)
    can_connect = hash_val % 100 > 20  # 80% success
    
    return {
        "user_id": user_id,
        "vpn_status": "connected" if can_connect else "connection_failed",
        "can_access": can_connect,
        "ip_address": f"10.0.{hash_val % 255}.{(hash_val * 3) % 255}" if can_connect else None,
        "connection_time": datetime.now().isoformat() if can_connect else None,
        "bandwidth": f"{50 + (hash_val % 50)} Mbps" if can_connect else None,
        "error": None if can_connect else ["Authentication failed", "VPN server unreachable", "Certificate expired"][hash_val % 3]
    }


def check_software_installation(user_id: str, software_name: str) -> Dict[str, Any]:
    """
    Checks if software is installed on user's machine
    FIXED Session 22: Deterministic
    """
    hash_val = _hash_user_id(user_id)
    installed = hash_val % 2 == 0
    
    return {
        "user_id": user_id,
        "software": software_name,
        "installed": installed,
        "version": f"{(hash_val % 10) + 1}.{hash_val % 9}.{hash_val % 99}" if installed else None,
        "install_date": "2025-06-15" if installed else None,
        "license_valid": (hash_val % 3) != 0 if installed else None,
        "needs_update": (hash_val % 4) == 0 if installed else None
    }


def get_recent_tickets(user_id: str = None) -> Dict[str, Any]:
    """
    Gets recent support tickets for user or all users
    FIXED Session 22: Deterministic
    """
    if user_id:
        hash_val = _hash_user_id(user_id)
        ticket_count = 2 + (hash_val % 3)
    else:
        ticket_count = 5
    
    tickets = []
    subjects = [
        "Password reset needed",
        "Cannot access shared drive",
        "Printer not working",
        "Email not syncing",
        "VPN connection issues"
    ]
    
    for i in range(ticket_count):
        tickets.append({
            "ticket_id": f"TKT-{1000 + i}",
            "user_id": user_id or f"user_{i}",
            "subject": subjects[i % len(subjects)],
            "status": ["open", "in_progress", "resolved"][i % 3],
            "priority": ["low", "medium", "high"][i % 3],
            "created": datetime.now().isoformat(),
            "assigned_to": "IT Support"
        })
    
    return {
        "user_id": user_id,
        "total_tickets": ticket_count,
        "open_tickets": len([t for t in tickets if t["status"] == "open"]),
        "tickets": tickets
    }


def ask_questions(questions: list, user_id: str = "") -> Dict[str, Any]:
    """
    Asks questions to gather additional information for troubleshooting.
    
    FIXED Session 22: Now uses RAG system to retrieve real answers from knowledge base
    instead of simulating responses with pattern matching.
    
    Session 23 FIX: Handle both string and list inputs (LLM may generate string)
    
    Args:
        questions: List of questions to ask (strings), or a single question string
        user_id: Optional user identifier for context
        
    Returns:
        Dictionary with responses retrieved from knowledge base or fallback answers
    """
    # FIXED Session 23: Handle LLM potentially sending string instead of list
    if isinstance(questions, str):
        # If it's a single string, treat it as one question (not individual characters)
        questions = [questions]
    
    # Ensure it's a list
    if not isinstance(questions, list):
        questions = [str(questions)]
    
    # Filter out empty strings and single characters that likely came from character iteration
    # A valid question should be at least 5 characters (accounting for "why?", etc.)
    questions = [q for q in questions if isinstance(q, str) and len(q.strip()) > 3]
    
    # If no valid questions, return minimal response
    if not questions:
        return {
            "success": True,
            "tool": "ask_questions",
            "domain": "user_support",
            "data": {
                "user_id": user_id if user_id else "general_inquiry",
                "questions_asked": 0,
                "responses": [],
                "timestamp": datetime.now().isoformat(),
                "context_gathered": False,
                "rag_enabled": get_rag_system() is not None,
                "note": "No valid questions provided"
            }
        }
    
    responses = []
    rag_system = get_rag_system()
    
    for question in questions:
        # FIXED Session 22: Try to retrieve real answer from RAG system
        if rag_system:
            try:
                # Query the RAG system for relevant information
                retrieved_chunks = rag_system.retrieve(question, top_k=1)
                
                if _DEBUG_MODE:
                    print(f"\n   [DEBUG] ask_questions querying RAG for: '{question[:60]}...'")
                
                if retrieved_chunks and len(retrieved_chunks) > 0:
                    # Use RAG-retrieved content
                    chunk = retrieved_chunks[0]
                    answer = chunk['chunk_text'][:300]
                    source = f"knowledge_base"
                    confidence = "high" if chunk['similarity'] > 0.6 else "medium"
                    
                    if _DEBUG_MODE:
                        print(f"   [DEBUG] RAG returned match (similarity: {chunk['similarity']:.2f})")
                else:
                    # No good match in RAG, fall back to fallback logic
                    answer, source, confidence = _get_fallback_answer(question)
                    if _DEBUG_MODE:
                        print(f"   [DEBUG] RAG returned no match, using fallback")
            except Exception as e:
                # RAG system error, fall back to template logic
                answer, source, confidence = _get_fallback_answer(question)
                if _DEBUG_MODE:
                    print(f"   [DEBUG] RAG error: {str(e)}, using fallback")
        else:
            # No RAG system available, use fallback
            answer, source, confidence = _get_fallback_answer(question)
            if _DEBUG_MODE:
                print(f"   [DEBUG] No RAG system available, using fallback")
        
        responses.append({
            "question": question,
            "answer": answer,
            "confidence": confidence,
            "source": source
        })
    
    return {
        "success": True,
        "tool": "ask_questions",
        "domain": "user_support",
        "data": {
            "user_id": user_id if user_id else "general_inquiry",
            "questions_asked": len(questions),
            "responses": responses,
            "timestamp": datetime.now().isoformat(),
            "context_gathered": True,
            "rag_enabled": rag_system is not None
        }
    }


def _get_fallback_answer(question: str) -> tuple:
    """
    Fallback function to generate answers when RAG is not available.
    Used only when RAG system is not initialized or fails.
    
    Returns:
        Tuple of (answer, source, confidence)
    """
    q_lower = question.lower()
    
    # Pattern matching for common IT support questions (FALLBACK ONLY)
    if "train" in q_lower or "storage" in q_lower or "file" in q_lower:
        answer = "Users have been trained on file storage best practices in Q3 2024. However, compliance has been inconsistent with approximately 60% adherence."
        source = "fallback_kb"
        confidence = "medium"
    elif "application" in q_lower or "app" in q_lower or "software" in q_lower:
        answer = "Recent application updates include database backup system (weekly), email archiving system (monthly), and temporary project files accumulating in shared drives."
        source = "fallback_kb"
        confidence = "medium"
    elif "printer" in q_lower or "print" in q_lower:
        answer = "Printer access is controlled through group policies. Users in Building A require explicit permission grants through IT Manager. Check if user is in 'Printer_Access_BuildingA' group."
        source = "fallback_kb"
        confidence = "medium"
    elif "access" in q_lower or "permission" in q_lower:
        answer = "Access permissions are managed through Active Directory groups. Verify user group memberships and resource-specific access control lists. Escalate to IT Manager if permissions need adjustment."
        source = "fallback_kb"
        confidence = "medium"
    elif "when" in q_lower or "how long" in q_lower:
        answer = "This issue started approximately 2-3 weeks ago based on monitoring alerts. Disk usage was at 65% last month, now at 86-90%."
        source = "fallback_kb"
        confidence = "medium"
    elif "user" in q_lower or "who" in q_lower or "which" in q_lower:
        answer = "Multiple departments affected, primarily IT (backups) and Operations (project files). No single user responsible."
        source = "fallback_kb"
        confidence = "medium"
    else:
        # Generic answer for unmatched questions
        answer = f"Insufficient information to answer this question. Recommend consulting IT Support documentation or contacting the IT Manager for guidance on: {question[:100]}"
        source = "fallback_generic"
        confidence = "low"
    
    return answer, source, confidence
