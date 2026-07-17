import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from guanzai.router import plan_task


class RouterTests(unittest.TestCase):
    def test_ordinary_research_prefers_free_workbuddy_model(self):
        plan = plan_task("调研三个同类产品并整理功能表")
        worker = plan["work_items"][0]
        self.assertEqual(worker["provider"], "workbuddy")
        self.assertEqual(worker["model"], "hunyuan-3")
        self.assertEqual(worker["reasoning"], "high")

    def test_short_research_nouns_stay_inline(self):
        for task in ("看看资料", "资料"):
            with self.subTest(task=task):
                self.assertEqual(plan_task(task)["work_items"], [])

    def test_simple_write_and_general_verbs_stay_inline(self):
        for task in ("修改标题", "新增一行", "整理标题", "比较大小", "收集垃圾"):
            with self.subTest(task=task):
                plan = plan_task(task)
                self.assertEqual(plan["decision"]["mode"], "solo")
                self.assertEqual(plan["work_items"], [])

    def test_architecture_reserves_premium_reasoning_for_critical_work(self):
        plan = plan_task("设计一个跨模型支付系统架构，涉及资金安全和不可逆迁移")
        critical = [item for item in plan["work_items"] if item["critical"]]
        self.assertTrue(critical)
        self.assertTrue(any(item["provider"] == "codex" for item in critical))
        self.assertTrue(any(item["reasoning"] in {"high", "xhigh"} for item in critical))

    def test_finance_task_adds_independent_evidence_review(self):
        plan = plan_task("分析这家公司的估值、现金流和投资风险")
        roles = {item["role"] for item in plan["work_items"]}
        self.assertIn("intelligence-analyst", roles)
        self.assertIn("auditor", roles)

    def test_fast_mode_is_never_selected(self):
        for prompt in (
            "快速总结这段文字",
            "实现复杂编译器并做安全审计",
            "分析股票组合风险",
        ):
            plan = plan_task(prompt)
            self.assertTrue(all(item["speed"] == "standard" for item in plan["work_items"]))


if __name__ == "__main__":
    unittest.main()
