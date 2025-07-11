import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

// Force dynamic rendering to prevent build-time pre-rendering
export const dynamic = 'force-dynamic'

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${BACKEND_URL}/workflow/graph`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const data = await response.json();
    
    return NextResponse.json(data, {
      status: 200,
      headers: {
        'Cache-Control': 'public, max-age=300', // Cache for 5 minutes
      },
    });
  } catch (error) {
    console.error('Error fetching workflow graph:', error);
    
    return NextResponse.json(
      { 
        error: 'Failed to fetch workflow graph',
        message: error instanceof Error ? error.message : 'Unknown error'
      },
      { status: 500 }
    );
  }
} 