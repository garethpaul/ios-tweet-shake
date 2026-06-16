# Login Transition Invalidation

status: completed

## Context

The login controller clears its visible state in `viewDidDisappear`. During an
animated segue or dismissal, a delayed Twitter login completion can therefore
arrive after the disappearance transition has started but before it has
finished, pass the visibility and generation checks, and perform duplicate or
out-of-owner UI work.

## Requirements

- Invalidate login completion ownership when disappearance begins.
- Remove the appearance-owned login button at the same lifecycle boundary.
- Preserve appearance generation capture, exact-generation matching, weak
  ownership, main-queue routing, the success segue, and the local failure alert.
- Preserve configured-credential and setup-message behavior.
- Add focused XCTest intent and mutation-sensitive static coverage for the
  transition boundary.

## Implementation

- Move visibility invalidation and login-button teardown from
  `viewDidDisappear` to `viewWillDisappear` in
  `tweetshake/LoginViewController.swift`.
- Extend `tweetshakeTests/tweetshakeTests.swift` with a lifecycle-oriented
  acceptance test for completion ownership before and after invalidation.
- Extend `scripts/check-baseline.py` and maintained guidance with source,
  regression, completed-plan, and verification contracts.

## Verification

- Run all four Make gates and the absolute Makefile gate from an external
  directory.
- Compile the checker, validate vendored framework digests, and parse project,
  plist, storyboard, workspace, asset, and workflow metadata.
- Reject isolated mutations that restore late invalidation, omit teardown,
  weaken the focused test, remove guidance, or falsify plan completion.
- Audit the exact diff, generated artifacts, file modes, conflicts, and
  credential-like additions before committing.

## Runtime Boundary

The repository retains retired Swift 1-era TwitterKit binaries, and this Linux
host cannot execute Xcode or a compatible live Twitter login. Local evidence
will cover the deterministic static boundary; hosted macOS compilation will be
recorded separately after push.

## Work Completed

- Moved visibility invalidation and appearance-owned button teardown to
  `viewWillDisappear`, closing the transition interval before the controller is
  fully gone.
- Added XCTest intent that accepts the active generation before disappearance
  and rejects it immediately after transition invalidation.
- Extended deterministic source, regression, guidance, and plan contracts.

## Verification Completed

- All four Make gates passed from the checkout and reported that `xcodebuild`
  was unavailable, so this Linux host exercised the complete static baseline.
- The absolute Makefile path passed the full gate from an external directory.
- `python3 -m py_compile scripts/check-baseline.py`, vendored framework digest
  validation, project/plist/storyboard/workspace/asset/workflow parsing, and
  `git diff --check` passed.
- Six isolated hostile mutations were rejected for late lifecycle invalidation,
  missing visibility invalidation, missing button teardown, weakened focused
  test coverage, maintained-guidance removal, and plan-status rollback.
- Exact intended-file, generated-artifact, file-mode, conflict-marker, and
  credential-pattern audits passed before commit.
