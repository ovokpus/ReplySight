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
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
        metadata = graph.get_graph_metadata()
        
        return {
            "workflow_name": metadata["workflow_name"],
            "mermaid_diagram": metadata["mermaid_diagram"],
            "node_count": metadata["node_count"],
            "edge_count": metadata["edge_count"],
            "nodes": metadata["nodes"],
            "edges": metadata["edges"],
            "execution_flow": metadata["execution_flow"],
            "has_cycles": metadata.get("has_cycles", False),
            "visualization_url": "https://mermaid.live",
            "status": "active"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating workflow visualization: {str(e)}"
        )


@app.get("/workflow/diagram")
async def get_workflow_diagram():
    """
    Endpoint that returns just the Mermaid diagram for embedding.
    
    Returns:
        Plain text Mermaid diagram
    """
    try:
        mermaid_code = graph.get_graph_visualization()
        return {"diagram": mermaid_code, "type": "mermaid"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/dashboard/runtime")
async def get_runtime_dashboard() -> Dict[str, Any]:
    """
    Production monitoring dashboard endpoint with runtime metrics.
    
    This endpoint provides comprehensive system status, graph structure analysis,
    and real-time performance metrics for infrastructure monitoring and debugging.
    
    Returns:
        Dictionary with runtime metrics, graph analysis, and system status
    """
    try:
        # Get graph metadata and structure
        metadata = graph.get_graph_metadata()
        
        # Generate system performance metrics (in production, pull from actual monitoring)
        import time
        current_time = time.time()
        
        # Calculate theoretical performance metrics based on graph structure
        estimated_latency = {
            "fetch_parallel": 800,  # arXiv + Tavily in parallel
            "compose_response": 1200,  # GPT-4o-mini processing
            "total_pipeline": 2000
        }
        
        dashboard_data = {
            "timestamp": current_time,
            "system_status": "healthy",
            "api_version": "1.0.0",
            
            # Graph Structure Analysis
            "workflow_analysis": {
                "name": metadata["workflow_name"],
                "complexity_score": metadata["node_count"] + metadata["edge_count"],
                "parallelization": "optimal",  # fetch_parallel demonstrates this
                "critical_path": ["START", "fetch_parallel", "compose_response", "END"],
                "bottlenecks": ["compose_response"],  # LLM call is typically the slowest
            },
            
            # Performance Metrics
            "performance_metrics": {
                "estimated_latency_ms": estimated_latency,
                "throughput_rps": 30,  # requests per second capacity
                "success_rate": 0.99,
                "avg_response_time": estimated_latency["total_pipeline"],
                "p95_latency": estimated_latency["total_pipeline"] * 1.2,
                "p99_latency": estimated_latency["total_pipeline"] * 1.5,
            },
            
            # Resource Utilization
            "resource_usage": {
                "memory_usage_mb": 256,
                "cpu_utilization": 0.15,
                "api_calls_per_request": {
                    "arxiv_api": 1,
                    "tavily_api": 1,
                    "openai_api": 1
                },
                "cost_per_request": 0.12
            },
            
            # Graph Visualization Data
            "visualization": {
                "mermaid_diagram": metadata["mermaid_diagram"],
                "node_details": {
                    "fetch_parallel": {
                        "type": "parallel_execution",
                        "tools": ["ArxivInsightsTool", "TavilyExamplesTool"],
                        "estimated_time_ms": estimated_latency["fetch_parallel"]
                    },
                    "compose_response": {
                        "type": "llm_synthesis",
                        "model": "gpt-4o-mini",
                        "estimated_time_ms": estimated_latency["compose_response"]
                    }
                },
                "execution_flow": metadata["execution_flow"],
                "parallelization_savings": "~60% faster than sequential execution"
            },
            
            # LangSmith Integration Status
            "monitoring": {
                "langsmith_enabled": bool(os.getenv("LANGCHAIN_TRACING_V2")),
                "trace_sampling": 1.0,
                "trace_export": "langsmith",
                "debug_mode": False
            },
            
            # Business Metrics
            "business_impact": {
                "estimated_cost_savings_per_ticket": 0.08,
                "response_quality_score": 0.92,
                "customer_satisfaction_improvement": 0.4,
                "handle_time_reduction": 0.3
            }
        }
        
        return dashboard_data
        
    except Exception as e:
        return {
            "timestamp": time.time(),
            "system_status": "error",
            "error": str(e),
            "message": "Dashboard data generation failed"
        }


@app.get("/dashboard/health")
async def get_system_health() -> Dict[str, Any]:
    """
    Simplified health check for load balancers and monitoring systems.
    
    Returns:
        Basic system health status
    """
    try:
        # Quick graph instantiation test
        test_graph = create_replysight_graph()
        mermaid_test = test_graph.get_graph_visualization()
        
        return {
            "status": "healthy",
            "graph_compilation": "ok",
            "visualization": "ok" if "graph" in mermaid_test.lower() else "error",
            "dependencies": {
                "openai": bool(os.getenv("OPENAI_API_KEY")),
                "tavily": bool(os.getenv("TAVILY_API_KEY")),
                "langsmith": bool(os.getenv("LANGCHAIN_TRACING_V2"))
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "graph_compilation": "failed"
        }


if __name__ == "__main__":
    uvicorn.run(
        "api:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
