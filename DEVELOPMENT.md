# Local Development Guide

This guide explains how to run ReplySight locally with the unified API structure.

## Project Structure

The project uses a single `api/` directory that contains both:
- **Serverless Functions**: For Vercel deployment (`api/health.py`, `api/respond.py`, etc.)
- **Backend Business Logic**: The core services, models, and configuration (`api/config/`, `api/models/`, etc.)
- **Local Development Server**: `api/server.py` for local FastAPI development

```
ReplySight/
├── api/                    # Unified API directory
│   ├── app.py             # FastAPI application (main app)
│   ├── server.py          # Local development server
│   ├── health.py          # Serverless function for health checks
│   ├── respond.py         # Serverless function for responses  
│   ├── graph.py           # LangGraph workflow orchestration
│   ├── tools.py           # LangChain tools for research
│   ├── workflow/          # Workflow serverless functions
│   │   └── graph.py       # Graph visualization endpoint
│   ├── config/            # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py    # Centralized settings
│   ├── models/            # Data models  
│   │   ├── __init__.py
│   │   ├── api_models.py  # Request/response models
│   │   └── workflow_models.py # Internal workflow models
│   ├── services/          # Core services
│   │   ├── __init__.py
│   │   ├── workflow_service.py # Business logic
│   │   └── graph_service.py    # Graph operations
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── error_handlers.py
│       └── validation_utils.py
├── frontend/              # Next.js frontend
│   ├── src/app/          # App router
│   ├── src/components/   # React components
│   ├── src/hooks/        # Custom hooks
│   ├── src/services/     # API services
│   ├── src/types/        # TypeScript definitions
│   └── src/constants/    # Constants
├── tests/                # Comprehensive test suites
├── .env.development      # Environment template
└── requirements.txt      # Python dependencies
```

## Local Development Setup

### 1. Prerequisites

- **Python 3.11+**: Required for backend
- **Node.js 18.0.0+**: Required for frontend
- **npm 8.0.0+**: Package manager for frontend

### 2. Install Dependencies

```bash
# Python dependencies (from project root)
pip install -r requirements.txt

# Frontend dependencies
cd frontend && npm install
```

### 3. Configure Environment

```bash
# Copy and edit the development environment file
cp .env.development .env.local

# Edit .env.local with your actual API keys:
# - OPENAI_API_KEY=sk-proj-...
# - TAVILY_API_KEY=tvly-...
# - LANGCHAIN_API_KEY=lsv2_... (optional)
# - LANGCHAIN_TRACING_V2=true (optional)
# - LANGCHAIN_PROJECT=replysight-local (optional)
```

### 4. Run the Application

#### Option A: Run Both Services (Recommended)

```bash
# Terminal 1: Start the API server
cd api
python server.py
# Server starts on http://localhost:8000

# Terminal 2: Start the frontend
cd frontend  
npm run dev
# Frontend starts on http://localhost:3000
```

#### Option B: Use npm Scripts (if configured)

```bash
# Start API server (if npm scripts are set up)
npm run dev:api

# Start frontend (in another terminal)
npm run dev:frontend

# Or start both with a process manager (if configured)
npm run dev:full
```

### 5. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Interactive Swagger UI)
- **API ReDoc**: http://localhost:8000/redoc (Alternative API docs)
- **Health Check**: http://localhost:8000/health

## How It Works

### Local Development
- **Frontend**: Next.js dev server on port 3000
- **API**: FastAPI server on port 8000  
- **Communication**: Frontend makes API calls to `http://localhost:8000`

### Vercel Deployment
- **Frontend**: Static Next.js site
- **API**: Serverless functions in `/api/` directory
- **Communication**: Frontend makes API calls to `/api/*` routes

## Development Workflow

### 1. Code Changes
- **Backend changes**: Edit files in `api/` directory
- **Frontend changes**: Edit files in `frontend/src/`
- **Both servers auto-reload**: Changes reflected immediately

### 2. Testing API Endpoints
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test response generation
curl -X POST http://localhost:8000/respond \
  -H "Content-Type: application/json" \
  -d '{"complaint": "Test complaint", "customer_id": "test"}'

