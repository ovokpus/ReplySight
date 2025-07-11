"""
Vercel serverless function for workflow graph visualization.

This function handles HTTP requests to /api/workflow/graph and delegates to the
backend GraphService for workflow diagram generation.
"""

from typing import Dict, Any
import json
from ..services import GraphService
from ..config import get_settings


def handler(request):
    """
    Vercel serverless function handler for workflow graph visualization.
    
    Args:
        request: Vercel request object
        
    Returns:
        HTTP response with Mermaid diagram, metadata, and graph structure
    """
    
    # Handle CORS for OPTIONS requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': ''
        }
    
    # Only allow GET requests
    if request.method != 'GET':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Initialize settings and service
        settings = get_settings()
        graph_service = GraphService(tavily_api_key=settings.tavily_api_key)
        
        # Get workflow metadata
        metadata = graph_service.get_workflow_metadata()
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(metadata)
        }
        
    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'error': f'Error generating workflow visualization: {str(e)}'
            })
        } 