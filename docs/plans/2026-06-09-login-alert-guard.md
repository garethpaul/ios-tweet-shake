# Login Alert Guard Plan

status: completed

## Context

`LoginViewController` shows a login-required alert when Twitter login fails or
is cancelled. The shake screen already avoids stacking local login-required
messages, but the login screen should keep the same modal boundary.

## Objectives

- Skip presenting a second login-required alert while one is already visible.
- Preserve the successful-login segue into the shake screen.
- Keep failed or cancelled login out of the compose flow.
- Extend the static baseline so duplicate login failure alerts remain guarded.

## Verification

- `make check`
- `python3 scripts/check-baseline.py`
- `git diff --check`
