#!/usr/bin/env python3
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED_SKILLS = {"architect", "maintain-architecture-decisions"}
REQUIRED_SECTIONS = {
    "Decision question",
    "Current decision",
    "Context and forces",
    "Invariants",
    "Alternatives and trade-offs",
    "Consequences",
    "Enforcement",
    "Revisit when",
}


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), path
    _, header, body = text.split("---\n", 2)
    return yaml.safe_load(header), body


class PackageStructureTests(unittest.TestCase):
    """Deterministic architectural contract invoked by adr check."""

    def test_exact_skill_surface_and_structured_visibility(self) -> None:
        skills = {path.name for path in SKILLS.iterdir() if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, skills)
        for name in sorted(skills):
            metadata, _ = frontmatter(SKILLS / name / "SKILL.md")
            self.assertEqual(name, metadata["name"])
            self.assertIsInstance(metadata["description"], str)
            self.assertLessEqual(len(metadata["description"]), 1024)
        architect = yaml.safe_load(
            (SKILLS / "architect" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        internal = yaml.safe_load(
            (SKILLS / "maintain-architecture-decisions" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        )
        self.assertNotEqual(False, architect.get("policy", {}).get("allow_implicit_invocation"))
        self.assertEqual(False, internal["policy"]["allow_implicit_invocation"])
        self.assertFalse((SKILLS / "clarify-and-plan").exists())
        self.assertFalse((SKILLS / "execute-to-pr").exists())

    def test_internal_skill_metadata_does_not_advertise_invocation(self) -> None:
        internal = (SKILLS / "maintain-architecture-decisions" / "agents" / "openai.yaml").read_text(encoding="utf-8")
        self.assertNotIn("$maintain-architecture-decisions", internal)
        architect = yaml.safe_load((SKILLS / "architect" / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        self.assertIn("$architect", architect["interface"]["default_prompt"])

    def test_adr_contract_is_repository_owned_and_tool_neutral(self) -> None:
        readme = (ROOT / "adr" / "README.md").read_text(encoding="utf-8")
        marker = yaml.safe_load((ROOT / "adr" / ".adr-system.yaml").read_text(encoding="utf-8"))
        index = yaml.safe_load((ROOT / "adr" / "index.yaml").read_text(encoding="utf-8"))
        self.assertEqual("semantic-living-adr", marker["schema"])
        self.assertEqual("semantic-living-adr-index", index["schema"])
        self.assertNotIn("generated_by", index)
        self.assertIn("repository-owned architecture data", readme)
        self.assertIn("reference clients, not exclusive authorities", readme)
        self.assertTrue((ROOT / "scripts" / "adr").is_file())

    def test_legacy_migration_playbook_is_connected_to_architect(self) -> None:
        architect = (SKILLS / "architect" / "SKILL.md").read_text(encoding="utf-8")
        maintainer = (SKILLS / "maintain-architecture-decisions" / "SKILL.md").read_text(encoding="utf-8")
        playbook = SKILLS / "maintain-architecture-decisions" / "references" / "migrate-legacy-v2.md"
        self.assertTrue(playbook.is_file())
        self.assertIn("migrate-legacy-v2.md", architect)
        self.assertIn("migrate-legacy-v2.md", maintainer)
        text = playbook.read_text(encoding="utf-8")
        self.assertIn("Do not assume one legacy enforcement entry equals one invariant", text)
        self.assertIn("update only the marker", text)
        self.assertIn("Do not resume the original change until migration passes", text)

    def test_skill_documents_have_bounded_progressive_disclosure(self) -> None:
        for path in sorted(SKILLS.glob("*/SKILL.md")):
            lines = path.read_text(encoding="utf-8").splitlines()
            self.assertLessEqual(len(lines), 180, path)
        self.assertTrue((SKILLS / "maintain-architecture-decisions" / "references" / "decision-policy.md").is_file())

    def test_adr_records_have_matching_body_invariant_ids(self) -> None:
        for path in sorted((ROOT / "adr" / "records").rglob("*.md")):
            metadata, body = frontmatter(path)
            ids = {entry["id"] for entry in metadata["invariants"]}
            body_ids = set(re.findall(r"^- `([a-z][a-z0-9-]*)`:", body, flags=re.MULTILINE))
            self.assertEqual(ids, body_ids, path)
            headings = set(re.findall(r"^## (.+)$", body, flags=re.MULTILINE))
            self.assertTrue(REQUIRED_SECTIONS.issubset(headings), path)

    def test_no_legacy_substring_enforcement_in_records(self) -> None:
        for path in sorted((ROOT / "adr" / "records").rglob("*.md")):
            metadata, _ = frontmatter(path)
            serialized = json.dumps(metadata)
            self.assertNotIn("must_contain", serialized)
            self.assertNotIn("must_not_contain", serialized)
            self.assertNotIn("enforcement_exception", serialized)

    def test_scenario_evidence_covers_manual_invariants(self) -> None:
        scenarios = json.loads((ROOT / "tests" / "scenarios.json").read_text(encoding="utf-8"))
        scenario_ids = {item["id"] for item in scenarios}
        for path in sorted((ROOT / "adr" / "records").rglob("*.md")):
            metadata, _ = frontmatter(path)
            for entry in metadata["enforcement"]:
                if entry["kind"] != "manual":
                    continue
                for evidence in entry["evidence"]:
                    if evidence.startswith("tests/scenarios.json#"):
                        self.assertIn(evidence.split("#", 1)[1], scenario_ids)


class PackagingTests(unittest.TestCase):
    def test_plugin_manifest_points_to_skills(self) -> None:
        manifest = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("./skills/", manifest["skills"])

    def test_scripts_are_executable(self) -> None:
        for path in [
            ROOT / "scripts" / "check.sh",
            ROOT / "scripts" / "adr",
            SKILLS / "maintain-architecture-decisions" / "scripts" / "adr",
        ]:
            self.assertTrue(path.stat().st_mode & 0o111, path)


if __name__ == "__main__":
    unittest.main()
