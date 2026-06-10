import yaml
from typing import Any

class ConfigLoader:
    def __init__(self, config_path: str = "config/default_config.yaml"):
        with open(config_path, 'r') as f:
            self._config = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        val = self._config
        for k in keys:
            if isinstance(val, dict):
                val = val.get(k, default)
            else:
                return default
        return val

config = ConfigLoader()