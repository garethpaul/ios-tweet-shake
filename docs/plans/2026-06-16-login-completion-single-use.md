# Login Completion Reservation

status: completed

## Context

The login controller rejects callbacks from hidden or older appearances, but an
accepted callback does not consume the installed button's attempt. If the
retired TwitterKit button invokes its completion more than once before
`viewWillDisappear`, each callback can pass the same appearance-generation
check and attempt another segue or alert presentation.

## Requirements

- R1. Allow at most one login completion to perform UI work for each installed
  login-button attempt.
- R2. Consume the active attempt token before starting either the success segue
  or failure alert path so reentrant or duplicate callbacks fail closed.
- R3. After a failed login alert is dismissed, install a fresh button attempt
  when the same appearance is still visible so an intentional retry remains
  possible. A successful attempt stays consumed through the transition.
- R4. Preserve stale-generation, hidden-controller, main-thread, credential,
  button teardown, and transition invalidation behavior.
- R5. Add focused XCTest intent and mutation-sensitive static contracts for the
  single-use boundary and reservation ordering.
- R6. Run without live Twitter credentials, retired-service requests, or
  changes to vendored framework binaries.

## Implementation Units

### U1. Completion reservation

**Files:** `tweetshake/LoginViewController.swift`

Give each installed login button a monotonic attempt token. Replace the
presence-only completion predicate with an operation that validates the current
visible appearance and active attempt, then immediately consumes the attempt
before returning success. The failure-alert dismissal path may install a fresh
attempt only while that same appearance remains visible.

### U2. Regression and maintained contracts

**Files:** `tweetshakeTests/tweetshakeTests.swift`,
`scripts/check-baseline.py`, `README.md`, `SECURITY.md`, `VISION.md`,
`CHANGES.md`, and this plan.

Cover first acceptance, duplicate rejection, stale rejection, hidden rejection,
failure retry with a fresh token, and source ordering that consumes the token
before either UI outcome.

## Verification

- Run the focused static baseline followed by all four Make gates from the
  repository and the canonical gate from an external directory.
- Run checker and shell syntax, vendored digest, project metadata, workflow,
  exact diff, artifact, secret-pattern, mode, conflict, and whitespace audits.
- Reject isolated mutations that remove reservation, restore a read-only
  predicate, reuse a consumed token, reinstall a retry before alert dismissal,
  move consumption after UI work, weaken focused tests, or leave plan evidence
  incomplete.
- Record the Linux Xcode/runtime limitation truthfully and require hosted macOS
  compilation on the exact pushed head.

## Scope Boundaries

- Do not migrate TwitterKit, change credentials, or alter login UX copy.
- Do not change composer, motion, shake, or tweet behavior.
- Do not merge or close any stacked pull request.

## Work Completed

- Added monotonic installed-button attempt tokens alongside the existing
  appearance generation and reserved each matching token before completion UI.
- Removed the consumed button immediately, kept successful attempts consumed,
  and restored a fresh attempt after failed-login alert dismissal while the
  same appearance remains visible.
- The code review found that an already-presented controller could otherwise
  strand the consumed attempt; the same guarded retry restoration now covers
  that alert-presentation conflict.
- Added focused XCTest intent, deterministic source-order contracts, and
  synchronized README, security, vision, and changelog guidance.

## Verification Completed

- An isolated exact-copy preflight passed All four Make gates and the canonical
  gate through the absolute Makefile path before this plan was marked complete.
- Seven isolated hostile mutations were rejected for active-token installation,
  attempt identity, pre-UI consumption, consumed-button teardown,
  alert-dismissal retry timing, focused test discovery, and plan-status
  evidence.
- The static baseline verified vendored framework SHA-256 pins, plist,
  storyboard, XIB, workspace, project, asset, workflow, source-order, test, and
  maintained-guidance contracts.
- `git diff --check`, exact intended-file, generated-artifact, file-mode,
  conflict-marker, and added-line credential-pattern audits passed during the
  implementation review.
- `xcodebuild` and a compatible retired Twitter runtime were unavailable on
  this Linux host, so live login and native XCTest execution remain hosted
  macOS validation boundaries.
