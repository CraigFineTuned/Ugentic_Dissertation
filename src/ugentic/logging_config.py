
import logging
import logging.config
import json
import os

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger_name": record.name,
            "message": record.getMessage(),
            "context": getattr(record, 'context', {})
        }
        return json.dumps(log_record) + '\n'

def setup_logging():
    LOGS_DIR = "C:/Users/craig/Desktop/MainProjects/Ugentic/logs"
    AGENTS_LOGS_DIR = os.path.join(LOGS_DIR, "agents")

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
    if not os.path.exists(AGENTS_LOGS_DIR):
        os.makedirs(AGENTS_LOGS_DIR)

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
                "maxBytes": 10485760,
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
    logging.config.dictConfig(LOGGING_CONFIG)
