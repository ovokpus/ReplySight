# ReplySight Test Suite

This directory contains comprehensive tests for the ReplySight backend system and integration workflows.

## Test Structure

### Backend Tests
- **`test_api_health.py`** - Tests API health, metrics, and documentation endpoints
- **`test_respond_endpoint.py`** - Tests the main `/respond` endpoint functionality
- **`test_api_direct.py`** - Direct API testing and validation
- **`test_full_workflow.py`** - End-to-end workflow testing
- **`test_openai_integration.py`** - OpenAI integration testing
- **`test_parallel_tools.py`** - Parallel tool execution testing

### Test Utilities
- **`run_all_tests.py`** - Test runner that executes all tests

## Running Tests

### Run All Tests
```bash
# From the project root
python -m pytest tests/ -v

# Or using the test runner
python tests/run_all_tests.py
```

### Run Individual Test Files
```bash
# Test API health and monitoring
python -m pytest tests/test_api_health.py -v

# Test main response endpoint
python -m pytest tests/test_respond_endpoint.py -v

# Test full workflow integration
python -m pytest tests/test_full_workflow.py -v

# Test OpenAI integration
python -m pytest tests/test_openai_integration.py -v

# Test parallel tool execution
python -m pytest tests/test_parallel_tools.py -v
```

### Run Specific Test Categories
```bash
# Run tests with specific markers (if configured)
python -m pytest tests/ -m "integration" -v
python -m pytest tests/ -m "unit" -v
python -m pytest tests/ -m "api" -v
```

## Test Coverage

The test suite provides comprehensive coverage of:

### 1. Component Integration
- ✅ **ArxivInsightsTool** - Import, initialization, and functionality
- ✅ **TavilyExamplesTool** - Import, initialization, and functionality
- ✅ **ResponseComposerTool** - Import, initialization, and functionality
- ✅ **LangGraph Workflow** - Graph creation and compilation
- ✅ **Service Layer** - Business logic and service integration

### 2. API Endpoints
- ✅ **`/health`** - Health check endpoint functionality
- ✅ **`/respond`** - Main response generation endpoint
- ✅ **`/workflow/graph`** - Workflow visualization endpoint
- ✅ **Error Handling** - Proper error responses and status codes
- ✅ **CORS Configuration** - Cross-origin request handling

### 3. End-to-End Workflows
- ✅ **Complete Complaint Processing** - Full pipeline execution
- ✅ **Response Generation** - AI-powered response creation
- ✅ **Citation Integration** - Academic and web source citations
- ✅ **Latency Tracking** - Performance measurement
- ✅ **Quality Assurance** - Response quality validation

### 4. Integration Testing
- ✅ **OpenAI API Integration** - LLM communication and responses
- ✅ **Tavily Search Integration** - Web research functionality
- ✅ **ArXiv API Integration** - Academic research retrieval
- ✅ **LangSmith Tracing** - Observability and monitoring

## Test Environment Setup

### Prerequisites
```bash
# Ensure you have the required environment variables
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
LANGCHAIN_API_KEY=your_langsmith_key  # Optional
```

### Installation
```bash
# Install test dependencies (included in requirements.txt)
pip install -r requirements.txt

# Or install specific testing tools
pip install pytest pytest-asyncio pytest-mock
```

### Configuration
```bash
# Copy environment template for testing
cp .env.development .env.test

# Edit .env.test with test-specific configurations
# You can use the same API keys as development
```

## Expected Test Results

When all tests pass, you should see output similar to:

```bash
========================= test session starts =========================
tests/test_api_health.py::test_health_endpoint PASSED           [ 16%]
tests/test_api_health.py::test_health_response_format PASSED    [ 33%]
tests/test_respond_endpoint.py::test_respond_endpoint PASSED    [ 50%]
tests/test_respond_endpoint.py::test_response_format PASSED     [ 66%]
tests/test_full_workflow.py::test_complete_workflow PASSED     [ 83%]
tests/test_full_workflow.py::test_citation_generation PASSED   [100%]

========================= 6 passed in 45.67s =========================
```

### Key Success Indicators
- ✅ **All components import successfully** - No import errors
- ✅ **API endpoints return expected status codes** - 200, 404, 500 as appropriate
- ✅ **Generated responses include citations** - Academic and web sources
- ✅ **Latency measurements are recorded** - Performance tracking works
- ✅ **Business metrics are calculated** - ROI and efficiency metrics

## Test Scenarios

