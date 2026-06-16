# Login Transition Invalidation

status: planned

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
