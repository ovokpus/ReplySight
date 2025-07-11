# Vercel Full-Stack Deployment Guide

## Overview

This guide explains how to deploy the ReplySight application to Vercel with a complete full-stack setup using serverless functions.

## Architecture

```
ReplySight Vercel Deployment
├── Frontend (Next.js)
│   ├── Deployed as static site
│   ├── Handles UI and client-side logic
│   └── Consumes API endpoints
├── Backend (Serverless Functions)
│   ├── /api/respond.py → Complaint response generation
│   ├── /api/health.py → Health check endpoint
│   └── /api/workflow/graph.py → Workflow visualization
└── Backend Library
    ├── backend/ → Business logic (imported by functions)
    ├── models/ → Data models
    └── services/ → Core services
```

## Deployment Steps

### 1. Prepare the Repository

Your repository is already configured with:
- ✅ Serverless functions in `/api/` directory
- ✅ Updated `vercel.json` with functions and rewrites
- ✅ Frontend configuration for Vercel deployment
- ✅ Optimized `requirements.txt` for functions
- ✅ `.vercelignore` for deployment optimization

### 2. Deploy to Vercel

#### Option A: Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from repository root
vercel

# Follow prompts to connect to your Vercel account
```

#### Option B: Using GitHub Integration

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "New Project"
3. Import your GitHub repository
4. Vercel will automatically detect the configuration

### 3. Configure Environment Variables

In your Vercel dashboard, add these environment variables:

#### Required Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `OPENAI_API_KEY` | `sk-proj-...` | OpenAI API key for GPT-4o |
| `TAVILY_API_KEY` | `tvly-...` | Tavily API key for research |
| `LANGCHAIN_API_KEY` | `lsv2_...` | LangSmith API key |
| `LANGCHAIN_TRACING_V2` | `true` | Enable LangSmith tracing |
| `LANGCHAIN_ENDPOINT` | `https://api.smith.langchain.com` | LangSmith endpoint |
| `LANGCHAIN_PROJECT` | `replysight-production` | LangSmith project name |

#### Optional Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `ENVIRONMENT` | `production` | Environment identifier |
| `API_BASE_URL` | `https://your-app.vercel.app` | Base URL for API calls |

### 4. Domain Configuration

- Your app will be available at `https://your-app-name.vercel.app`
- You can configure a custom domain in the Vercel dashboard

## API Endpoints

Once deployed, your API endpoints will be available at:

- `https://your-app.vercel.app/api/respond` - Generate complaint responses
- `https://your-app.vercel.app/api/health` - Health check
- `https://your-app.vercel.app/api/workflow/graph` - Workflow visualization

## Verification

### 1. Health Check

```bash
curl https://your-app.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ReplySight",
  "version": "1.0.0",
  "workflow": {...},
  "dependencies": {
    "openai": true,
    "tavily": true,
    "langsmith": true
  }
}
```

### 2. Frontend Access

Visit `https://your-app.vercel.app` to access the main application.

### 3. API Functionality

Test the complaint response generation:

```bash
curl -X POST https://your-app.vercel.app/api/respond \
  -H "Content-Type: application/json" \
  -d '{
    "complaint": "I received a damaged product",
    "customer_id": "test-customer",
    "priority": "high"
  }'
```

## File Structure

```
ReplySight/
├── api/                    # Unified API directory (serverless + business logic)
│   ├── respond.py         # Main complaint processing function
│   ├── health.py          # Health monitoring function
│   ├── app.py             # FastAPI application (for local dev)
│   ├── server.py          # Local development server
│   ├── graph.py           # LangGraph workflow orchestration
│   ├── tools.py           # LangChain research tools
│   ├── workflow/          # Workflow serverless functions
│   │   └── graph.py       # Graph visualization endpoint
│   ├── config/            # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py    # Centralized settings
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   ├── api_models.py  # Request/response models
│   │   └── workflow_models.py # Internal workflow models
│   ├── services/          # Core business logic
│   │   ├── __init__.py
│   │   ├── workflow_service.py # Workflow orchestration
│   │   └── graph_service.py    # Graph operations
│   └── utils/             # Utility functions
│       ├── __init__.py
│       ├── error_handlers.py
│       └── validation_utils.py
├── frontend/              # Next.js application
│   ├── src/app/          # App router
│   ├── src/components/   # React components
│   ├── src/hooks/        # Custom hooks
│   ├── src/services/     # API services
│   ├── src/types/        # TypeScript definitions
│   └── src/constants/    # Constants
├── tests/                # Comprehensive test suites
├── vercel.json           # Vercel deployment configuration
├── requirements.txt      # Python dependencies for all environments
├── .vercelignore         # Files to exclude from deployment
└── .env.development      # Environment template
```

