# Non-Shake Motion Forwarding

status: completed

## Context

The shake controller overrode `motionEnded` but returned without calling the
inherited implementation for every motion subtype. Apple documents that the
default `UIResponder` implementation forwards the message up the responder
chain, so the override unintentionally consumed motion events it did not handle.

## Design

- Return to the inherited implementation only when the subtype is not
  `UIEventSubtype.MotionShake`.
- Call `super.motionEnded(motion, withEvent: event)` exactly once before
  returning from the non-shake branch.
- Preserve the existing shake session check, composer reservation, tweet text,
  user confirmation, and main-thread completion behavior unchanged.

## Test First

The static baseline first required a non-shake branch that forwards to the
inherited implementation before session or composer work. The unchanged source
failed this red-first contract before implementation.

## Verification

- `python3 scripts/check-baseline.py` passed after implementation.
- `/usr/bin/make lint`, `/usr/bin/make test`, `/usr/bin/make build`, and
  `/usr/bin/make check` passed from the checkout and from `/tmp` through the
  absolute Makefile path.
- `python3 -m py_compile scripts/check-baseline.py` passed.
- Three isolated hostile mutations were rejected: removing the inherited call,
  moving the forwarding branch after session work, and hiding the inherited
  call in a block comment.
- `git diff --check` passed.
- Current Xcode compilation is not claimed for this Swift 1-era source-review
  sample; hosted project parsing remains authoritative.

## Scope Boundaries

- No shake behavior, session policy, tweet text, composer callback, credential,
  persistence, logging, networking, project, or vendored binary change.
- Physical motion behavior still requires a compatible historical toolchain and
  hardware validation.

## Reference

- https://developer.apple.com/documentation/uikit/uiresponder/motionended%28_%3Awith%3A%29
