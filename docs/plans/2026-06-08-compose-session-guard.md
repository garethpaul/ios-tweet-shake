# Compose Session Guard Plan

status: completed

## Context

`ios-tweet-shake` gates the shake screen behind successful Twitter login, but the shake controller itself can still open the composer if reached with no current local Twitter session.

## Objectives

- Check the local Twitter session before showing the tweet composer.
- Keep composer presentation user-confirmed through `TWTRComposer`.
- Show a local login-required message when a shake occurs without a session.
- Avoid stacking login-required messages on repeated shakes.
- Extend the static baseline so session checks remain in the shake-to-compose flow.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
