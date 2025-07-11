"""
API request and response models for the ReplySight backend.

This module contains all Pydantic models used for API validation
and serialization, extracted from the main API file for better organization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ComplaintRequest(BaseModel):
    """
    Request model for customer complaint submissions.
    
    This model validates and structures incoming complaint data
    for processing by the ReplySight workflow.
    """
    
    complaint: str = Field(..., description="The customer complaint text")
    customer_id: Optional[str] = Field(None, description="Customer identifier")
    priority: str = Field(default="normal", description="Priority level")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            str: lambda v: v.strip() if v else v
        }
        schema_extra = {
            "example": {
                "complaint": "I ordered a product last week but it hasn't arrived yet.",
                "customer_id": "cust_123",
                "priority": "normal"
            }
        }


class ResponseOutput(BaseModel):
    """
    Response model for generated customer service replies.
    
    This model structures the API response with the generated reply,
    supporting citations, and latency metrics for business tracking.
    """
    
    reply: str = Field(..., description="The generated customer service response")
    citations: List[str] = Field(default_factory=list, description="Supporting citations")
    latency_ms: int = Field(..., description="Response generation latency in milliseconds")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "reply": "Thank you for reaching out. I sincerely apologize for the delay...",
                "citations": ["Smith, J. et al. (2023). Customer Service Recovery"],
                "latency_ms": 1850
            }
        } 