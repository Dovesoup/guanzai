import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from guanzai.gate import assess_task


class GateTests(unittest.TestCase):
    def test_short_rewrite_stays_solo(self):
        result = assess_task("把这句话润色得自然一点")
        self.assertEqual(result["mode"], "solo")
        self.assertFalse(result["delegate"])

    def test_bulk_mechanical_work_is_not_mistaken_for_teamwork(self):
        result = assess_task("把50个文件里的变量 foo 批量重命名为 bar，并运行现有测试")
        self.assertIn(result["mode"], {"solo", "single"})

    def test_patterned_endpoint_uses_one_worker(self):
        result = assess_task("按照现有模式新增一个API接口，并运行现有测试")
        self.assertEqual(result["mode"], "single")

    def test_cross_domain_finance_build_earns_team(self):
        result = assess_task("调研金融数据产品，设计前后端架构，实现投资组合风险仪表盘并测试")
        self.assertEqual(result["mode"], "audited")
        self.assertGreaterEqual(result["base_mode_rank"], 2)

    def test_small_billing_mutation_forces_audit(self):
        result = assess_task("修改一行账单计费公式并发布")
        self.assertEqual(result["mode"], "audited")

    def test_read_only_security_report_does_not_force_audit(self):
        result = assess_task("只读检查安全配置并输出报告，不做任何修改")
        self.assertNotEqual(result["mode"], "audited")

    def test_read_only_clause_cannot_hide_later_production_mutation(self):
        result = assess_task("先只读检查配置，然后修改生产数据库并发布")
        self.assertTrue(result["mutation"])
        self.assertEqual(result["mode"], "audited")

    def test_explanatory_mentions_of_implementation_are_read_only(self):
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
        ):
            with self.subTest(task=task):
                self.assertFalse(assess_task(task)["mutation"])

    def test_implementation_requests_and_mixed_intents_are_mutations(self):
        for task in (
            "请实现方案中的接口并测试",
            "实现方案并测试",
            "实现思路中的第一步",
            "分析并实现方案",
            "分析、实现方案并测试",
            "分析和实现方案并测试",
            "分析与实现方案并测试",
            "评估后实现方案并测试",
            "先只读检查配置，然后修改超时设置",
            "不要修改旧代码，但新增测试",
        ):
            with self.subTest(task=task):
                self.assertTrue(assess_task(task)["mutation"])

    def test_write_executor_verbs_are_mutations(self):
        for task in ("删除文件", "创建目录", "部署服务"):
            with self.subTest(task=task):
                self.assertTrue(assess_task(task)["mutation"])

    def test_common_security_fix_verbs_are_mutations(self):
        result = assess_task("审计安全配置并修复生产漏洞")
        self.assertTrue(result["mutation"])
        self.assertEqual(result["mode"], "audited")


if __name__ == "__main__":
    unittest.main()
