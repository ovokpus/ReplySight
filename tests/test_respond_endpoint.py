#!/usr/bin/env python3
"""
Test script to verify the /respond endpoint functionality.
"""

import sys
import os
from fastapi.testclient import TestClient

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

def test_respond_endpoint():
    """Test the main /respond endpoint."""
    
    print("🔧 Testing /respond endpoint...")
    
    try:
        # Import the FastAPI app
        from api.app import app
        
        # Create a test client
        client = TestClient(app)
        
        # Test data
        test_complaint = {
            "complaint": "My earbuds stopped charging after one week. This is unacceptable!",
            "customer_id": "test_customer_123",
            "priority": "high"
        }
        
        print(f"📤 Sending test complaint: {test_complaint['complaint'][:50]}...")
        
        # Make the request
        response = client.post("/respond", json=test_complaint)
        
        print(f"📡 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            
            print("✅ Response received successfully!")
            print(f"📝 Reply length: {len(data.get('reply', ''))} characters")
            print(f"📚 Citations count: {len(data.get('citations', []))}")
            print(f"⏱️  Latency: {data.get('latency_ms', 0)}ms")
            
            print("\n--- Generated Response ---")
            print(data.get('reply', 'No reply'))
            
            if data.get('citations'):
                print("\n--- Citations ---")
                for i, citation in enumerate(data.get('citations', []), 1):
                    print(f"{i}. {citation}")
            
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Error details: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing /respond endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Testing ReplySight /respond Endpoint")
    print("=" * 60)
    
    success = test_respond_endpoint()
    
    if success:
        print("\n✅ /respond endpoint test passed!")
        sys.exit(0)
    else:
        print("\n❌ /respond endpoint test failed!")
        sys.exit(1) 