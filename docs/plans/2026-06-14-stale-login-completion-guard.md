# Stale Login Completion Guard

status: completed

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

## Work Completed

- Added explicit login-controller visibility tracking across appearance and
  disappearance callbacks.
- Rejected login completion UI work after the controller disappears while
  preserving weak capture, main-queue routing, success navigation, and local
  failure presentation.
- Added lifecycle and callback-order contracts plus project documentation.

## Verification Completed

- Python checker compilation passed. Before this completion record was added,
  the baseline reached only the expected pending-plan evidence failure.
- `make lint`, `make test`, `make build`, and `make check` passed from the
  repository root; `make check` also passed through the absolute Makefile path
  from `/tmp`.
- Six isolated hostile mutations were rejected: removing visibility state,
  preventing the visible state from becoming true, removing the stale callback
  guard, replacing the main-queue dispatch, reverting the plan to pending, and
  erasing hostile-mutation verification evidence.
- Xcode and a compatible retired Twitter runtime are unavailable on this Linux
  host, so live login and navigation execution are not claimed.
