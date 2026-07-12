import re
import uuid
from typing import Dict, List

from .gate import assess_task
from .models import cheapest_model


FINANCE = re.compile(r"金融|股票|估值|现金流|投资|证券|基金|财务|银行|支付|资金")
BUILD = re.compile(r"开发|实现|新增|修改|修复|更新|编程|代码|前端|后端|接口|系统|架构|迁移|编译器|仪表盘")
CRITICAL = re.compile(r"架构|安全|不可逆|资金|支付|迁移|合规|复杂|关键")
RESEARCH = re.compile(r"调研|搜索|整理|总结|比较|竞品|资料")


def _item(role: str, objective: str, critical: bool, quality: int, reasoning: str) -> Dict[str, object]:
    model = cheapest_model(quality)
    if model.provider == "workbuddy":
        reasoning = "high"
    return {
        "id": str(uuid.uuid4()),
        "role": role,
        "objective": objective,
        "critical": critical,
        "provider": model.provider,
        "model": model.id,
        "reasoning": reasoning,
        "speed": "standard",
        "execution": "planned",
    }


def plan_task(task: str, mode: str = "auto", max_workers=None) -> Dict[str, object]:
    task = task.strip()
    if not task:
        raise ValueError("task must not be empty")
    if mode not in {"auto", "solo", "single", "team"}:
        raise ValueError("mode must be auto, solo, single, or team")
    if max_workers is not None and max_workers < 1:
        raise ValueError("max_workers must be positive")

    decision = assess_task(task)
    selected_mode = decision["mode"] if mode == "auto" else mode
    if decision["audit_required"]:
        selected_mode = "audited"
    budget_overridden = bool(selected_mode == "audited" and max_workers is not None and max_workers < 2)
    decision = dict(
        decision,
        requested_mode=mode,
        mode=selected_mode,
        budget_overridden_for_safety=budget_overridden,
    )
    if selected_mode == "solo":
        return {
            "schema_version": "0.2",
            "task": task,
            "orchestrator": "guanzai",
            "decision": decision,
            "policy": {"fast_mode": "forbidden", "strategy": "orchestration-value-gate"},
            "work_items": [],
        }

    finance = bool(FINANCE.search(task))
    build = bool(BUILD.search(task))
    critical = bool(CRITICAL.search(task))
    research = bool(RESEARCH.search(task))
    items: List[Dict[str, object]] = []

    if finance:
        items.append(_item("intelligence-analyst", f"建立证据链并分析：{task}", critical, 5 if critical else 3, "high" if critical else "medium"))
    elif build:
        items.append(_item("product-systems-architect", f"定义边界与验收标准：{task}", critical, 5 if critical else 3, "high" if critical else "medium"))
    else:
        items.append(_item("intelligence-analyst", f"收集、归纳并标注依据：{task}", False, 2, "low" if research else "medium"))

    if build:
        items.append(_item("builder", f"按已确认方案实现并自测：{task}", False, 3, "medium"))

    if finance or critical:
        items.append(_item("auditor", f"独立检查事实、风险和遗漏：{task}", True, 5, "high"))

    if selected_mode == "audited":
        if not items:
            items.append(_item("builder", f"执行受控变更并验证：{task}", True, 3, "medium"))
        if not any(item["role"] == "auditor" for item in items):
            items.append(_item("auditor", f"独立检查事实、风险和遗漏：{task}", True, 5, "high"))

    desired = {"single": 1, "team": 3, "audited": max(2, len(items))}.get(selected_mode, len(items))
    if selected_mode == "team" and len(items) < desired:
        items.insert(0, _item("product-systems-architect", f"定义边界与验收标准：{task}", False, 3, "medium"))
        if len(items) < desired:
            items.append(_item("auditor", f"独立验证结果：{task}", True, 5, "high"))
    if selected_mode == "single":
        builder_item = next((item for item in items if item["role"] == "builder"), None)
        items = [builder_item or items[0]]
    if selected_mode == "audited":
        desired = max(2, desired)
    limit = min(desired, max_workers) if max_workers is not None else desired
    if selected_mode == "audited":
        limit = max(2, limit)
    if selected_mode == "audited" and len(items) > limit:
        auditor = next(item for item in items if item["role"] == "auditor")
        executors = [item for item in items if item["role"] != "auditor"]
        items = executors[: limit - 1] + [auditor]
    else:
        items = items[:limit]

    return {
        "schema_version": "0.2",
        "task": task,
        "orchestrator": "guanzai",
        "decision": decision,
        "policy": {"fast_mode": "forbidden", "strategy": "orchestration-value-gate"},
        "work_items": items,
    }
