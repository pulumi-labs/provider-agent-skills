#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${repo_root}"

count=0
while IFS= read -r skill_file; do
  agentskills validate "$(dirname "${skill_file}")"
  count=$((count + 1))
done < <(find packages -type f -path '*/skills/*/SKILL.md' -print | LC_ALL=C sort)

if ((count == 0)); then
  echo "No skills found" >&2
  exit 1
fi

echo "Validated ${count} skills against the Agent Skills specification."
