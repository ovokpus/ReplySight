"""
Configuration management for the ReplySight backend.

This package provides centralized configuration management for all backend services.
"""

from .settings import Settings, get_settings

__all__ = ['Settings', 'get_settings'] 