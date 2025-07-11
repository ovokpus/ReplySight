"""
Vercel serverless function for generating customer service responses.

This function handles HTTP requests to /api/respond and delegates to the
backend WorkflowService for complaint processing.
"""

from typing import Dict, Any
import json
from services import WorkflowService
from models import ComplaintRequest, ResponseOutput
from config import get_settings


def handler(request):
    """
    Vercel serverless function handler for complaint response generation.
    
    Args:
        request: Vercel request object
        
    Returns:
        HTTP response with generated reply, citations, and latency metrics
    """
    
    # Handle CORS for OPTIONS requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': ''
        }
    
    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = json.loads(request.body)
        else:
            # Handle Vercel's request format
            body = request.json
        
        # Create complaint request
        complaint_request = ComplaintRequest(**body)
        
        # Initialize settings and service
        settings = get_settings()
        workflow_service = WorkflowService(tavily_api_key=settings.tavily_api_key)
        
        # Generate response using backend service (sync version)
        import asyncio
        result = asyncio.run(workflow_service.generate_response(complaint_request))
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(result.dict())
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
                'error': f'Error processing complaint: {str(e)}'
            })
        }


# Alternative async handler for better performance
async def async_handler(request):
    """
    Async version of the handler for better performance.
    """
    
    # Handle CORS for OPTIONS requests
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            },
            'body': ''
        }
    
    # Only allow POST requests
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse request body
        if hasattr(request, 'body'):
            body = json.loads(request.body)
        else:
            # Handle Vercel's request format
            body = request.json
        
        # Create complaint request
        complaint_request = ComplaintRequest(**body)
        
        # Initialize settings and service
        settings = get_settings()
        workflow_service = WorkflowService(tavily_api_key=settings.tavily_api_key)
        
        # Generate response using backend service (async)
        result = await workflow_service.generate_response(complaint_request)
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(result.dict())
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
                'error': f'Error processing complaint: {str(e)}'
            })
        } 