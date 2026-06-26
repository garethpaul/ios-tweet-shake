# Stale Shake Visibility Guard

Status: Completed

## Goal

Prevent queued shake callbacks from performing Twitter session, alert, or
composer work after the shake controller begins disappearing.

## Work

- Added an early hidden-screen return after non-shake responder forwarding.
- Kept session lookup, login alert, composer reservation, and composer creation
  behind the visibility boundary.
- Added red-first source ordering coverage and direct XCTest visibility-state
  evidence after `viewWillDisappear`.
- Updated maintained agent, README, security, vision, and change guidance.
- Extended the baseline with source, test, guidance, and completed-plan checks.

## Verification

- Run `make check` from the repository root and an external directory.
- Reject hostile stale-shake mutations across ordering, source, test, guidance,
  and plan status.
- Run Python syntax, whitespace, generated-artifact, and secret-shaped audits.

## Completion Evidence

- Before implementation, the baseline failed because no visibility return
  existed before `hasTwitterSession()`.
- After implementation, the portable baseline passed.
- The repository-root and external-directory `make check` passed.
- Six hostile stale-shake mutations were rejected across source removal,
  visibility ordering, session ordering, XCTest evidence, guidance, and plan
  status.
- Python syntax, whitespace, generated-artifact, and likely-secret audits
  passed.
- Native compilation and physical shake delivery were not performed because the
  historical Swift/iOS toolchain is unavailable locally. Hosted checks must
  pass on the exact pull request head before merge.
