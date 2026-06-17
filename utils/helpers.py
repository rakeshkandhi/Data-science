"""
Shared helper utilities for the AI Engineer learning repo.
Import from any notebook or script:
    from utils.helpers import timer, get_project_root

Environment / secrets:
    Use pydantic-settings via the root config.py:
    from config import settings
"""

import functools
import time
from pathlib import Path


def timer(func):
    """Decorator to time any function execution."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  {func.__name__} ran in {elapsed:.4f}s")
        return result

    return wrapper


def get_project_root() -> Path:
    """Return the absolute path to the repo root."""
    return Path(__file__).parent.parent
