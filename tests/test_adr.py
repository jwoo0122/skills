#!/usr/bin/env python3
import importlib.util
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Optional
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "maintain-architecture-decisions" / "scripts" / "adr.py"
LAUNCHER = ROOT / "skills" / "maintain-architecture-decisions" / "scripts" / "adr"
DOGFOOD = ROOT / "adr"


def load_adr_tool():
    spec = importlib.util.spec_from_file_location("adr_tool_under_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ADR_TOOL = load_adr_tool()


class AdrToolTests(unittest.TestCase):
    def run_cli(self, command: str, root: Path, expected: int = 0) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            [sys.executable, str(SCRIPT), command, "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def copy_dogfood(self, destination: Path) -> None:
        shutil.copytree(DOGFOOD, destination / "adr")

    def run_launcher(
        self,
        *arguments: str,
        python: Optional[str] = None,
    ) -> subprocess.CompletedProcess[str]:
        environment = os.environ.copy()
        if python is not None:
            environment["ADR_PYTHON"] = python
        return subprocess.run(
            [str(LAUNCHER), *arguments],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )

    def test_launcher_selects_explicit_python(self) -> None:
        result = self.run_launcher("--print-python", python=sys.executable)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            Path(sys.executable).resolve(),
            Path(result.stdout.strip()).resolve(),
        )

    def test_launcher_runs_adr_with_selected_python(self) -> None:
        result = self.run_launcher(
            "validate",
            "--root",
            str(ROOT),
            python=sys.executable,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("validate: ok (6 records)", result.stdout)
        self.assertIn("PyYAML", result.stderr)

    def test_launcher_rejects_explicit_python_without_pyyaml(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            fake_python = Path(directory) / "python"
            fake_python.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            fake_python.chmod(0o755)

            result = self.run_launcher("--print-python", python=str(fake_python))

        self.assertEqual(2, result.returncode)
        self.assertIn("cannot import PyYAML", result.stderr)
        self.assertIn("ADR_PYTHON", result.stderr)

    def test_launcher_skips_unusable_path_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            unusable_python = directory_path / "python3"
            unusable_python.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
            unusable_python.chmod(0o755)

            usable_python = directory_path / "python"
            usable_python.write_text(
                f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n",
                encoding="utf-8",
            )
            usable_python.chmod(0o755)

            environment = os.environ.copy()
            environment.pop("ADR_PYTHON", None)
            environment.pop("VIRTUAL_ENV", None)
            environment["PATH"] = f"{directory}{os.pathsep}{environment['PATH']}"
            result = subprocess.run(
                [str(LAUNCHER), "--print-python"],
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            Path(sys.executable).resolve(),
            Path(result.stdout.strip()).resolve(),
        )

    def test_launcher_checks_repository_virtualenv_before_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repository = Path(directory) / "repository"
            repository.mkdir()
            repository_python = repository / ".venv" / "bin" / "python"
            repository_python.parent.mkdir(parents=True)
            repository_python.write_text(
                f"#!/bin/sh\nexec {shlex.quote(sys.executable)} \"$@\"\n",
                encoding="utf-8",
            )
            repository_python.chmod(0o755)

            unusable_path = Path(directory) / "path"
            unusable_path.mkdir()
            for name in ("python3", "python"):
                candidate = unusable_path / name
                candidate.write_text("#!/bin/sh\nexit 7\n", encoding="utf-8")
                candidate.chmod(0o755)

            environment = os.environ.copy()
            environment.pop("ADR_PYTHON", None)
            environment.pop("VIRTUAL_ENV", None)
            environment["PATH"] = f"{unusable_path}{os.pathsep}{environment['PATH']}"
            result = subprocess.run(
                [str(LAUNCHER), "--print-python", "--root", str(repository)],
                text=True,
                capture_output=True,
                env=environment,
                check=False,
            )

        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertEqual(
            Path(sys.executable).resolve(),
            Path(result.stdout.strip()).resolve(),
        )

    def test_dogfood_records_and_index_validate(self) -> None:
        result = self.run_cli("validate", ROOT)
        self.assertIn("validate: ok (6 records)", result.stdout)

    def test_dogfood_enforcement_checks_pass(self) -> None:
        result = self.run_cli("check", ROOT)
        self.assertIn("check: ok (9 enforcement checks)", result.stdout)

    def test_enforcement_detects_source_drift(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            shutil.copytree(ROOT / "skills", root / "skills")
            source = root / "skills" / "clarify-and-plan" / "SKILL.md"
            source.write_text(
                source.read_text(encoding="utf-8").replace(
                    "sole user-facing entry point", "the entry point", 1
                ),
                encoding="utf-8",
            )
            result = self.run_cli("check", root, expected=1)
            self.assertIn("enforcement failed", result.stderr)
            self.assertIn("workflow.public-entrypoint/sole-entry", result.stderr)

    def test_enforcement_detects_forbidden_source_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            shutil.copytree(ROOT / "skills", root / "skills")
            source = root / "skills" / "execute-to-pr" / "agents" / "openai.yaml"
            source.write_text(source.read_text(encoding="utf-8") + "\n$execute-to-pr\n", encoding="utf-8")
            result = self.run_cli("check", root, expected=1)
            self.assertIn("forbids", result.stderr)
            self.assertIn("workflow.public-entrypoint/internal-metadata", result.stderr)

    def test_enforcement_exception_allows_explicit_manual_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            shutil.copytree(ROOT / "skills", root / "skills")
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            text = record.read_text(encoding="utf-8")
            start = text.index("enforcement:\n")
            end = text.index("---\n", start)
            exception = (
                "enforcement: []\n"
                "enforcement_exception:\n"
                "  status: manual\n"
                "  reason: The harness exposes internal skill visibility outside repository text.\n"
                "  evidence:\n"
                "    - tests/test_package.py::check_skills\n"
                "  revisit_when:\n"
                "    - The Agent Skills specification defines private composition.\n"
            )
            record.write_text(text[:start] + exception + text[end:], encoding="utf-8")
            self.run_cli("reindex", root)
            result = self.run_cli("check", root)
            self.assertIn("7 enforcement checks, 1 declared exception", result.stdout)

    def test_enforcement_requires_nonempty_checks_for_accepted_records(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            shutil.copytree(ROOT / "skills", root / "skills")
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            text = record.read_text(encoding="utf-8")
            start = text.index("enforcement:\n")
            end = text.index("---\n", start)
            record.write_text(text[:start] + "enforcement: []\n" + text[end:], encoding="utf-8")
            self.run_cli("reindex", root)
            result = self.run_cli("check", root, expected=1)
            self.assertIn("no enforcement checks or declared exception", result.stderr)

    def test_enforcement_rejects_stale_index(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "clarify-and-plan is the sole user-facing entry point",
                    "clarify-and-plan remains the sole user-facing entry point",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_cli("check", root, expected=1)
            self.assertIn("stale index", result.stderr)

    def test_enforcement_rejects_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            shutil.copytree(ROOT / "skills", root / "skills")
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "skills/clarify-and-plan/SKILL.md", "skills/missing/SKILL.md", 1
                ),
                encoding="utf-8",
            )
            self.run_cli("reindex", root)
            result = self.run_cli("check", root, expected=1)
            self.assertIn("matched no files", result.stderr)

    def test_init_is_non_destructive_and_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = self.run_cli("init", root)
            readme = root / "adr" / "README.md"
            template = root / "adr" / "_template.md"
            index = root / "adr" / "index.yaml"
            self.assertTrue(readme.is_file())
            self.assertTrue(template.is_file())
            self.assertTrue(index.is_file())
            self.assertTrue((root / "adr" / ".adr-system.yaml").is_file())
            self.assertTrue((root / "adr" / "records").is_dir())
            self.assertIn("initialized:", first.stdout)

            readme.write_text("user-owned\n", encoding="utf-8")
            second = self.run_cli("init", root)
            self.assertEqual("user-owned\n", readme.read_text(encoding="utf-8"))
            self.assertIn("no changes", second.stdout)
            self.run_cli("validate", root)

    def test_init_rejects_unmarked_or_incompatible_existing_adr(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            adr_root = root / "adr"
            adr_root.mkdir()
            (adr_root / "README.md").write_text("unmanaged\n", encoding="utf-8")
            result = self.run_cli("init", root, expected=1)
            self.assertIn("ownership marker is missing", result.stderr)
            self.assertFalse((adr_root / ".adr-system.yaml").exists())
            self.assertFalse((adr_root / "index.yaml").exists())

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_cli("init", root)
            marker = root / "adr" / ".adr-system.yaml"
            marker.write_text(
                "schema: maintain-architecture-decisions\nversion: 99\n",
                encoding="utf-8",
            )
            result = self.run_cli("init", root, expected=1)
            self.assertIn("marker/version conflict", result.stderr)

    def test_writes_reject_symlinked_or_external_adr_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            external_adr = Path(outside) / "adr"
            external_adr.mkdir()
            (root / "adr").symlink_to(external_adr, target_is_directory=True)
            result = self.run_cli("init", root, expected=1)
            self.assertIn("refusing symlinked ADR directory", result.stderr)
            self.assertEqual([], list(external_adr.iterdir()))

        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            self.copy_dogfood(root)
            index = root / "adr" / "index.yaml"
            index.unlink()
            external_index = Path(outside) / "index.yaml"
            external_index.write_text("external\n", encoding="utf-8")
            index.symlink_to(external_index)
            result = self.run_cli("reindex", root, expected=1)
            self.assertIn("refusing symlink inside ADR directory", result.stderr)
            self.assertEqual("external\n", external_index.read_text(encoding="utf-8"))

    def test_reindex_repairs_stale_index_and_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "summary: \"clarify-and-plan is the sole user-facing entry point for the workflow skill set.\"",
                    "summary: \"clarify-and-plan remains the sole public workflow entry point.\"",
                ),
                encoding="utf-8",
            )

            stale = self.run_cli("validate", root, expected=1)
            self.assertIn("stale index", stale.stderr)
            self.run_cli("reindex", root)
            index = root / "adr" / "index.yaml"
            first = index.read_bytes()
            unchanged = self.run_cli("reindex", root)
            self.assertEqual(first, index.read_bytes())
            self.assertIn("unchanged", unchanged.stdout)
            self.run_cli("validate", root)

    def test_reindex_recovers_missing_index_with_same_directory_atomic_replace(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            index = root / "adr" / "index.yaml"
            index.unlink()
            calls: list[tuple[Path, Path]] = []
            original_replace = os.replace

            def tracked_replace(source, destination):
                calls.append((Path(source), Path(destination)))
                return original_replace(source, destination)

            with mock.patch.object(ADR_TOOL.os, "replace", side_effect=tracked_replace):
                ADR_TOOL.reindex_repository(root)

            self.assertEqual(1, len(calls))
            source, destination = calls[0]
            self.assertEqual(index.parent.resolve(), source.parent.resolve())
            self.assertEqual(index.parent.resolve(), destination.parent.resolve())
            self.assertEqual(index.resolve(), destination.resolve())
            self.run_cli("validate", root)

    def test_atomic_write_uses_normal_new_mode_and_preserves_existing_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "new.yaml"
            with mock.patch.object(ADR_TOOL.os, "umask", side_effect=[0o022, None]):
                ADR_TOOL.atomic_write(path, "new\n")
            self.assertEqual(0o644, path.stat().st_mode & 0o777)

            path.chmod(0o640)
            ADR_TOOL.atomic_write(path, "replacement\n")
            self.assertEqual(0o640, path.stat().st_mode & 0o777)

    def test_validate_rejects_non_semantic_ids(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_cli("init", root)
            path = root / "adr" / "records" / "system" / "0001-choice.md"
            path.parent.mkdir(parents=True)
            body = (root / "adr" / "_template.md").read_text(encoding="utf-8")
            path.write_text(
                body.replace("template: true\n", "")
                .replace("scope.stable-question", "system.0001-choice")
                .replace("scope: scope", "scope: system")
                .replace("applies_to: []", "applies_to:\n  - src/**"),
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("non-semantic ADR id", result.stderr)

    def test_validate_rejects_template_sentinel_and_empty_sections(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_cli("init", root)
            record = root / "adr" / "records" / "scope" / "stable-question.md"
            record.parent.mkdir(parents=True)
            shutil.copyfile(root / "adr" / "_template.md", record)
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("template sentinel remains", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            text = record.read_text(encoding="utf-8")
            record.write_text(
                text[: text.index("## Revisit when")] + "## Revisit when\n\n",
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("empty section 'Revisit when'", result.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.run_cli("init", root)
            record = root / "adr" / "records" / "system" / "stable-question.md"
            record.parent.mkdir(parents=True)
            text = (root / "adr" / "_template.md").read_text(encoding="utf-8")
            record.write_text(
                text.replace("template: true\n", "")
                .replace("scope.stable-question", "system.stable-question")
                .replace("scope: scope", "scope: system")
                .replace("applies_to: []", "applies_to:\n  - src/**")
                .replace('last_reviewed: "YYYY-MM-DD"', 'last_reviewed: "2026-07-15"'),
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("template placeholder remains", result.stderr)

    def test_validate_rejects_duplicate_yaml_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "status: accepted", "status: accepted\nstatus: retired", 1
                ),
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("duplicate key: 'status'", result.stderr)

    def test_validate_rejects_invalid_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace("status: accepted", "status: historical", 1),
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("invalid status", result.stderr)

    def test_validate_rejects_missing_and_inconsistent_relations(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
            record.write_text(
                record.read_text(encoding="utf-8").replace(
                    "depends_on: []", "depends_on:\n  - missing.decision", 1
                ),
                encoding="utf-8",
            )
            missing = self.run_cli("validate", root, expected=1)
            self.assertIn("references missing ADR", missing.stderr)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            record = root / "adr" / "records" / "architecture" / "living-decisions.md"
            record.write_text(
                record.read_text(encoding="utf-8")
                .replace("status: accepted", "status: superseded", 1)
                .replace(
                    "superseded_by: []",
                    "superseded_by:\n  - workflow.public-entrypoint",
                    1,
                ),
                encoding="utf-8",
            )
            inconsistent = self.run_cli("validate", root, expected=1)
            self.assertIn("supersession is not bidirectional", inconsistent.stderr)

    def test_accepted_dependencies_must_also_be_accepted(self) -> None:
        for status in ("proposed", "retired", "superseded"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.copy_dogfood(root)
                public = root / "adr" / "records" / "workflow" / "public-entrypoint.md"
                public_text = public.read_text(encoding="utf-8").replace(
                    "status: accepted", f"status: {status}", 1
                )
                if status == "superseded":
                    public_text = public_text.replace(
                        "superseded_by: []",
                        "superseded_by:\n  - workflow.independent-facets",
                        1,
                    )
                    replacement = (
                        root / "adr" / "records" / "workflow" / "independent-facets.md"
                    )
                    replacement.write_text(
                        replacement.read_text(encoding="utf-8").replace(
                            "supersedes: []",
                            "supersedes:\n  - workflow.public-entrypoint",
                            1,
                        ),
                        encoding="utf-8",
                    )
                public.write_text(public_text, encoding="utf-8")
                result = self.run_cli("validate", root, expected=1)
                self.assertIn(
                    f"depends on {status} ADR: workflow.public-entrypoint",
                    result.stderr,
                )

    def test_proposed_or_retired_records_may_not_replace_decisions(self) -> None:
        for status in ("proposed", "retired"):
            with self.subTest(status=status), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                self.copy_dogfood(root)
                replaced = root / "adr" / "records" / "architecture" / "living-decisions.md"
                replaced.write_text(
                    replaced.read_text(encoding="utf-8")
                    .replace("status: accepted", "status: superseded", 1)
                    .replace(
                        "superseded_by: []",
                        "superseded_by:\n  - interaction.material-ambiguity-loop",
                        1,
                    ),
                    encoding="utf-8",
                )
                replacement = (
                    root / "adr" / "records" / "interaction" / "material-ambiguity-loop.md"
                )
                replacement.write_text(
                    replacement.read_text(encoding="utf-8")
                    .replace("status: accepted", f"status: {status}", 1)
                    .replace(
                        "supersedes: []",
                        "supersedes:\n  - architecture.living-decisions",
                        1,
                    ),
                    encoding="utf-8",
                )
                result = self.run_cli("validate", root, expected=1)
                self.assertIn(
                    "superseded_by target must have accepted or superseded status",
                    result.stderr,
                )

    def test_non_accepted_record_cannot_declare_supersedes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            replaced = root / "adr" / "records" / "interaction" / "material-ambiguity-loop.md"
            replaced.write_text(
                replaced.read_text(encoding="utf-8")
                .replace("status: accepted", "status: superseded", 1)
                .replace(
                    "superseded_by: []",
                    "superseded_by:\n  - architecture.living-decisions",
                    1,
                ),
                encoding="utf-8",
            )
            replacement = root / "adr" / "records" / "architecture" / "living-decisions.md"
            replacement.write_text(
                replacement.read_text(encoding="utf-8")
                .replace("status: accepted", "status: proposed", 1)
                .replace(
                    "supersedes: []",
                    "supersedes:\n  - interaction.material-ambiguity-loop",
                    1,
                ),
                encoding="utf-8",
            )
            result = self.run_cli("validate", root, expected=1)
            self.assertIn("only accepted or superseded ADRs may supersede", result.stderr)

    def test_multi_generation_supersession_chain_is_valid(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.copy_dogfood(root)
            body = "\n".join(
                [
                    "# Supersession fixture",
                    "",
                    *[
                        f"## {section}\n\nFixture evidence."
                        for section in ADR_TOOL.REQUIRED_SECTIONS
                    ],
                    "",
                ]
            )

            def write_record(
                decision_id: str,
                status: str,
                supersedes: list[str],
                superseded_by: list[str],
            ) -> None:
                data = {
                    "id": decision_id,
                    "status": status,
                    "scope": "history",
                    "decision_type": "test-fixture",
                    "applies_to": ["src/**"],
                    "summary": f"Fixture for {decision_id}.",
                    "constrains": [],
                    "depends_on": [],
                    "supersedes": supersedes,
                    "superseded_by": superseded_by,
                    "last_reviewed": "2026-07-15",
                    "enforcement": [],
                }
                path = root / "adr" / "records" / Path(*decision_id.split(".")).with_suffix(".md")
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    f"---\n{ADR_TOOL.dump_yaml(data)}---\n{body}",
                    encoding="utf-8",
                )

            write_record("history.first", "superseded", [], ["history.second"])
            write_record(
                "history.second",
                "superseded",
                ["history.first"],
                ["history.current"],
            )
            write_record("history.current", "accepted", ["history.second"], [])
            self.run_cli("reindex", root)
            self.run_cli("validate", root)

    def test_missing_pyyaml_has_an_actionable_error(self) -> None:
        result = subprocess.run(
            [sys.executable, "-S", str(SCRIPT), "validate", "--root", str(ROOT)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, result.returncode)
        self.assertIn("PyYAML is required", result.stderr)
        self.assertIn("scripts/adr", result.stderr)


if __name__ == "__main__":
    unittest.main()
