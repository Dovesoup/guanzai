import json
from typing import Dict


def build_packet(item: Dict[str, object]) -> str:
    packet = {
        "role": item["role"],
        "objective": item["objective"],
        "constraints": [
            "Do only this bounded objective.",
            "Use the smallest change that satisfies the objective; do not add speculative features.",
            "Validate plausible failure modes for the affected surface and disclose what was not tested.",
            "Fast mode is forbidden.",
            "Do not infer missing permissions or claim unperformed actions.",
        ],
        "output": {
            "format": "strict JSON",
            "fields": ["status", "result", "evidence", "risks", "confidence"],
        },
    }
    return json.dumps(packet, ensure_ascii=False, separators=(",", ":"))
