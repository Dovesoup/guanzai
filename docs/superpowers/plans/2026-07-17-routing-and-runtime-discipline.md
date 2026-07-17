# GuanZai Routing and Runtime Discipline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prevent read-only analysis from creating implementation workers, and add compact scope, verification, and progress-update rules without turning GuanZai into a larger methodology.

**Architecture:** Keep `gate.assess_task()` as the single source of truth for whether mutation is authorized. Let `router.plan_task()` use that result when selecting roles, route non-mutating design work to an architect rather than a builder, and keep worker packets and the public Skill aligned with the smallest-change and risk-based-validation rules. This plan is one small vertical slice; state persistence, task-contract schemas, observable execution, and controlled delivery remain separate later plans.

**Tech Stack:** Python 3.9+, standard-library `unittest`, Markdown, Git

---

### Task 1: Make mutation authority control builder routing

**Files:**
- Modify: `tests/test_modes.py`
- Modify: `src/guanzai/router.py`

- [ ] **Step 1: Write the failing read-only routing test**

Add this test to `ModeTests` in `tests/test_modes.py`:

```python
def test_read_only_design_routes_to_architect_not_builder(self):
    plan = plan_task("评估 GuanZai 现有架构设计，只做分析，不修改项目")

    self.assertFalse(plan["decision"]["mutation"])
    self.assertEqual(plan["decision"]["mode"], "single")
    self.assertEqual(plan["work_items"][0]["role"], "product-systems-architect")
    self.assertNotIn("builder", {item["role"] for item in plan["work_items"]})
    self.assertNotIn("实现并自测", plan["work_items"][0]["objective"])
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest tests.test_modes.ModeTests.test_read_only_design_routes_to_architect_not_builder -v
```

Expected: FAIL because the current router selects `builder` from raw keywords such as `架构` or the negated `修改`.

- [ ] **Step 3: Make the router consume the gate decision**

In `src/guanzai/router.py`, derive design intent from the gate reasons and require mutation authority before creating build work:

```python
finance = bool(FINANCE.search(task))
design = "design" in decision["reasons"]
build = bool(BUILD.search(task)) and bool(decision["mutation"])
critical = bool(CRITICAL.search(task))
research = bool(RESEARCH.search(task))
```

Replace the first-item selection with this ordering:

```python
if finance:
    items.append(_item("intelligence-analyst", f"建立证据链并分析：{task}", critical, 5 if critical else 3, "high" if critical else "medium"))
elif build:
    items.append(_item("product-systems-architect", f"定义边界与验收标准：{task}", critical, 5 if critical else 3, "high" if critical else "medium"))
elif design:
    items.append(_item("product-systems-architect", f"只读分析边界、取舍和验收标准：{task}", critical, 5 if critical else 3, "high" if critical else "medium"))
else:
    items.append(_item("intelligence-analyst", f"收集、归纳并标注依据：{task}", False, 2, "low" if research else "medium"))
```

Keep the existing `if build:` block that adds a builder. Because `build` now requires `decision["mutation"]`, read-only tasks cannot create it.

- [ ] **Step 4: Run the focused and routing suites and verify GREEN**

Run:

```bash
python3 -m unittest tests.test_modes -v
python3 -m unittest tests.test_gate -v
```

Expected: all mode and gate tests pass, including the new read-only regression.

- [ ] **Step 5: Commit the routing fix**

```bash
git add tests/test_modes.py src/guanzai/router.py
git commit -m "fix: keep read-only design out of builder routing"
```

### Task 2: Put scope restraint and failure-surface validation in worker packets

**Files:**
- Modify: `tests/test_packets.py`
- Modify: `src/guanzai/packets.py`

- [ ] **Step 1: Write the failing packet-contract test**

Extend `test_packet_is_slim_and_self_verifying` in `tests/test_packets.py`:

