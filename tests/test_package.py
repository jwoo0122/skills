#!/usr/bin/env python3
import json
import re
import stat
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "coding-workflow-core",
    "workflow-router",
    "clarify-and-plan",
    "execute-to-pr",
    "diagnose-bug",
    "evidence-research",
    "review-change",
    "maintain-architecture-decisions",
}
INTERNAL_SKILLS = {
    "coding-workflow-core",
    "workflow-router",
    "execute-to-pr",
    "diagnose-bug",
    "evidence-research",
    "review-change",
    "maintain-architecture-decisions",
}


class UniqueKeyLoader(yaml.SafeLoader):
    pass


def construct_mapping(loader: UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        assert key not in mapping, f"duplicate YAML key: {key}"
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)


def load_yaml(path: Path) -> Any:
    return yaml.load(path.read_text(), Loader=UniqueKeyLoader)


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text()
    assert "TODO" not in text, f"placeholder remains in {path}"
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert match, f"missing frontmatter in {path}"
    data = yaml.load(match.group(1), Loader=UniqueKeyLoader)
    assert isinstance(data, dict), f"frontmatter is not a mapping in {path}"
    return data


def check_skills() -> None:
    skills_root = ROOT / "skills"
    generated = [
        path
        for path in skills_root.rglob("*")
        if path.name == "__pycache__" or path.suffix in {".pyc", ".pyo"}
    ]
    assert not generated, f"generated Python artifacts remain in skill package: {generated}"
    found = {path.name for path in skills_root.iterdir() if path.is_dir()}
    assert found == EXPECTED_SKILLS, f"unexpected skill set: {found}"

    hidden_from_users = set()
    for skill_name in sorted(found):
        skill_file = skills_root / skill_name / "SKILL.md"
        data = frontmatter(skill_file)
        assert {"name", "description"} <= set(data), f"missing required frontmatter in {skill_file}"
        assert data["name"] == skill_name
        assert re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_name)
        assert isinstance(data["description"], str)
        assert 1 <= len(data["description"]) <= 1024
        assert len(skill_file.read_text().splitlines()) < 500
        if data.get("user-invocable") is False:
            hidden_from_users.add(skill_name)
            assert data["description"].startswith("Internal ")
        if skill_name in INTERNAL_SKILLS:
            assert data.get("user-invocable") is False, f"internal skill is user-visible: {skill_name}"
        openai_yaml = skills_root / skill_name / "agents" / "openai.yaml"
        assert openai_yaml.is_file(), f"missing Codex UI metadata for {skill_name}"
        metadata = load_yaml(openai_yaml)
        assert isinstance(metadata, dict) and isinstance(metadata.get("interface"), dict)
        interface = metadata["interface"]
        assert isinstance(interface.get("display_name"), str) and interface["display_name"]
        assert isinstance(interface.get("short_description"), str) and interface["short_description"]
        prompt = openai_yaml.read_text()
        if skill_name in INTERNAL_SKILLS:
            assert "display_name: \"Internal " in prompt
            assert f"${skill_name}" not in prompt, f"internal skill advertises direct invocation: {skill_name}"

    assert hidden_from_users == INTERNAL_SKILLS
    entrypoint = frontmatter(skills_root / "clarify-and-plan" / "SKILL.md")
    assert "user-invocable" not in entrypoint
    assert entrypoint["description"].startswith("User-facing ")

    all_skill_text = "\n".join(path.read_text() for path in skills_root.rglob("*") if path.is_file())
    assert "disable-model-invocation" not in all_skill_text
    assert "metadata.internal" not in all_skill_text


def check_policy_scope() -> None:
    banned = ("taskctl", ".tasks/", "central server")
    for path in (ROOT / "skills").rglob("*"):
        if path.is_file():
            lowered = path.read_text().lower()
            for term in banned:
                assert term not in lowered, f"excluded feature '{term}' found in {path}"


def check_legacy_install_removed() -> None:
    for relative in ("install.sh", "adapters", "tests/test_install.sh"):
        assert not (ROOT / relative).exists(), f"obsolete installation path remains: {relative}"


