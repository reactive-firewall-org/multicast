#!/usr/bin/env bash
# .github/tools/resolve-sha.sh
# Shared SHA validation and resolution script
#
# This script validates and resolves git commit SHAs from various input formats.
# It accepts: direct 40-char SHAs, full refs, branch names, or tag names.
#
# Environment variables (expected):
#   CI_INPUT_TARGET_SHA: The input SHA/ref to resolve
#
# Output:
#   GITHUB_OUTPUT: sha=<40-char-sha>
#   GITHUB_ENV: BUILD_SHA=<40-char-sha>
#
# Exit codes:
#   0: Success
#   1: Validation or resolution failed

set -euo pipefail

# Enable debug mode if requested
if [[ "${DEBUG_RESOLVE_SHA:-0}" == "1" ]]; then
  set -x
fi

raw_input="${CI_INPUT_TARGET_SHA:-}"

# Reject NUL or newline immediately
if printf '%s' "$raw_input" | grep -q '[^[:print:]]'; then
  printf "::error title='Invalid':: %s\n" "Error: input contains disallowed control characters" >&2
  exit 1
fi

# Strip one level of surrounding quotes and trim whitespace
normalize() {
  local s="$1"
  s="${s#"${s%%[![:space:]]*}"}"
  s="${s%"${s##*[![:space:]]}"}"
  if [[ (${s:0:1} == "'" && ${s: -1} == "'") || (${s:0:1} == '"' && ${s: -1} == '"') ]]; then
    s="${s:1:-1}"
  fi
  printf '%s' "$s"
}
input="$(normalize "$raw_input")"

# Reject inputs starting with '-' (options)
if [[ "${input:0:1}" == "-" ]]; then
  printf "::error title='Invalid':: %s\n" "Error: input may not start with '-'" >&2
  exit 1
fi

# If it's a 40-char SHA, accept directly
if [[ "$input" =~ ^[0-9a-f]{40}$ ]]; then
  resolved_sha="$input"
else
  # Try explicit namespaces in order: full refs, refs/heads/, refs/tags/, then bare branch/tag
  resolved_sha=""
  # 1) If input is a full ref path starting with refs/, resolve only that
  if [[ "$input" == refs/* ]]; then
    if git rev-parse --verify "$input" >/dev/null 2>&1; then
      resolved_sha="$(git rev-parse --verify "$input")"
    else
      printf "::error title='Invalid':: %s\n" "Error: ref not found: $input" >&2
      exit 1
    fi
  else
    # 2) Try refs/heads/<input>
    if git rev-parse --verify "refs/heads/$input" >/dev/null 2>&1; then
      resolved_sha="$(git rev-parse --verify "refs/heads/$input")"
    # 3) Try refs/tags/<input>
    elif git rev-parse --verify "refs/tags/$input" >/dev/null 2>&1; then
      resolved_sha="$(git rev-parse --verify "refs/tags/$input")"
    else
      printf "::error title='Invalid':: %s\n" "Error: no matching branch or tag found for: $input" >&2
      exit 1
    fi
  fi
fi

# Ensure final resolved value is a full 40-char commit SHA
if [[ ! "$resolved_sha" =~ ^[0-9a-f]{40}$ ]]; then
  printf "::error title='Invalid':: %s\n" "Error: resolved value is not a full commit SHA" >&2
  exit 1
fi

# Output to both GITHUB_OUTPUT and GITHUB_ENV
printf "sha=%s\n" "$resolved_sha" >> "$GITHUB_OUTPUT"
printf "BUILD_SHA=%s\n" "$resolved_sha" >> "$GITHUB_ENV"

# Debug output if enabled
if [[ "${DEBUG_RESOLVE_SHA:-0}" == "1" ]]; then
  printf "::debug:: %s\n" "Resolved SHA: $resolved_sha" >&2
fi

exit 0
