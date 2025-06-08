import os
import yaml

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
DEFAULT_CONFIG_PATH = os.path.join(BASE, "config", "default_config.yaml")
USER_CONFIG_PATH = os.path.join(BASE, "config", "user_config.yaml")

def _deep_merge(orig: dict, new: dict) -> dict:
    for key, val in new.items():
        if key in orig and isinstance(orig[key], dict) and isinstance(val, dict):
            _deep_merge(orig[key], val)
        else:
            orig[key] = val
    return orig

def load_config() -> dict:

    if not os.path.isfile(DEFAULT_CONFIG_PATH):
        raise FileNotFoundError(f"Default config file not found at {DEFAULT_CONFIG_PATH}")
    with open(DEFAULT_CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f) or {}

    # Load user settings if present
    if os.path.isfile(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH, "r") as f:
            user_config = yaml.safe_load(f) or {}
        config = _deep_merge(config, user_config)

    return config

def save_user_config(config: dict) -> None:
    if os.path.isfile(USER_CONFIG_PATH):
        with open(USER_CONFIG_PATH) as f:
            current = yaml.safe_load(f) or {}
    else:
        current = {}
    merged = _deep_merge(current, config)

    with open(USER_CONFIG_PATH, "w") as f:
        yaml.safe_dump(merged, f, default_flow_style=False)