# /// script
# requires-python = ">=3.13"
# dependencies = ["PyYAML==6.0.2"]
# ///

"""Validate policies specific to the provider-agent-skills repository."""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path
import re
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = ROOT / "packages"
IGNORED_PARTS = {".git", ".mise", "apm_modules", "build"}
PORTABILITY_PATTERNS = (
    "repo-search-hygiene",
    "/Users/",
    "app-native",
    "sidecar-to-parent",
)
TEXT_SUFFIXES = {".md", ".py", ".sh", ".toml", ".txt", ".yaml", ".yml"}
REFERENCE_PATTERN = re.compile(r"references/[A-Za-z0-9._/-]+\.md")


def source_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in IGNORED_PARTS for part in path.parts):
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in {".gitignore", "LICENSE"}:
            files.append(path)
    return sorted(files)


def check_manifests(errors: list[str]) -> None:
    manifests = sorted(PACKAGES.glob("*/apm.yml"))
    if not manifests:
        errors.append("no package manifests found")
        return

    versions: dict[str, str] = {}
    for manifest in manifests:
        try:
            data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        except yaml.YAMLError as error:
            errors.append(f"{manifest.relative_to(ROOT)}: invalid YAML: {error}")
            continue

        if not isinstance(data, dict):
            errors.append(f"{manifest.relative_to(ROOT)}: manifest must be a mapping")
            continue

        name = data.get("name")
        version = data.get("version")
        if not isinstance(name, str) or not name:
            errors.append(f"{manifest.relative_to(ROOT)}: missing package name")
        if not isinstance(version, str) or not version:
            errors.append(f"{manifest.relative_to(ROOT)}: version must be a quoted string")
            continue
        versions[manifest.parent.name] = version

    if len(set(versions.values())) > 1:
        rendered = ", ".join(f"{name}={version}" for name, version in versions.items())
        errors.append(f"package versions are not lockstep: {rendered}")


def check_skills(errors: list[str]) -> None:
    skill_files = sorted(PACKAGES.glob("*/skills/*/SKILL.md"))
    if not skill_files:
        errors.append("no skills found")
        return

    owners: defaultdict[str, list[Path]] = defaultdict(list)
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        owners[skill_dir.name].append(skill_file)

        for markdown_file in sorted(skill_dir.rglob("*.md")):
            text = markdown_file.read_text(encoding="utf-8")
            for reference in set(REFERENCE_PATTERN.findall(text)):
                target = (skill_dir / reference).resolve()
                try:
                    target.relative_to(skill_dir.resolve())
                except ValueError:
                    errors.append(
                        f"{markdown_file.relative_to(ROOT)}: reference escapes skill: {reference}"
                    )
                    continue
                if not target.is_file():
                    errors.append(
                        f"{markdown_file.relative_to(ROOT)}: missing reference: {reference}"
                    )

    for name, paths in owners.items():
        if len(paths) > 1:
            rendered = ", ".join(str(path.relative_to(ROOT)) for path in paths)
            errors.append(f"duplicate skill name {name}: {rendered}")


def check_portability(errors: list[str]) -> None:
    for path in sorted(PACKAGES.rglob("*")):
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PORTABILITY_PATTERNS:
            if pattern in text:
                errors.append(
                    f"{path.relative_to(ROOT)}: non-portable reference {pattern!r}"
                )


def check_text_hygiene(errors: list[str]) -> None:
    for path in source_files():
        content = path.read_bytes()
        if content and not content.endswith(b"\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")

        for line_number, line in enumerate(content.splitlines(), start=1):
            if line.rstrip(b" \t") != line:
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: trailing whitespace")


def main() -> int:
    errors: list[str] = []
    check_manifests(errors)
    check_skills(errors)
    check_portability(errors)
    check_text_hygiene(errors)

    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1

    package_count = len(list(PACKAGES.glob("*/apm.yml")))
    skill_count = len(list(PACKAGES.glob("*/skills/*/SKILL.md")))
    print(f"Validated repository policy for {package_count} packages and {skill_count} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
