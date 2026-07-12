import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from guanzai.cli import capabilities


class DoctorTests(unittest.TestCase):
    @patch("guanzai.cli.Path.exists", return_value=False)
    @patch("guanzai.cli.shutil.which", return_value=None)
    def test_absent_workbuddy_is_reported_without_claiming_execution(self, _which, _exists):
        report = capabilities()
        self.assertFalse(report["workbuddy"]["execution"])
        self.assertFalse(report["workbuddy"]["model_selection"])
        self.assertFalse(report["codex"]["per_subagent_model_selection"])

    @patch("guanzai.cli.shutil.which", return_value="/Applications/WorkBuddy/codebuddy")
    def test_present_workbuddy_exposes_model_and_reasoning_selection(self, _which):
        report = capabilities()
        self.assertTrue(report["workbuddy"]["execution"])
        self.assertTrue(report["workbuddy"]["model_selection"])
        self.assertTrue(report["workbuddy"]["reasoning_selection"])

    @patch("guanzai.cli.Path.exists", return_value=True)
    @patch("guanzai.cli.shutil.which", return_value=None)
    def test_bundled_workbuddy_cli_is_discovered(self, _which, _exists):
        report = capabilities()
        self.assertTrue(report["workbuddy"]["execution"])
        self.assertIn("WorkBuddy.app", report["workbuddy"]["cli"])


if __name__ == "__main__":
    unittest.main()
