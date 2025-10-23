"""
UGENTIC Constants and Magic Strings
Centralized definitions for all constants used throughout the system

Best practice: Single source of truth for all magic strings and configuration constants
"""

# Investigation Status Values
class InvestigationStatus:
    """Investigation state constants"""
    ROOT_CAUSE_FOUND = "ROOT_CAUSE_FOUND"
    NEEDS_COLLABORATION = "NEEDS_COLLABORATION"
    RESOLVED = "RESOLVED"
    INVESTIGATION_COMPLETE = "INVESTIGATION_COMPLETE"
    UBUNTU_COLLABORATION_COMPLETE = "UBUNTU_COLLABORATION_COMPLETE"
    ESCALATE_TO_HUMAN = "ESCALATE_TO_HUMAN"
    NEEDS_COLLABORATION_DETAIL = "NEEDS_COLLABORATION"
    INVESTIGATING = "INVESTIGATING"


# Agent Names (must match agent initialization)
class AgentNames:
    """Canonical agent names"""
    IT_MANAGER = "IT Manager"
    SERVICE_DESK_MANAGER = "Service Desk Manager"
    IT_SUPPORT = "IT Support"
    APP_SUPPORT = "App Support"
    NETWORK_SUPPORT = "Network Support"
    INFRASTRUCTURE = "Infrastructure"
    
    @classmethod
    def all_names(cls):
        """Get all agent names as list"""
        return [
            cls.IT_MANAGER,
            cls.SERVICE_DESK_MANAGER,
            cls.IT_SUPPORT,
            cls.APP_SUPPORT,
            cls.NETWORK_SUPPORT,
            cls.INFRASTRUCTURE,
        ]
    
    @classmethod
    def specialist_agents(cls):
        """Get specialist agent names (not managers)"""
        return [
            cls.IT_SUPPORT,
            cls.APP_SUPPORT,
            cls.NETWORK_SUPPORT,
            cls.INFRASTRUCTURE,
        ]


# Agent Types
class AgentTypes:
    """Agent role types"""
    MANAGER = "Manager"
    OPERATIONAL = "Operational"
    SPECIALIST = "Specialist"
    ORCHESTRATOR = "Orchestrator"


# Reflection Status Values
class ReflectionStatus:
    """Reflection evaluation constants"""
    HYPOTHESIS_CONFIRMED = "hypothesis_confirmed"
    HYPOTHESIS_REFUTED = "hypothesis_refuted"
    ROOT_CAUSE_FOUND = "root_cause_found"
    NEEDS_COLLABORATION = "needs_collaboration"


# LLM Model Names (from config)
class ModelNames:
    """LLM model names (keep in sync with config.json)"""
    DEFAULT_REASONING = "deepseek-v3.1:671b-cloud"
    DEFAULT_FAST = "gemma3n:e4b"
    DEFAULT_REASONING_SPECIALIST = "deepseek-r1:7b"
    DEFAULT_MULTILINGUAL = "granite4:tiny-h"
    DEFAULT_EMBEDDING = "embeddinggemma:latest"


# Tool Categories
class ToolCategories:
    """Tool organization categories"""
    INFRASTRUCTURE = "infrastructure"
    NETWORK = "network"
    APPLICATION = "application"
    SUPPORT = "support"
    MANAGER = "manager"


# Infrastructure Tools
class InfrastructureTools:
    """Infrastructure domain tools"""
    CHECK_SERVER_METRICS = "check_server_metrics"
    CHECK_SERVER_LOGS = "check_server_logs"
    CHECK_SERVICE_STATUS = "check_service_status"
    CHECK_DISK_SPACE = "check_disk_space"
    CHECK_PROCESS_LIST = "check_process_list"
    MEASURE_SERVER_RESPONSE_TIME = "measure_server_response_time"
    GET_SYSTEM_UPTIME = "get_system_uptime"
    CHECK_BACKUP_STATUS = "check_backup_status"


# Network Tools
class NetworkTools:
    """Network domain tools"""
    CHECK_NETWORK_BANDWIDTH = "check_network_bandwidth"
    PING_TEST = "ping_test"
    CHECK_DNS_RESOLUTION = "check_dns_resolution"
    TRACEROUTE = "traceroute"
    MEASURE_NETWORK_LATENCY = "measure_network_latency"
    CHECK_FIREWALL_RULES = "check_firewall_rules"
    GET_NETWORK_UTILIZATION = "get_network_utilization"


# Application Tools
class ApplicationTools:
    """Application domain tools"""
    QUERY_APP_LOGS = "query_app_logs"
    CHECK_APP_RESPONSE_TIME = "check_app_response_time"
    GET_USER_SESSION_DATA = "get_user_session_data"
    CHECK_APP_AVAILABILITY = "check_app_availability"
    GET_APP_ERROR_RATE = "get_app_error_rate"
    CHECK_APP_DATABASE_PERFORMANCE = "check_app_database_performance"
    CHECK_CLIENT_METRICS = "check_client_metrics"


