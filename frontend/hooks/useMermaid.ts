import { useState, useEffect, useCallback, useRef } from 'react';
import { MermaidType } from '@/types';
import { MERMAID_CONFIG, ERROR_MESSAGES } from '@/constants';

export interface UseMermaidReturn {
  // State
  mermaid: MermaidType | null;
  mermaidLoaded: boolean;
  error: string | null;
  
  // Ref for mermaid container
  mermaidRef: React.RefObject<HTMLDivElement>;
  
  // Actions
  renderDiagram: (diagramCode: string) => Promise<void>;
  setError: (error: string | null) => void;
}

export const useMermaid = (): UseMermaidReturn => {
  const [mermaid, setMermaid] = useState<MermaidType | null>(null);
  const [mermaidLoaded, setMermaidLoaded] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const mermaidRef = useRef<HTMLDivElement>(null);

  // Load Mermaid.js dynamically
  useEffect(() => {
    const loadMermaid = async () => {
      try {
        const mermaidModule = await import('mermaid');
        const mermaidInstance = mermaidModule.default;
        
        // Initialize Mermaid with configuration
        mermaidInstance.initialize({
          startOnLoad: false,
          ...MERMAID_CONFIG,
        });
        
        setMermaid(mermaidInstance);
        setMermaidLoaded(true);
      } catch (error) {
        console.error('Failed to load Mermaid:', error);
        setError(ERROR_MESSAGES.DIAGRAM_LIBRARY_FAILED);
      }
    };

    loadMermaid();
  }, []);

  const renderDiagram = useCallback(async (diagramCode: string) => {
    if (!mermaid || !mermaidRef.current) {
      return;
    }

    try {
      // Clear any existing content
      mermaidRef.current.innerHTML = '';
      
      // Generate unique ID for this diagram
      const diagramId = `mermaid-diagram-${Date.now()}`;
      
      const { svg } = await mermaid.render(diagramId, diagramCode);
      
      if (mermaidRef.current) {
        mermaidRef.current.innerHTML = svg;
        
        // Apply additional styling to the generated SVG
        const svgElement = mermaidRef.current.querySelector('svg');
        if (svgElement) {
          svgElement.style.width = '100%';
          svgElement.style.height = '100%';
          svgElement.style.maxWidth = '100%';
          svgElement.style.maxHeight = '800px';
          svgElement.style.minHeight = '600px';
          svgElement.setAttribute('viewBox', svgElement.getAttribute('viewBox') || '0 0 800 600');
          svgElement.setAttribute('preserveAspectRatio', 'xMidYMid meet');
        }
      }
    } catch (mermaidError) {
      console.error('Mermaid rendering error:', mermaidError);
      setError(ERROR_MESSAGES.DIAGRAM_RENDER_FAILED);
    }
  }, [mermaid]);

  return {
    mermaid,
    mermaidLoaded,
    error,
    mermaidRef,
    renderDiagram,
    setError,
  };
}; 