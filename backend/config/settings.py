"""
Centralized settings management for the ReplySight backend.

This module provides a single source of truth for all configuration values,
using Pydantic for validation and environment variable management.
"""

import os
from functools import lru_cache
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseModel):
    """
    Application settings with validation and environment variable support.
    
    All configuration values are centralized here for easy management
    and consistent access across the application.
    """
    
    # API Configuration
    app_name: str = Field(default="ReplySight API", description="Application name")
    app_version: str = Field(default="1.0.0", description="Application version")
    app_description: str = Field(
        default="Research-backed customer service response generation",
        description="Application description"
    )
    
    # Server Configuration
    host: str = Field(default="0.0.0.0", description="Server host")
    port: int = Field(default=8000, description="Server port")
    debug: bool = Field(default=False, description="Debug mode")
    reload: bool = Field(default=False, description="Auto-reload on changes")
    
    # API Keys
    openai_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("OPENAI_API_KEY"),
        description="OpenAI API key"
    )
    tavily_api_key: Optional[str] = Field(
        default_factory=lambda: os.getenv("TAVILY_API_KEY"),
        description="Tavily API key"
    )
    
    # LangSmith Configuration
    langsmith_enabled: bool = Field(
        default_factory=lambda: bool(os.getenv("LANGCHAIN_TRACING_V2")),
        description="Enable LangSmith tracing"
    )
    langsmith_project: Optional[str] = Field(
        default_factory=lambda: os.getenv("LANGCHAIN_PROJECT"),
        description="LangSmith project name"
    )
    
    # LLM Configuration
    llm_model: str = Field(default="gpt-4o", description="Primary LLM model")
    llm_temperature: float = Field(default=0.3, description="LLM temperature")
    composer_model: str = Field(default="gpt-4o-mini", description="Response composer model")
    composer_temperature: float = Field(default=0.7, description="Composer temperature")
    helpfulness_model: str = Field(default="gpt-4o-mini", description="Helpfulness checker model")
    helpfulness_temperature: float = Field(default=0.1, description="Helpfulness temperature")
    
    # Workflow Configuration
    max_iterations: int = Field(default=5, description="Maximum workflow iterations")
    helpfulness_threshold: float = Field(default=0.7, description="Helpfulness threshold")
    
    # ArXiv Configuration
    arxiv_max_results: int = Field(default=3, description="Maximum ArXiv results")
    arxiv_sort_by: str = Field(default="relevance", description="ArXiv sort criteria")
    
    # Tavily Configuration
    tavily_search_depth: str = Field(default="basic", description="Tavily search depth")
    tavily_max_results: int = Field(default=3, description="Maximum Tavily results")
    
    # Performance Metrics
    estimated_latency_ms: int = Field(default=2000, description="Estimated response latency")
    cost_per_request: float = Field(default=0.12, description="Estimated cost per request")
    throughput_rps: int = Field(default=30, description="Requests per second capacity")
    
    # CORS Configuration
    allow_origins: list[str] = Field(default=["*"], description="Allowed CORS origins")
    allow_credentials: bool = Field(default=True, description="Allow credentials")
    allow_methods: list[str] = Field(default=["*"], description="Allowed HTTP methods")
    allow_headers: list[str] = Field(default=["*"], description="Allowed headers")
    
    class Config:
        """Pydantic configuration."""
        env_prefix = "REPLYSIGHT_"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Configured settings instance
    """
    return Settings() 