# Main-Thread Composer Completion

status: completed

## Context

The retired vendored Twitter composer invokes a completion closure after the
user finishes or cancels. Its callback queue is not documented by this archival
sample, but the closure directly resets view-controller presentation state.
UIKit-owned state should be restored on the main thread regardless of the
vendored callback queue.

## Work Completed

- Dispatch composer completion state restoration to the main queue.
- Keep weak controller capture and user-confirmed composer behavior unchanged.
- Do not modify vendored framework binaries or add background API behavior.
- Extend the static baseline and documentation with the callback-thread
  invariant.
- Mutation-test removal of the main-thread dispatch.

## Verification Completed

- Local `make check`, `make lint`, `make test`, and `make build` passed. The
  local environment did not provide `xcodebuild`, so these runs exercised the
  complete static and vendored-framework integrity baseline.
- `python3 -m py_compile scripts/check-baseline.py` and `git diff --check`
  passed.
- Hostile mutations changing the plan status, inserting an unfinished-work
  marker, falsifying a run ID, replacing the main queue with a global queue, or
  removing weak controller capture were rejected.
- The implementation push Check run `27395561147` completed successfully for
  commit `a004f93fa1a517557477e8da842070a2316671ff`.
- The implementation pull-request Check run `27395565855` completed
  successfully for commit `a004f93fa1a517557477e8da842070a2316671ff` and
  parsed the archival Xcode project on hosted macOS.
- The post-merge push Check run `27395584932` completed successfully for
  commit `fa6dfb98f577eded11c8bc0988514b03766b67ec`.
- The CodeQL setup run `27402323797` completed successfully for commit
  `fa6dfb98f577eded11c8bc0988514b03766b67ec`.
- Composer completion preserves `composer.showWithCompletion { [weak self]`,
  `dispatch_async(dispatch_get_main_queue())`, and
  `self?.isShowingComposer = false` in that order.
