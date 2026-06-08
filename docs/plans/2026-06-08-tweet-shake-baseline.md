# iOS Tweet Shake Baseline Plan

status: completed

## Context

`ios-tweet-shake` is a legacy Swift iOS sample that uses bundled Fabric,
TwitterCore, and TwitterKit frameworks. The real app `Info.plist` is ignored
because Twitter/Fabric credentials belong in local configuration, so repository
verification needs a sanitized template and static checks while full validation
remains a macOS/Xcode/device responsibility.

## Objectives

- Keep Twitter login and shake-triggered composer behavior user-controlled.
- Avoid segueing into the composer flow when login fails or returns no session.
- Remove console logging of Twitter login or compose state.
- Keep real Fabric/Twitter credentials out of git while documenting required placeholders.
- Add a reproducible `make check` baseline for project metadata, storyboard/asset parsing, framework references, credential boundaries, and local privacy guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
