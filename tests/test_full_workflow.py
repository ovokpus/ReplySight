"""
Complete workflow test for ReplySight with OpenAI integration.

This script tests the full end-to-end workflow including:
- arXiv research insights fetching
- Tavily best practice examples
- OpenAI GPT-4o-mini response generation
- Citation assembly and latency tracking
"""

import os
import asyncio
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.append('..')
from backend.graph import create_replysight_graph

async def test_workflow():
    """Test the complete workflow with a sample complaint."""
    print("🧪 Testing complete ReplySight workflow with OpenAI...")
    print("=" * 60)
    
    # Check if API keys are set
    openai_key = os.getenv('OPENAI_API_KEY')
    tavily_key = os.getenv('TAVILY_API_KEY')
    
    if not openai_key or openai_key == 'your_openai_api_key_here':
        print("⚠️  No OpenAI API key found - will use fallback responses")
    else:
        print("✅ OpenAI API key detected")
        
    if not tavily_key or tavily_key == 'your_tavily_api_key_here':
        print("⚠️  No Tavily API key found - will use mock data")
    else:
        print("✅ Tavily API key detected")
    
    try:
        # Create the graph
        graph = create_replysight_graph(tavily_api_key=tavily_key)
        print("✅ Graph created successfully")
        
        # Test with a sample complaint
        test_complaint = "My charging cable stopped working after just 2 weeks. This is ridiculous! I expected better quality from your company and I'm really disappointed."
        
        print(f"\n📝 Test complaint: {test_complaint}")
        print("\n⚙️  Processing through ReplySight workflow...")
        print("   1. Fetching arXiv research insights...")
        print("   2. Retrieving Tavily best practice examples...")
        print("   3. Generating AI-powered response...")
        
        # Run the workflow
        result = await graph.generate_response(test_complaint)
        
        print(f"\n✅ Workflow completed successfully!")
        print("=" * 60)
        print(f"⏱️  Response Time: {result['latency_ms']}ms")
        print(f"📄 Citations Found: {len(result['citations'])} sources")
        
        print(f"\n💬 Generated Response:")
        print("-" * 40)
        print(result['reply'])
        print("-" * 40)
        
        # Analyze response quality
        response_text = result['reply'].lower()
        quality_indicators = {
            'Empathy': any(word in response_text for word in ['understand', 'apologize', 'sorry', 'frustrated']),
            'Personalization': len(result['reply']) > 100,
            'Solution-focused': any(word in response_text for word in ['will', 'arrange', 'resolve', 'fix', 'replace']),
            'Professional tone': 'thank you' in response_text or 'please' in response_text,
        }
        
        print(f"\n📊 Response Quality Analysis:")
        for indicator, present in quality_indicators.items():
            status = "✅" if present else "❌"
            print(f"   {status} {indicator}")
        
        # Check if it's using AI or fallback
        if "I sincerely apologize for the inconvenience you've experienced" in result['reply']:
            print("\n🤖 Response Type: OpenAI Fallback (template)")
            print("   → This indicates the OpenAI API call failed or API key issues")
        else:
            print("\n🎯 Response Type: OpenAI Generated")
            print("   → Successfully using GPT-4o-mini for dynamic responses!")
            
        # Show citations if available
        if result['citations']:
            print(f"\n📚 Sources Referenced:")
            for i, citation in enumerate(result['citations'][:3], 1):
                if citation:
                    print(f"   {i}. {citation}")
        
        return True
            
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        print("\nDebugging tips:")
        print("• Check your .env file has OPENAI_API_KEY set")
        print("• Verify your OpenAI API key is valid")
        print("• Ensure you have sufficient OpenAI credits")
        print("• Check network connectivity")
        return False

async def test_multiple_scenarios():
    """Test with different types of complaints."""
    scenarios = [
        {
            "name": "Product Defect",
            "complaint": "My headphones broke after 1 month. The sound quality was terrible from day one."
        },
        {
            "name": "Shipping Issue", 
            "complaint": "I ordered my package 2 weeks ago and still no tracking information. Where is my order?"
        },
        {
            "name": "Billing Problem",
            "complaint": "I was charged twice for the same order. This is unacceptable! I want my money back immediately."
        }
    ]
    
    print(f"\n🎭 Testing Multiple Complaint Scenarios...")
    print("=" * 60)
    
    graph = create_replysight_graph(tavily_api_key=os.getenv('TAVILY_API_KEY'))
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"💬 Complaint: {scenario['complaint']}")
        
        try:
            result = await graph.generate_response(scenario['complaint'])
            response_preview = result['reply'][:80] + "..." if len(result['reply']) > 80 else result['reply']
            print(f"✅ Response: {response_preview}")
            print(f"⏱️  Time: {result['latency_ms']}ms")
        except Exception as e:
            print(f"❌ Failed: {e}")

if __name__ == "__main__":
    """Run the complete test suite."""
    print("🚀 ReplySight Full Workflow Test Suite")
    print("=" * 60)
    
    async def run_all_tests():
        # Main workflow test
        success = await test_workflow()
        
        if success:
            # Multiple scenarios test
            await test_multiple_scenarios()
            
            print("\n" + "=" * 60)
            print("🎉 All tests completed! ReplySight is ready to handle customer complaints!")
            print("💡 Pro tip: Monitor your OpenAI usage in the dashboard")
        else:
            print("\n" + "=" * 60)
            print("🔧 Please fix the issues above and try again")
    
    asyncio.run(run_all_tests()) 