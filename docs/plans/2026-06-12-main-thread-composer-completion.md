# Main-Thread Composer Completion

status: planned

## Context

The retired vendored Twitter composer invokes a completion closure after the
user finishes or cancels. Its callback queue is not documented by this archival
sample, but the closure directly resets view-controller presentation state.
UIKit-owned state should be restored on the main thread regardless of the
vendored callback queue.

## Scope

- Dispatch composer completion state restoration to the main queue.
- Keep weak controller capture and user-confirmed composer behavior unchanged.
- Do not modify vendored framework binaries or add background API behavior.
- Extend the static baseline and documentation with the callback-thread
  invariant.
- Mutation-test removal of the main-thread dispatch.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `python3 -m py_compile scripts/check-baseline.py`
- vendored framework digest verification
- `git diff --check`
