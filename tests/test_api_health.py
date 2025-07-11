#!/usr/bin/env python3
"""
Test script to verify ReplySight API health and configuration.
"""

import sys
import os
from fastapi.testclient import TestClient

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_api_health():
    """Test the API health endpoint and basic functionality."""
    
    print("🔧 Testing ReplySight API Health...")
    
    try:
        # Import the FastAPI app
        from api.app import app
        print("✅ Backend API imported successfully")
        
        # Create a test client
        client = TestClient(app)
        print("✅ FastAPI test client created")
        
        # Test health endpoint
        response = client.get("/health")
        print(f"📡 Health endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Health check passed: {health_data}")
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
        
        # Test metrics endpoint
        response = client.get("/metrics")
        print(f"📊 Metrics endpoint status: {response.status_code}")
        
        if response.status_code == 200:
            metrics_data = response.json()
            print(f"✅ Metrics endpoint working: {metrics_data}")
        else:
            print(f"❌ Metrics endpoint failed with status {response.status_code}")
        
        # Test API documentation
        response = client.get("/docs")
        print(f"📚 Docs endpoint status: {response.status_code}")
        
        print("\n🎉 API health check completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing API: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_individual_components():
    """Test individual components to identify any issues."""
    
    print("\n🔍 Testing individual components...")
    
    try:
        # Test tools import
        from api.tools import ArxivInsightsTool, TavilyExamplesTool, ResponseComposerTool
        print("✅ Tools imported successfully")
        
        # Test graph import
        from api.graph import create_replysight_graph
        print("✅ Graph module imported successfully")
        
        # Test graph creation (without API keys for now)
        graph = create_replysight_graph(tavily_api_key=None)
        print("✅ ReplySight graph created successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing components: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 ReplySight Backend Health Check")
    print("=" * 60)
    
    # Test components first
    components_ok = test_individual_components()
    
    if components_ok:
        # Test API if components are working
        api_ok = test_api_health()
        
        if api_ok:
            print("\n✅ All tests passed! Backend is ready.")
            sys.exit(0)
        else:
            print("\n❌ API tests failed.")
            sys.exit(1)
    else:
        print("\n❌ Component tests failed.")
        sys.exit(1) 