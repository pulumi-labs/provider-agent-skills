#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

validate_install() {
  local package="$1"
  local expected_file="${repo_root}/scripts/expected-skills/${package}.txt"
  local tmp_dir

  if [[ ! -f "${expected_file}" ]]; then
    echo "Missing expected skill inventory: ${expected_file}" >&2
    return 1
  fi

  tmp_dir="$(mktemp -d)"
  (
    trap 'rm -rf "${tmp_dir}"' EXIT
    cd "${tmp_dir}"
    apm init consumer --yes >/dev/null
    cd consumer

    apm install "${repo_root}/packages/${package}" --target opencode

    find .agents/skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; \
      | LC_ALL=C sort >"${tmp_dir}/actual-skills.txt"

    if ! diff -u "${expected_file}" "${tmp_dir}/actual-skills.txt"; then
      echo "Unexpected installed skills for ${package}" >&2
      exit 1
    fi

    # The temporary consumer deliberately has no Git remote, so organization
    # policy discovery is out of scope for this package integration test.
    apm audit --ci --no-policy
  )
}

validate_install core
validate_install bridged

echo "Clean APM consumer installs passed."
