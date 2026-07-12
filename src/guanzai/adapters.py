from pathlib import Path
from typing import Dict, List

from .packets import build_packet


def codex_command(item: Dict[str, object], project: str) -> List[str]:
    sandbox = "workspace-write" if item["role"] == "builder" else "read-only"
    return [
        "codex",
        "exec",
        "--ephemeral",
        "--skip-git-repo-check",
        "--sandbox",
        sandbox,
        "--model",
        str(item["model"]),
        "--config",
        'model_reasoning_effort="%s"' % item["reasoning"],
        "--cd",
        project,
        build_packet(item),
    ]


def workbuddy_command(item: Dict[str, object], app_path: str = "/Applications/WorkBuddy.app") -> List[str]:
    binary = Path(app_path) / "Contents/Resources/app.asar.unpacked/cli/bin/codebuddy"
    builder = item["role"] == "builder"
    return [
        str(binary),
        "--print",
        "--model",
        str(item["model"]),
        "--effort",
        "high",
        "--tools",
        "Read,Edit,Bash" if builder else "",
        "--max-turns",
        "3" if builder else "1",
        "--output-format",
        "json",
        build_packet(item),
    ]
