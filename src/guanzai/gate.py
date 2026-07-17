import re
from typing import Dict, List


READ_ONLY = re.compile(r"只读|仅查看|不做.*修改|不修改|输出报告|解释|总结|润色|改短")
MUTATION_VERBS = r"修改|实现|开发|修复|创建|新增|更新|执行|写入|删除|发布|上线|部署|迁移|付款|转账|计费|账单|公式|授权"
NEGATION_PREFIX = r"(?:不(?:需要|要|用)?|不得|无需|请勿)"
NEGATION_OBJECT = r"(?:对(?:现有)?代码)?"
NEGATION_AUX = r"(?:做|进行|执行)?(?:任何)?"
COORDINATOR = r"(?:并且|以及|和|与|或|并|、|及)"
MUTATION = re.compile(rf"(?:{MUTATION_VERBS})")
NEGATED_MUTATION = re.compile(
    rf"{NEGATION_PREFIX}{NEGATION_OBJECT}{NEGATION_AUX}(?:{MUTATION_VERBS})"
    rf"(?:{COORDINATOR}{NEGATION_OBJECT}{NEGATION_AUX}(?:{MUTATION_VERBS}))*"
)
NOMINAL_IMPLEMENTATION = re.compile(r"(?<![和与并或、及])实现(?:原理|方式|细节|机制|思路|方案)")
NOMINAL_MUTATION = re.compile(r"(?:修改|修复|更新)(?:记录|建议|说明|历史|方案)")
READ_ONLY_ACTION = re.compile(r"只读|仅查看|分析|解释|评估|审查|查看|检查|阅读|理解|输出报告")
MAIN_SCOPE_BOUNDARY = re.compile(
    rf"[，,。；;！？!?]|然后|随后|但是|但|再|而要(?=(?:{MUTATION_VERBS}))|后(?=(?:{MUTATION_VERBS}))"
)
COORDINATED_MUTATION_BOUNDARY = re.compile(rf"{COORDINATOR}\s*(?=(?:{MUTATION_VERBS}))")
SENSITIVE = re.compile(r"金融|资金|账单|计费|支付|投资|安全|隐私|合规|生产|数据库")
FINANCIAL_DECISION = re.compile(r"估值|投资风险|现金流|买入|卖出|授信|定价|财务结论")
IRREVERSIBLE = re.compile(r"不可逆|无法回滚|无备份|删除|付款|转账|发布")
MECHANICAL = re.compile(r"批量|重命名|替换|格式化|现有测试|按照现有模式|依照现有模式")
RESEARCH_SIGNAL = re.compile(r"调研|搜索|整理|比较|收集|竞品|证据|资料")
RESEARCH_ACTION = re.compile(r"调研|搜索|查找|检索")
DESIGN = re.compile(r"设计|架构|方案|需求")
BUILD_ACTION = re.compile(r"开发|实现|编程|迁移|修复|(?:修改|新增)[^，,。；;！？!?]*(?:接口|系统|配置|设置|测试|仪表盘|代码|前端|后端|编译器)")
VERIFY = re.compile(r"测试|审计|验证|复核|检查")
UNCERTAIN = re.compile(r"不确定|探索|冲突|模糊|未知|从零|复杂")


def _has_mutation(task: str) -> bool:
    for scope in MAIN_SCOPE_BOUNDARY.split(task):
        scope = NEGATED_MUTATION.sub("", scope)
        if READ_ONLY_ACTION.search(scope):
            scope = NOMINAL_MUTATION.sub("", scope)
            scope = NOMINAL_IMPLEMENTATION.sub("", scope)
        for clause in COORDINATED_MUTATION_BOUNDARY.split(scope):
            if MUTATION.search(clause):
                return True
    return False


def assess_task(task: str) -> Dict[str, object]:
    task = task.strip()
    if not task:
        raise ValueError("task must not be empty")

    reasons: List[str] = []
    mutation = _has_mutation(task)
    dimensions = {
        "research": bool(RESEARCH_ACTION.search(task)),
        "design": bool(DESIGN.search(task)),
        "build": mutation and bool(BUILD_ACTION.search(task)),
        "verify": bool(VERIFY.search(task)),
        "uncertainty": bool(UNCERTAIN.search(task)),
    }
    cognitive = sum(dimensions.values())
    mechanical = bool(MECHANICAL.search(task))
    research_signal = bool(RESEARCH_SIGNAL.search(task))
    sensitive = bool(SENSITIVE.search(task))
    irreversible = bool(IRREVERSIBLE.search(task)) and mutation
    audit_required = bool(FINANCIAL_DECISION.search(task)) or (
        mutation and sensitive and (irreversible or bool(re.search(r"公式|计费|账单|生产|资金|支付|投资组合|金融系统|安全.*(?:修复|更新|部署)", task)))
    )

    if mechanical:
        cognitive = min(cognitive, 2)
        reasons.append("mechanical-volume-not-cognitive-complexity")
    if research_signal and not dimensions["research"]:
        reasons.append("research-topic-without-explicit-action")
    if dimensions["build"]:
        base_rank = 2 if cognitive >= 3 else 1
    elif len(task) < 24 and cognitive <= 1 and not dimensions["research"]:
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
