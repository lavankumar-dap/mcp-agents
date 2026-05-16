from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List

from mcp.server.fastmcp import FastMCP

DATA_FILE = Path(__file__).parent / "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False


def _load() -> List[Task]:
    if not DATA_FILE.exists():
        return []
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Task(**t) for t in data]


def _save(tasks: List[Task]) -> None:
    DATA_FILE.write_text(json.dumps([asdict(t) for t in tasks], indent=2), encoding="utf-8")


mcp = FastMCP("TaskTracker")


@mcp.tool()
def add_task(title: str) -> str:
    # Add a task and return its id
    tasks = _load()
    next_id = (max([t.id for t in tasks]) + 1) if tasks else 1
    tasks.append(Task(id=next_id, title=title, done=False))
    _save(tasks)
    return f"Added task #{next_id}: {title}"


@mcp.tool()
def list_tasks() -> list[dict]:
    return [asdict(t) for t in _load()]


@mcp.tool()
def complete_task(task_id: int) -> str:
    tasks = _load()
    for t in tasks:
        if t.id == task_id:
            t.done = True
            _save(tasks)
            return f"Completed task #{task_id}"
    return f"Task #{task_id} not found"


@mcp.resource("tasks://all")
def tasks_resource() -> str:
    tasks = _load()
    lines = [f"[{'x' if t.done else ' '}] {t.id}. {t.title}" for t in tasks]
    return "
".join(lines) if lines else "No tasks yet."


@mcp.prompt()
def summarize_tasks() -> str:
    return (
        "Summarize the tasks below, group by status (done/pending), and suggest next actions:

"
        "{{resource:tasks://all}}
"
    )


if __name__ == "__main__":
    mcp.run()
