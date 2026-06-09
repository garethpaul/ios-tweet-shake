## iOS Tweet Shake Vision

This document explains the current state and direction of the project.
Project overview and developer docs: [`README.md`](README.md)

iOS Tweet Shake is a Swift iOS sample that integrates TwitterKit/Fabric
and lets a user shake the phone to compose a tweet.

The repository is useful as a legacy social and motion-interaction sample with
bundled Fabric/Twitter frameworks and a small Xcode project.

The goal is to preserve the sample while making credentials, session data, and
user-confirmed posting boundaries explicit.

Current baseline: `make check` runs `scripts/check-baseline.py` to verify the
legacy Xcode project shape, committed app/test plists,
TwitterKit/Fabric framework references, login gating, user-confirmed compose
behavior, duplicate login failure alerts, credential helper guardrails, and
Twitter kit name checks.

The current focus is:

Priority:

- Preserve Twitter login and shake-triggered compose behavior
- Keep Fabric/Twitter framework assumptions visible
- Avoid committing real Twitter/Fabric credentials or signing material
- Guard Fabric/TwitterKit startup until credential build settings are configured
- Keep credential helper handling free of optional force unwraps
- Keep credential helper tests focused on local placeholder handling
- Require the Twitter kit name before accepting KitInfo credentials
- Avoid stacking duplicate login failure alerts
- Keep posting user-confirmed through the Twitter composer
- Keep shake-to-compose guarded by a current local Twitter session
- Maintain security policy for the sample

Next priorities:

- Add README setup, credentials, and verification instructions
- Modernize Twitter/Fabric dependencies only in a dedicated pass
- Add tests or manual checks around motion handling and compose behavior
- Clarify that posting should remain user-confirmed

Contribution rules:

- One PR = one focused Twitter, motion, build, or documentation change.
- Verify shake behavior on hardware when changing motion code.
- Run `make check` before pushing source, project, plist, asset,
  vendored framework reference, or security documentation changes.
- Keep credential placeholders empty in committed source.
- Do not add silent account actions.
- Keep failed or cancelled login out of the compose screen.
- Keep missing-session states out of the compose screen.

## Security And Privacy

Canonical security policy and reporting:

- [`SECURITY.md`](SECURITY.md)

Twitter sessions and user intent are sensitive. Real credentials must stay out
of git, and tweet creation should remain explicit through user-controlled UI.
The committed app plist uses build-setting placeholders so local credentials can
be supplied without changing tracked files.

## What We Will Not Merge (For Now)

- Hardcoded Twitter/Fabric credentials
- Silent posting or background account actions
- Motion tracking unrelated to the compose flow
- Broad dependency migration bundled with behavior changes

This list is a roadmap guardrail, not a permanent rule.
Strong user demand and strong technical rationale can change it.
