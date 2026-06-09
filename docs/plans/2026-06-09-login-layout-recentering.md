# Login Layout Recentering

status: completed

## Context

The login screen creates the Twitter login button in code and previously placed
it once during `viewDidLoad`. That could leave the button or credential setup
message stale after Auto Layout, rotation, or another bounds change.

## Completed Scope

- Retained the generated Twitter login button and credential setup label.
- Recentered the login button from the current view bounds during layout.
- Reframed the credential setup message from the current view bounds during
  layout.
- Extended the static baseline and docs to preserve the login layout guardrail.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- `git diff --check`
