# Changes

## 2026-06-25 06:17 - P1 - Scope shake responder ownership

### Summary
Made the visible shake controller explicitly own first-responder motion delivery
and release it before disappearance.

### Work completed
- Added Swift 1-era first-responder eligibility to the shake controller.
- Acquired responder ownership after appearance in the active hierarchy.
- Resigned before visibility and composer ownership invalidation.
- Added focused XCTest, mutation-sensitive static contracts, and documentation.
- Hardened lifecycle parsing after a commented-out acquisition mutation exposed
  a false pass; line and nested block comments are now excluded safely.

### Threads
- Started: none — work completed directly in the current repository.
- Continued: none.
- Stopped: none.

### Files changed
- `tweetshake/ViewController.swift` — scopes motion responder ownership.
- `tweetshakeTests/tweetshakeTests.swift` — covers responder eligibility.
- `scripts/check-baseline.py` — enforces acquisition, resignation, and order.
- Documentation and plan files — record lifecycle and hardware boundaries.

### Validation
- `python3 scripts/check-baseline.py` — failed before implementation on the
  missing lifecycle contract and passed afterward.
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` — passed the complete static baseline.
- Six isolated hostile mutations removing eligibility, acquisition,
  resignation, correct teardown order, or hiding acquisition in line/block
  comments were rejected.
- String-aware nested Swift comment stripping, Python compilation, and
  `git diff --check` — passed.
- Codex review — clean with no actionable findings; parallel `make check`
  passed.
- Hosted push baseline run `28172964648`, pull-request baseline run
  `28172968567`, and CodeQL run `28172966032` passed on reviewed head
  `5e9a32f5e760ec214473a84369f7d8e0f8f74aa0`.

### Bugs / findings
- P1: `motionEnded` depended on implicit responder-chain behavior even though
  UIKit initially delivers motion events to the first responder and responders
  reject first-responder ownership by default.

### Blockers
- The Swift 1-era app and retired vendored SDKs are source-review only under the
  current environment; physical shake delivery requires historical hardware
  and toolchain validation.

### Next action
- Revalidate the evidence-only amendment, then merge PR #13 on exact green head.

## 2026-06-19

- Reserved each shake-triggered composer presentation and completion by visible
  appearance and attempt so a delayed duplicate callback cannot clear a newer
  composer's presentation guard.
- Invalidated composer ownership when the shake controller begins disappearing
  and rejected new composer work while another controller owns presentation.

## 2026-06-16

- Reserved each installed Twitter login attempt before completion UI, rejecting
  duplicate callbacks while preserving a fresh retry after failure dismissal.
- Invalidated Twitter login completion ownership when disappearance begins so
  delayed callbacks cannot mutate UI during an animated transition.

## 2026-06-15

- Bound Twitter login callbacks to the controller appearance that installed
  their button so an old completion stays stale after the screen reappears.

## 2026-06-14

- Ignored delayed Twitter login completions after the login controller
  disappears.

## 2026-06-13

- Made all Make verification aliases location-independent when invoked through
  an absolute Makefile path.
- Routed retired Twitter login completion navigation and failure presentation
  through the main queue while preserving weak controller capture.

## 2026-06-12

- Restored composer presentation state on the main thread after the retired
  TwitterKit completion callback.

## 2026-06-10

- Documented and enforced the legacy SDK modernization boundary for the Swift
  1-era, iOS 8.3, Fabric, TwitterCore, and TwitterKit baseline.
- Added SHA-256 integrity pinning for the vendored Fabric, TwitterCore, and
  TwitterKit executables and Fabric installer.
- Added pinned, read-only macOS hosted project validation for `make check` and
  `tweetshake.xcodeproj` parsing without credentials or account access.
- Added a credential setup message guard so repeated missing-credential checks
  do not stack duplicate setup labels.

## 2026-06-09

- Added local `make lint`, `make test`, and `make build` gate aliases for the
  static Tweet Shake baseline.
- Kept login layout centered and the credential setup message fitted after view
  layout changes.
- Avoided stacking duplicate login failure alerts when repeated failed login
  callbacks occur.
- Added incomplete credentials coverage for missing Fabric API keys and missing
  Twitter consumer secrets.

## 2026-06-08

- Guarded Twitter login completion so the shake screen opens only after a non-nil session and no login error.
- Kept failed or cancelled login out of the shake-to-compose screen.
- Checked for a current local Twitter session before showing the tweet composer.
- Removed tweet-composer console logging and avoided retaining compose outcomes in local state.
- Used the motion subtype parameter for shake detection instead of reading the event object.
- Restored the committed app `Info.plist` with build-setting placeholders for Fabric/Twitter values while keeping real credentials local.
- Guarded Fabric/TwitterKit startup when credential build settings are empty or unresolved placeholders.
- Removed the optional force unwrap from the credential helper.
- Added credential helper tests for missing, blank, placeholder, and trimmed local values.
- Required the Twitter kit name before accepting KitInfo credentials from Fabric configuration.
- Added `make check` and a static TwitterKit baseline for project wiring, credential placeholders, login/compose guardrails, and local privacy checks.
