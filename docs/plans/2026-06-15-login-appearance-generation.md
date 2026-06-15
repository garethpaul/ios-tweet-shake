# Login Appearance Generation

status: completed

## Context

The current visibility guard rejects a delayed Twitter login callback while
the controller is hidden, but the same callback can become acceptable again if
the controller reappears. Login completions must remain bound to the appearance
that installed their login button.

## Requirements

- Assign a new generation whenever the login controller appears.
- Install a login button whose completion captures that appearance generation.
- Accept completion UI work only while visible and when the captured generation
  still matches the current appearance.
- Remove the prior appearance's button on disappearance without weakening the
  weak capture, main-queue dispatch, success predicate, segue, or failure alert.
- Add focused XCTest and mutation-sensitive static coverage.

## Scope Boundaries

- Do not modernize the Swift 1-era source or retired vendored SDKs.
- Do not add credentials, persistence, analytics, logging, or background API
  behavior.
- Do not claim live Twitter login or current-Xcode runtime coverage.

## Verification

- Run the focused checker and all four Make gates from the checkout.
- Run `make check` through the absolute Makefile path from an external working
  directory.
- Compile the checker, validate vendored framework digests, and run shell,
  project, plist, storyboard, artifact, secret, and diff audits.
- Reject isolated mutations that remove generation changes, captured identity,
  exact-generation rejection, focused tests, or completed evidence.

## Work Completed

- Recreated the Twitter login button for each visible controller appearance.
- Bound each completion to the generation that installed its button and removed
  the button when that appearance ended.
- Added focused XCTest, static contracts, and changelog evidence.

## Verification Completed

- All four Make gates passed from the checkout; `xcodebuild` was unavailable on
  this Linux host, so live legacy Twitter execution was not claimed.
- `make check` passed from an external directory through the absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py`, vendored framework digest
  validation, plist, storyboard, workspace, project, asset,
  and workflow parsing, and `git diff --check` passed.
- Six isolated hostile mutations were rejected: missing generation increment,
  missing captured generation, weakened exact-generation match, missing button
  teardown, missing focused test discovery, and weakened completion evidence.
- The teardown mutation initially exposed an under-specified checker assertion;
  the contract was tightened to require both installation and disappearance
  cleanup call sites before all six mutations passed.
