# Legacy SDK modernization boundary

status: completed

## Current boundary

This snapshot uses Swift 1-era syntax, an iOS 8.3 deployment target, and
vendored Fabric, TwitterCore, and TwitterKit binaries. Current Xcode and iOS SDK
releases cannot be treated as drop-in build environments for this code.

## Modernization sequence

1. Preserve the current static credential, session, and user-confirmed compose baseline before changing build metadata.
2. Replace retired Fabric, TwitterCore, and TwitterKit authentication and compose integrations.
3. Convert Swift syntax and UIKit lifecycle and motion APIs in reviewable stages.
4. Add current XCTest coverage for login, session, shake, and compose boundaries.
5. Raise the deployment target only after those flows are verified on supported devices.

Until that work is scheduled, changes should remain compatible with the
archival baseline and must not imply that the app builds with a current SDK.
