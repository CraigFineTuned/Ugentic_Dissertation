"""
Infrastructure Diagnostic Tools
Server, system, and infrastructure monitoring
"""

import psutil
import random
from datetime import datetime
from typing import Dict, Any


def check_server_metrics(server_name: str = "localhost") -> Dict[str, Any]:
    """
    Checks actual server CPU, memory, disk usage
    Returns real-time performance data
    """
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Classify status
        status = "normal"
        if cpu_percent > 80 or memory.percent > 85:
            status = "critical"
        elif cpu_percent > 60 or memory.percent > 70:
            status = "degraded"
        
        return {
            "server": server_name,
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": round(cpu_percent, 2),
            "memory_percent": round(memory.percent, 2),
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "memory_total_gb": round(memory.total / (1024**3), 2),
            "disk_percent": round(disk.percent, 2),
            "disk_free_gb": round(disk.free / (1024**3), 2),
            "status": status
        }
    except Exception as e:
        return {
            "server": server_name,
            "error": str(e),
            "status": "unknown"
        }


def check_server_logs(server_name: str = "localhost", hours: int = 1) -> Dict[str, Any]:
    """
    Reads server error logs for specified timeframe
    Returns error summaries
    """
    # Simulated for now - would connect to actual log system
    error_types = [
        "OutOfMemoryError",
        "DiskSpaceWarning",
        "ServiceTimeout",
        "ConnectionRefused",
        "DatabaseConnectionError"
    ]
    
    # Simulate some errors
    num_errors = random.randint(0, 10)
    errors = []
    
    for i in range(num_errors):
        errors.append({
            "timestamp": datetime.now().isoformat(),
            "error_type": random.choice(error_types),
            "severity": random.choice(["WARNING", "ERROR", "CRITICAL"]),
            "message": f"Error message {i+1}"
        })
    
    return {
        "server": server_name,
        "timeframe_hours": hours,
        "total_errors": num_errors,
        "errors": errors,
        "top_error": error_types[0] if errors else None
    }


def check_service_status(server_name: str = "localhost", service_name: str = "unknown") -> Dict[str, Any]:
    """
    Checks if specific service is running
    Returns service state and uptime
    """
    # Check if service process exists (simplified)
    running_services = {
        "apache": True,
        "mysql": True,
        "nginx": True,
        "docker": True,
        "postgresql": False,  # Simulate stopped service
    }
    
    is_running = running_services.get(service_name.lower(), True)
    
    return {
        "server": server_name,
        "service": service_name,
        "running": is_running,
        "status": "active" if is_running else "stopped",
        "uptime_hours": random.randint(1, 720) if is_running else 0,
        "restarts_today": random.randint(0, 3)
    }


def check_disk_space(server_name: str = "localhost") -> Dict[str, Any]:
    """
    Checks disk space on all mounted drives
    """
    try:
        partitions = psutil.disk_partitions()
        disk_info = []
        
        for partition in partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                disk_info.append({
                    "device": partition.device,
                    "mountpoint": partition.mountpoint,
                    "total_gb": round(usage.total / (1024**3), 2),
                    "used_gb": round(usage.used / (1024**3), 2),
                    "free_gb": round(usage.free / (1024**3), 2),
                    "percent": round(usage.percent, 2),
                    "status": "critical" if usage.percent > 90 else "warning" if usage.percent > 80 else "normal"
                })
            except PermissionError:
                continue
        
        return {
            "server": server_name,
            "disks": disk_info,
            "critical_disks": [d for d in disk_info if d["status"] == "critical"]
        }
    except Exception as e:
        return {
            "server": server_name,
            "error": str(e)
        }


def check_process_list(server_name: str = "localhost", top_n: int = 10) -> Dict[str, Any]:
    """
    Gets list of running processes, sorted by resource usage
    """
    try:
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu_percent": proc.info['cpu_percent'],
                    "memory_percent": round(proc.info['memory_percent'], 2)
                })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
        
        return {
            "server": server_name,
            "total_processes": len(processes),
            "top_processes": processes[:top_n],
            "high_cpu_count": len([p for p in processes if (p['cpu_percent'] or 0) > 50])
        }
    except Exception as e:
        return {
            "server": server_name,
            "error": str(e)
        }


def measure_server_response_time(server_name: str = "localhost") -> Dict[str, Any]:
    """
    Measures server response time for basic operations
    """
    import time
    
    # Simulate response time measurement
    start = time.time()
    time.sleep(random.uniform(0.01, 0.5))  # Simulate operation
    duration = (time.time() - start) * 1000  # ms
    
    status = "normal"
    if duration > 500:
        status = "slow"
    elif duration > 1000:
        status = "very_slow"
    
    return {
        "server": server_name,
        "response_time_ms": round(duration, 2),
        "status": status,
        "timestamp": datetime.now().isoformat()
    }


def get_system_uptime(server_name: str = "localhost") -> Dict[str, Any]:
    """
    Gets system uptime
    """
    try:
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        uptime = datetime.now() - boot_time
        
        return {
            "server": server_name,
            "boot_time": boot_time.isoformat(),
            "uptime_days": uptime.days,
            "uptime_hours": uptime.seconds // 3600,
            "uptime_minutes": (uptime.seconds % 3600) // 60
        }
    except Exception as e:
        return {
            "server": server_name,
            "error": str(e)
        }


def check_backup_status(server_name: str = "localhost") -> Dict[str, Any]:
    """
    Checks backup status and last backup time
    """
    # Simulated - would check actual backup system
    last_backup_hours_ago = random.randint(1, 72)
    status = "ok" if last_backup_hours_ago < 24 else "warning" if last_backup_hours_ago < 48 else "critical"
    
    return {
        "server": server_name,
        "last_backup_hours_ago": last_backup_hours_ago,
        "status": status,
        "backup_size_gb": round(random.uniform(10, 500), 2),
        "next_scheduled": "2025-10-09T02:00:00"
    }
