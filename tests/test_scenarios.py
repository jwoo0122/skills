#!/usr/bin/env python3
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ScenarioEvidenceTests(unittest.TestCase):
    def test_scenarios_are_unique_and_actionable(self) -> None:
        scenarios = json.loads((ROOT / "tests" / "scenarios.json").read_text(encoding="utf-8"))
        ids = [scenario["id"] for scenario in scenarios]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(scenarios)
        for scenario in scenarios:
            self.assertTrue(scenario["request"].strip())
            self.assertGreaterEqual(len(scenario["expected"]), 2)
            self.assertTrue(all(item.strip() for item in scenario["expected"]))


if __name__ == "__main__":
    unittest.main()
