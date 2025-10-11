"""
IT Support Diagnostic Tools
Front-line user support and basic troubleshooting
"""

import random
from datetime import datetime
from typing import Dict, Any


def get_user_profile(user_id: str) -> Dict[str, Any]:
    """
    Gets user profile information
    """
    return {
        "user_id": user_id,
        "username": f"user_{user_id}",
        "email": f"{user_id}@company.com",
        "department": random.choice(["IT", "HR", "Finance", "Operations", "Marketing"]),
        "account_status": random.choice(["active", "locked", "disabled"]),
        "last_login": datetime.now().isoformat(),
        "password_expires_days": random.randint(1, 90),
        "groups": ["Domain Users", "VPN Users"]
    }


def check_user_permissions(user_id: str, resource: str) -> Dict[str, Any]:
    """
    Checks user permissions for a specific resource
    """
    has_access = random.choice([True, False])
    
    return {
        "user_id": user_id,
        "resource": resource,
        "has_access": has_access,
        "permission_level": random.choice(["read", "write", "admin"]) if has_access else None,
        "granted_by": "IT Manager" if has_access else None,
        "expires": "2025-12-31" if has_access else None
    }


def reset_user_password(user_id: str) -> Dict[str, Any]:
    """
    Resets user password
    """
    success = random.random() > 0.1  # 90% success rate
    
    return {
        "user_id": user_id,
        "success": success,
        "temporary_password": "TempPass123!" if success else None,
        "must_change_on_login": True if success else None,
        "error": None if success else "Password policy violation",
        "timestamp": datetime.now().isoformat()
    }


def unlock_user_account(user_id: str) -> Dict[str, Any]:
    """
    Unlocks user account
    """
    success = random.random() > 0.05  # 95% success rate
    
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
    """
    status = random.choice(["online", "offline", "error", "paper_jam", "low_toner"])
    
    return {
        "printer_name": printer_name,
        "status": status,
        "ip_address": f"192.168.1.{random.randint(100, 200)}",
        "jobs_in_queue": random.randint(0, 10),
        "paper_level": f"{random.randint(0, 100)}%",
        "toner_level": f"{random.randint(10, 100)}%",
        "last_job": "5 minutes ago" if status == "online" else "2 hours ago"
    }


def verify_email_config(user_id: str) -> Dict[str, Any]:
    """
    Verifies email configuration for user
    """
    config_ok = random.random() > 0.2  # 80% config ok
    
    issues = []
    if not config_ok:
        issues = random.sample([
            "Incorrect server settings",
            "Authentication failure",
            "Port blocked",
            "SSL certificate issue"
        ], random.randint(1, 2))
    
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
    """
    can_connect = random.random() > 0.15  # 85% success rate
    
    return {
        "user_id": user_id,
        "vpn_status": "connected" if can_connect else "connection_failed",
        "can_access": can_connect,
        "ip_address": f"10.0.{random.randint(1, 255)}.{random.randint(1, 255)}" if can_connect else None,
        "connection_time": datetime.now().isoformat() if can_connect else None,
        "bandwidth": f"{random.randint(10, 100)} Mbps" if can_connect else None,
        "error": None if can_connect else random.choice([
            "Authentication failed",
            "VPN server unreachable",
            "Certificate expired",
            "Too many active connections"
        ])
    }


def check_software_installation(user_id: str, software_name: str) -> Dict[str, Any]:
    """
    Checks if software is installed on user's machine
    """
    installed = random.choice([True, False])
    
    return {
        "user_id": user_id,
        "software": software_name,
        "installed": installed,
        "version": f"{random.randint(1, 10)}.{random.randint(0, 9)}.{random.randint(0, 99)}" if installed else None,
        "install_date": "2025-06-15" if installed else None,
        "license_valid": random.choice([True, False]) if installed else None,
        "needs_update": random.choice([True, False]) if installed else None
    }


def get_recent_tickets(user_id: str = None) -> Dict[str, Any]:
    """
    Gets recent support tickets for user or all users
    """
    ticket_count = random.randint(1, 10)
    tickets = []
    
    for i in range(ticket_count):
        tickets.append({
            "ticket_id": f"TKT-{random.randint(1000, 9999)}",
            "user_id": user_id or f"user_{random.randint(100, 999)}",
            "subject": random.choice([
                "Password reset needed",
                "Cannot access shared drive",
                "Printer not working",
                "Email not syncing",
                "VPN connection issues"
            ]),
            "status": random.choice(["open", "in_progress", "resolved", "closed"]),
            "priority": random.choice(["low", "medium", "high"]),
            "created": datetime.now().isoformat(),
            "assigned_to": "IT Support"
        })
    
    return {
        "user_id": user_id,
        "total_tickets": ticket_count,
        "open_tickets": len([t for t in tickets if t["status"] == "open"]),
        "tickets": tickets
    }
