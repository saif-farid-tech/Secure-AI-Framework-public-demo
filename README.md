# SAIF — Secure AI Framework

A full-stack demo that visualizes an AI safety pipeline in real time. User prompts flow through multi-agent input filters, an LLM, and output filters — all grounded in the **UAE Charter for the Development and Use of Artificial Intelligence (July 2024)**.

Four LangGraph agents (two input, two output) assess and transform content against 12 charter principles covering safety, privacy, fairness, transparency, governance, and legal compliance. The entire pipeline streams results to the frontend via Server-Sent Events.

## Features

- **Real-time pipeline visualization** — watch prompts flow through input filters → LLM → output filters with animated connectors
- **Multi-agent safety filtering** — four agents powered by GPT-4o-mini, each covering a subset of UAE Charter principles
- **GraphRAG knowledge base** — agents query a NetworkX knowledge graph (not vector RAG) built from UAE banking policy documents
- **Harm classification** — each agent classifies content as safe, mild, moderate, or severe
- **SSE streaming** — pipeline stages update the UI incrementally as they complete

## Tech Stack

**Frontend:** React, TypeScript, Vite, Tailwind CSS, shadcn/ui, React Router

**Backend:** Python, Flask, LangGraph, LangChain, OpenAI API (GPT-4o-mini), NetworkX

## Project Structure

```
backend/
  app.py                 # Flask server with /process-pipeline SSE endpoint
  Prompt_filter.py       # Input filter agents (LangGraph)
  Output_filter.py       # Output filter agents (LangGraph)
  Agent_1/               # Knowledge base docs for Agent 1 (principles 1–6)
  Agent_2/               # Knowledge base docs for Agent 2 (principles 7–12)

src/
  pages/
    Index.tsx            # Main pipeline visualization page
  components/pipeline/   # Pipeline UI components (AgentCard, FilterStage, etc.)
  hooks/
    usePipeline.ts       # Pipeline state management & SSE consumption
  types/
    pipeline.ts          # TypeScript types for pipeline state
```

## Getting Started

### Prerequisites

- Node.js & npm — [install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating)
- Python 3 & pip

### Environment Variables

```sh
cp .env.example .env
```

Fill in your keys:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4o-mini and embeddings |
| `NGROK_API_KEY` | ngrok auth token for tunneling the Flask server |

`.env` is listed in `.gitignore` and must never be committed. When deploying, set these as secrets in your platform's environment settings.

### Frontend

```sh
npm install
npm run dev
```

The dev server starts on port 8080.

### Backend

```sh
pip install -r requirements.txt
python backend/app.py
```

The Flask server starts on port 5000.

## How It Works

1. **User enters a prompt** and clicks "Run Pipeline"
2. **Input filter agents** assess the prompt against UAE Charter principles and sanitize it if needed
   - Agent 1: Human-Machine Ties, Safety, Algorithmic Bias, Data Privacy, Transparency, Human Oversight
   - Agent 2: Governance, Accountability, Tech Excellence, Human Commitment, Peaceful Coexistence, AI Awareness, Legal Compliance
3. **LLM processes** the filtered prompt using GPT-4o-mini
4. **Output filter agents** assess and sanitize the LLM's response using the same principle sets
5. **Final output** is displayed with full traceability of each agent's assessment

Each agent uses a two-step LangGraph workflow: `assess_harm` → `transform`, querying a knowledge graph built from UAE banking policy documents for relevant context.
