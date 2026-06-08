# Changes

## 2026-06-08

- Guarded Twitter login completion so the shake screen opens only after a non-nil session and no login error.
- Removed tweet-composer console logging and kept compose outcome in local in-memory state.
- Used the motion subtype parameter for shake detection instead of reading the event object.
- Added `tweetshake/Info.plist.example` with placeholder Fabric/Twitter values while keeping real credentials ignored.
- Added `make check` and a static TwitterKit baseline for project wiring, credential placeholders, login/compose guardrails, and local privacy checks.
