"""
Vercel serverless function for health checks.

This function handles HTTP requests to /api/health and delegates to the
backend services for system health monitoring.
"""

from typing import Dict, Any
import json
from backend.services import WorkflowService
from backend.config import get_settings


def handler(request):
    """
    Vercel serverless function handler for health checks.
    
    Args:
        request: Vercel request object
        
    Returns:
        HTTP response with system health status
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
        workflow_service = WorkflowService(tavily_api_key=settings.tavily_api_key)
        
        # Perform comprehensive health check
        workflow_health = workflow_service.health_check()
        
        health_status = {
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
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(health_status)
        }
        
    except Exception as e:
        # Return error response
        error_status = {
            "status": "unhealthy",
            "service": settings.app_name if 'settings' in locals() else "ReplySight",
            "version": settings.app_version if 'settings' in locals() else "unknown",
            "error": str(e)
        }
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps(error_status)
        } 