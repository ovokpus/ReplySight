"""
Workflow and agent state models for the ReplySight backend.

This module contains Pydantic models used internally by the workflow
system, extracted from the graph module for better organization.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict, Annotated
import operator


class AgentState(TypedDict):
    """
    Agent state model for the ToolNode-based workflow.
    
    This class defines the state that flows through the LangGraph,
    using messages for ToolNode compatibility and tracking workflow progress.
    """
    messages: Annotated[List[Any], operator.add]
    complaint: str
    insights: Dict[str, Any]
    examples: Dict[str, Any]
    response: str
    citations: List[str]
    latency_ms: int
    start_time: float
    iteration_count: int
    decision: str  # "continue", "arxiv_tools", "tavily_tools", "compose", "end"
    arxiv_complete: bool
    tavily_complete: bool
    helpfulness_score: float


class WorkflowMetadata(BaseModel):
    """
    Metadata model for workflow visualization and monitoring.
    
    This model structures the workflow information returned by the graph
    for use in visualization and monitoring systems.
    """
    
    workflow_name: str = Field(..., description="Name of the workflow")
    mermaid_diagram: str = Field(..., description="Mermaid diagram code")
    node_count: int = Field(..., description="Number of nodes in the workflow")
    edge_count: int = Field(..., description="Number of edges in the workflow")
    nodes: List[str] = Field(default_factory=list, description="List of node names")
    edges: List[Dict[str, str]] = Field(default_factory=list, description="List of edges")
    execution_flow: List[str] = Field(default_factory=list, description="Execution flow order")
    has_cycles: bool = Field(default=False, description="Whether the workflow has cycles")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "workflow_name": "ReplySight Response Generation",
                "mermaid_diagram": "graph TD\n    A[Start] --> B[Fetch Research]",
                "node_count": 5,
                "edge_count": 6,
                "nodes": ["START", "fetch_parallel", "compose_response", "END"],
                "edges": [{"from": "START", "to": "fetch_parallel"}],
                "execution_flow": ["START", "fetch_parallel", "compose_response", "END"],
                "has_cycles": False
            }
        }


class ToolResult(BaseModel):
    """
    Model for tool execution results.
    
    This model standardizes the output from different tools
    for consistent processing in the workflow.
    """
    
    tool_name: str = Field(..., description="Name of the tool that executed")
    result: Dict[str, Any] = Field(..., description="Tool execution result")
    error: Optional[str] = Field(None, description="Error message if tool failed")
    execution_time_ms: Optional[int] = Field(None, description="Tool execution time")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "tool_name": "arxiv_insights",
                "result": {
                    "papers": [],
                    "query": "customer service empathy",
                    "source": "arXiv"
                },
                "error": None,
                "execution_time_ms": 450
            }
        } 