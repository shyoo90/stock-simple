import { NextResponse } from 'next/server';
import axios from 'axios';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query');

  const response = await axios.get(`http://backend:8000/stocks?query=${query}`);
  return NextResponse.json(response.data);
}
