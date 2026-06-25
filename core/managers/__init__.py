from .config_manager import ConfigManager
from .log_manager import LogManager

config = ConfigManager()
logger = LogManager()

__all__ = [
    "config",
    "logger",
    "ConfigManager",
    "LogManager",
]