```python
self.assertIn("smallest change", packet)
self.assertIn("speculative features", packet)
self.assertIn("plausible failure modes", packet)
self.assertIn("what was not tested", packet)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run:

```bash
python3 -m unittest tests.test_packets.PacketTests.test_packet_is_slim_and_self_verifying -v
```

Expected: FAIL because the current packet does not contain the scope or failure-surface rules.

- [ ] **Step 3: Add the two compact worker constraints**

Update the `constraints` list in `src/guanzai/packets.py` to:

```python
"constraints": [
    "Do only this bounded objective.",
    "Use the smallest change that satisfies the objective; do not add speculative features.",
    "Validate plausible failure modes for the affected surface and disclose what was not tested.",
    "Fast mode is forbidden.",
    "Do not infer missing permissions or claim unperformed actions.",
],
```

Do not add named laws, examples, or a new framework to the packet. The behavior matters; the slogans do not.

- [ ] **Step 4: Run packet tests and verify GREEN**

Run:

```bash
python3 -m unittest tests.test_packets -v
```

Expected: all packet and adapter tests pass, and the serialized packet remains below the existing 1,500-character limit.

- [ ] **Step 5: Commit the packet discipline**

```bash
git add tests/test_packets.py src/guanzai/packets.py
git commit -m "feat: keep worker scope and validation disciplined"
```

### Task 3: Align the public Skill and design contract

**Files:**
- Modify: `skill/guanzai/SKILL.md`
- Modify: `skill/guanzai/references/routing-policy.md`
- Modify: `docs/superpowers/specs/2026-07-15-guanzai-ai-project-caregiver-design.md`

- [ ] **Step 1: Add the compact runtime rules to the Skill**

Add this workflow item after the existing execution boundary in `skill/guanzai/SKILL.md`:

```markdown
5. Send user-visible updates only at the start, major phase changes, blockers, or findings that change the plan. Do not narrate routine tool calls.
```

Renumber the existing independent-review and memory items to 6 and 7. Add these invariants:

```markdown
- Prefer the smallest change that satisfies the task contract; do not add speculative features.
- Validate plausible failure modes in proportion to the affected surface and disclose what remains untested.
- A downstream router may not turn a gate-level `mutation = false` decision into a builder or other write-capable work item.
```

- [ ] **Step 2: Document precedence in the routing policy**

Add this paragraph under `## Escalation` in `skill/guanzai/references/routing-policy.md`:

```markdown
Authorization precedes role keywords. Once the gate resolves a task as non-mutating, downstream routing must not create a builder or write-capable work item merely because the text mentions design, architecture, code, or a negated mutation such as “do not modify.” Route read-only design judgment to the architect function and preserve the original boundary in the objective.
```

- [ ] **Step 3: Add the two article-derived rules to the design specification**

Under `### 3.4 证明结果，不规定思维表演`, add:

```markdown
范围克制采用可检查的决策规则：每个新增文件、抽象、依赖、配置或功能都必须对应任务合同中的结果、不可退化项或已经证明的风险；否则默认不增加。GuanZai 不把“奥卡姆剃刀”作为必须背诵的口号，而把它落实为可追踪的范围差异。

验证扩展也采用风险规则：根据受影响表面列出合理可预见的失败方式，优先执行能证伪当前实现的负例、边界和恢复检查，并明确未测试范围。它不要求穷举所有灾难，也不把一次成功路径当成完整验收。
```

Under `### 5.7 最小运行宪法`, add:

```markdown
用户可见进度遵循稀疏更新：开始时说明第一步；只在主要阶段变化、出现阻碍或新发现改变计划时更新；不播报常规工具调用和内部推理。沉默不能掩盖风险、失败或等待用户决定的节点。
```

- [ ] **Step 4: Verify the documentation contract**

Run:

```bash
rg -n "smallest change|plausible failure modes|mutation = false|routine tool calls" skill/guanzai/SKILL.md skill/guanzai/references/routing-policy.md
rg -n "范围克制|合理可预见的失败方式|稀疏更新" docs/superpowers/specs/2026-07-15-guanzai-ai-project-caregiver-design.md
git diff --check
```

Expected: every rule appears once in the intended layer and `git diff --check` prints nothing.

- [ ] **Step 5: Commit the aligned documentation**

```bash
git add skill/guanzai/SKILL.md skill/guanzai/references/routing-policy.md docs/superpowers/specs/2026-07-15-guanzai-ai-project-caregiver-design.md
git commit -m "docs: codify lean execution and sparse updates"
```

### Task 4: Verify the complete vertical slice

**Files:**
- Verify: `src/guanzai/router.py`
- Verify: `src/guanzai/packets.py`
- Verify: `tests/`
- Verify: `skill/guanzai/`
- Verify: `docs/superpowers/specs/2026-07-15-guanzai-ai-project-caregiver-design.md`

- [ ] **Step 1: Run the complete automated suite**

```bash
python3 -m unittest discover -s tests -v
```

Expected: 29 tests pass: the existing 28 plus the new read-only routing regression.

- [ ] **Step 2: Run the real CLI regression case**

```bash
PYTHONPATH=src python3 -m guanzai.cli plan "评估 GuanZai 现有架构设计，只做分析，不修改项目" --json
```

Expected JSON facts:

```text
decision.mutation = false
decision.mode = "single"
work_items[0].role = "product-systems-architect"
no work item has role = "builder"
no objective contains "实现并自测"
```

- [ ] **Step 3: Run repository hygiene checks**

```bash
git diff --check
git status --short
```

Expected: no whitespace errors and no uncommitted changes after the three task commits.

- [ ] **Step 4: Review scope against the approved design**

Confirm all four statements are true:

```text
Read-only authorization is decided once in gate.py and consumed downstream.
Builder routing still works for explicitly authorized implementation tasks.
Worker packets gained only two short, testable constraints.
Progress guidance is sparse but still reports blockers, changed plans, and approval points.
```

Do not start state persistence, task-contract storage, external worker execution, merge automation, or deployment in this plan.
