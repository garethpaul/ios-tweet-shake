# Vendored SDK Integrity

status: completed

## Problem

The repository commits retired Fabric, TwitterCore, and TwitterKit executable
artifacts without an integrity manifest. A binary or installer-script change can
therefore blend into unrelated source work without a deterministic baseline
failure.

## Scope

- Record SHA-256 digests for each vendored framework executable and the Fabric
  installer executable.
- Recompute and compare every digest in `make check`.
- Reject missing, malformed, duplicate, unexpected, or absolute manifest paths.
- Document that digest pinning detects repository drift but does not establish
  provenance, patch vulnerabilities, or make the retired SDK production-safe.
- Keep credentials, account access, network calls, signing, and app execution
  outside verification.

## Verification

- `make lint`
- `make test`
- `make build`
- `make check`
- mutation check against a changed vendored executable
- `git diff --check`
