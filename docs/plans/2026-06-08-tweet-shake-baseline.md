# iOS Tweet Shake Baseline Plan

status: completed

## Context

`ios-tweet-shake` is a legacy Swift iOS sample that uses bundled Fabric,
TwitterCore, and TwitterKit frameworks. The Xcode project references app and
test `Info.plist` files, so the repository needs committed plist files with
credential build-setting placeholders while real Twitter/Fabric credentials stay
in local configuration. Full validation remains a macOS/Xcode/device
responsibility.

## Objectives

- Keep Twitter login and shake-triggered composer behavior user-controlled.
- Restore committed app and test `Info.plist` files referenced by the Xcode project.
- Keep Fabric/Twitter credential values as build-setting placeholders in git.
- Guard Fabric/TwitterKit startup when credential build settings are empty or unresolved placeholders.
- Avoid segueing into the composer flow when login fails or returns no session.
- Remove console logging of Twitter login or compose state.
- Avoid retaining compose outcomes in local state.
- Add a reproducible `make check` baseline for project metadata, storyboard/asset parsing, framework references, credential boundaries, and local privacy guardrails.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