def check_scenarios() -> None:
    scenarios = json.loads((ROOT / "tests" / "scenarios.json").read_text())
    assert len(scenarios) >= 12
    ids = [scenario["id"] for scenario in scenarios]
    assert len(ids) == len(set(ids)), "duplicate scenario id"
    allowed = {
        "clarification": {"proceed", "ask"},
        "adr": {"none", "reference", "reconcile"},
        "execution": {"none", "direct", "delegate", "decompose"},
        "verification": {"self", "independent", "multi-axis"},
    }
    required_ids = {
        "read-only-diagnosis",
        "direct-typo",
        "implicit-local-delivery-boundary",
        "clarify-vague-onboarding",
        "clarify-conflicting-answers",
        "large-but-clear-retry-system",
        "small-code-large-architecture",
        "small-code-large-product-decision",
        "implement-existing-adr",
        "improve-stale-adr-scope",
        "midstream-adr-conflict",
        "bug-without-reproduction",
        "external-evidence-dependency",
        "local-only-delivery-boundary",
    }
    assert required_ids <= set(ids), "critical forward-test cases are missing"
    for scenario in scenarios:
        assert scenario["entry_skill"] == "clarify-and-plan"
        assert scenario["prompt"].strip()
        facets = scenario["expected_facets"]
        assert set(facets) == set(allowed), f"incomplete facets in {scenario['id']}"
        for facet, values in facets.items():
            assert isinstance(values, list) and values, f"empty {facet} in {scenario['id']}"
            assert set(values) <= allowed[facet], f"invalid {facet} in {scenario['id']}"
        assert scenario["must"]
        assert scenario["must_not"]
    conflicting = next(item for item in scenarios if item["id"] == "clarify-conflicting-answers")
    assert len(conflicting.get("followups", [])) >= 2, "grilling fixture lacks repeated user answers"


def check_scripts() -> None:
    for relative in ("scripts/check.sh",):
        path = ROOT / relative
        assert path.is_file()
        assert path.stat().st_mode & stat.S_IXUSR, f"not executable: {relative}"

    adr_script = ROOT / "skills" / "maintain-architecture-decisions" / "scripts" / "adr.py"
    assert adr_script.is_file(), "missing ADR maintenance script"


def check_required_resources() -> None:
    required = (
        "skills/clarify-and-plan/references/grilling-loop.md",
        "skills/execute-to-pr/references/implementation-loop.md",
        "skills/execute-to-pr/references/work-packets.md",
        "skills/maintain-architecture-decisions/references/decision-policy.md",
        "skills/maintain-architecture-decisions/assets/adr-readme.md",
        "skills/maintain-architecture-decisions/assets/record-template.md",
        "skills/maintain-architecture-decisions/assets/index-template.yaml",
        "skills/maintain-architecture-decisions/assets/system-marker.yaml",
        "adr/README.md",
        "adr/.adr-system.yaml",
        "adr/index.yaml",
    )
    for relative in required:
        assert (ROOT / relative).is_file(), f"missing required resource: {relative}"

    records = list((ROOT / "adr" / "records").rglob("*.md"))
    assert not any(re.match(r"^\d{4}-", path.name) for path in records), "ADR uses sequence identity"
    index = load_yaml(ROOT / "adr" / "index.yaml")
    indexed_ids = {decision["id"] for decision in index["decisions"]}
    required_ids = {
        "workflow.public-entrypoint",
        "workflow.independent-facets",
        "interaction.material-ambiguity-loop",
        "architecture.living-decisions",
        "execution.adaptive-delegation",
    }
    assert required_ids <= indexed_ids, "accepted workflow decisions are missing from the ADR map"


def check_install_documentation() -> None:
    command = "npx skills add {source} --skill '*'"
    for relative in ("README.md", "docs/COMPATIBILITY.md"):
        text = (ROOT / relative).read_text()
        assert command.format(source=".") in text, f"missing local skills CLI command in {relative}"
        assert command.format(source="OWNER/REPOSITORY") in text, f"missing GitHub skills CLI command in {relative}"
        assert "all eight" in text.lower(), f"all eight skills are not required in {relative}"
        assert "install.sh" not in text, f"custom installer remains documented in {relative}"
        assert "adapters/" not in text, f"legacy adapters remain documented in {relative}"
        assert "bootstrap" not in text.lower(), f"legacy bootstrap remains documented in {relative}"


def check_pi_manifest() -> None:
    package = json.loads((ROOT / "package.json").read_text())
    assert "pi-package" in package["keywords"]
    assert package["pi"]["skills"] == ["./skills"]
    assert re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", package["version"])


def check_release_automation() -> None:
    package = json.loads((ROOT / "package.json").read_text())
    manifest = json.loads((ROOT / ".release-please-manifest.json").read_text())
    config = json.loads((ROOT / "release-please-config.json").read_text())
    workflow = (ROOT / ".github" / "workflows" / "release-please.yml").read_text()
    changelog = (ROOT / "CHANGELOG.md").read_text()

    assert manifest == {".": package["version"]}
    assert config["release-type"] == "node"
    assert re.fullmatch(r"[0-9a-f]{40}", config["bootstrap-sha"])
    assert "." in config["packages"]
    assert "branches:\n      - main" in workflow
    assert "googleapis/release-please-action@" in workflow
    assert "contents: write" in workflow
    assert "pull-requests: write" in workflow
    assert f"## {package['version']}" in changelog


def main() -> None:
    check_skills()
    check_policy_scope()
    check_legacy_install_removed()
    check_scenarios()
    check_scripts()
    check_required_resources()
    check_install_documentation()
    check_pi_manifest()
    check_release_automation()
    print("package structure: ok")


if __name__ == "__main__":
    main()
