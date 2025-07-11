# Local Development Guide

This guide explains how to run ReplySight locally with the new merged API structure.

## Project Structure

After merging, the project now has a single `api/` directory that contains both:
- **Serverless Functions**: For Vercel deployment (`api/health.py`, `api/respond.py`, etc.)
- **Backend Business Logic**: The core services, models, and configuration (`api/backend/`)

```
ReplySight/
├── api/                    # Merged API directory
│   ├── health.py          # Serverless function for health checks
│   ├── respond.py         # Serverless function for responses
│   ├── workflow/          # Workflow serverless functions
│   │   └── graph.py       # Graph visualization endpoint
│   ├── backend/           # Backend business logic
│   │   ├── services/      # Core services
│   │   ├── models/        # Data models
│   │   ├── config/        # Configuration
│   │   └── app.py         # FastAPI application
│   └── server.py          # Local development server
├── frontend/              # Next.js frontend
└── .env.development       # Local development environment
```

## Local Development Setup

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend && npm install
```

### 2. Configure Environment

```bash
# Copy and edit the development environment file
cp .env.development .env.local

# Edit .env.local with your actual API keys:
# - OPENAI_API_KEY
# - TAVILY_API_KEY
# - LANGCHAIN_API_KEY (optional)
```

### 3. Run the Application

#### Option A: Run Both Services (Recommended)

```bash
# Terminal 1: Start the API server
cd api
python server.py

# Terminal 2: Start the frontend
cd frontend
npm run dev
```

#### Option B: Use the Root Scripts

```bash
# Start API server
npm run dev:api

# Start frontend (in another terminal)
npm run dev:frontend

# Or start both with a process manager
npm run dev:full
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
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

## Key Files

- `api/server.py` - Local development server
- `api/app.py` - FastAPI application
- `frontend/services/api.ts` - Frontend API client
- `.env.development` - Development environment template

## Environment Variables

The application uses the following environment variables:

| Variable | Development | Production |
|----------|-------------|------------|
| `API_BASE_URL` | `http://localhost:8000` | `https://your-app.vercel.app` |
| `NEXT_PUBLIC_API_BASE_URL` | `http://localhost:8000` | `https://your-app.vercel.app` |
| `OPENAI_API_KEY` | Your OpenAI API key | Same |
| `TAVILY_API_KEY` | Your Tavily API key | Same |
| `LANGCHAIN_API_KEY` | Your LangSmith API key | Same |

## Troubleshooting

1. **Port Already in Use**: If port 8000 is busy, edit `api/server.py` to use a different port
2. **Import Errors**: Make sure you're running the server from the `api/` directory
3. **API Keys**: Ensure your `.env.local` file has valid API keys
4. **CORS Issues**: The FastAPI server is configured for CORS, but check browser console for errors

## Development Workflow

1. Make changes to backend code in `api/backend/`
2. FastAPI server will auto-reload (thanks to `reload=True`)
3. Make changes to frontend code in `frontend/`
4. Next.js will auto-reload with hot module replacement
5. Test API endpoints at `http://localhost:8000/docs`
6. Test full application at `http://localhost:3000` 