# Credential Helper Unwrap Plan

status: completed

## Context

`TweetShakeHasConfiguredCredentialValue` rejects missing, empty, and unresolved credential build settings before Fabric/TwitterKit startup. The helper checks for nil and then force-unwraps the optional value, which is unnecessary in a credential boundary.

## Objectives

- Replace the optional force unwrap with `guard let`.
- Preserve empty and unresolved placeholder rejection.
- Extend the static baseline so the credential helper remains unwrap-free.
- Document the credential helper guardrail.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