# Support Tools
class SupportTools:
    """IT Support domain tools"""
    GET_USER_PROFILE = "get_user_profile"
    CHECK_USER_PERMISSIONS = "check_user_permissions"
    RESET_USER_PASSWORD = "reset_user_password"
    UNLOCK_USER_ACCOUNT = "unlock_user_account"
    CHECK_PRINTER_STATUS = "check_printer_status"
    VERIFY_EMAIL_CONFIG = "verify_email_config"
    TEST_REMOTE_ACCESS = "test_remote_access"
    CHECK_SOFTWARE_INSTALLATION = "check_software_installation"
    GET_RECENT_TICKETS = "get_recent_tickets"
    ASK_QUESTIONS = "ask_questions"


# Manager Tools
class ManagerTools:
    """Manager domain tools"""
    GET_TECHNICIAN_WORKLOAD = "get_technician_workload"
    GET_TEAM_AVAILABILITY = "get_team_availability"
    CHECK_SKILL_MATCH = "check_skill_match"
    GET_OPEN_TICKETS = "get_open_tickets"
    GET_SLA_STATUS = "get_sla_status"
    GET_ESCALATION_HISTORY = "get_escalation_history"
    SEARCH_KNOWLEDGE_BASE = "search_knowledge_base"


# Ubuntu Principles (for documentation and messaging)
class UbuntuPrinciples:
    """Core Ubuntu philosophy principles"""
    COLLECTIVE_HUMANITY = "Collective Humanity"
    KNOWLEDGE_SHARING = "Knowledge Sharing"
    MUTUAL_SUPPORT = "Mutual Support"
    CONSENSUS_BUILDING = "Consensus Building"
    DIGNITY_AND_RESPECT = "Dignity and Respect"


# Configuration Keys
class ConfigKeys:
    """Configuration file keys"""
    REASONING_MODEL = "reasoning_model"
    EMBEDDING_MODEL = "embedding_model"
    ALTERNATIVE_MODELS = "alternative_models"
    FAST_MODEL = "fast"
    REASONING_SPECIALIST = "reasoning"
    MULTILINGUAL_MODEL = "multilingual"


# ReAct Engine Constants
class ReactConstants:
    """ReAct engine configuration"""
    DEFAULT_MAX_ITERATIONS = 10
    TOOL_DIVERSITY_THRESHOLD = 0.5
    TOOL_LOOP_DETECTION_THRESHOLD = 5  # Same tool 5 times = loop
    LLM_RETRY_ATTEMPTS = 3
    LLM_RETRY_BASE_DELAY = 0.5  # seconds, then exponential backoff
    REFLECTION_FREQUENCY = 2  # Every 2 iterations
    

# Logging Levels
class LogLevels:
    """Standard logging levels"""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


# File Paths (relative to project root)
class FilePaths:
    """Standard file path constants"""
    CONFIG_FILE = "config.json"
    LOGS_DIR = "logs"
    AGENTS_LOGS_DIR = "logs/agents"
    KNOWLEDGE_BASE_DIR = "knowledge_base"
    PLANS_DIR = "plans"
    TEST_RESULTS_DIR = "test_results"
    DATA_DIR = "data"


# Error Messages
class ErrorMessages:
    """Standard error messages"""
    OLLAMA_CONNECTION_FAILED = (
        "Failed to connect to Ollama service. "
        "Ensure Ollama is running: 'ollama serve'"
    )
    
    MODEL_NOT_FOUND = "Model '{model}' not found in Ollama"
    
    CONFIG_LOAD_FAILED = (
        "Failed to load configuration. "
        "Check config.json syntax and permissions."
    )
    
    EMBEDDING_INIT_FAILED = (
        "Embedding model initialization failed. "
        "RAG and memory features will be disabled."
    )
    
    AGENT_INITIALIZATION_FAILED = (
        "Agent initialization failed. "
        "Check LLM connection and configuration."
    )


# Success Messages
class SuccessMessages:
    """Standard success messages"""
    SYSTEM_READY = "✓ System ready"
    CONFIG_LOADED = "✓ Configuration loaded"
    LLM_INITIALIZED = "✓ LLM initialized"
    AGENTS_INITIALIZED = "✓ Agents initialized"
    RAG_INITIALIZED = "✓ RAG system initialized"


# Timeout Values (in seconds)
class Timeouts:
    """Standard timeout values"""
    LLM_DEFAULT = 30
    RAG_RETRIEVAL = 10
    MEMORY_OPERATION = 10
    TOOL_EXECUTION = 60


# Performance Thresholds
class PerformanceThresholds:
    """Performance monitoring thresholds"""
    SLOW_ITERATION_MS = 5000  # 5 seconds
    MAX_INVESTIGATION_TIME_MIN = 30  # 30 minutes
    TOOL_DIVERSITY_WARNING = 0.3  # Below this = low diversity warning
    STUCK_THRESHOLD = 0.1  # Progress score below this = stuck
