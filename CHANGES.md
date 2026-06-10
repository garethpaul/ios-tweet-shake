# Changes

## 2026-06-10

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
