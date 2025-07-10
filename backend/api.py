"""
FastAPI application for the ReplySight customer service response API.

This module provides the REST API endpoints for generating research-backed
customer service responses, with integrated LangSmith tracing and latency
tracking for business metrics.
"""

import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langsmith import traceable
import uvicorn

from backend.graph import create_replysight_graph


class ComplaintRequest(BaseModel):
    """
    Request model for customer complaint submissions.
    
    This model validates and structures incoming complaint data
    for processing by the ReplySight workflow.
    """

    complaint: str
    customer_id: str = None
    priority: str = "normal"


class ResponseOutput(BaseModel):
    """
    Response model for generated customer service replies.
    
    This model structures the API response with the generated reply,
    supporting citations, and latency metrics for business tracking.
    """

    reply: str
    citations: list[str]
    latency_ms: int


# Initialize FastAPI app
app = FastAPI(
    title="ReplySight API",
    description="Research-backed customer service response generation",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ReplySight graph
graph = create_replysight_graph(
    tavily_api_key=os.getenv("TAVILY_API_KEY")
)


@app.post("/respond", response_model=ResponseOutput)
@traceable(name="api_respond")
async def respond_to_complaint(request: ComplaintRequest) -> ResponseOutput:
    """
    Generate an empathetic, research-backed response to a customer complaint.
    
    This endpoint processes customer complaints through the ReplySight workflow,
    fetching academic insights and best practices to compose thoughtful responses
    with proper citations and latency tracking.
    
    Args:
        request: ComplaintRequest containing the customer complaint
        
    Returns:
        ResponseOutput with generated reply, citations, and latency metrics
        
    Raises:
        HTTPException: If complaint processing fails
    """
    try:
        result = await graph.generate_response(request.complaint)

        return ResponseOutput(
            reply=result["reply"],
            citations=result["citations"],
            latency_ms=result["latency_ms"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing complaint: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint for monitoring and deployment verification.
    
    Returns:
        Dictionary with service status and version information
    """
    return {
        "status": "healthy",
        "service": "ReplySight API",
        "version": "1.0.0"
    }


@app.get("/metrics")
async def get_metrics() -> Dict[str, Any]:
    """
    Endpoint for retrieving business metrics and system performance.
    
    Returns:
        Dictionary with latency statistics and cost calculations
    """
    # In production, this would pull from actual metrics storage
    return {
        "avg_latency_ms": 1847,
        "cost_per_ticket": 0.12,
        "handle_time_reduction": 0.3,
        "estimated_annual_savings": 286000
    }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
