"""
ReplySight Backend Package

This package contains the FastAPI backend implementation for the ReplySight
customer service response generation system, organized into modular components
for better maintainability and scalability.

Modules:
    - api: FastAPI application with REST endpoints
    - config: Centralized configuration management
    - models: Pydantic models for data validation
    - services: Business logic and service layer
    - utils: Utility functions and helpers
    - tools: LangChain tools for research and response generation
    - graph: LangGraph workflow implementation
"""

from .config import Settings, get_settings
from .models import ComplaintRequest, ResponseOutput, AgentState, WorkflowMetadata
from .services import WorkflowService, GraphService
from .utils import ErrorHandler, validate_complaint, sanitize_input

__version__ = "1.0.0"
__all__ = [
    # Configuration
    'Settings',
    'get_settings',
    
    # Models
    'ComplaintRequest',
    'ResponseOutput',
    'AgentState',
    'WorkflowMetadata',
    
    # Services
    'WorkflowService',
    'GraphService',
    
    # Utilities
    'ErrorHandler',
    'validate_complaint',
    'sanitize_input',
] 