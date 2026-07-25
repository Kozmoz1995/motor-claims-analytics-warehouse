import unittest
from pathlib import Path

from motor_dwh.cli import validate_file


class CliTests(unittest.TestCase):
    def test_sample_quality_summary(self):
        report = validate_file(Path("data/sample/crashes.jsonl"))
        self.assertEqual(4, report["total"])
        self.assertEqual(2, report["valid"])
        self.assertEqual(1, report["errors"]["duplicate_collision_id"])
        self.assertEqual(1, report["errors"]["injury_components_exceed_total"])


if __name__ == "__main__":
    unittest.main()
