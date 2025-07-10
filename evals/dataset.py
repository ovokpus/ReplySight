"""
Evaluation dataset for ReplySight customer service response generation.

This module defines test cases covering various complaint types, languages,
and scenarios to validate system performance and business metrics.
"""

from typing import List, Dict, Any

# Test dataset with diverse complaint scenarios
EVALUATION_DATASET: List[Dict[str, Any]] = [
    {
        "id": "earbud_charging_issue",
        "complaint": "The right earbud stopped charging after one week and your site says I'm not eligible for a return. This is ridiculous.",
        "expected_elements": [
            "apology",
            "replacement_offer",
            "empathy",
            "proactive_solution"
        ],
        "max_latency_ms": 3000,
        "min_citations": 1,
        "priority": "high"
    },
    {
        "id": "shipping_delay_spanish",
        "complaint": "¡Llevo dos semanas esperando mi número de seguimiento! Esto es inaceptable.",
        "expected_elements": [
            "spanish_response",
            "tracking_solution",
            "timeline_commitment"
        ],
        "max_latency_ms": 3000,
        "min_citations": 1,
        "priority": "normal"
    },
    {
        "id": "defective_smartwatch",
        "complaint": "My smartwatch screen went black after 3 days. I paid $299 for this and it's already broken. I want a full refund immediately.",
        "expected_elements": [
            "immediate_refund_offer",
            "quality_acknowledgment",
            "premium_customer_treatment"
        ],
        "max_latency_ms": 3000,
        "min_citations": 1,
        "priority": "high"
    },
    {
        "id": "wrong_item_shipped",
        "complaint": "You sent me black headphones instead of white ones. I specifically ordered white for my setup. This is the second time this has happened.",
        "expected_elements": [
            "correct_item_expedite",
            "repeat_issue_acknowledgment",
            "process_improvement_mention"
        ],
        "max_latency_ms": 3000,
        "min_citations": 1,
        "priority": "normal"
    }
]


def get_evaluation_dataset() -> List[Dict[str, Any]]:
    """
    Get the complete evaluation dataset for testing.
    
    Returns:
        List of test cases with complaints and expected criteria
    """
    return EVALUATION_DATASET


def get_test_case(test_id: str) -> Dict[str, Any]:
    """
    Get a specific test case by ID.
    
    Args:
        test_id: Unique identifier for the test case
        
    Returns:
        Test case dictionary or None if not found
    """
    for case in EVALUATION_DATASET:
        if case["id"] == test_id:
            return case
    return None
