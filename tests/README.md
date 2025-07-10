# ReplySight Test Suite

This directory contains comprehensive tests for the ReplySight backend system.

## Test Files

- **`test_api_health.py`** - Tests API health, metrics, and documentation endpoints
- **`test_respond_endpoint.py`** - Tests the main `/respond` endpoint functionality
- **`run_all_tests.py`** - Test runner that executes all tests

## Running Tests

### Run All Tests
```bash
# From the project root
uv run python tests/run_all_tests.py
```

### Run Individual Tests
```bash
# Test API health
uv run python tests/test_api_health.py

# Test respond endpoint
uv run python tests/test_respond_endpoint.py
```

## Test Coverage

The test suite covers:

1. **Component Integration**
   - ArxivInsightsTool import and initialization
   - TavilyExamplesTool import and initialization  
   - ResponseComposerTool import and initialization
   - LangGraph workflow creation

2. **API Endpoints**
   - `/health` - Health check endpoint
   - `/metrics` - Business metrics endpoint
   - `/docs` - API documentation endpoint
   - `/respond` - Main response generation endpoint

3. **End-to-End Workflow**
   - Complete complaint processing
   - Response generation with citations
   - Latency tracking
   - Error handling

## Expected Results

When all tests pass, you should see:

- ✅ All components import successfully
- ✅ API endpoints return expected status codes
- ✅ Generated responses include citations
- ✅ Latency measurements are recorded
- ✅ Business metrics are calculated

## Troubleshooting

If tests fail:

1. Ensure virtual environment is activated: `source .venv/bin/activate`
2. Check dependencies are installed: `uv sync`
3. Verify environment variables are set (see `.env_sample`)
4. Check that no other services are running on port 8000-8001 