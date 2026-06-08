## iOS Tweet Shake Vision

iOS Tweet Shake is an Objective-C iOS sample that integrates TwitterKit/Fabric
and lets a user shake the phone to compose a tweet.

The repository is useful as a legacy social and motion-interaction sample with
bundled Fabric/Twitter frameworks and a small Xcode project.

The goal is to preserve the sample while making credentials, session data, and
user-confirmed posting boundaries explicit.

The current focus is:

Priority:

- Preserve Twitter login and shake-triggered compose behavior
- Keep Fabric/Twitter framework assumptions visible
- Avoid committing real Twitter/Fabric credentials or signing material
- Maintain security policy for the sample

Next priorities:

- Add README setup, credentials, and verification instructions
- Modernize Twitter/Fabric dependencies only in a dedicated pass
- Add tests or manual checks around motion handling and compose behavior
- Clarify that posting should remain user-confirmed

Contribution rules:

- One PR = one focused Twitter, motion, build, or documentation change.
- Verify shake behavior on hardware when changing motion code.
- Keep credential placeholders empty in committed source.
- Do not add silent account actions.

## Security And Privacy

Twitter sessions and user intent are sensitive. Real credentials must stay out
of git, and tweet creation should remain explicit through user-controlled UI.

## What We Will Not Merge For Now

- Hardcoded Twitter/Fabric credentials
- Silent posting or background account actions
- Motion tracking unrelated to the compose flow
- Broad dependency migration bundled with behavior changes
