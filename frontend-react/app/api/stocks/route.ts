import { NextResponse } from 'next/server';
import axios from 'axios';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query');

  if (!query) {
    return NextResponse.json({ error: 'Query parameter is required' }, { status: 400 });
  }

  try {
    const response = await axios.get(`http://backend:8000/stocks`, {
      params: { query }
    });
    return NextResponse.json(response.data);
  } catch (error) {
    console.error("Error fetching stocks from backend:", error);
    return NextResponse.json({ error: 'Error fetching stocks from backend' }, { status: 500 });
  }
}

