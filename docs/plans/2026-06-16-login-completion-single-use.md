# Login Completion Reservation

status: planned

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

## Verification Completed

Pending implementation and validation.
