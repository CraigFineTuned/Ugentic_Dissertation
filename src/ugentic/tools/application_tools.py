"""
Application Diagnostic Tools
Application monitoring, logs, and performance
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any, List


def query_app_logs(app_name: str, user_id: str = None, hours: int = 1) -> Dict[str, Any]:
    """
    Gets application logs for specific user/timeframe
    """
    # Simulate log entries
    log_levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
    num_entries = random.randint(10, 100)
    
    errors = []
    warnings = []
    crashes = []
    
    for i in range(num_entries):
        level = random.choice(log_levels)
        entry = {
            "timestamp": (datetime.now() - timedelta(minutes=random.randint(0, hours * 60))).isoformat(),
            "level": level,
            "message": f"{app_name} log entry {i+1}",
            "user_id": user_id
        }
        
        if level == "ERROR" or level == "CRITICAL":
            errors.append(entry)
        elif level == "WARNING":
            warnings.append(entry)
        
        # Simulate some crashes
        if random.random() < 0.1:
            crashes.append(entry)
    
    return {
        "application": app_name,
        "user_id": user_id,
        "timeframe_hours": hours,
        "total_entries": num_entries,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "crash_count": len(crashes),
        "errors": errors[:10],  # First 10
        "recent_errors": errors[:5] if errors else []
    }


def check_app_response_time(app_name: str, test_operation: str = "login") -> Dict[str, Any]:
    """
    Measures application response time
    """
    import time
    
    # Simulate multiple tests
    response_times = []
    successes = 0
    
    for _ in range(5):
        start = time.time()
        time.sleep(random.uniform(0.1, 2))  # Simulate operation
        duration = (time.time() - start) * 1000  # ms
        response_times.append(duration)
        if random.random() > 0.1:  # 90% success rate
            successes += 1
    
    avg_response = sum(response_times) / len(response_times)
    
    # Classify status
    status = "normal"
    if avg_response > 5000:
        status = "very_slow"
    elif avg_response > 2000:
        status = "slow"
    
    return {
        "application": app_name,
        "operation": test_operation,
        "avg_response_ms": round(avg_response, 2),
        "max_response_ms": round(max(response_times), 2),
        "min_response_ms": round(min(response_times), 2),
        "success_rate": round(successes / 5, 2),
        "status": status
    }


def get_user_session_data(user_id: str, app_name: str = None) -> Dict[str, Any]:
    """
    Gets active session information for user
    """
    return {
        "user_id": user_id,
        "application": app_name,
        "active_sessions": random.randint(1, 3),
        "session_duration_minutes": random.randint(5, 240),
        "last_activity": datetime.now().isoformat(),
        "ip_address": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
        "device_type": random.choice(["desktop", "laptop", "mobile"]),
        "logged_in": True
    }


def check_app_availability(app_name: str) -> Dict[str, Any]:
    """
    Checks if application is available and responding
    """
    # Simulate availability check
    available = random.random() > 0.1  # 90% uptime
    
    return {
        "application": app_name,
        "available": available,
        "status": "online" if available else "offline",
        "response_time_ms": round(random.uniform(100, 500), 2) if available else None,
        "uptime_percent": round(random.uniform(95, 99.9), 2),
        "last_outage": "2025-10-01T14:30:00" if not available else None
    }


def get_app_error_rate(app_name: str, hours: int = 24) -> Dict[str, Any]:
    """
    Gets application error rate over timeframe
    """
    total_requests = random.randint(10000, 100000)
    error_count = random.randint(10, 500)
    error_rate = (error_count / total_requests) * 100
    
    status = "healthy" if error_rate < 1 else "warning" if error_rate < 5 else "critical"
    
    return {
        "application": app_name,
        "timeframe_hours": hours,
        "total_requests": total_requests,
        "error_count": error_count,
        "error_rate_percent": round(error_rate, 3),
        "status": status,
        "top_errors": [
            {"code": "500", "count": random.randint(10, 100)},
            {"code": "404", "count": random.randint(5, 50)},
            {"code": "503", "count": random.randint(1, 20)}
        ]
    }


def check_app_database_performance(app_name: str) -> Dict[str, Any]:
    """
    Checks database performance for application
    """
    avg_query_time = random.uniform(10, 5000)  # ms
    
    status = "good" if avg_query_time < 100 else "degraded" if avg_query_time < 1000 else "poor"
    
    return {
        "application": app_name,
        "avg_query_time_ms": round(avg_query_time, 2),
        "slow_queries": random.randint(0, 50),
        "active_connections": random.randint(5, 95),
        "max_connections": 100,
        "connection_percent": random.randint(5, 95),
        "status": status
    }


def check_client_metrics(user_id: str) -> Dict[str, Any]:
    """
    Gets metrics from user's client machine
    """
    memory_total_gb = 16
    memory_used_gb = random.uniform(4, 15)
    memory_percent = (memory_used_gb / memory_total_gb) * 100
    
    return {
        "user_id": user_id,
        "machine_name": f"PC-{user_id[-4:].upper()}",
        "cpu_usage_percent": round(random.uniform(10, 90), 2),
        "memory_total_gb": memory_total_gb,
        "memory_used_gb": round(memory_used_gb, 2),
        "memory_available_gb": round(memory_total_gb - memory_used_gb, 2),
        "memory_used_percent": round(memory_percent, 2),
        "disk_space_gb": round(random.uniform(50, 500), 2),
        "running_processes": random.randint(80, 200),
        "top_memory_consumers": [
            {"name": "chrome.exe", "memory_mb": random.randint(500, 2000)},
            {"name": "outlook.exe", "memory_mb": random.randint(300, 1000)},
            {"name": "teams.exe", "memory_mb": random.randint(200, 800)}
        ]
    }
