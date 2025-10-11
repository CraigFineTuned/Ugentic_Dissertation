"""
Service Desk Manager Diagnostic Tools
Team coordination and management
"""

import random
from datetime import datetime
from typing import Dict, Any, List


def get_technician_workload() -> Dict[str, Any]:
    """
    Gets current workload for all technicians
    """
    technicians = []
    
    for i in range(3):  # 3 technicians
        tech_name = f"Tech_{i+1}"
        open_tickets = random.randint(2, 15)
        technicians.append({
            "name": tech_name,
            "status": random.choice(["available", "busy", "on_break"]),
            "open_tickets": open_tickets,
            "avg_resolution_time_hours": random.uniform(1, 24),
            "specialization": random.choice(["general", "network", "applications"]),
            "workload_level": "high" if open_tickets > 10 else "medium" if open_tickets > 5 else "low"
        })
    
    return {
        "total_technicians": len(technicians),
        "available_technicians": len([t for t in technicians if t["status"] == "available"]),
        "total_open_tickets": sum(t["open_tickets"] for t in technicians),
        "technicians": technicians,
        "team_capacity": random.choice(["available", "moderate", "overloaded"])
    }


def get_team_availability() -> Dict[str, Any]:
    """
    Gets team availability status
    """
    return {
        "timestamp": datetime.now().isoformat(),
        "available_now": random.randint(1, 3),
        "total_team_size": 3,
        "on_break": random.randint(0, 1),
        "in_meeting": random.randint(0, 1),
        "handling_tickets": random.randint(1, 3),
        "shift_coverage": random.choice(["full", "partial", "minimal"]),
        "estimated_wait_time_minutes": random.randint(5, 45)
    }


def check_skill_match(issue_type: str) -> Dict[str, Any]:
    """
    Checks which technician is best suited for issue type
    """
    technicians_by_skill = {
        "network": ["Tech_1", "Tech_3"],
        "application": ["Tech_2", "Tech_3"],
        "hardware": ["Tech_1"],
        "user_account": ["Tech_2", "Tech_3"],
        "general": ["Tech_1", "Tech_2", "Tech_3"]
    }
    
    matched_techs = technicians_by_skill.get(issue_type.lower(), technicians_by_skill["general"])
    
    return {
        "issue_type": issue_type,
        "matched_technicians": matched_techs,
        "best_match": random.choice(matched_techs),
        "match_confidence": random.uniform(0.7, 0.95),
        "estimated_resolution_time_hours": random.uniform(0.5, 4)
    }


def get_open_tickets() -> Dict[str, Any]:
    """
    Gets all open tickets in the queue
    """
    ticket_count = random.randint(5, 25)
    tickets = []
    
    priorities = ["low", "medium", "high", "critical"]
    
    for i in range(ticket_count):
        priority = random.choice(priorities)
        tickets.append({
            "ticket_id": f"TKT-{random.randint(1000, 9999)}",
            "user": f"user_{random.randint(100, 999)}",
            "subject": random.choice([
                "Password reset",
                "Cannot access shared drive",
                "Printer issues",
                "Email problems",
                "VPN not connecting",
                "Application crash",
                "Slow performance"
            ]),
            "priority": priority,
            "status": "open",
            "age_hours": random.uniform(0.5, 48),
            "assigned_to": random.choice(["Tech_1", "Tech_2", "Tech_3", "Unassigned"]),
            "sla_breach_risk": priority in ["high", "critical"] and random.random() > 0.5
        })
    
    # Sort by priority and age
    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    tickets.sort(key=lambda x: (priority_order[x["priority"]], -x["age_hours"]))
    
    return {
        "total_open": ticket_count,
        "critical": len([t for t in tickets if t["priority"] == "critical"]),
        "high": len([t for t in tickets if t["priority"] == "high"]),
        "medium": len([t for t in tickets if t["priority"] == "medium"]),
        "low": len([t for t in tickets if t["priority"] == "low"]),
        "at_risk_of_sla_breach": len([t for t in tickets if t.get("sla_breach_risk")]),
        "unassigned": len([t for t in tickets if t["assigned_to"] == "Unassigned"]),
        "tickets": tickets[:10]  # Top 10 by priority
    }


def get_sla_status(ticket_id: str) -> Dict[str, Any]:
    """
    Gets SLA status for specific ticket
    """
    priority = random.choice(["low", "medium", "high", "critical"])
    sla_hours = {"critical": 2, "high": 4, "medium": 8, "low": 24}[priority]
    age_hours = random.uniform(0, sla_hours * 1.5)
    remaining_hours = max(0, sla_hours - age_hours)
    
    return {
        "ticket_id": ticket_id,
        "priority": priority,
        "sla_target_hours": sla_hours,
        "ticket_age_hours": round(age_hours, 2),
        "remaining_hours": round(remaining_hours, 2),
        "sla_status": "breached" if remaining_hours <= 0 else "at_risk" if remaining_hours < 1 else "ok",
        "percent_time_used": round((age_hours / sla_hours) * 100, 1)
    }


def get_escalation_history() -> Dict[str, Any]:
    """
    Gets recent escalation history
    """
    escalation_count = random.randint(2, 10)
    escalations = []
    
    for i in range(escalation_count):
        escalations.append({
            "ticket_id": f"TKT-{random.randint(1000, 9999)}",
            "escalated_from": "IT Support",
            "escalated_to": random.choice(["Infrastructure", "Network Support", "App Support"]),
            "reason": random.choice([
                "Requires specialist knowledge",
                "Server-level issue",
                "Network infrastructure",
                "Application bug",
                "Performance issue"
            ]),
            "timestamp": datetime.now().isoformat(),
            "resolution_status": random.choice(["pending", "in_progress", "resolved"])
        })
    
    return {
        "total_escalations_today": escalation_count,
        "most_escalated_to": "Infrastructure",
        "common_reasons": [
            "Requires specialist knowledge",
            "Server-level issue"
        ],
        "escalations": escalations[:5]  # Last 5
    }


def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Searches knowledge base for solutions
    """
    # Simulated KB search
    results = []
    
    if random.random() > 0.3:  # 70% find something
        num_results = random.randint(1, 5)
        for i in range(num_results):
            results.append({
                "article_id": f"KB-{random.randint(1000, 9999)}",
                "title": f"Solution for {query}",
                "relevance_score": random.uniform(0.6, 0.95),
                "solution_summary": f"To resolve {query}, follow these steps...",
                "success_rate": random.uniform(0.7, 0.98),
                "last_updated": "2025-09-15"
            })
    
    return {
        "query": query,
        "results_found": len(results),
        "top_result": results[0] if results else None,
        "all_results": results
    }
