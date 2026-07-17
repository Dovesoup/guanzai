import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from guanzai.adapters import codex_command, workbuddy_command
from guanzai.packets import build_packet


ITEM = {
    "role": "auditor",
    "objective": "检查计费公式",
    "model": "gpt-5.6-terra",
    "reasoning": "low",
    "speed": "standard",
}


class PacketTests(unittest.TestCase):
    def test_packet_is_slim_and_self_verifying(self):
        packet = build_packet(ITEM)
        self.assertLess(len(packet), 1500)
        self.assertIn("strict JSON", packet)
        self.assertIn("Fast mode is forbidden", packet)
        self.assertIn("smallest change", packet)
        self.assertIn("speculative features", packet)
        self.assertIn("plausible failure modes", packet)
        self.assertIn("what was not tested", packet)
        self.assertNotIn("conversation history", packet.lower())

    def test_codex_command_selects_model_effort_and_ephemeral_mode(self):
        command = codex_command(ITEM, "/tmp/project")
        self.assertIn("gpt-5.6-terra", command)
        self.assertIn('model_reasoning_effort="low"', command)
        self.assertIn("--ephemeral", command)

    def test_workbuddy_command_disables_tools_for_reasoning_only(self):
        item = dict(ITEM, model="hy3")
        command = workbuddy_command(item, "/Applications/WorkBuddy.app")
        self.assertIn("--model", command)
        self.assertIn("hy3", command)
        self.assertIn("--tools", command)
        self.assertEqual(command[command.index("--tools") + 1], "")
        self.assertEqual(command[command.index("--effort") + 1], "high")

    def test_builder_gets_bounded_write_tools(self):
        builder = dict(ITEM, role="builder", objective="实现并测试功能", model="gpt-5.6-luna")
        codex = codex_command(builder, "/tmp/project")
        self.assertEqual(codex[codex.index("--sandbox") + 1], "workspace-write")
        workbuddy = workbuddy_command(dict(builder, model="hy3"), "/Applications/WorkBuddy.app")
        self.assertEqual(workbuddy[workbuddy.index("--tools") + 1], "Read,Edit,Bash")
        self.assertEqual(workbuddy[workbuddy.index("--max-turns") + 1], "3")


if __name__ == "__main__":
    unittest.main()
