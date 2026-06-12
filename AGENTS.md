# AGENTS.md

## Repository purpose

`garethpaul/ios-tweet-shake` is a legacy Swift iOS sample that opens a
user-confirmed Twitter composer after a shake gesture.

## Project structure

- `Makefile` - repository verification targets
- `scripts` - baseline checks and helper scripts
- `docs` - plans, notes, and generated README assets
- `tweetshake.xcodeproj` - Xcode project
- `Fabric.framework` - vendored legacy Fabric runtime and installer
- `tweetshake` - application source, storyboards, assets, and metadata
- `tweetshakeTests` - XCTest credential-helper coverage and test metadata
- `TwitterCore.framework` - vendored legacy Twitter authentication runtime
- `TwitterKit.framework` - vendored legacy Twitter login and composer runtime

## Development commands

- Install dependencies: no repository-specific install command is documented.
- Full baseline: `make check`
- Local Apple development: `open tweetshake.xcodeproj`
- If a command above skips because a platform toolchain is missing, verify on a machine with that SDK before claiming platform behavior is tested.

## Coding conventions

- Language mix noted in the README: C/C++ headers (28), Swift (4).
- Preserve legacy Xcode project settings and signing assumptions unless the change is explicitly about modernization.

## Testing guidance

- Test-related files detected: `docs/plans/2026-06-08-credential-helper-tests.md`, `tweetshakeTests/tweetshakeTests.swift`
- Start with the narrowest relevant test or Make target, then run `make check` before handing off if the change is not documentation-only.
- Keep README verification notes in sync when commands, fixtures, or supported toolchains change.

## PR / change guidance

- Keep diffs focused on the requested repository and avoid unrelated modernization or formatting churn.
- Preserve public APIs, sample behavior, file formats, and documented environment variables unless the task explicitly changes them.
- Update tests, README notes, or docs/plans when behavior, security posture, or validation commands change.
- Call out skipped platform validation, legacy toolchain assumptions, and any risky files touched in the final summary.

## Safety and gotchas

- Detected references to Twitter. Keep API keys, OAuth credentials, tokens, and account-specific values in local configuration only.
- Keep local `.xcconfig`, `.env`, signing, local plist overrides, and generated build files out of git.
- The checked-in Fabric/TwitterKit values must stay as build-setting placeholders, not real credentials.
- Do not commit real credentials to source or app plists. Do not add silent posting, background account actions, session bypasses, or tweet-composer console logging.
- This is an archival Apple platform sample. The Swift 1-era syntax, iOS 8.3
  target, and vendored Fabric/TwitterKit binaries require a historical toolchain.
- Run `make lint`, `make test`, `make build`, and `make check` before pushing changes to Swift sources, plists, storyboards, assets, vendored framework references, or security docs.

## Agent workflow

1. Inspect the README, Makefile, manifests, and the files directly related to the request.
2. Make the smallest source or docs change that satisfies the task; avoid generated, vendored, or local-environment files unless required.
3. Run the narrowest useful validation first, then `make check` or the documented package/platform gate when available.
4. If a required SDK, service credential, or external runtime is unavailable, record the skipped command and why.
5. Summarize changed files, commands run, and remaining risks or follow-up validation.
