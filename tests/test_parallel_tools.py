"""
Test suite for parallel tool execution in ReplySight.

This module tests both the LangGraph parallel execution
and the direct LLM tool binding approaches.
"""

import asyncio
import time
import pytest
from unittest.mock import Mock, patch

from api.graph import create_replysight_graph
from api.models import AgentState
from api.tools import ArxivInsightsTool, TavilyExamplesTool


class TestParallelExecution:
    """Test parallel tool execution patterns."""

    @pytest.mark.asyncio
    async def test_parallel_fetch_timing(self):
        """Test that parallel fetch is faster than sequential."""
        # Create graph with mocked tools for timing test
        graph = create_replysight_graph()
        
        # Mock the tools to simulate delay
        with patch.object(ArxivInsightsTool, '_arun') as mock_arxiv, \
             patch.object(TavilyExamplesTool, '_arun') as mock_tavily:
            
            # Each tool takes 1 second
            async def mock_delay(*args):
                await asyncio.sleep(1)
                return {"test": "data"}
            
            mock_arxiv.side_effect = mock_delay
            mock_tavily.side_effect = mock_delay
            
            # Test parallel execution
            start_time = time.time()
            result = await graph.generate_response("Test complaint")
            end_time = time.time()
            
            parallel_duration = end_time - start_time
            
            # Should be closer to 1 second (parallel) than 2 seconds (sequential)
            assert parallel_duration < 1.5, f"Parallel execution took {parallel_duration}s, expected < 1.5s"
            assert parallel_duration > 0.8, f"Execution was too fast: {parallel_duration}s"

    @pytest.mark.asyncio
    async def test_fetch_parallel_node(self):
        """Test the fetch_parallel node directly."""
        graph = create_replysight_graph()
        
        # Test state
        state: AgentState = {
            "messages": [],
            "complaint": "I'm unhappy with my service",
            "insights": {},
            "examples": {},
            "response": "",
            "citations": [],
            "latency_ms": 0,
            "start_time": time.time(),
            "iteration_count": 0,
            "decision": "continue",
            "arxiv_complete": False,
            "tavily_complete": False,
            "helpfulness_score": 0.0
        }
        
        # Mock both tools
        with patch.object(ArxivInsightsTool, '_arun') as mock_arxiv, \
             patch.object(TavilyExamplesTool, '_arun') as mock_tavily:
            
            mock_arxiv.return_value = {"papers": [{"title": "Test Paper"}]}
            mock_tavily.return_value = {"examples": [{"title": "Test Example"}]}
            
            # Call the generate_response method which includes parallel execution
            result = await graph.generate_response("I'm unhappy with my service")
            
            # Verify both tools were called
            mock_arxiv.assert_called()
            mock_tavily.assert_called()
            
            # Verify response was generated
            assert "response" in result
            assert isinstance(result["citations"], list)

    def test_asyncio_gather_pattern(self):
        """Test the asyncio.gather pattern used for parallel execution."""
        async def mock_task_1():
            await asyncio.sleep(0.1)
            return "result1"
        
        async def mock_task_2():
            await asyncio.sleep(0.1)
            return "result2"
        
        async def run_parallel():
            start = time.time()
            results = await asyncio.gather(mock_task_1(), mock_task_2())
            end = time.time()
            return results, (end - start)
        
        results, duration = asyncio.run(run_parallel())
        
        # Verify parallel execution
        assert results == ["result1", "result2"]
        assert duration < 0.15, f"Parallel execution took {duration}s, expected < 0.15s"


if __name__ == "__main__":
    # Simple test runner
    asyncio.run(TestParallelExecution().test_fetch_parallel_node())
    print("✅ Parallel execution tests passed!") 