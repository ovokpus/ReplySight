"""
Pytest evaluation suite for ReplySight system performance and quality.

This module runs comprehensive tests against the evaluation dataset,
measuring response quality, latency, citations, and business metrics
to validate the $286K upside projections.
"""

from .dataset import get_evaluation_dataset
from backend.graph import create_replysight_graph
import pytest
import asyncio
import statistics
from typing import List, Dict, Any
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestReplySightSystem:
    """
    Test suite for validating ReplySight system performance.
    
    This class runs comprehensive evaluations covering response quality,
    latency requirements, citation accuracy, and business impact metrics.
    """

    @pytest.fixture(scope="class")
    def graph(self):
        """
        Create ReplySight graph instance for testing.
        
        Returns:
            Configured ReplySightGraph instance
        """
        return create_replysight_graph(
            tavily_api_key=os.getenv("TAVILY_API_KEY")
        )

    @pytest.fixture(scope="class")
    def dataset(self):
        """
        Load evaluation dataset for testing.
        
        Returns:
            List of test cases
        """
        return get_evaluation_dataset()

    @pytest.mark.asyncio
    async def test_response_generation_quality(self, graph, dataset):
        """
        Test that responses meet quality criteria for all test cases.
        
        Validates:
        - Non-empty responses
        - Minimum citation count
        - Latency under 3000ms
        - Expected response elements
        """
        results = []

        for test_case in dataset:
            complaint = test_case["complaint"]

            # Generate response
            result = await graph.generate_response(complaint)

            # Validate response quality
            assert result["reply"], f"Empty response for case {test_case['id']}"
            assert len(result["citations"]) >= test_case["min_citations"], \
                f"Insufficient citations for case {test_case['id']}"
            assert result["latency_ms"] < test_case["max_latency_ms"], \
                f"Latency too high for case {test_case['id']}: {result['latency_ms']}ms"

            results.append({
                "case_id": test_case["id"],
                "latency_ms": result["latency_ms"],
                "citations_count": len(result["citations"]),
                "response_length": len(result["reply"]),
                "passed": True
            })

        # Print summary statistics
        latencies = [r["latency_ms"] for r in results]
        citations = [r["citations_count"] for r in results]

        print(f"\n=== EVALUATION SUMMARY ===")
        print(f"Test cases: {len(results)}")
        print(f"Mean latency: {statistics.mean(latencies):.0f}ms")
        print(f"Mean citations: {statistics.mean(citations):.1f}")
        print(f"Max latency: {max(latencies)}ms")
        print(f"All cases passed: {all(r['passed'] for r in results)}")

    @pytest.mark.asyncio
    async def test_business_metrics_calculation(self, graph, dataset):
        """
        Test business impact calculations and ROI projections.
        
        Validates:
        - Handle time reduction calculations
        - Cost per ticket estimates
        - Annual savings projections
        """
        # Run sample of requests to get average metrics
        sample_cases = dataset[:2]  # Use first 2 for speed
        latencies = []

        for test_case in sample_cases:
            result = await graph.generate_response(test_case["complaint"])
            latencies.append(result["latency_ms"])

        # Calculate business metrics
        avg_latency_ms = statistics.mean(latencies)
        avg_latency_min = avg_latency_ms / 60000  # Convert to minutes

        # Business calculations
        original_handle_time = 3.5  # minutes
        ai_assisted_time = original_handle_time - avg_latency_min
        time_reduction = (original_handle_time -
                          ai_assisted_time) / original_handle_time

        # Cost calculations
        agent_cost_per_minute = 0.5  # $0.50 per minute
        tickets_per_year = 12000

        cost_savings = (
            (original_handle_time - ai_assisted_time) *
            agent_cost_per_minute *
            tickets_per_year
        )

        # Churn impact (1% reduction in 5% base churn)
        revenue_per_customer = 150
        customer_base = 25000
        churn_reduction = 0.01  # 1% absolute reduction
        churn_savings = customer_base * churn_reduction * revenue_per_customer

        total_savings = cost_savings + churn_savings

        print(f"\n=== BUSINESS METRICS ===")
        print(
            f"Average response time: {avg_latency_ms:.0f}ms ({avg_latency_min:.2f}min)")
        print(f"Handle time reduction: {time_reduction:.1%}")
        print(f"Labor cost savings: ${cost_savings:,.0f}")
        print(f"Churn reduction savings: ${churn_savings:,.0f}")
        print(f"Total annual savings: ${total_savings:,.0f}")

        # Validate savings target
        assert total_savings >= 250000, f"Savings target not met: ${total_savings:,.0f}"

    @pytest.mark.asyncio
    async def test_specific_scenarios(self, graph):
        """
        Test specific high-value scenarios mentioned in requirements.
        
        Validates:
        - Broken earbud scenario
        - Spanish shipping delay
        - Response appropriateness
        """
        # Test Case A: Broken earbud
        earbud_complaint = "The right earbud stopped charging after one week and your site says I'm not eligible for a return. This is ridiculous."

        result_a = await graph.generate_response(earbud_complaint)

        assert "replacement" in result_a["reply"].lower(
        ), "No replacement offer found"
        assert "apologize" in result_a["reply"].lower(), "No apology found"
        assert len(result_a["citations"]) >= 1, "No citations provided"
        assert result_a["latency_ms"] < 3000, "Latency too high"

        # Test Case B: Spanish shipping delay
        spanish_complaint = "¡Llevo dos semanas esperando mi número de seguimiento! Esto es inaceptable."

        result_b = await graph.generate_response(spanish_complaint)

        assert result_b["reply"], "No response generated"
        assert len(result_b["citations"]) >= 1, "No citations provided"
        assert result_b["latency_ms"] < 3000, "Latency too high"

        print(f"\n=== SCENARIO TESTS ===")
        print(f"Earbud case latency: {result_a['latency_ms']}ms")
        print(f"Spanish case latency: {result_b['latency_ms']}ms")
        print(
            f"Average citations: {(len(result_a['citations']) + len(result_b['citations']))/2:.1f}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
