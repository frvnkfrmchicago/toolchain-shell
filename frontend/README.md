# Toolchain Frontend

AI Tool Discovery Platform - Next.js Frontend with React 19 and Tailwind CSS.

## Overview

Toolchain is an AI-powered tool discovery platform that helps developers find the best tools, frameworks, and services for their projects. This frontend provides a modern, responsive interface for interacting with the multi-agent backend.

## Quick Start

### Prerequisites

- Node.js 18+ or Bun (recommended)
- Backend API running at `http://localhost:8000`

### Setup

1. **Install dependencies:**
```bash
bun install
```

2. **Configure environment:**
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run development server:**
```bash
bun dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Project Structure

```
src/
├── app/             # Next.js App Router pages
│   ├── layout.tsx   # Root layout with providers
│   ├── page.tsx     # Homepage
│   └── ...
├── components/      # React components
│   ├── sections/    # Page sections (Hero, Features, etc.)
│   ├── ui/          # Reusable UI components
│   └── visuals/     # Visual effects (WarpField, etc.)
├── lib/             # Utilities and helpers
└── types/           # TypeScript types
```

## API Integration

The frontend connects to the backend API:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/tools` | GET | List all tools with filters |
| `/api/tools/:id` | GET | Get tool details |
| `/api/categories` | GET | List categories with counts |
| `/api/query` | POST | Query AI for recommendations |
| `/api/query/stream` | POST | Stream query results (SSE) |
| `/api/subscribe` | POST | Subscribe to updates |

### Example Query Request

```typescript
const response = await fetch(`${API_URL}/api/query`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Best vector database for RAG?' }),
});
const data = await response.json();
console.log(data.response);
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Yes | Backend API URL |

## Build & Deploy

### Production Build
```bash
bun run build
bun start
```

### Deploy to Vercel
1. Push to GitHub
2. Import to [Vercel](https://vercel.com/new)
3. Set environment variables
4. Deploy

## Tech Stack

- **Framework:** Next.js 15+ (App Router)
- **UI:** React 19, Tailwind CSS
- **Animations:** Framer Motion
- **Icons:** Lucide React
- **Package Manager:** Bun

## Development

### Run Linter
```bash
bun lint
```

### Type Check
```bash
bun run type-check
```
