from typing import Tuple
from pathlib import Path
import tomllib


def load() -> Tuple[dict, dict]:
    """Read both configs and return general and local config as dict"""
    config_general = load_general()
    config_local = load_local()
    return config_general, config_local


def load_general() -> dict:
    """Read general Config as dict"""
    with open("config.toml", "rb") as f:
        return tomllib.load(f)


def load_local() -> dict:
    """Read local config with paths as dict"""
    with open("local_config.toml", "rb") as f:
        return tomllib.load(f)