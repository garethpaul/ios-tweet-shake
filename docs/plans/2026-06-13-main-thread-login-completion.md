# Main-Thread Login Completion

status: completed

## Context

The retired Twitter login button completion performs a segue or presents an
alert directly from the SDK callback. UIKit navigation and presentation must be
serialized on the main queue, as the composer completion already is.

## Requirements

- Dispatch login completion UI handling to the main queue.
- Resolve weak controller capture inside that dispatch.
- Preserve the exact success predicate, segue, failure alert, credentials
  boundary, and archival SDK replacement-first guidance.
- Add callback-scoped contracts and completed verification evidence.

## Scope Boundaries

- Do not modernize Swift syntax or vendored SDKs in this focused patch.
- Do not add credentials, account storage, networking, logging, or analytics.
- Do not claim runtime login coverage on current Xcode.

## Work Completed

- Dispatched retired Twitter login completion UI handling to the main queue.
- Resolved weak controller ownership inside that dispatch.
- Preserved the exact success predicate, shake segue, and local failure alert.
- Added callback-scoped static contracts and documentation.

## Verification Completed

- All four Make gates, `make lint`, `make test`, `make build`, and `make check`,
  passed against the archival static baseline.
- Python compilation, plist/XML/JSON/YAML parsing, PNG and vendored digest
  validation, and `git diff --check` passed.
- Eight hostile mutations covering dispatch queue, weak resolution ordering,
  success predicate, success route, failure route, and weak capture were
  rejected, along with plan status and verification evidence mutations. The
  failure-route mutation initially exposed an over-broad checker
  search; the contract was scoped to the completion closure and the mutation
  was then rejected.
- Xcode and a compatible retired Twitter runtime were unavailable, so login and
  navigation execution were not claimed.
