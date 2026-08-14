#!/usr/bin/env python3
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "maintain-architecture-decisions" / "scripts" / "adr.py"
LAUNCHER = ROOT / "skills" / "maintain-architecture-decisions" / "scripts" / "adr"
class AdrTestCase(unittest.TestCase):
    def run_cli(self, command: str, root: Path, expected: int = 0):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), command, "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def write_repo(
        self,
        root: Path,
        *,
        invariants: str = """\
  - id: contract-holds
    statement: "The contract holds."
""",
        enforcement: str = """\
  - invariant: contract-holds
    kind: executable
    check: contract
""",
        registry: str = """\
  contract:
    argv:
      - python3
      - -c
      - "pass"
""",
        expected: int = 0,
    ):
        adr = root / "adr"
        (adr / "records" / "scope").mkdir(parents=True)
        (adr / "README.md").write_text("# ADR\n", encoding="utf-8")
        (adr / "_template.md").write_text("# template\n", encoding="utf-8")
        checks_yaml = "checks: {}\n" if registry.strip() == "{}" else "checks:\n" + registry
        (adr / ".adr-system.yaml").write_text(
            "schema: maintain-architecture-decisions\nversion: 3\n" + checks_yaml,
            encoding="utf-8",
        )
        invariants_yaml = "invariants: []\n" if invariants.strip() == "[]" else "invariants:\n" + invariants
        enforcement_yaml = "enforcement: []\n" if enforcement.strip() == "[]" else "enforcement:\n" + enforcement
        record = f"""\
---
id: scope.question
status: accepted
scope: scope
decision_type: policy
applies_to:
  - src/**
summary: "Current answer"
constrains: []
depends_on: []
supersedes: []
superseded_by: []
last_reviewed: "2026-08-15"
{invariants_yaml}{enforcement_yaml}---

# Decision

## Decision question
Question?

## Current decision
Answer.

## Context and forces
Context.

## Invariants
Contract.

## Alternatives and trade-offs
Alternative.

## Consequences
Consequence.

## Enforcement
Checks.

## Revisit when
Trigger.
"""
        (adr / "records" / "scope" / "question.md").write_text(record, encoding="utf-8")
        return self.run_cli("reindex", root, expected=expected)


class AdrSchemaContractTests(AdrTestCase):
    """Deterministic contract used by the dogfood ADR registry."""

    def test_dogfood_repository_validates(self) -> None:
        result = self.run_cli("validate", ROOT)
        self.assertIn("validate: ok (4 records)", result.stdout)

    def test_accepted_record_requires_invariants(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.write_repo(root, invariants="[]\n", enforcement="[]\n", expected=1)
            self.assertIn("accepted ADR must declare invariants", result.stderr)

    def test_every_invariant_requires_exactly_one_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = self.write_repo(root, enforcement="[]\n", expected=1)
            self.assertIn("unenforced invariants", result.stderr)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            duplicate = """\
  - invariant: contract-holds
    kind: executable
    check: contract
  - invariant: contract-holds
    kind: executable
    check: contract
"""
            result = self.write_repo(root, enforcement=duplicate, expected=1)
            self.assertIn("multiple enforcement", result.stderr)

    def test_legacy_source_substring_enforcement_is_rejected(self) -> None:
        legacy = """\
  - invariant: contract-holds
    kind: executable
    check: contract
    must_contain:
      - magic
"""
        with tempfile.TemporaryDirectory() as directory:
            result = self.write_repo(Path(directory), enforcement=legacy, expected=1)
            self.assertIn("must contain invariant, kind, and check", result.stderr)

    def test_manual_mapping_requires_reason_evidence_and_revisit_condition(self) -> None:
        incomplete = """\
  - invariant: contract-holds
    kind: manual
    reason: "Contextual"
    evidence: []
    revisit_when:
      - "Harness support exists."
"""
        with tempfile.TemporaryDirectory() as directory:
            result = self.write_repo(Path(directory), enforcement=incomplete, expected=1)
            self.assertIn("evidence must be a non-empty", result.stderr)

    def test_registry_requires_argv_and_rejects_recursive_adr_check(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.write_repo(Path(directory), registry="  contract:\n    run: echo pass\n", expected=1)
            self.assertIn("must contain only argv", result.stderr)
        recursive = """\
  contract:
    argv:
      - skills/maintain-architecture-decisions/scripts/adr
      - check
"""
        with tempfile.TemporaryDirectory() as directory:
            result = self.write_repo(Path(directory), registry=recursive, expected=1)
            self.assertIn("recursively invoke", result.stderr)

    def test_registered_check_runs_once_from_repository_root(self) -> None:
        script = "from pathlib import Path; p=Path('count'); p.write_text(str(int(p.read_text())+1) if p.exists() else '1')"
        registry = f"""\
  contract:
    argv:
      - {shlex.quote(sys.executable)}
      - -c
      - {script!r}
"""
        invariants = """\
  - id: first
    statement: "First."
  - id: second
    statement: "Second."
"""
        enforcement = """\
  - invariant: first
    kind: executable
    check: contract
  - invariant: second
    kind: executable
    check: contract
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root, invariants=invariants, enforcement=enforcement, registry=registry)
            result = self.run_cli("check", root)
            self.assertEqual("1", (root / "count").read_text(encoding="utf-8"))
            self.assertIn("1 executable checks", result.stdout)

    def test_python_registry_token_uses_current_interpreter(self) -> None:
        registry = """\
  contract:
    argv:
      - "{python}"
      - -c
      - "from pathlib import Path; Path('python-path').write_text(__import__('sys').executable)"
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root, registry=registry)
            self.run_cli("check", root)
            self.assertEqual(Path(sys.executable).resolve(), Path((root / "python-path").read_text()).resolve())

    def test_failed_check_names_all_covered_invariants(self) -> None:
        registry = f"""\
  contract:
    argv:
      - {shlex.quote(sys.executable)}
      - -c
      - "raise SystemExit(7)"
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root, registry=registry)
            result = self.run_cli("check", root, expected=1)
            self.assertIn("contract: exited 7", result.stderr)
            self.assertIn("scope.question/contract-holds", result.stderr)

    def test_manual_invariant_is_explicitly_not_mechanically_verified(self) -> None:
        manual = """\
  - invariant: contract-holds
    kind: manual
    reason: "Requires contextual judgment."
    evidence:
      - evidence/review.md
    revisit_when:
      - "A deterministic evaluator exists."
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root, enforcement=manual, registry="{}\n")
            result = self.run_cli("check", root)
            self.assertIn("manual (not mechanically verified)", result.stdout)
            self.assertIn("0 executable checks, 1 manual", result.stdout)

    def test_unregistered_check_fails_global_gate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root, registry="{}\n")
            result = self.run_cli("check", root, expected=1)
            self.assertIn("unregistered check", result.stderr)

    def test_stale_index_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.write_repo(root)
            index = root / "adr" / "index.yaml"
            index.write_text(
                index.read_text(encoding="utf-8").replace(
                    "generated_by: maintain-architecture-decisions", "generated_by: stale-generator"
                ),
                encoding="utf-8",
            )
            self.run_cli("validate", root, expected=1)


