# Login Appearance Generation

status: planned

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
