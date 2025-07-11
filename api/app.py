"""
Vercel serverless function entry point for ReplySight API.

This file serves as the main entry point for all API routes, routing requests
to the appropriate handlers based on the URL path.
"""

import json
from urllib.parse import urlparse, parse_qs

# Import our existing handlers
from health import handler as health_handler
from respond import handler as respond_handler
from workflow.graph import handler as workflow_graph_handler


def handler(request):
    """
    Main Vercel serverless function handler that routes requests to appropriate endpoints.
    
    Args:
        request: Vercel request object
        
    Returns:
        HTTP response from the appropriate handler
    """
    
    # Get the path from the request
    path = getattr(request, 'path', '') or getattr(request, 'url', '')
    
    # Parse the path to determine routing
    if path.startswith('/api/'):
        path = path[4:]  # Remove /api/ prefix
    
    # Route based on path
    if path == 'health' or path == '/health':
        return health_handler(request)
    elif path == 'respond' or path == '/respond':
        return respond_handler(request)
    elif path == 'workflow/graph' or path == '/workflow/graph':
        return workflow_graph_handler(request)
    else:
        # Default 404 response for unknown paths
        return {
            'statusCode': 404,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json',
            },
            'body': json.dumps({
                'error': 'Endpoint not found',
                'path': path,
                'available_endpoints': ['/health', '/respond', '/workflow/graph']
            })
        } 