"""
FastAPI application for the ReplySight customer service response API.

This module provides the REST API endpoints for generating research-backed
customer service responses, with integrated LangSmith tracing and latency
tracking for business metrics.
"""

from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langsmith import traceable
import uvicorn

try:
    # Try relative imports first (when imported as a module)
    from .config import get_settings
    from .models import ComplaintRequest, ResponseOutput
    from .services import WorkflowService, GraphService
except ImportError:
    # Fall back to direct imports (when run directly)
    from config import get_settings
    from models import ComplaintRequest, ResponseOutput
    from services import WorkflowService, GraphService


# Initialize settings
settings = get_settings()

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allow_methods,
    allow_headers=settings.allow_headers,
)

# Initialize services
workflow_service = WorkflowService(tavily_api_key=settings.tavily_api_key)
graph_service = GraphService(tavily_api_key=settings.tavily_api_key)


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
        result = await workflow_service.generate_response(request)
        return result

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing complaint: {str(e)}"
        )


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for monitoring and deployment verification.
    
    Returns:
        Dictionary with service status and system health information
    """
    try:
        # Perform comprehensive health check
        workflow_health = workflow_service.health_check()

        return {
            "status": "healthy" if workflow_health["status"] == "healthy" else "unhealthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "workflow": workflow_health,
            "dependencies": {
                "openai": bool(settings.openai_api_key),
                "tavily": bool(settings.tavily_api_key),
                "langsmith": settings.langsmith_enabled
            }
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "service": settings.app_name,
            "version": settings.app_version,
            "error": str(e)
        }


@app.get("/workflow/graph")
async def get_workflow_graph() -> Dict[str, Any]:
    """
    Endpoint for retrieving the workflow graph visualization.
    
    This endpoint provides Mermaid diagram code and metadata for 
    displaying the ReplySight workflow in web interfaces.
    
    Returns:
        Dictionary with Mermaid diagram, metadata, and graph structure
    """
    try:
        metadata = graph_service.get_workflow_metadata()
        return metadata

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating workflow visualization: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "api.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )
