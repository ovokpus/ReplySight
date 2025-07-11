# ReplySight Frontend

> **AI-Powered Customer Service Response Generation Interface**

A modern, responsive Next.js application that provides an intuitive interface for generating empathetic, research-backed customer service responses using advanced AI workflows.

## 🎯 Overview

ReplySight Frontend is a React-based web application built with Next.js that connects to the ReplySight AI backend to generate professional customer service responses. The application features a clean, modern UI with real-time response generation, citation tracking, and workflow visualization.

## ✨ Key Features

### Core Functionality
- **🤖 AI Response Generation**: Generate empathetic customer service responses using GPT-4o
- **📚 Research-Backed**: Responses include academic citations and web research
- **⚡ Real-Time Processing**: Live response generation with latency tracking
- **🎨 Professional UI**: Clean, modern interface with responsive design
- **📊 Workflow Visualization**: Interactive Mermaid diagrams of AI workflow
- **📋 Copy & Generate**: Easy response copying and regeneration

### Technical Features
- **🔧 TypeScript**: Full TypeScript implementation for type safety
- **🎨 Tailwind CSS**: Modern styling with custom design system
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **🚀 Performance**: Optimized bundle size and fast loading
- **🔗 API Integration**: Seamless backend communication
- **⚠️ Error Handling**: Comprehensive error states and loading indicators

## 🏗️ Architecture

### Project Structure
```
frontend/
├── app/                    # Next.js App Router
│   ├── api/               # API routes (proxy to backend)
│   │   └── respond/       # Customer response generation
│   ├── graph/             # Workflow visualization page
│   ├── workflow/          # Alternative workflow route
│   ├── layout.tsx         # Root layout component
│   ├── page.tsx           # Main chat interface
│   └── globals.css        # Global styles
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components (buttons, cards, etc.)
│   ├── ErrorState.tsx    # Error display component
│   ├── LoadingState.tsx  # Loading indicator component
│   ├── PageHeader.tsx    # Page header component
│   ├── StatCard.tsx      # Statistics card component
│   ├── StatsGrid.tsx     # Stats grid layout
│   └── WorkflowVisualization.tsx # Workflow diagram component
├── hooks/                 # Custom React hooks
│   ├── useComplaintForm.ts # Form state management
│   ├── useGraphData.ts    # Graph data fetching
│   └── useMermaid.ts      # Mermaid diagram rendering
├── lib/                   # Utility functions
│   └── utils.ts          # Tailwind class utilities
├── services/             # API services
│   └── api.ts           # Backend API communication
├── types/                # TypeScript type definitions
│   └── index.ts         # Shared type definitions
└── constants/            # Application constants
    └── index.ts         # UI constants and configuration
```

### Component Architecture

#### Core Components
- **Main Interface** (`app/page.tsx`): Primary chat interface with form and response display
- **Workflow Visualization** (`components/WorkflowVisualization.tsx`): Interactive diagram rendering
- **Response Display**: Markdown-formatted customer service responses
- **Citation System**: Academic reference display with proper formatting

#### UI Components
- **StatCard**: Displays key metrics (AI model, response time, etc.)
- **LoadingState**: Animated loading indicators with contextual messages
- **ErrorState**: Error handling with retry functionality
- **PageHeader**: Consistent navigation and branding

#### Custom Hooks
- **useComplaintForm**: Manages form state, submission, and response handling
- **useGraphData**: Fetches and manages workflow graph data
- **useMermaid**: Handles Mermaid diagram rendering and lifecycle

## 🚀 Getting Started

### Prerequisites
- Node.js 18.0.0 or higher
- npm 8.0.0 or higher
- ReplySight Backend running on port 8000

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ovokpus/ReplySight.git
cd ReplySight/frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Set up environment variables:**
```bash
# Create .env.local file
echo "API_BASE_URL=http://localhost:8000" > .env.local
```

4. **Start the development server:**
```bash
npm run dev
```

5. **Open in browser:**
```
http://localhost:3000
```

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

## 🔧 Configuration

### Environment Variables
```bash
# Backend API URL
API_BASE_URL=http://localhost:8000

# Next.js Configuration
NEXT_PUBLIC_APP_NAME=ReplySight
NEXT_PUBLIC_VERSION=1.0.0
```

### Tailwind Configuration
The application uses a custom Tailwind configuration with:
- **Typography Plugin**: For proper Markdown rendering
- **Custom Colors**: Brand-specific color palette
- **Responsive Design**: Mobile-first approach
- **Animation**: Smooth transitions and loading states

## 📋 Core Functionality

### 1. Response Generation
**Location**: `app/page.tsx`
- Enter customer complaints in the textarea
- AI generates empathetic, research-backed responses
- Real-time processing with latency tracking
- Professional formatting with proper paragraph spacing

### 2. Workflow Visualization
**Location**: `app/graph/page.tsx`, `app/workflow/page.tsx`
- Interactive Mermaid diagrams of AI workflow
- Real-time graph data from backend
- Execution flow visualization
- Performance metrics and node statistics

### 3. Citation System
**Location**: Response display component
- Academic references from ArXiv and web sources
- Clickable links for external references
- Proper citation formatting
- Source count tracking

### 4. Performance Monitoring
**Location**: Throughout the application
- Response time tracking
- Error rate monitoring
- Loading state management
- Performance metrics display

## 🎨 UI/UX Features

### Design System
- **Color Palette**: Professional blue and gray tones
- **Typography**: Clean, readable fonts with proper hierarchy
- **Spacing**: Consistent spacing using Tailwind utilities
- **Responsive**: Mobile-first design with breakpoints

### Interactive Elements
- **Buttons**: Hover states and loading animations
- **Forms**: Real-time validation and feedback
- **Cards**: Elevation and shadow effects
- **Navigation**: Smooth transitions between pages

### Accessibility
- **Keyboard Navigation**: Full keyboard support
- **Screen Reader**: Proper ARIA labels and descriptions
- **Color Contrast**: WCAG AA compliant colors
- **Focus Management**: Clear focus indicators

## 🔌 API Integration

### Backend Communication
**File**: `services/api.ts`

```typescript
// Generate customer service response
const response = await generateResponse(complaint);

// Fetch workflow graph data
const graphData = await fetchGraphData();
```

### API Routes
**File**: `app/api/respond/route.ts`
- Proxy requests to backend API
- Error handling and response formatting
- CORS configuration
- Request/response logging

## 🧪 Testing

### Manual Testing
1. **Response Generation**: Test various complaint types
2. **Workflow Visualization**: Verify diagram rendering
3. **Error Handling**: Test offline scenarios
4. **Responsive Design**: Test on different screen sizes

### Test Scenarios
```typescript
// Example test complaints
const testComplaintts = [
  "My order arrived damaged",
  "Customer service was unresponsive",
  "Product stopped working after one week",
  "Refund was denied unfairly"
];
```

## 🔍 Troubleshooting

### Common Issues

#### 1. Build Errors
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Rebuild
npm run build
```

#### 2. Connection Issues
- Verify backend is running on port 8000
- Check API_BASE_URL environment variable
- Ensure CORS is properly configured

#### 3. Styling Issues
- Verify Tailwind CSS is properly configured
- Check that @tailwindcss/typography is installed
- Ensure custom CSS doesn't conflict with Tailwind

#### 4. TypeScript Errors
- Run type checking: `npm run type-check`
- Ensure all types are properly imported
- Check for missing type definitions

## 📊 Performance Optimization

### Bundle Optimization
- **Code Splitting**: Automatic route-based splitting
- **Tree Shaking**: Unused code elimination
- **Image Optimization**: Next.js Image component
- **CSS Optimization**: Tailwind CSS purging

### Runtime Performance
- **React Hooks**: Optimized state management
- **Memoization**: Prevent unnecessary re-renders
- **Lazy Loading**: Components loaded on demand
- **Caching**: API response caching

## 🔒 Security

### Input Validation
- **Client-side**: Form validation before submission
- **Sanitization**: Prevent XSS attacks
- **Rate Limiting**: Prevent abuse
- **CSRF Protection**: Built-in Next.js protection

### API Security
- **CORS**: Proper cross-origin configuration
- **Headers**: Security headers in responses
- **Environment Variables**: Secure configuration management
- **Error Handling**: No sensitive data in error messages

## 📈 Analytics & Monitoring

### Performance Metrics
- **Response Times**: Track API call latency
- **Error Rates**: Monitor failed requests
- **User Interactions**: Track form submissions
- **Load Times**: Monitor page load performance

### User Experience Metrics
- **Completion Rates**: Track successful responses
- **Error Recovery**: Monitor error handling effectiveness
- **User Flow**: Track navigation patterns
- **Feedback**: Monitor user satisfaction

## 🛠️ Development

### Scripts
```bash
# Development server
npm run dev

# Production build
npm run build

# Type checking
npm run type-check

# Linting
npm run lint

# Start production server
npm start
```

### Code Quality
- **ESLint**: Code linting and formatting
- **TypeScript**: Type checking and safety
- **Prettier**: Code formatting
- **Husky**: Pre-commit hooks

## 📚 Dependencies

### Core Dependencies
- **Next.js**: React framework with App Router
- **React**: UI library
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling framework
- **React Markdown**: Markdown rendering
- **Mermaid**: Diagram generation
- **Lucide React**: Icon library

### Development Dependencies
- **ESLint**: Linting
- **Prettier**: Code formatting
- **@types/**: TypeScript type definitions
- **Autoprefixer**: CSS prefixing
- **PostCSS**: CSS processing

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Code Style
- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Maintain consistent component structure
- Write descriptive commit messages

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](../LICENSE) file for details.

## 🔗 Links

- **Backend Documentation**: [backend/README.md](../backend/README.md)
- **Main Project**: [README.md](../README.md)
- **GitHub Repository**: [ReplySight](https://github.com/ovokpus/ReplySight)
- **Live Demo**: [Coming Soon]

## 📞 Support

For questions, issues, or contributions:
- **Issues**: [GitHub Issues](https://github.com/ovokpus/ReplySight/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ovokpus/ReplySight/discussions)
- **Email**: [Contact Information]

---

**Built with ❤️ using Next.js, React, and Tailwind CSS** 