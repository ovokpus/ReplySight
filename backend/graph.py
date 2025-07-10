"""
LangGraph implementation for the ReplySight response generation workflow.

This module defines the graph structure that orchestrates parallel fetching
of research insights and examples, then composes them into empathetic
customer service responses with full LangSmith tracing.
"""

import time
from typing import Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from langsmith import traceable
from pydantic import BaseModel
from typing_extensions import TypedDict

from backend.tools import ArxivInsightsTool, TavilyExamplesTool, ResponseComposerTool


class ResponseState(TypedDict):
    """
    State model for the response generation workflow.
    
    This class defines the state that flows through the LangGraph,
    tracking the complaint, fetched insights, examples, and final response.
    """

    complaint: str
    insights: Dict[str, Any]
    examples: Dict[str, Any]
    response: str
    citations: List[str]
    latency_ms: int
    start_time: float


class ReplySightGraph:
    """
    LangGraph workflow for generating research-backed customer service responses.
    
    This class orchestrates the three-node workflow:
    1. Parallel fetch of insights and examples
    2. Response composition with citations
    3. Latency tracking and LangSmith integration
    """

    def __init__(self, tavily_api_key: Optional[str] = None):
        """
        Initialize the ReplySight workflow graph.
        
        Args:
            tavily_api_key: API key for Tavily search service
        """
        self.arxiv_tool = ArxivInsightsTool()
        self.tavily_tool = TavilyExamplesTool(api_key=tavily_api_key)
        self.composer_tool = ResponseComposerTool()

        # Build the graph
        self.graph = self._build_graph()
        self.compiled_graph = self.graph.compile(
            checkpointer=MemorySaver(),
            interrupt_before=[]
        )

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow with three nodes in sequence.
        
        Returns:
            Configured StateGraph ready for compilation
        """
        workflow = StateGraph(ResponseState)

        # Add nodes
        workflow.add_node("fetch_insights", self._fetch_insights)
        workflow.add_node("fetch_examples", self._fetch_examples)
        workflow.add_node("compose_response", self._compose_response)
        
        # Set entry point
        workflow.set_entry_point("fetch_insights")

        # Add edges for sequential execution
        workflow.add_edge("fetch_insights", "fetch_examples")
        workflow.add_edge("fetch_examples", "compose_response")
        workflow.add_edge("compose_response", END)

        return workflow

    @traceable(name="fetch_insights")
    async def _fetch_insights(self, state: ResponseState) -> ResponseState:
        """
        Fetch academic research insights from arXiv.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with research insights
        """
        insights = await self.arxiv_tool._arun(state["complaint"])
        state["insights"] = insights
        return state

    @traceable(name="fetch_examples")
    async def _fetch_examples(self, state: ResponseState) -> ResponseState:
        """
        Fetch best-practice examples via Tavily.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated state with example responses
        """
        examples = await self.tavily_tool._arun(state["complaint"])
        state["examples"] = examples
        return state

    @traceable(name="compose_response")
    async def _compose_response(self, state: ResponseState) -> ResponseState:
        """
        Compose final empathetic response with citations.
        
        Args:
            state: Current workflow state with insights and examples
            
        Returns:
            Final state with composed response and citations
        """
        result = await self.composer_tool._arun(
            state["complaint"],
            state["insights"],
            state["examples"]
        )

        state["response"] = result['response']
        state["citations"] = result['citations']
        return state

    @traceable(name="generate_response")
    async def generate_response(self, complaint: str) -> Dict[str, Any]:
        """
        Generate a complete response to a customer complaint.
        
        This method orchestrates the full workflow: timing, parallel fetching,
        composition, and latency tracking for business metrics.
        
        Args:
            complaint: Customer complaint text
            
        Returns:
            Dictionary with response, citations, and latency metrics
        """
        start_time = time.time()

        # Initialize state
        initial_state: ResponseState = {
            "complaint": complaint,
            "insights": {},
            "examples": {},
            "response": "",
            "citations": [],
            "latency_ms": 0,
            "start_time": start_time
        }

        # Run the workflow
        config = {"configurable": {
            "thread_id": f"complaint_{int(start_time)}"}}

        final_state = await self.compiled_graph.ainvoke(
            initial_state,
            config=config
        )

        # Calculate latency
        end_time = time.time()
        latency_ms = int((end_time - start_time) * 1000)

        return {
            "reply": final_state["response"],
            "citations": final_state["citations"],
            "latency_ms": latency_ms
        }


# Factory function for easy instantiation
def create_replysight_graph(tavily_api_key: Optional[str] = None) -> ReplySightGraph:
    """
    Factory function to create a configured ReplySight graph.
    
    Args:
        tavily_api_key: API key for Tavily search service
        
    Returns:
        Configured ReplySightGraph instance
    """
    return ReplySightGraph(tavily_api_key=tavily_api_key)
