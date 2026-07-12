from pathlib import Path


DEFAULT_CONFIG = """schema_version = \"0.2\"
strategy = \"orchestration-value-gate\"
fast_mode = \"forbidden\"
mode = \"auto\"
worker_overhead_tokens = 20000
max_workers = 3

[workbuddy]
preferred_models = [\"hunyuan-3\", \"deepseek-v4-pro\"]
blocked_models = [\"glm\"]
default_reasoning = \"high\"

[codex]
premium_model = \"gpt-5.6-sol\"
allowed_reasoning = [\"low\", \"medium\", \"high\", \"xhigh\"]

[memory]
project_path = \".guanzai/memory\"
promotion_requires_validation = true
"""


def initialize_project(root: Path) -> Path:
    directory = root / ".guanzai"
    config = directory / "config.toml"
    if config.exists():
        raise FileExistsError(f"refusing to overwrite {config}")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "memory").mkdir(exist_ok=True)
    config.write_text(DEFAULT_CONFIG, encoding="utf-8")
    return config
