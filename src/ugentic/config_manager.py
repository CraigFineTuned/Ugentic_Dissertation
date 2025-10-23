"""
UGENTIC Configuration Manager
Handles all configuration with defaults, validation, and cross-platform support

Best practices:
- Single source of truth for all configuration
- Graceful fallbacks to defaults
- Environment-aware settings
- Type-safe configuration access
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ModelConfig:
    """LLM model configuration"""
    reasoning_model: str = "deepseek-v3.1:671b-cloud"
    fast_model: str = "gemma3n:e4b"
    reasoning_specialist: str = "deepseek-r1:7b"
    multilingual_model: str = "granite4:tiny-h"
    embedding_model: str = "embeddinggemma:latest"


@dataclass
class PathConfig:
    """Path configuration - all computed relative to project root"""
    project_root: str = None  # Set during init
    logs_dir: str = "logs"
    knowledge_base_dir: str = "knowledge_base"
    plans_dir: str = "plans"
    test_results_dir: str = "test_results"
    data_dir: str = "data"
    
    def __post_init__(self):
        """Compute absolute paths after initialization"""
        if self.project_root is None:
            self.project_root = self._compute_project_root()
    
    def _compute_project_root(self) -> str:
        """
        Compute project root directory
        Works whether running from project root, src/, or anywhere in project
        """
        current = Path(__file__).resolve().parent.parent.parent
        
        # Look for marker files/dirs that identify project root
        markers = ["config.json", "requirements.txt", ".git", "app.py"]
        
        while current != current.parent:  # Stop at filesystem root
            if any((current / marker).exists() for marker in markers):
                return str(current)
            current = current.parent
        
        # Fallback to script location
        return str(Path(__file__).resolve().parent.parent.parent)
    
    def get_logs_path(self) -> str:
        """Get absolute path to logs directory"""
        path = Path(self.project_root) / self.logs_dir
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    def get_agents_logs_path(self) -> str:
        """Get absolute path to agents logs subdirectory"""
        path = Path(self.project_root) / self.logs_dir / "agents"
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    def get_knowledge_base_path(self) -> str:
        """Get absolute path to knowledge base directory"""
        path = Path(self.project_root) / self.knowledge_base_dir
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    def get_plans_path(self) -> str:
        """Get absolute path to plans directory"""
        path = Path(self.project_root) / self.plans_dir
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    def get_test_results_path(self) -> str:
        """Get absolute path to test results directory"""
        path = Path(self.project_root) / self.test_results_dir
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
    
    def get_data_path(self) -> str:
        """Get absolute path to data directory"""
        path = Path(self.project_root) / self.data_dir
        path.mkdir(parents=True, exist_ok=True)
        return str(path)


class ConfigManager:
    """
    Singleton configuration manager
    Handles loading, validation, and access to all configuration
    """
    
    _instance: Optional['ConfigManager'] = None
    
    def __new__(cls):
        """Implement singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize configuration (only on first instantiation)"""
        if self._initialized:
            return
        
        self.paths = PathConfig()
        self.models = ModelConfig()
        self._load_config()
        self._initialized = True
    
    def _load_config(self):
        """Load configuration from config.json if it exists"""
        config_path = Path(self.paths.project_root) / "config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = json.load(f)
                
                # Merge with defaults
                if 'reasoning_model' in config_data:
                    self.models.reasoning_model = config_data['reasoning_model']
                
                if 'embedding_model' in config_data:
                    self.models.embedding_model = config_data['embedding_model']
                
                if 'alternative_models' in config_data:
                    alt = config_data['alternative_models']
                    if 'fast' in alt:
                        self.models.fast_model = alt['fast']
                    if 'reasoning' in alt:
                        self.models.reasoning_specialist = alt['reasoning']
                    if 'multilingual' in alt:
                        self.models.multilingual_model = alt['multilingual']
                
                print(f"✓ Configuration loaded from {config_path}")
            except json.JSONDecodeError as e:
                print(f"⚠ Warning: config.json is invalid JSON: {e}")
                print(f"  Using default configuration")
            except Exception as e:
                print(f"⚠ Warning: Failed to load config.json: {e}")
                print(f"  Using default configuration")
        else:
            print(f"ℹ No config.json found at {config_path}")
            print(f"  Using default configuration")
    
    @property
    def reasoning_model(self) -> str:
        """Get reasoning model name"""
        return self.models.reasoning_model
    
    @property
    def embedding_model(self) -> str:
        """Get embedding model name"""
        return self.models.embedding_model
    
    @property
    def fast_model(self) -> str:
        """Get fast model name"""
        return self.models.fast_model
    
    @property
    def project_root(self) -> str:
        """Get project root directory"""
        return self.paths.project_root
    
    @property
    def logs_dir(self) -> str:
        """Get logs directory"""
        return self.paths.get_logs_path()
    
    @property
    def agents_logs_dir(self) -> str:
        """Get agents logs directory"""
        return self.paths.get_agents_logs_path()
    
    @property
    def knowledge_base_dir(self) -> str:
        """Get knowledge base directory"""
        return self.paths.get_knowledge_base_path()
    
    @property
    def plans_dir(self) -> str:
        """Get plans directory"""
        return self.paths.get_plans_path()
    
    @property
    def test_results_dir(self) -> str:
        """Get test results directory"""
        return self.paths.get_test_results_path()
    
    @property
    def data_dir(self) -> str:
        """Get data directory"""
        return self.paths.get_data_path()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get human-readable configuration summary"""
        return {
            "project_root": self.project_root,
            "reasoning_model": self.reasoning_model,
            "embedding_model": self.embedding_model,
            "fast_model": self.fast_model,
            "logs_directory": self.logs_dir,
            "knowledge_base_directory": self.knowledge_base_dir,
            "plans_directory": self.plans_dir,
        }


def get_config() -> ConfigManager:
    """
    Get singleton instance of ConfigManager
    
    Usage:
        config = get_config()
        logs_dir = config.logs_dir
        model = config.reasoning_model
    """
    return ConfigManager()
