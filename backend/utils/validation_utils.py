"""
Validation utilities for the ReplySight backend.

This module provides input validation and sanitization functions
to ensure data integrity and security.
"""

import re
from typing import Optional
from pydantic import ValidationError


def validate_complaint(complaint: str) -> str:
    """
    Validate and sanitize customer complaint input.
    
    Args:
        complaint: The raw complaint text
        
    Returns:
        str: Sanitized complaint text
        
    Raises:
        ValueError: If complaint is invalid
    """
    if not complaint:
        raise ValueError("Complaint cannot be empty")
    
    # Remove leading/trailing whitespace
    complaint = complaint.strip()
    
    # Check minimum length
    if len(complaint) < 10:
        raise ValueError("Complaint must be at least 10 characters long")
    
    # Check maximum length (prevent abuse)
    if len(complaint) > 5000:
        raise ValueError("Complaint cannot exceed 5000 characters")
    
    # Basic sanitization - remove potentially harmful characters
    # Keep letters, numbers, punctuation, and common symbols
    sanitized = re.sub(r'[^\w\s\.\,\!\?\-\(\)\[\]\'\"\:\;]', '', complaint)
    
    if not sanitized.strip():
        raise ValueError("Complaint contains no valid content")
    
    return sanitized


def sanitize_input(text: str, max_length: int = 1000) -> str:
    """
    General input sanitization function.
    
    Args:
        text: Input text to sanitize
        max_length: Maximum allowed length
        
    Returns:
        str: Sanitized text
        
    Raises:
        ValueError: If input is invalid
    """
    if not text:
        return ""
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Check length
    if len(text) > max_length:
        raise ValueError(f"Input cannot exceed {max_length} characters")
    
    # Basic sanitization
    sanitized = re.sub(r'[^\w\s\.\,\!\?\-\(\)\[\]\'\"\:\;]', '', text)
    
    return sanitized


def validate_customer_id(customer_id: Optional[str]) -> Optional[str]:
    """
    Validate customer ID format.
    
    Args:
        customer_id: Customer identifier
        
    Returns:
        Optional[str]: Validated customer ID or None
        
    Raises:
        ValueError: If customer ID format is invalid
    """
    if not customer_id:
        return None
    
    # Allow alphanumeric characters, hyphens, and underscores
    if not re.match(r'^[a-zA-Z0-9_-]+$', customer_id):
        raise ValueError("Customer ID contains invalid characters")
    
    if len(customer_id) > 50:
        raise ValueError("Customer ID cannot exceed 50 characters")
    
    return customer_id


def validate_priority(priority: str) -> str:
    """
    Validate priority level.
    
    Args:
        priority: Priority level
        
    Returns:
        str: Validated priority
        
    Raises:
        ValueError: If priority is invalid
    """
    valid_priorities = ["low", "normal", "high", "urgent"]
    
    if priority.lower() not in valid_priorities:
        raise ValueError(f"Priority must be one of: {', '.join(valid_priorities)}")
    
    return priority.lower() 