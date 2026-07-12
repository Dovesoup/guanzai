import argparse
import json
import shutil
import sys
from pathlib import Path

from .config import initialize_project
from .router import plan_task


def capabilities():
    workbuddy = shutil.which("codebuddy")
    bundled = Path("/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/bin/codebuddy")
    if not workbuddy and bundled.exists():
        workbuddy = str(bundled)
    return {
        "codex": {
            "planning": True,
            "subagents": True,
            "per_subagent_model_selection": False,
            "cli_workers": bool(shutil.which("codex")),
            "per_cli_worker_model_selection": bool(shutil.which("codex")),
            "note": "Current Codex collaboration tool does not expose a model argument.",
        },
        "workbuddy": {
            "cli": workbuddy,
            "execution": bool(workbuddy),
            "model_selection": bool(workbuddy),
            "reasoning_selection": bool(workbuddy),
        },
    }


def parser():
    root = argparse.ArgumentParser(prog="guanzai")
    commands = root.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    plan = commands.add_parser("plan")
    plan.add_argument("task")
    plan.add_argument("--json", action="store_true")
    plan.add_argument("--mode", choices=("auto", "solo", "single", "team"), default="auto")
    plan.add_argument("--max-workers", type=int)
    commands.add_parser("doctor")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        if args.command == "init":
            print(initialize_project(Path.cwd()))
        elif args.command == "plan":
            result = plan_task(args.task, mode=args.mode, max_workers=args.max_workers)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "doctor":
            print(json.dumps(capabilities(), ensure_ascii=False, indent=2))
    except (FileExistsError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
