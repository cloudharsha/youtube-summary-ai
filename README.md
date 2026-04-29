# youtube-summary-ai
A simple Python CLI tool to summarize YouTube videos locally from WSL using transcripts and AI-generated summaries.

## Quick Start

Install dependencies:
```bash
pip3 install -r requirements.txt
```

Run with OpenAI:
```bash
export OPENAI_API_KEY=your_key_here
python3 main.py "https://www.youtube.com/watch?v=..."
```

Run with local LLM:
```bash
export ANTHROPIC_BASE_URL=http://localhost:8082
export ANTHROPIC_AUTH_TOKEN=freecc
python3 main.py "https://www.youtube.com/watch?v=..."
```

The tool automatically detects which backend to use based on environment variables, handles errors gracefully, and outputs formatted summaries with TL;DR, key points, and actionable insights.
