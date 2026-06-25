# Shake First-Responder Lifecycle

status: completed

## Context

The shake controller implemented `motionEnded`, but did not opt into or acquire
first-responder status. UIKit sends motion events to the first responder before
forwarding them through the responder chain, and responders reject first-
responder ownership by default.

## Design

- Override the Swift 1-era `canBecomeFirstResponder()` method and return true.
- Acquire first-responder status in `viewDidAppear`, after the controller is in
  the active view hierarchy.
- Resign first-responder status at the start of `viewWillDisappear`, before the
  existing visibility and composer ownership invalidation.
- Preserve session checks, composer confirmation, generation tokens, vendored
  frameworks, credentials, and tweet text unchanged.

## Test First

The static baseline and focused XCTest first required first-responder
eligibility and lifecycle ownership. The unchanged source failed both lifecycle
requirements before implementation.

## Verification

- `python3 scripts/check-baseline.py` passed.
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` passed.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- Six isolated hostile mutations were rejected: removed eligibility,
  acquisition, resignation, late resignation, line-commented acquisition, and
  block-commented acquisition.
- String-aware nested Swift comment stripping preserved URL-like strings.
- `git diff --check` passed.
- Codex review reported no actionable findings while parallel `make check`
  passed.
- Hosted push baseline run `28172964648`, pull-request baseline run
  `28172968567`, and CodeQL run `28172966032` passed on reviewed head
  `5e9a32f5e760ec214473a84369f7d8e0f8f74aa0`.
- Current Xcode compilation is not claimed for this Swift 1-era source-review
  sample; hosted project parsing remains authoritative.

## Scope Boundaries

- No motion manager, background sensor use, silent posting, new Twitter API
  request, credential behavior, persistence, or vendored binary change.
- Hardware shake delivery still requires manual verification with the historical
  toolchain and a configured local Twitter session.

## References

- https://developer.apple.com/documentation/uikit/uiresponder/motionended%28_%3Awith%3A%29
- https://developer.apple.com/documentation/uikit/uiresponder/canbecomefirstresponder
- https://developer.apple.com/documentation/uikit/uiresponder/becomefirstresponder%28%29
