# Stale Shake Visibility Guard Design

Status: Completed

## Problem

The controller resigns first-responder ownership and marks itself hidden when
disappearance begins, but a shake callback already queued by UIKit can still
enter `motionEnded`. Composer presentation checks visibility, while the
no-session branch queries Twitter and may present a login alert first. A stale
controller can therefore perform account and presentation work off-screen.

## Options

1. Rely only on responder resignation. This does not reject already queued
   callbacks.
2. Guard only the login alert. This still performs stale Twitter session work.
3. Return immediately for a shake when the shake screen is not visible, before
   session lookup or either presentation path.

## Decision

Use option 3. Keep non-shake responder forwarding first, then enforce visible
shake-screen ownership before Twitter or composer work.
