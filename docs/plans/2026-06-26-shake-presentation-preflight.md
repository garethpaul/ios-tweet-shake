# Shake Presentation Preflight

Status: Completed

## Goal

Reject shakes while an alert or composer owns presentation before inspecting
the Twitter session.

## Work

- Add a visible/idle presentation predicate.
- Invoke it before Twitter session lookup.
- Reuse it when reserving composer ownership.
- Add static ordering, XCTest, guidance, and plan contracts.

## Verification

- The red-first checker failed on the missing preflight and plan evidence.
- Focused baseline and seven hostile presentation-preflight mutations pass after implementation.
- repository-root and external-directory `make check` passed.
- All Make aliases, Python compilation, and `git diff --check` passed.
- Native Swift execution remains unavailable without the historical toolchain.

Implementation head `6463f23ebe76ea6fff115d8b7f8263f68e8f2d1f` passed hosted
push baseline `28269500144`, pull-request baseline `28269501676`, and CodeQL
run `28269500778`. Codex review stopped before analysis with OpenAI HTTP 401;
immutable manual review found no actionable issues. The final evidence-only
head must repeat hosted validation.

## Scope

No credentials, tweet text, session semantics, background APIs, vendored
frameworks, project settings, or user-confirmed posting behavior changed.
