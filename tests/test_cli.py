import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class CliTests(unittest.TestCase):
    def run_cli(self, *args, cwd):
        env = os.environ.copy()
        env["PYTHONPATH"] = str(ROOT / "src")
        return subprocess.run(
            [sys.executable, "-m", "guanzai.cli", *args],
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
        )

    def test_init_creates_project_policy_without_overwriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = self.run_cli("init", cwd=tmp)
            self.assertEqual(first.returncode, 0, first.stderr)
            config = Path(tmp) / ".guanzai" / "config.toml"
            self.assertTrue(config.exists())
            config.write_text("sentinel = true\n", encoding="utf-8")
            second = self.run_cli("init", cwd=tmp)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(config.read_text(encoding="utf-8"), "sentinel = true\n")

    def test_plan_outputs_machine_readable_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.run_cli("init", cwd=tmp)
            result = self.run_cli("plan", "开发一个金融数据仪表盘", "--json", cwd=tmp)
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["schema_version"], "0.2")
            self.assertGreaterEqual(len(payload["work_items"]), 1)


if __name__ == "__main__":
    unittest.main()
