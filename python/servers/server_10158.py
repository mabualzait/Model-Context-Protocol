# 📖 Chapter: Chapter 7: Building Your First MCP Server
# 📖 Section: 7.6 Production Deployment Considerations

import os
from pathlib import Path
from typing import Dict

class ConfigManager:
    """Manage server configuration for different environments."""
    
    def __init__(self):
        self.environment = os.getenv("MCP_ENV", "development")
        self.config_path = Path("config")
    
    def load_config(self) -> Dict:
        """Load configuration for current environment."""
        config_file = self.config_path / f"{self.environment}.json"
        
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        
        import json
        with open(config_file) as f:
            config = json.load(f)
        
        # Override with environment variables
        config = self._apply_env_overrides(config)
        
        return config
    
    def _apply_env_overrides(self, config: Dict) -> Dict:
        """Apply environment variable overrides."""
        overrides = {
            "server.port": os.getenv("MCP_PORT"),
            "server.host": os.getenv("MCP_HOST"),
            "server.debug": os.getenv("MCP_DEBUG", "false").lower() == "true",
            "security.api_key": os.getenv("MCP_API_KEY"),
        }
        
        for key, value in overrides.items():
            if value is not None:
                keys = key.split(".")
                target = config
                for k in keys[:-1]:
                    if k not in target:
                        target[k] = {}
                    target = target[k]
                target[keys[-1]] = value
        
        return config