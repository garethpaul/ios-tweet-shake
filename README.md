# ios-tweet-shake

<!-- README-OVERVIEW-IMAGE -->
![Project overview](docs/readme-overview.svg)

## Overview

`garethpaul/ios-tweet-shake` is an Apple platform application or Swift sample. Shake phone to Tweet.

This README is based on the checked-in source, manifests, scripts, and repository metadata on the `master` branch. The project language mix found during review was: C/C++ headers (28), Swift (4).

## Repository Contents

- `Fabric.framework` - source or example code
- `CHANGES.md` - recent maintenance changes
- `Makefile` - local static verification entry point
- `SECURITY.md` - security reporting and disclosure guidance
- `scripts/check-baseline.py` - static TwitterKit/Fabric baseline checks
- `tweetshake` - source or example code
- `tweetshake.xcodeproj` - Xcode project file
- `tweetshakeTests` - source or example code
- `TwitterCore.framework` - source or example code
- `TwitterKit.framework` - source or example code
- `VISION.md` - project direction and maintenance guardrails

Additional scan context:

- Source directories: Fabric.framework, TwitterCore.framework, TwitterKit.framework, tweetshake, tweetshakeTests
- Dependency and build manifests: none detected
- Entry points or build surfaces: `make lint`, `make test`, `make build`, `make check`, tweetshake.xcodeproj
- Test-looking files: tweetshakeTests/tweetshakeTests.swift

## Getting Started

### Prerequisites

- Git
- Python 3 for static verification with `make lint`, `make test`, `make build`, and `make check`
- macOS with Xcode for building Apple platform projects
- Fabric/TwitterKit credentials from an app you control when exercising login and compose behavior

### Setup

```bash
git clone https://github.com/garethpaul/ios-tweet-shake.git
cd ios-tweet-shake
make lint
make test
make build
make check
```

The committed `tweetshake/Info.plist` uses build-setting placeholders for
`FABRIC_API_KEY`, `TWITTER_CONSUMER_KEY`, and `TWITTER_CONSUMER_SECRET`. Keep
real values in local Xcode build settings, local `.xcconfig` files, or
command-line overrides.

## Running or Using the Project

- Open `tweetshake.xcodeproj` in Xcode, choose the app or sample scheme, and run it on the matching simulator/device.
- The app uses bundled legacy `Fabric.framework`, `TwitterCore.framework`, and
  `TwitterKit.framework` binaries.
- `VENDORED_FRAMEWORKS.sha256` pins the exact framework executables and Fabric
  installer. `make check` recomputes every digest; this detects repository drift
  but does not establish provenance or make the retired SDK production-safe.
- When credential build settings are empty or unresolved placeholders, the app
  skips TwitterKit startup and shows a credential setup message on the login
  screen. The credential helper rejects missing values without force-unwrapping
  optional configuration. Credential helper tests cover missing, blank,
  placeholder, trimmed local values, and the Twitter kit name boundary. Failed
  login attempts avoid stacking duplicate login failure alerts. Incomplete credentials
  such as a missing Fabric API key or missing Twitter consumer secret stay
  covered by focused helper tests. The credential setup message guard keeps
  repeated setup checks from stacking duplicate labels.
- The login layout keeps the generated Twitter login button centered and the
  credential setup message fitted from the current view bounds after layout
  changes.
- Tweet creation should remain user-confirmed through `TWTRComposer`; shaking
  the device opens the composer instead of silently posting.
- The shake screen checks for a current local Twitter session before presenting
  the composer and shows a local login-required message when the session is
  missing.

Example command-line credential override:

```bash
xcodebuild -project tweetshake.xcodeproj \
  -target tweetshake \
  FABRIC_API_KEY=... \
  TWITTER_CONSUMER_KEY=... \
  TWITTER_CONSUMER_SECRET=...
```

## Testing and Verification

- `make lint`, `make test`, `make build`, and `make check` run
  `scripts/check-baseline.py`, which verifies Xcode project
  wiring, the committed app and test plists,
  plist/storyboard/asset files, TwitterKit login gating, login alert handling,
  shake-to-compose behavior, vendored framework references, credential helper
  guardrails, credential helper tests, the Twitter kit name guard,
  incomplete credentials, the credential setup message guard, login layout,
  user-confirmed posting, and session boundaries.
