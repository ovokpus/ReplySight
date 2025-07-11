#!/usr/bin/env python3
"""
Local development server for ReplySight API.
Runs the FastAPI application with uvicorn for local development.
"""

import uvicorn
from backend.api import app

if __name__ == "__main__":
    print("Starting ReplySight API server...")
    print("API will be available at: http://localhost:8000")
    print("Health check: http://localhost:8000/health")
    print("API docs: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 