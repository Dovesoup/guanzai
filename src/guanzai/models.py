from dataclasses import asdict, dataclass
from typing import Dict, List


@dataclass(frozen=True)
class Model:
    id: str
    provider: str
    cost: int
    quality: int
    available: bool = True

    def to_dict(self) -> Dict[str, object]:
        return asdict(self)


DEFAULT_MODELS: List[Model] = [
    Model("hy3", "workbuddy", cost=0, quality=2),
    Model("deepseek-v4-pro", "workbuddy", cost=1, quality=3),
    Model("gpt-5.6-sol", "codex", cost=4, quality=5),
    Model("glm", "workbuddy", cost=5, quality=3, available=False),
]


def cheapest_model(min_quality: int) -> Model:
    candidates = [m for m in DEFAULT_MODELS if m.available and m.quality >= min_quality]
    return sorted(candidates, key=lambda m: (m.cost, -m.quality))[0]