# Test workflow graph
curl http://localhost:8000/workflow/graph
```

### 3. Testing Frontend
- Navigate to http://localhost:3000
- Use the complaint form to test response generation
- Check browser developer tools for any errors
- Test workflow visualization at http://localhost:3000/graph

## Key Development Files

- **`api/server.py`** - Local development server (starts FastAPI app)
- **`api/app.py`** - Main FastAPI application with all endpoints
- **`api/config/settings.py`** - Centralized configuration management
- **`frontend/src/services/api.ts`** - Frontend API client
- **`.env.development`** - Environment template (copy to `.env.local`)

## Environment Variables

The application uses the following environment variables:

### Backend Configuration
| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `OPENAI_API_KEY` | Required | Required | OpenAI API key for GPT-4o |
| `TAVILY_API_KEY` | Required | Required | Tavily API key for research |
| `LANGCHAIN_API_KEY` | Optional | Optional | LangSmith API key for tracing |
| `LANGCHAIN_TRACING_V2` | `true` | `true` | Enable LangSmith tracing |
| `LANGCHAIN_PROJECT` | `replysight-local` | `replysight-production` | LangSmith project name |
| `REPLYSIGHT_HOST` | `0.0.0.0` | N/A | Local server host |
| `REPLYSIGHT_PORT` | `8000` | N/A | Local server port |

### Frontend Configuration  
| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `API_BASE_URL` | `http://localhost:8000` | `https://your-app.vercel.app` | Backend API URL |

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   - If port 8000 is busy, edit `api/server.py` to use a different port
   - Or kill the process using port 8000: `lsof -ti:8000 | xargs kill`

2. **Import Errors**
   - Make sure you're running the server from the project root or `api/` directory
   - Verify all dependencies are installed: `pip install -r requirements.txt`

3. **API Keys Missing**
   - Ensure your `.env.local` file has valid API keys
   - Check that environment variables are being loaded correctly

4. **CORS Issues**
   - The FastAPI server is configured for CORS, but check browser console for errors
   - Ensure frontend is making requests to the correct API URL

5. **Frontend Build Errors**
   - Run `npm install` in the frontend directory
   - Check for TypeScript errors: `npm run type-check`
   - Verify all imports are correct

### Debug Commands

```bash
# Check Python environment
python --version
pip list | grep -E "(fastapi|langchain|openai)"

# Check Node.js environment  
node --version
npm --version

# Test individual components
cd api && python -c "from app import app; print('✅ FastAPI app loads successfully')"
cd frontend && npm run build
```

### Performance Tips

1. **Backend Performance**
   - Use `python server.py` for development (auto-reload enabled)
   - Monitor API response times in the browser Network tab
   - Check LangSmith traces for bottlenecks (if enabled)

2. **Frontend Performance**
   - Use `npm run dev` for hot module replacement
   - Check browser developer tools for performance issues
   - Monitor bundle size with `npm run build`

## Advanced Development

### Running Tests

```bash
# Backend tests
python -m pytest tests/ -v

# Frontend tests (if configured)
cd frontend
npm test

# Integration tests
python tests/test_full_workflow.py
```

### Code Quality

```bash
# Python code formatting (if configured)
black api/
isort api/

# Frontend code formatting  
cd frontend
npm run lint
npm run type-check
```

### Environment Switching

```bash
# Development environment
cp .env.development .env.local

# Production testing (local)
cp .env.production .env.local  # if you have this file
```

---

## 🔗 **Related Documentation**

- **[Main Project README](README.md)** - Project overview, quick start, and demo scenarios
- **[API Documentation](api/README.md)** - FastAPI server, LangGraph workflows, and deployment guide
- **[Frontend Documentation](frontend/README.md)** - Next.js interface, components, and user experience
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment and infrastructure setup
- **[Merge Instructions](MERGE.md)** - Current branch status and merge procedures
- **[Test Suite Guide](tests/README.md)** - Testing documentation and test scenarios
- **[License](LICENSE)** - MIT License details

### **External Resources**
- **[GitHub Repository](https://github.com/ovokpus/ReplySight)** - Source code and issues
- **[FastAPI Documentation](https://fastapi.tiangolo.com/)** - FastAPI framework documentation
- **[Next.js Documentation](https://nextjs.org/docs)** - Next.js framework documentation
- **[LangChain Documentation](https://python.langchain.com/)** - LangChain framework documentation
- **[Vercel Documentation](https://vercel.com/docs)** - Deployment platform documentation

---

**Development Status**: ✅ Ready for local development with unified API structure and comprehensive documentation. 