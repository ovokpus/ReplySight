"""
Workflow service for managing ReplySight response generation.

This service provides a clean abstraction for the workflow execution,
handling the business logic for generating customer service responses.
"""

import time
from typing import Dict, Any, Optional
from langsmith import traceable

try:
    # Try relative imports first (when imported as a module)
    from ..config import get_settings
    from ..models import ComplaintRequest, ResponseOutput
    from ..graph import create_replysight_graph
except ImportError:
    # Fall back to direct imports (when Railway runs from api/ directory)
    from config import get_settings
    from models.api_models import ComplaintRequest, ResponseOutput
    from graph import create_replysight_graph


class WorkflowService:
    """
    Service for managing workflow execution and response generation.
    
    This service provides a clean interface for the API layer to execute
    the ReplySight workflow without direct coupling to the graph implementation.
    """
    
    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize the workflow service.
        
        Args:
            tavily_api_key: Tavily API key for search functionality
        """
        self.settings = get_settings()
        self.graph = create_replysight_graph(
            tavily_api_key or self.settings.tavily_api_key
        )
    
    @traceable(name="workflow_service_generate_response")
    async def generate_response(self, request: ComplaintRequest) -> ResponseOutput:
        """
        Generate a customer service response for the given complaint.
        
        Args:
            request: The complaint request containing customer complaint data
            
        Returns:
            ResponseOutput: Generated response with citations and metrics
            
        Raises:
            Exception: If response generation fails
        """
        start_time = time.time()
        
        try:
            # Execute the workflow
            result = await self.graph.generate_response(request.complaint)
            
            # Calculate actual latency
            end_time = time.time()
            actual_latency = int((end_time - start_time) * 1000)
            
            # Return structured response
            return ResponseOutput(
                reply=result["reply"],
                citations=result.get("citations", []),
                latency_ms=actual_latency
            )
            
        except Exception as e:
            # Log error and re-raise with context
            end_time = time.time()
            error_latency = int((end_time - start_time) * 1000)
            
            # In production, log this error
            raise Exception(f"Workflow execution failed after {error_latency}ms: {str(e)}")
    
    def get_workflow_metadata(self) -> Dict[str, Any]:
        """
        Get workflow metadata for visualization and monitoring.
        
        Returns:
            Dict containing workflow metadata
        """
        try:
            return self.graph.get_graph_metadata()
        except Exception as e:
            raise Exception(f"Failed to get workflow metadata: {str(e)}")
    
    def get_workflow_diagram(self) -> str:
        """
        Get the Mermaid diagram for the workflow.
        
        Returns:
            String containing the Mermaid diagram code
        """
        try:
            return self.graph.get_graph_visualization()
        except Exception as e:
            raise Exception(f"Failed to get workflow diagram: {str(e)}")
    
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check of the workflow system.
        
        Returns:
            Dict containing health check results
        """
        try:
            # Test graph compilation
            metadata = self.get_workflow_metadata()
            
            # Test visualization generation
            diagram = self.get_workflow_diagram()
            
            return {
                "status": "healthy",
                "graph_compilation": "ok",
                "visualization": "ok" if "graph" in diagram.lower() else "error",
                "node_count": metadata.get("node_count", 0),
                "edge_count": metadata.get("edge_count", 0),
                "workflow_name": metadata.get("workflow_name", "Unknown")
            }
            
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "graph_compilation": "failed"
            } 