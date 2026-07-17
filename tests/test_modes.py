import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from guanzai.router import plan_task


class ModeTests(unittest.TestCase):
    def test_auto_simple_task_has_no_external_workers(self):
        plan = plan_task("把标题改短一点")
        self.assertEqual(plan["decision"]["mode"], "solo")
        self.assertEqual(plan["work_items"], [])

    def test_solo_override_cannot_bypass_mandatory_audit(self):
        plan = plan_task("开发一个复杂金融系统", mode="solo")
        self.assertEqual(plan["decision"]["mode"], "audited")
        self.assertIn("auditor", {item["role"] for item in plan["work_items"]})

    def test_team_override_respects_worker_cap(self):
        plan = plan_task("设计并开发一个网站", mode="team", max_workers=2)
        self.assertEqual(len(plan["work_items"]), 2)

    def test_single_implementation_routes_to_builder(self):
        plan = plan_task("按照现有模式新增一个API接口并运行测试")
        self.assertEqual(plan["decision"]["mode"], "single")
        self.assertEqual(plan["work_items"][0]["role"], "builder")

    def test_read_only_design_routes_to_architect_not_builder(self):
        plan = plan_task("评估 GuanZai 现有架构设计，只做分析，不修改项目")

        self.assertFalse(plan["decision"]["mutation"])
        self.assertEqual(plan["decision"]["mode"], "single")
        self.assertEqual(plan["work_items"][0]["role"], "product-systems-architect")
        self.assertNotIn("builder", {item["role"] for item in plan["work_items"]})
        self.assertNotIn("实现并自测", plan["work_items"][0]["objective"])

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            plan_task("任务", mode="ultra")

    def test_audited_mode_always_has_independent_auditor(self):
        plan = plan_task("修改一行账单计费公式并发布")
        self.assertGreaterEqual(len(plan["work_items"]), 2)
        self.assertIn("auditor", {item["role"] for item in plan["work_items"]})

    def test_worker_cap_cannot_remove_mandatory_auditor(self):
        plan = plan_task("设计不可逆资金支付迁移", max_workers=1)
        roles = {item["role"] for item in plan["work_items"]}
        self.assertGreaterEqual(len(plan["work_items"]), 2)
        self.assertIn("auditor", roles)
        self.assertTrue(plan["decision"]["budget_overridden_for_safety"])


if __name__ == "__main__":
    unittest.main()
