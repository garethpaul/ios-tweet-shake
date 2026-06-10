# Credential Setup Message Guard

status: completed

## Context

When Twitter/Fabric credentials are not configured, the login screen displays a
credential setup message instead of creating a Twitter login button. The helper
always added a new label, so a future repeated setup check could stack duplicate
messages on the login screen.

## Completed Scope

- Made `showCredentialSetupMessage` return early when the setup label already
  exists.
- Kept the existing layout path for the first setup message and future bounds
  changes.
- Extended the static baseline and docs so duplicate credential setup messages
  remain guarded without adding silent posting, persistence, analytics, or
  credential storage behavior.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
