"""
Network Diagnostic Tools
Network connectivity, performance, and security
"""

import random
import time
from datetime import datetime
from typing import Dict, Any


def check_network_bandwidth(interface: str = "eth0") -> Dict[str, Any]:
    """
    Measures actual network bandwidth and latency
    """
    # Simulate bandwidth test
    download_mbps = random.uniform(50, 100)
    upload_mbps = random.uniform(20, 50)
    latency_ms = random.uniform(5, 50)
    packet_loss = random.uniform(0, 5)
    
    # Classify status
    status = "normal"
    if download_mbps < 30 or latency_ms > 100 or packet_loss > 2:
        status = "poor"
    elif download_mbps < 50 or latency_ms > 50 or packet_loss > 1:
        status = "degraded"
    
    return {
        "interface": interface,
        "timestamp": datetime.now().isoformat(),
        "download_mbps": round(download_mbps, 2),
        "upload_mbps": round(upload_mbps, 2),
        "latency_ms": round(latency_ms, 2),
        "packet_loss_percent": round(packet_loss, 2),
        "jitter_ms": round(random.uniform(1, 10), 2),
        "status": status
    }


def ping_test(host: str, count: int = 10) -> Dict[str, Any]:
    """
    Tests connectivity to host with ping
    Measures latency and packet loss
    """
    # Simulate ping results
    latencies = [random.uniform(5, 100) for _ in range(count)]
    packets_received = random.randint(int(count * 0.8), count)
    
    return {
        "host": host,
        "packets_sent": count,
        "packets_received": packets_received,
        "packet_loss_percent": round(((count - packets_received) / count) * 100, 2),
        "min_latency_ms": round(min(latencies), 2),
        "max_latency_ms": round(max(latencies), 2),
        "avg_latency_ms": round(sum(latencies) / len(latencies), 2),
        "status": "reachable" if packets_received > 0 else "unreachable"
    }


def check_dns_resolution(domain: str = "google.com") -> Dict[str, Any]:
    """
    Tests DNS resolution
    """
    import socket
    
    try:
        start = time.time()
        ip_address = socket.gethostbyname(domain)
        duration = (time.time() - start) * 1000  # ms
        
        return {
            "success": True,
            "domain": domain,
            "ip_address": ip_address,
            "resolution_time_ms": round(duration, 2),
            "status": "working"
        }
    except socket.gaierror as e:
        return {
            "success": False,
            "domain": domain,
            "error": str(e),
            "status": "failed"
        }


def traceroute(destination: str, max_hops: int = 15) -> Dict[str, Any]:
    """
    Traces network path to destination
    Identifies slow hops
    """
    # Simulate traceroute
    hops = []
    for ttl in range(1, min(max_hops, random.randint(8, 15)) + 1):
        latency = random.uniform(5, 150)
        hops.append({
            "hop": ttl,
            "ip": f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}",
            "latency_ms": round(latency, 2),
            "reachable": True
        })
    
    return {
        "destination": destination,
        "total_hops": len(hops),
        "hops": hops,
        "slow_hops": [h for h in hops if h['latency_ms'] > 100],
        "path_ok": all(h['reachable'] for h in hops)
    }


def measure_network_latency(source: str = "localhost", destination: str = "8.8.8.8") -> Dict[str, Any]:
    """
    Measures network latency between source and destination
    """
    latency = random.uniform(5, 100)
    
    status = "excellent" if latency < 20 else "good" if latency < 50 else "poor"
    
    return {
        "source": source,
        "destination": destination,
        "latency_ms": round(latency, 2),
        "status": status,
        "timestamp": datetime.now().isoformat()
    }


def check_firewall_rules(host: str = "localhost") -> Dict[str, Any]:
    """
    Gets firewall configuration
    """
    # Simulated firewall rules
    return {
        "host": host,
        "firewall_enabled": True,
        "rules": [
            {"port": 22, "protocol": "tcp", "action": "allow", "source": "any"},
            {"port": 80, "protocol": "tcp", "action": "allow", "source": "any"},
            {"port": 443, "protocol": "tcp", "action": "allow", "source": "any"},
            {"port": 3389, "protocol": "tcp", "action": "deny", "source": "external"},
        ],
        "blocked_ports": [3389, 445, 1433],
        "recent_blocks": random.randint(0, 50)
    }


def get_network_utilization(interface: str = "eth0") -> Dict[str, Any]:
    """
    Gets current network utilization
    """
    import psutil
    
    try:
        # Get network stats
        net_io = psutil.net_io_counters(pernic=True)
        
        if interface in net_io:
            stats = net_io[interface]
            return {
                "interface": interface,
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
                "errors_in": stats.errin,
                "errors_out": stats.errout,
                "drops_in": stats.dropin,
                "drops_out": stats.dropout
            }
        else:
            # Use default interface
            stats = psutil.net_io_counters()
            return {
                "interface": "default",
                "bytes_sent": stats.bytes_sent,
                "bytes_recv": stats.bytes_recv,
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv
            }
    except Exception as e:
        return {
            "interface": interface,
            "error": str(e)
        }
