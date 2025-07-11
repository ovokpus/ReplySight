#!/usr/bin/env python3
"""
Local development server for the ReplySight API.

This script runs the FastAPI application locally for development and testing.
"""

import uvicorn

if __name__ == "__main__":
    # Import and run the FastAPI app
    try:
        from app import app  # Import from api/app.py
    except ImportError:
        # Fallback if the structure is different
        from api.app import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 