### Basic Functionality Tests
```python
# Simple complaint processing
test_complaints = [
    "My order arrived damaged",
    "The product stopped working after one week",
    "I haven't received my refund yet",
    "Customer service was unresponsive"
]
```

### Advanced Integration Tests
```python
# Complex scenarios
advanced_scenarios = [
    "Multi-language complaint testing",
    "Accessibility-focused responses",
    "High-priority escalation handling",
    "Edge case error handling"
]
```

### Performance Tests
```python
# Latency and throughput testing
performance_metrics = {
    "response_time_target": "< 20 seconds",
    "citation_count_min": 2,
    "helpfulness_score_min": 0.7
}
```

## Troubleshooting Test Issues

### Common Test Failures

#### 1. API Key Issues
```bash
# Verify API keys are set
echo $OPENAI_API_KEY
echo $TAVILY_API_KEY

# Check if keys are valid
curl -H "Authorization: Bearer $OPENAI_API_KEY" https://api.openai.com/v1/models
```

#### 2. Import Errors
```bash
# Ensure you're running tests from project root
cd /path/to/ReplySight
python -m pytest tests/

# Check Python path and dependencies
python -c "import sys; print('\n'.join(sys.path))"
pip list | grep -E "(fastapi|langchain|openai|tavily)"
```

#### 3. Network/API Failures
```bash
# Check internet connectivity
ping api.openai.com
ping api.tavily.com

# Verify API services are available
curl -s https://api.openai.com/v1/models | head -20
```

#### 4. Port Conflicts
```bash
# Ensure no other services are running on test ports
lsof -ti:8000-8001 | xargs kill  # Kill processes on ports 8000-8001

# Or use different ports for testing
export TEST_PORT=8002
```

### Debug Mode Testing
```bash
# Run tests with verbose output and debugging
python -m pytest tests/ -v -s --tb=long

# Run single test with maximum verbosity
python -m pytest tests/test_respond_endpoint.py::test_respond_endpoint -vvv -s
```

## Continuous Integration

### GitHub Actions (if configured)
The test suite is designed to work with CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
name: Test Suite
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/ -v
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          TAVILY_API_KEY: ${{ secrets.TAVILY_API_KEY }}
```

## Test Development

### Adding New Tests
When adding new functionality, include corresponding tests:

```python
# Example test structure
def test_new_feature():
    """Test description."""
    # Arrange
    test_input = "test data"
    expected_output = "expected result"
    
    # Act
    result = new_feature(test_input)
    
    # Assert
    assert result == expected_output
    assert "citation" in result
    assert len(result) > 0
```

### Best Practices
- **Descriptive Names**: Use clear, descriptive test function names
- **Isolated Tests**: Each test should be independent
- **Mocking**: Mock external API calls when appropriate
- **Coverage**: Aim for comprehensive test coverage
- **Performance**: Test both functionality and performance
- **Error Cases**: Include tests for error conditions

## Performance Benchmarks

### Target Metrics
- **Response Generation**: < 20 seconds end-to-end
- **API Health Check**: < 1 second
- **Workflow Graph**: < 2 seconds
- **Citation Count**: ≥ 2 sources per response
- **Success Rate**: ≥ 95% for valid inputs

### Load Testing
```bash
# Example load testing (if tools are available)
# pip install locust
# locust -f tests/load_test.py --host=http://localhost:8000
```

---

**Testing Status**: ✅ Comprehensive test suite covering all major functionality, integration points, and performance requirements.

---

## 🔗 **Related Documentation**

- **[Main Project README](../README.md)** - Project overview, quick start, and demo scenarios
- **[API Documentation](../api/README.md)** - FastAPI server, LangGraph workflows, and deployment guide  
- **[Frontend Documentation](../frontend/README.md)** - Next.js interface, components, and user experience
- **[Development Guide](../DEVELOPMENT.md)** - Local development setup and project structure
- **[Deployment Guide](../DEPLOYMENT.md)** - Production deployment and infrastructure
- **[License](../LICENSE)** - MIT License details

### **External Resources**
- **[GitHub Repository](https://github.com/ovokpus/ReplySight)** - Source code and issues
- **[GitHub Issues](https://github.com/ovokpus/ReplySight/issues)** - Bug reports and feature requests
- **[PyTest Documentation](https://docs.pytest.org/)** - Testing framework documentation
- **[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)** - API testing best practices
- **[LangChain Testing](https://python.langchain.com/docs/guides/testing/)** - AI workflow testing guidance 