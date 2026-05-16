# MCP Task Tracker Server (Python)

A small **Model Context Protocol (MCP)** server built with **FastMCP**.

Exposes:
- Tools: `add_task`, `list_tasks`, `complete_task`
- Resource: `tasks://all`
- Prompt: `summarize_tasks`

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
python src/server.py
```

> This uses the default **stdio** transport, which is ideal for IDE MCP hosts.