- The `lint`, `test`, and `build` targets intentionally alias the static
  baseline on hosts without the legacy Xcode toolchain, keeping the standard
  local gate commands available without claiming to replace Xcode verification.
- Pinned `macos-15` GitHub Actions runs `make check` and parses
  `tweetshake.xcodeproj` with `xcodebuild -list`. This hosted validation does
  not use credentials, access Twitter accounts, run simulator interaction, or
  submit tweets.
- Xcode's test action or `xcodebuild test` with the appropriate scheme and destination

When the required SDK or runtime is unavailable, use static checks and source review first, then verify on a machine that has the matching platform toolchain.

## Configuration and Secrets

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- Keep local `.xcconfig`, `.env`, signing, local plist overrides, and generated build files out of git.
- The checked-in Fabric/TwitterKit values must stay as build-setting placeholders, not real credentials.

## Security and Privacy Notes

- Review changes touching authentication or token handling; examples from the scan include TwitterCore.framework/Headers/TWTRAPIErrorCode.h, TwitterCore.framework/Headers/TWTRAuthSession.h, TwitterCore.framework/Headers/TWTRConstants.h, TwitterCore.framework/Headers/TWTRCoreOAuthSigning.h, and 5 more.
- Do not commit real credentials to source or app plists. Do not add silent
  posting, background account actions, session bypasses, or tweet-composer
  console logging.
- Review changes touching external API calls or credential-adjacent configuration; examples from the scan include Fabric.framework/Headers/FABAttributes.h, Fabric.framework/Headers/Fabric.h, TwitterCore.framework/Headers/TWTRAPIErrorCode.h, TwitterCore.framework/Headers/TWTRAuthConfig.h, and 6 more.
- Review changes touching network requests, sockets, or service endpoints; examples from the scan include TwitterCore.framework/Headers/TWTRAPIErrorCode.h, TwitterCore.framework/Headers/TWTRAuthConfig.h, TwitterCore.framework/Headers/TWTRCoreOAuthSigning.h, TwitterKit.framework/Headers/TWTRAPIClient.h, and 3 more.
- Review changes touching mobile permissions or privacy-sensitive device data; examples from the scan include TwitterCore.framework/Headers/TWTRConstants.h.
- Review changes touching file, media, JSON, XML, CSV, OCR, or data parsing; examples from the scan include TwitterCore.framework/Headers/TWTRConstants.h, TwitterCore.framework/Headers/TWTRCoreOAuthSigning.h, TwitterKit.framework/Headers/TWTRAPIClient.h, TwitterKit.framework/Headers/TWTRComposer.h, and 2 more.
- Review changes touching database, model, or persistence code; examples from the scan include TwitterKit.framework/Headers/TWTRTweetTableViewCell.h, TwitterKit.framework/Headers/TWTRTweetViewDelegate.h.

## Maintenance Notes

This is an archival Swift 1-era baseline with an iOS 8.3 deployment target and
vendored Fabric, TwitterCore, and TwitterKit binaries. Those SDKs are retired,
so the project is not expected to build unchanged with a current SDK. Follow
`docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md` before changing the
authentication, compose, Swift, or deployment-target layers.

- This looks like an Apple platform project or sample. Xcode, Swift, CocoaPods, and deployment target versions may need to match the original project era.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing
  changes to Swift sources, plists, storyboards, assets, vendored framework
  references, or security docs.
- See `SECURITY.md` for vulnerability reporting and safe research guidance.
- See `VISION.md` for project direction and contribution guardrails.
- See `docs/plans/2026-06-09-make-gate-aliases.md` for the local gate alias guardrail.
- See `docs/plans/2026-06-10-credential-setup-message-guard.md` for the credential setup message guardrail.

## Contributing

Keep changes small and tied to the project that is already present in this repository. For code changes, document the toolchain used, avoid committing generated dependency directories or local configuration, and update this README when setup or verification steps change.
