# Composer Completion Reservation

status: completed

## Context

`ViewController` used one Boolean to block overlapping `TWTRComposer`
presentations. Every completion callback unconditionally cleared that Boolean
after dispatching to the main queue. If the retired SDK delivered a duplicate
or delayed callback after a later composer had started, the old callback could
clear the newer composer's guard and allow a third presentation to overlap it.
The same callback could also mutate state after the shake controller began
leaving the screen.

## Requirements

- Bind each composer to the visible shake-screen appearance and a monotonic
  presentation attempt.
- Consume only the matching active attempt on the main thread.
- Reject duplicate, stale-attempt, stale-appearance, and hidden-controller
  completions without changing current presentation state.
- Invalidate ownership when disappearance begins.
- Reject a new composer reservation while another controller owns presentation.
- Preserve the local-session guard and user-confirmed `TWTRComposer` flow.

## Implementation

- Track shake-screen visibility, appearance generation, composer attempt
  generation, and the active composer attempt in `ViewController`.
- Reserve an attempt before constructing or showing the composer.
- Capture appearance and attempt identities in the completion closure and
  reserve the matching completion before clearing presentation state.
- Reset active ownership at `viewWillDisappear`, before transition-owned UI can
  outlive the controller.

## Verification Completed

- Added focused XCTest intent for first completion, duplicate rejection, stale
  attempt isolation, disappearance invalidation, and visible/idle presentation
  reservation.
- Added deterministic source and ordering contracts to
  `scripts/check-baseline.py`.
- Observed the baseline fail before production changes because the reservation
  methods and state did not exist, then pass after the minimal implementation.
- Ran hostile mutation checks that remove current-attempt matching, remove
  disappearance invalidation, remove occupied-presentation rejection, and
  bypass completion reservation; each mutation was rejected.
- Ran all Make gates and the canonical absolute-Makefile gate. Native build and
  device/service limitations are recorded in the final review evidence.
- Xcode 26.0.1 parsed the project and reached target setup, then correctly
  stopped because the archival target has no supported `SWIFT_VERSION` and an
  iOS 8.3 deployment target below the current simulator floor.

## Residual Risk

The repository retains Swift 1-era source and retired TwitterKit binaries.
Live Twitter authentication, physical shake delivery, composer presentation,
callback cardinality, and simulator/device lifecycle transitions require a
compatible historical iOS runtime and credentials and are not claimed here.
