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
        self.assertEqual(len(plan["work_items"]), 1)
        self.assertEqual(plan["work_items"][0]["role"], "product-systems-architect")
        self.assertNotIn("builder", {item["role"] for item in plan["work_items"]})
        self.assertNotIn("实现并自测", plan["work_items"][0]["objective"])

    def test_explanatory_mentions_of_implementation_do_not_route_to_builder(self):
        for task in (
            "分析现有代码的实现原理，不修改代码",
            "解释接口设计，不执行任何修改",
            "不执行修改，只输出报告",
            "不进行任何修改，只分析架构",
            "无需修改代码，只解释实现原理",
            "不要修改代码，只分析架构",
            "解释实现方案，不修改代码",
            "不用修改代码，只分析架构",
            "不需要修改代码，只分析架构",
            "请勿修改代码，只分析架构",
            "无需对代码进行任何修改，只分析架构",
            "不要对现有代码做修改，只分析架构",
            "不得修改代码，只分析架构",
            "检查代码修改记录并输出报告",
            "不要修改和删除文件，只分析影响",
            "无需修改或删除代码，只输出报告",
            "只分析实现方案和修改建议",
            "请评估现有实现方案和修改建议，不进行任何修改",
            "分析风险和修复建议",
        ):
            with self.subTest(task=task):
                plan = plan_task(task)
                self.assertFalse(plan["decision"]["mutation"])
                self.assertNotIn("builder", {item["role"] for item in plan["work_items"]})
                self.assertTrue(all("实现并自测" not in item["objective"] for item in plan["work_items"]))

    def test_implementation_requests_and_mixed_intents_route_to_builder(self):
        for task in (
            "请实现方案中的接口并测试",
            "实现方案并测试",
            "实现思路中的第一步",
            "分析、实现方案并测试",
            "分析和实现方案并测试",
            "分析与实现方案并测试",
            "评估后实现方案并测试",
            "分析后修改代码",
            "分析并新增测试",
            "先只读检查配置，然后修改超时设置",
            "不要修改旧代码，但新增测试",
        ):
            with self.subTest(task=task):
                plan = plan_task(task)
                self.assertTrue(plan["decision"]["mutation"])
                self.assertIn("builder", {item["role"] for item in plan["work_items"]})

    def test_explicit_single_write_executor_routes_to_builder(self):
        for task in ("删除文件", "创建目录", "部署服务"):
            with self.subTest(task=task):
                plan = plan_task(task, mode="single")
                self.assertTrue(plan["decision"]["mutation"])
                self.assertEqual([item["role"] for item in plan["work_items"]], ["builder"])

    def test_explicit_single_mutation_noun_edits_route_to_builder(self):
        for task in ("请修改记录页面并测试", "修改建议内容"):
            with self.subTest(task=task):
                plan = plan_task(task, mode="single")
                self.assertTrue(plan["decision"]["mutation"])
                self.assertEqual([item["role"] for item in plan["work_items"]], ["builder"])

    def test_long_auto_mutation_routes_to_builder_not_analyst(self):
        plan = plan_task("删除全部临时文件，验证清理结果并保留操作日志以供复核")
        roles = {item["role"] for item in plan["work_items"]}
        self.assertTrue(plan["decision"]["mutation"])
        self.assertIn("builder", roles)
        self.assertNotIn("intelligence-analyst", roles)

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
