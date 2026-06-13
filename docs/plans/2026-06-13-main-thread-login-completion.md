# Main-Thread Login Completion

status: planned

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

## Verification

- All four Make gates and Python compilation.
- XML/plist/YAML/project/asset parsing and `git diff --check`.
- Hostile mutations for missing dispatch, early weak resolution, changed success
  predicate, changed success/failure routing, plan status, and evidence.