class AdrLauncherTests(AdrTestCase):
    def run_launcher(self, *arguments: str, python: Optional[str] = None):
        env = os.environ.copy()
        if python is not None:
            env["ADR_PYTHON"] = python
        return subprocess.run([str(LAUNCHER), *arguments], text=True, capture_output=True, env=env, check=False)

    def test_launcher_selects_explicit_compatible_python(self) -> None:
        result = self.run_launcher("--print-python", python=sys.executable)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(Path(sys.executable).resolve(), Path(result.stdout.strip()).resolve())

    def test_launcher_rejects_python_without_pyyaml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fake = Path(directory) / "python"
            fake.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            fake.chmod(0o755)
            result = self.run_launcher("--print-python", python=str(fake))
        self.assertEqual(2, result.returncode)
        self.assertIn("cannot import PyYAML", result.stderr)

    def test_launcher_runs_with_explicit_compatible_python(self) -> None:
        result = self.run_launcher("validate", "--root", str(ROOT), python=sys.executable)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("validate: ok (4 records)", result.stdout)
        self.assertIn("PyYAML", result.stderr)

    def test_launcher_skips_unusable_path_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            unusable = directory_path / "python3"
            unusable.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            unusable.chmod(0o755)
            usable = directory_path / "python"
            usable.write_text(f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n", encoding="utf-8")
            usable.chmod(0o755)
            env = os.environ.copy()
            env.pop("ADR_PYTHON", None)
            env.pop("VIRTUAL_ENV", None)
            env["PATH"] = f"{directory}{os.pathsep}{env['PATH']}"
            result = subprocess.run([str(LAUNCHER), "--print-python"], text=True, capture_output=True, env=env, check=False)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(Path(sys.executable).resolve(), Path(result.stdout.strip()).resolve())

    def test_launcher_prefers_repository_virtualenv(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            candidate = root / ".venv" / "bin" / "python"
            candidate.parent.mkdir(parents=True)
            candidate.write_text(f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n", encoding="utf-8")
            candidate.chmod(0o755)
            env = os.environ.copy()
            env.pop("ADR_PYTHON", None)
            env.pop("VIRTUAL_ENV", None)
            result = subprocess.run(
                [str(LAUNCHER), "--print-python", "--root", str(root)],
                text=True, capture_output=True, env=env, check=False,
            )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(Path(sys.executable).resolve(), Path(result.stdout.strip()).resolve())

    def test_init_refuses_unowned_nonempty_adr_directory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "adr").mkdir()
            (root / "adr" / "notes.md").write_text("existing", encoding="utf-8")
            result = self.run_cli("init", root, expected=1)
            self.assertIn("marker is missing", result.stderr)

    def test_init_creates_versioned_empty_system(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_cli("init", root)
            marker = (root / "adr" / ".adr-system.yaml").read_text(encoding="utf-8")
            self.assertIn("version: 3", marker)
            self.assertIn("checks: {}", marker)
            self.run_cli("validate", root)


if __name__ == "__main__":
    unittest.main()
