# Changes

## 2026-06-08

- Guarded Twitter login completion so the shake screen opens only after a non-nil session and no login error.
- Kept failed or cancelled login out of the shake-to-compose screen.
- Removed tweet-composer console logging and avoided retaining compose outcomes in local state.
- Used the motion subtype parameter for shake detection instead of reading the event object.
- Restored the committed app `Info.plist` with build-setting placeholders for Fabric/Twitter values while keeping real credentials local.
- Guarded Fabric/TwitterKit startup when credential build settings are empty or unresolved placeholders.
- Added `make check` and a static TwitterKit baseline for project wiring, credential placeholders, login/compose guardrails, and local privacy checks.
