"""
UGENTIC Package - Ubuntu-Driven Agentic Collective Intelligence

Multi-agent IT support system integrating Ubuntu philosophy with AI reasoning.
"""

__version__ = "1.0.0"
__author__ = "UGENTIC Research Team"
__license__ = "Research"

from .config_manager import get_config, ConfigManager
from .constants import (
    InvestigationStatus,
    AgentNames,
    InfrastructureTools,
    NetworkTools,
    ApplicationTools,
    SupportTools,
    ManagerTools,
)

__all__ = [
    'get_config',
    'ConfigManager',
    'InvestigationStatus',
    'AgentNames',
    'InfrastructureTools',
    'NetworkTools',
    'ApplicationTools',
    'SupportTools',
    'ManagerTools',
]
