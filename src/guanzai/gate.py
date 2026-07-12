import re
from typing import Dict, List


READ_ONLY = re.compile(r"只读|仅查看|不做.*修改|不修改|输出报告|解释|总结|润色|改短")
MUTATION = re.compile(r"修改|实现|开发|修复|创建|新增|更新|执行|写入|删除|发布|上线|部署|迁移|付款|转账|计费|账单|公式|授权")
NEGATED_MUTATION = re.compile(r"不(?:做任何|做|进行)?(?:修改|实现|开发|修复|创建|新增|更新|执行|写入|删除|发布|上线|部署|迁移|付款|转账|计费|授权)")
SENSITIVE = re.compile(r"金融|资金|账单|计费|支付|投资|安全|隐私|合规|生产|数据库")
FINANCIAL_DECISION = re.compile(r"估值|投资风险|现金流|买入|卖出|授信|定价|财务结论")
IRREVERSIBLE = re.compile(r"不可逆|无法回滚|无备份|删除|付款|转账|发布")
MECHANICAL = re.compile(r"批量|重命名|替换|格式化|现有测试|按照现有模式|依照现有模式")
RESEARCH = re.compile(r"调研|搜索|竞品|证据|资料")
DESIGN = re.compile(r"设计|架构|方案|需求|产品")
BUILD = re.compile(r"开发|实现|编程|代码|前端|后端|接口|仪表盘")
VERIFY = re.compile(r"测试|审计|验证|复核|检查")
UNCERTAIN = re.compile(r"不确定|探索|冲突|模糊|未知|从零|复杂")


def assess_task(task: str) -> Dict[str, object]:
    task = task.strip()
    if not task:
        raise ValueError("task must not be empty")

    reasons: List[str] = []
    dimensions = {
        "research": bool(RESEARCH.search(task)),
        "design": bool(DESIGN.search(task)),
        "build": bool(BUILD.search(task)),
        "verify": bool(VERIFY.search(task)),
        "uncertainty": bool(UNCERTAIN.search(task)),
    }
    cognitive = sum(dimensions.values())
    mechanical = bool(MECHANICAL.search(task))
    mutation_text = NEGATED_MUTATION.sub("", task)
    mutation = bool(MUTATION.search(mutation_text))
    sensitive = bool(SENSITIVE.search(task))
    irreversible = bool(IRREVERSIBLE.search(task)) and mutation
    audit_required = bool(FINANCIAL_DECISION.search(task)) or (
        mutation and sensitive and (irreversible or bool(re.search(r"公式|计费|账单|生产|资金|支付|投资组合|金融系统|安全.*(?:修复|更新|部署)", task)))
    )

    if mechanical:
        cognitive = min(cognitive, 2)
        reasons.append("mechanical-volume-not-cognitive-complexity")
    if dimensions["build"]:
        base_rank = 2 if cognitive >= 3 else 1
    elif len(task) < 24 and cognitive <= 1:
        base_rank = 0
    elif cognitive >= 3:
        base_rank = 2
    else:
        base_rank = 1

    base_mode = ("solo", "single", "team")[base_rank]
    mode = "audited" if audit_required else base_mode
    expected_work_tokens = (5000, 30000, 70000)[base_rank]
    worker_overhead_tokens = 20000
    delegate = base_rank > 0 and (expected_work_tokens >= worker_overhead_tokens or audit_required)
    if audit_required:
        delegate = True
        reasons.append("action-impact-audit-override")
    elif sensitive:
        reasons.append("sensitive-topic-without-risky-action")
    reasons.extend(name for name, present in dimensions.items() if present)

    return {
        "score": cognitive,
        "base_mode": base_mode,
        "base_mode_rank": base_rank,
        "mode": mode,
        "delegate": delegate,
        "audit_required": audit_required,
        "audit_recommended": sensitive,
        "mutation": mutation,
        "expected_work_tokens": expected_work_tokens,
        "worker_overhead_tokens": worker_overhead_tokens,
        "reasons": reasons,
    }
