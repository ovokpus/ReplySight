"""
Error handling utilities for the ReplySight backend.

This module provides consistent error handling and formatting
across all backend services.
"""

import logging
from typing import Dict, Any, Optional
from fastapi import HTTPException


class ErrorHandler:
    """
    Centralized error handling for consistent error responses.
    
    This class provides standardized error handling and logging
    for all backend services and API endpoints.
    """
    
    def __init__(self, logger_name: str = "replysight"):
        """
        Initialize the error handler.
        
        Args:
            logger_name: Name for the logger instance
        """
        self.logger = logging.getLogger(logger_name)
    
    def handle_workflow_error(self, error: Exception, context: str = "workflow") -> HTTPException:
        """
        Handle workflow-related errors with proper logging.
        
        Args:
            error: The exception that occurred
            context: Context information for logging
            
        Returns:
            HTTPException: Formatted HTTP exception
        """
        error_msg = f"Workflow error in {context}: {str(error)}"
        self.logger.error(error_msg)
        
        return HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(error)}"
        )
    
    def handle_validation_error(self, error: Exception, field: str = "input") -> HTTPException:
        """
        Handle validation errors with proper logging.
        
        Args:
            error: The validation exception
            field: Field that failed validation
            
        Returns:
            HTTPException: Formatted HTTP exception
        """
        error_msg = f"Validation error for {field}: {str(error)}"
        self.logger.warning(error_msg)
        
        return HTTPException(
            status_code=400,
            detail=f"Invalid {field}: {str(error)}"
        )
    
    def handle_service_error(self, error: Exception, service: str = "service") -> HTTPException:
        """
        Handle service-related errors with proper logging.
        
        Args:
            error: The service exception
            service: Name of the service that failed
            
        Returns:
            HTTPException: Formatted HTTP exception
        """
        error_msg = f"Service error in {service}: {str(error)}"
        self.logger.error(error_msg)
        
        return HTTPException(
            status_code=500,
            detail=f"Service temporarily unavailable: {service}"
        )
    
    def log_info(self, message: str, **kwargs) -> None:
        """
        Log informational messages with context.
        
        Args:
            message: The message to log
            **kwargs: Additional context information
        """
        if kwargs:
            message = f"{message} - Context: {kwargs}"
        self.logger.info(message)
    
    def log_warning(self, message: str, **kwargs) -> None:
        """
        Log warning messages with context.
        
        Args:
            message: The warning message
            **kwargs: Additional context information
        """
        if kwargs:
            message = f"{message} - Context: {kwargs}"
        self.logger.warning(message)
    
    def create_error_response(self, 
                            status_code: int, 
                            message: str, 
                            details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create standardized error response.
        
        Args:
            status_code: HTTP status code
            message: Error message
            details: Optional additional details
            
        Returns:
            Dict containing error response
        """
        response = {
            "error": True,
            "status_code": status_code,
            "message": message
        }
        
        if details:
            response["details"] = details
            
        return response 