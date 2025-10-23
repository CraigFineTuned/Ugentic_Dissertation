"""
UGENTIC Logging Configuration
Structured JSON logging with rotation and per-module handlers
All paths are dynamic and cross-platform
"""

import logging
import logging.config
import json
import os
from pathlib import Path


class JsonFormatter(logging.Formatter):
    """Custom formatter that outputs JSON log entries"""
    
    def format(self, record):
        """Format log record as JSON"""
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "context": getattr(record, 'context', {})
        }
        return json.dumps(log_record) + '\n'


def setup_logging():
    """
    Setup logging configuration with dynamic paths
    
    Supports:
    - JSON structured logging
    - Rotating file handlers (10MB per file, 5 backups)
    - Per-module loggers
    - Console and file output
    - Error-specific logging
    """
    
    # Import here to avoid circular dependency
    from .config_manager import get_config
    
    config = get_config()
    
    LOGS_DIR = config.logs_dir
    AGENTS_LOGS_DIR = config.agents_logs_dir
    
    # Ensure directories exist
    Path(LOGS_DIR).mkdir(parents=True, exist_ok=True)
    Path(AGENTS_LOGS_DIR).mkdir(parents=True, exist_ok=True)
    
    # Define logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": "INFO"
            },
            "main_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(LOGS_DIR, "main.jsonl"),
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "level": "INFO"
            },
            "workflow_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(LOGS_DIR, "workflow.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "llm_interactions_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(LOGS_DIR, "llm_interactions.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "tools_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(LOGS_DIR, "tools.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "errors_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(LOGS_DIR, "errors.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "ERROR"
            },
            "orchestrator_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "orchestrator.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "finance_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "finance.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "hr_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "hr.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "operations_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "operations.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "marketing_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "marketing.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            },
            "sales_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(AGENTS_LOGS_DIR, "sales.jsonl"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "level": "INFO"
            }
        },
        "loggers": {
            "ugentic": {
                "handlers": ["console", "main_file", "errors_file"],
                "level": "DEBUG"
            },
            "ugentic.workflow": {
                "handlers": ["workflow_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.llm": {
                "handlers": ["llm_interactions_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.tool": {
                "handlers": ["tools_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.MainOrchestrator": {
                "handlers": ["orchestrator_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.finance": {
                "handlers": ["finance_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.hr": {
                "handlers": ["hr_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.operations": {
                "handlers": ["operations_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.marketing": {
                "handlers": ["marketing_file"],
                "level": "DEBUG",
                "propagate": True
            },
            "ugentic.agent.sales": {
                "handlers": ["sales_file"],
                "level": "DEBUG",
                "propagate": True
            }
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log setup completion
    logger = logging.getLogger("ugentic")
    logger.info(
        "Logging system initialized",
        extra={"context": {"logs_directory": LOGS_DIR}}
    )