## Troubleshooting

### Common Issues

#### 1. Function Timeout

If functions timeout, check:
- API key validity
- Network connectivity
- LangChain service availability

#### 2. Import Errors

If you see import errors:
- Verify `requirements.txt` includes all dependencies
- Check that backend code is properly structured

#### 3. CORS Issues

CORS is handled in each function. If you encounter issues:
- Verify `Access-Control-Allow-Origin` headers
- Check that OPTIONS requests are handled

#### 4. Environment Variables

If functions can't access environment variables:
- Verify variables are set in Vercel dashboard
- Check variable names match exactly
- Ensure variables are available to functions

### Debug Steps

1. **Check Function Logs**
   - Go to Vercel Dashboard → Functions → View logs
   - Look for Python errors or import issues

2. **Test Individual Endpoints**
   - Use curl or Postman to test each API endpoint
   - Check response status codes and error messages

3. **Verify Dependencies**
   - Ensure all required packages are in `requirements.txt`
   - Check for version compatibility issues

## Performance Optimization

### Cold Start Optimization

- Functions are optimized for minimal cold start time
- Only essential dependencies included in `requirements.txt`
- Lightweight imports in function handlers

### Caching Strategy

- Frontend assets cached by Vercel CDN
- API responses can be cached based on request patterns
- Static assets optimized for performance

## Monitoring

### Built-in Monitoring

- Vercel provides automatic monitoring
- Function execution metrics available in dashboard
- Real-time error tracking

### LangSmith Integration

- All AI operations traced in LangSmith
- Performance metrics and debugging available
- Custom project tracking enabled

## Security

### Environment Variables

- All sensitive data stored as environment variables
- No hardcoded secrets in code
- Proper access controls in place

### CORS Configuration

- Proper CORS headers for all endpoints
- Secure cross-origin request handling
- Options preflight handling

## Scaling

### Automatic Scaling

- Vercel automatically scales based on traffic
- No manual scaling configuration needed
- Pay-per-use pricing model

### Resource Limits

- Functions have memory and execution time limits
- Monitor usage in Vercel dashboard
- Upgrade plan if needed for higher limits

## Support

For deployment issues:
1. Check Vercel documentation
2. Review function logs in dashboard
3. Test API endpoints individually
4. Verify environment variable configuration

---

**Deployment Status**: ✅ Ready for full-stack deployment to Vercel

The application is now fully configured for Vercel deployment with:
- Complete serverless function setup
- Optimized build configuration
- Proper environment variable handling
- Frontend and backend integration
- Comprehensive error handling and CORS support

---

## 🔗 **Related Documentation**

- **[Main Project README](README.md)** - Project overview, quick start, and demo scenarios
- **[API Documentation](api/README.md)** - FastAPI server, LangGraph workflows, and deployment guide
- **[Frontend Documentation](frontend/README.md)** - Next.js interface, components, and user experience
- **[Development Guide](DEVELOPMENT.md)** - Local development setup and project structure
- **[Merge Instructions](MERGE.md)** - Current branch status and merge procedures
- **[Test Suite Guide](tests/README.md)** - Testing documentation and test scenarios
- **[License](LICENSE)** - MIT License details

### **External Resources**
- **[GitHub Repository](https://github.com/ovokpus/ReplySight)** - Source code and issues
- **[Vercel Documentation](https://vercel.com/docs)** - Deployment platform documentation
- **[Vercel CLI](https://vercel.com/cli)** - Command-line interface for deployment
- **[Railway Documentation](https://docs.railway.app/)** - Alternative deployment platform
- **[FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)** - FastAPI deployment best practices

---

**Deployment Ready**: ✅ All systems configured for production deployment to Vercel with full-stack integration. 