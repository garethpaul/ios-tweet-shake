# Stale Login Completion Guard

status: pending

## Context

The retired Twitter login callback is dispatched to the main queue, but it can
still navigate or present an alert after the login controller has disappeared.
A delayed SDK completion must not mutate UI owned by an inactive controller.

## Requirements

- Track whether the login controller is currently visible.
- Ignore login completion UI work after the controller disappears.
- Preserve the existing weak capture, main-queue routing, success predicate,
  shake segue, and local failure alert.
- Add mutation-sensitive static contracts for lifecycle state and callback
  ordering.

## Scope Boundaries

- Do not modernize the Swift 1-era source or retired vendored SDKs.
- Do not add credentials, persistence, analytics, logging, or background API
  behavior.
- Do not claim live Twitter login or current-Xcode runtime coverage.

## Planned Verification

- Run all four Make gates from the repository root and `make check` through the
  absolute Makefile path from an external directory.
- Compile the Python checker, parse maintained metadata, and run diff,
  artifact, and changed-line credential audits.
- Reject isolated mutations that remove visibility tracking, stale-completion
  rejection, main-queue ordering, completed status, or verification evidence.
