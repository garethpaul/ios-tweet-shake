# Incomplete Twitter Credentials

status: completed

## Context

The credential helper already rejects missing Fabric API keys and incomplete
Twitter kit configuration. The checked-in tests covered placeholder and named-kit
boundaries, but not incomplete credentials inside otherwise shaped Fabric
configuration dictionaries.

## Completed Scope

- Added a test for missing Fabric API keys.
- Added a test for missing Twitter consumer secrets.
- Extended the static baseline and docs so incomplete credentials remain covered
  without committing real Twitter or Fabric values.

## Verification

- `make check`
- `git diff --check`
