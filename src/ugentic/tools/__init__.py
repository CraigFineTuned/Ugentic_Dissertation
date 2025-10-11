"""
UGENTIC Diagnostic Tools
Domain-specific tools for ReAct agents
"""

from .infrastructure_tools import (
    check_server_metrics,
    check_server_logs,
    check_service_status,
    check_disk_space,
    check_process_list,
    measure_server_response_time,
    get_system_uptime,
    check_backup_status
)

from .network_tools import (
    check_network_bandwidth,
    ping_test,
    check_dns_resolution,
    traceroute,
    measure_network_latency,
    check_firewall_rules,
    get_network_utilization
)

from .application_tools import (
    query_app_logs,
    check_app_response_time,
    get_user_session_data,
    check_app_availability,
    get_app_error_rate,
    check_app_database_performance,
    check_client_metrics
)

from .support_tools import (
    get_user_profile,
    check_user_permissions,
    reset_user_password,
    unlock_user_account,
    check_printer_status,
    verify_email_config,
    test_remote_access,
    check_software_installation,
    get_recent_tickets
)

from .manager_tools import (
    get_technician_workload,
    get_team_availability,
    check_skill_match,
    get_open_tickets,
    get_sla_status,
    get_escalation_history,
    search_knowledge_base
)

__all__ = [
    # Infrastructure
    'check_server_metrics',
    'check_server_logs',
    'check_service_status',
    'check_disk_space',
    'check_process_list',
    'measure_server_response_time',
    'get_system_uptime',
    'check_backup_status',
    # Network
    'check_network_bandwidth',
    'ping_test',
    'check_dns_resolution',
    'traceroute',
    'measure_network_latency',
    'check_firewall_rules',
    'get_network_utilization',
    # Application
    'query_app_logs',
    'check_app_response_time',
    'get_user_session_data',
    'check_app_availability',
    'get_app_error_rate',
    'check_app_database_performance',
    'check_client_metrics',
    # IT Support
    'get_user_profile',
    'check_user_permissions',
    'reset_user_password',
    'unlock_user_account',
    'check_printer_status',
    'verify_email_config',
    'test_remote_access',
    'check_software_installation',
    'get_recent_tickets',
    # Service Desk Manager
    'get_technician_workload',
    'get_team_availability',
    'check_skill_match',
    'get_open_tickets',
    'get_sla_status',
    'get_escalation_history',
    'search_knowledge_base',
]
