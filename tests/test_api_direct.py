"""
Direct test of the ReplySight API endpoints without running uvicorn server.
This tests the OpenAI integration directly.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from backend.api import respond_to_complaint, ComplaintRequest

async def test_api_directly():
    """Test the API endpoint function directly."""
    print("🧪 Testing ReplySight API directly with OpenAI...")
    print("=" * 50)
    
    # Check environment variables
    openai_key = os.getenv('OPENAI_API_KEY')
    tavily_key = os.getenv('TAVILY_API_KEY')
    
    print(f"OpenAI Key: {'✅ SET' if openai_key and openai_key != 'your_openai_api_key_here' else '❌ NOT SET'}")
    print(f"Tavily Key: {'✅ SET' if tavily_key and tavily_key != 'your_tavily_api_key_here' else '❌ NOT SET'}")
    
    # Create test request
    test_request = ComplaintRequest(
        complaint="My wireless earbuds stopped working after just 1 week. The sound quality was terrible and now they won't charge at all. This is completely unacceptable for a $120 product!",
        customer_id="test-user-123",
        priority="high"
    )
    
    print(f"\n📝 Test Complaint: {test_request.complaint}")
    print("\n⚙️  Processing through ReplySight API...")
    
    try:
        # Call the API function directly
        response = await respond_to_complaint(test_request)
        
        print(f"\n✅ API Response Generated!")
        print("=" * 50)
        print(f"⏱️  Latency: {response.latency_ms}ms")
        print(f"📄 Citations: {len(response.citations)}")
        
        print(f"\n💬 Generated Response:")
        print("-" * 40)
        print(response.reply)
        print("-" * 40)
        
        # Check if it's OpenAI generated or fallback
        if "I sincerely apologize for the inconvenience you've experienced" in response.reply:
            print("\n🤖 Response Type: Fallback Template")
            print("   → OpenAI API call likely failed")
        else:
            print("\n🎯 Response Type: OpenAI Generated")
            print("   → GPT-4o-mini successfully generated response!")
            
        if response.citations:
            print(f"\n📚 Citations:")
            for i, citation in enumerate(response.citations, 1):
                print(f"   {i}. {citation}")
                
        return response
        
    except Exception as e:
        print(f"\n❌ API Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(test_api_directly()) 