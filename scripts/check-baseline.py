#!/usr/bin/env python3
from pathlib import Path
import hashlib
import json
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MODERNIZATION_PLAN = ROOT / "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md"
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-tweet-shake-baseline.md"
SESSION_GUARD_PLAN = ROOT / "docs/plans/2026-06-08-compose-session-guard.md"
CREDENTIAL_HELPER_PLAN = ROOT / "docs/plans/2026-06-08-credential-helper-unwrap.md"
CREDENTIAL_TEST_PLAN = ROOT / "docs/plans/2026-06-08-credential-helper-tests.md"
LOGIN_ALERT_GUARD_PLAN = ROOT / "docs/plans/2026-06-09-login-alert-guard.md"
KIT_NAME_GUARD_PLAN = ROOT / "docs/plans/2026-06-09-twitter-kit-name-guard.md"
INCOMPLETE_CREDENTIAL_PLAN = ROOT / "docs/plans/2026-06-09-incomplete-twitter-credentials.md"
LOGIN_LAYOUT_PLAN = ROOT / "docs/plans/2026-06-09-login-layout-recentering.md"
MAKE_GATES_PLAN = ROOT / "docs/plans/2026-06-09-make-gate-aliases.md"
CREDENTIAL_SETUP_MESSAGE_PLAN = ROOT / "docs/plans/2026-06-10-credential-setup-message-guard.md"
HOSTED_VALIDATION_PLAN = ROOT / "docs/plans/2026-06-10-hosted-project-validation.md"
VENDORED_INTEGRITY_PLAN = ROOT / "docs/plans/2026-06-10-vendored-sdk-integrity.md"
COMPOSER_MAIN_THREAD_PLAN = ROOT / "docs/plans/2026-06-12-main-thread-composer-completion.md"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
EXPECTED_WORKFLOW = """name: Check
on:
  pull_request:
  push:
  workflow_dispatch:
permissions:
  contents: read
concurrency:
  group: check-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
jobs:
  baseline:
    runs-on: macos-15
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@df4cb1c069e1874edd31b4311f1884172cec0e10
        with:
          persist-credentials: false
      - run: make check
"""


def require(condition, message, failures):
    if not condition:
        failures.append(message)


def read(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8", errors="replace")


def strip_swift_line_comments(text):
    return "\n".join(line.split("//", 1)[0] for line in text.splitlines())


def parse_xml(relative_path, failures):
    try:
        ET.parse(str(ROOT / relative_path))
    except ET.ParseError as error:
        failures.append(f"{relative_path} is not well-formed XML: {error}")


def parse_json(relative_path, failures):
    try:
        return json.loads(read(relative_path))
    except json.JSONDecodeError as error:
        failures.append(f"{relative_path} is not valid JSON: {error}")
        return {}


def parse_plist(relative_path, failures):
    try:
        with (ROOT / relative_path).open("rb") as file:
            return plistlib.load(file)
    except Exception as error:
        failures.append(f"{relative_path} is not a readable plist: {error}")
        return {}


def check_png(relative_path, failures):
    path = ROOT / relative_path
    try:
        with path.open("rb") as file:
            signature = file.read(len(PNG_SIGNATURE))
        require(signature == PNG_SIGNATURE, f"{relative_path} must be a PNG image", failures)
        require(path.stat().st_size > 100, f"{relative_path} must not be empty", failures)
    except OSError as error:
        failures.append(f"{relative_path} could not be read: {error}")


def git_ignores(path):
    result = subprocess.run(
        ["git", "check-ignore", "-q", path],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode == 0


def is_build_setting_placeholder(value):
    return isinstance(value, str) and value.startswith("$(") and value.endswith(")")


def main():
    failures = []
    required_files = [
        ".gitignore",
        ".github/workflows/check.yml",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "VENDORED_FRAMEWORKS.sha256",
        "tweetshake.xcodeproj/project.pbxproj",
        "tweetshake.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "tweetshake/Info.plist",
        "tweetshake/AppDelegate.swift",
        "tweetshake/LoginViewController.swift",
        "tweetshake/ViewController.swift",
        "tweetshake/Base.lproj/Main.storyboard",
        "tweetshake/Base.lproj/LaunchScreen.xib",
        "tweetshake/Images.xcassets/AppIcon.appiconset/Contents.json",
        "tweetshake/Images.xcassets/logo.imageset/Contents.json",
        "tweetshake/Images.xcassets/logo.imageset/logo.png",
        "tweetshakeTests/Info.plist",
        "tweetshakeTests/tweetshakeTests.swift",
        "Fabric.framework/Fabric",
        "Fabric.framework/Headers/Fabric.h",
        "Fabric.framework/run",
        "TwitterCore.framework/TwitterCore",
        "TwitterCore.framework/Headers/TWTRAuthConfig.h",
        "TwitterKit.framework/TwitterKit",
        "TwitterKit.framework/Headers/Twitter.h",
        "TwitterKit.framework/Headers/TWTRComposer.h",
        "docs/plans/2026-06-08-compose-session-guard.md",
        "docs/plans/2026-06-08-credential-helper-unwrap.md",
        "docs/plans/2026-06-08-credential-helper-tests.md",
        "docs/plans/2026-06-09-login-alert-guard.md",
        "docs/plans/2026-06-09-twitter-kit-name-guard.md",
        "docs/plans/2026-06-09-incomplete-twitter-credentials.md",
        "docs/plans/2026-06-09-login-layout-recentering.md",
        "docs/plans/2026-06-09-make-gate-aliases.md",
        "docs/plans/2026-06-10-credential-setup-message-guard.md",
        "docs/plans/2026-06-10-legacy-sdk-modernization-boundary.md",
        "docs/plans/2026-06-10-hosted-project-validation.md",
        "docs/plans/2026-06-10-vendored-sdk-integrity.md",
        "docs/plans/2026-06-12-main-thread-composer-completion.md",
        "docs/plans/2026-06-08-tweet-shake-baseline.md",
        "docs/readme-overview.svg",
    ]

    for relative_path in required_files:
        require((ROOT / relative_path).is_file(), f"Required file missing: {relative_path}", failures)

    require((ROOT / "TwitterKit.framework/Versions/A/Resources/TwitterKitResources.bundle").is_dir(),
            "TwitterKitResources.bundle must remain available for the Xcode resource phase",
            failures)

    for xml_file in [
        "tweetshake.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "tweetshake/Base.lproj/Main.storyboard",
        "tweetshake/Base.lproj/LaunchScreen.xib",
        "docs/readme-overview.svg",
    ]:
        parse_xml(xml_file, failures)

    for json_file in [
        "tweetshake/Images.xcassets/AppIcon.appiconset/Contents.json",
        "tweetshake/Images.xcassets/logo.imageset/Contents.json",
    ]:
        parse_json(json_file, failures)

    check_png("tweetshake/Images.xcassets/logo.imageset/logo.png", failures)

    app_plist = parse_plist("tweetshake/Info.plist", failures)
    test_plist = parse_plist("tweetshakeTests/Info.plist", failures)
    project = read("tweetshake.xcodeproj/project.pbxproj")
    tests = read("tweetshakeTests/tweetshakeTests.swift")
    app_delegate = read("tweetshake/AppDelegate.swift")
    login_controller = read("tweetshake/LoginViewController.swift")
    shake_controller = read("tweetshake/ViewController.swift")
    swift_sources = "\n".join(strip_swift_line_comments(path.read_text(encoding="utf-8", errors="replace"))
                              for path in sorted((ROOT / "tweetshake").glob("*.swift")))
    readme = read("README.md")
    vision = read("VISION.md")
    security = read("SECURITY.md")
    changes = read("CHANGES.md")
    gitignore = read(".gitignore")
    makefile = read("Makefile")
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    session_guard_plan = SESSION_GUARD_PLAN.read_text(encoding="utf-8") if SESSION_GUARD_PLAN.exists() else ""
    credential_helper_plan = CREDENTIAL_HELPER_PLAN.read_text(encoding="utf-8") if CREDENTIAL_HELPER_PLAN.exists() else ""
    credential_test_plan = CREDENTIAL_TEST_PLAN.read_text(encoding="utf-8") if CREDENTIAL_TEST_PLAN.exists() else ""
    login_alert_guard_plan = LOGIN_ALERT_GUARD_PLAN.read_text(encoding="utf-8") if LOGIN_ALERT_GUARD_PLAN.exists() else ""
    kit_name_guard_plan = KIT_NAME_GUARD_PLAN.read_text(encoding="utf-8") if KIT_NAME_GUARD_PLAN.exists() else ""
    incomplete_credential_plan = INCOMPLETE_CREDENTIAL_PLAN.read_text(encoding="utf-8") if INCOMPLETE_CREDENTIAL_PLAN.exists() else ""
    login_layout_plan = LOGIN_LAYOUT_PLAN.read_text(encoding="utf-8") if LOGIN_LAYOUT_PLAN.exists() else ""
    make_gates_plan = MAKE_GATES_PLAN.read_text(encoding="utf-8") if MAKE_GATES_PLAN.exists() else ""
    credential_setup_message_plan = CREDENTIAL_SETUP_MESSAGE_PLAN.read_text(encoding="utf-8") if CREDENTIAL_SETUP_MESSAGE_PLAN.exists() else ""
    modernization_plan = MODERNIZATION_PLAN.read_text(encoding="utf-8") if MODERNIZATION_PLAN.exists() else ""
    hosted_validation_plan = HOSTED_VALIDATION_PLAN.read_text(encoding="utf-8") if HOSTED_VALIDATION_PLAN.exists() else ""
    vendored_integrity_plan = VENDORED_INTEGRITY_PLAN.read_text(encoding="utf-8") if VENDORED_INTEGRITY_PLAN.exists() else ""
    composer_main_thread_plan = COMPOSER_MAIN_THREAD_PLAN.read_text(encoding="utf-8") if COMPOSER_MAIN_THREAD_PLAN.exists() else ""
    workflow = read(".github/workflows/check.yml")

    fabric = app_plist.get("Fabric", {})
    kits = fabric.get("Kits", []) if isinstance(fabric, dict) else []
    twitter_kit = next((kit for kit in kits if kit.get("KitName") == "Twitter"), {})
    kit_info = twitter_kit.get("KitInfo", {}) if isinstance(twitter_kit, dict) else {}
    url_types = app_plist.get("CFBundleURLTypes", [])
    url_schemes = []
    for url_type in url_types:
        url_schemes.extend(url_type.get("CFBundleURLSchemes", []))

    require(app_plist.get("CFBundleIdentifier") == "com.garethpaul.tweetshake",
            "tweetshake Info.plist must keep the sample bundle identifier",
            failures)
    require(app_plist.get("UIMainStoryboardFile") == "Main" and app_plist.get("UILaunchStoryboardName") == "LaunchScreen",
            "tweetshake Info.plist must wire the main storyboard and launch screen",
            failures)
    require(is_build_setting_placeholder(fabric.get("APIKey")),
            "Fabric API key must remain a build-setting placeholder in git",
            failures)
    require(is_build_setting_placeholder(kit_info.get("consumerKey")) and is_build_setting_placeholder(kit_info.get("consumerSecret")),
            "Twitter consumer key and secret must remain build-setting placeholders in git",
            failures)
    require("twitterkit-$(TWITTER_CONSUMER_KEY)" in url_schemes,
            "Twitter callback URL scheme must be derived from the local consumer key",
            failures)
    require(test_plist.get("CFBundlePackageType") == "BNDL",
            "tweetshakeTests Info.plist must remain a test bundle plist",
            failures)

    require("INFOPLIST_FILE = tweetshake/Info.plist;" in project and "INFOPLIST_FILE = tweetshakeTests/Info.plist;" in project,
            "Xcode project must preserve app and test Info.plist wiring",
            failures)
    require("ENABLE_TESTABILITY = YES;" in project and "@testable import tweetshake" in tests,
            "Xcode project and unit tests must keep tweetshake app code testable from XCTest",
            failures)
    for setting in ["FABRIC_API_KEY = \"\";", "TWITTER_CONSUMER_KEY = \"\";", "TWITTER_CONSUMER_SECRET = \"\";"]:
        require(setting in project, f"Xcode project must default local credential build setting: {setting}", failures)
    for framework in ["Fabric.framework", "TwitterCore.framework", "TwitterKit.framework", "TwitterKitResources.bundle"]:
        require(framework in project, f"Xcode project must keep framework/resource reference: {framework}", failures)
    expected_vendored_paths = {
        "Fabric.framework/Fabric",
        "Fabric.framework/run",
        "TwitterCore.framework/TwitterCore",
        "TwitterKit.framework/TwitterKit",
    }
    manifest_entries = {}
    for line_number, line in enumerate(read("VENDORED_FRAMEWORKS.sha256").splitlines(), 1):
        parts = line.split("  ", 1)
        require(len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]) is not None,
                f"VENDORED_FRAMEWORKS.sha256 line {line_number} must contain a lowercase SHA-256 digest and path",
                failures)
        if len(parts) != 2:
            continue
        digest, relative_path = parts
        require(relative_path not in manifest_entries and not Path(relative_path).is_absolute() and ".." not in Path(relative_path).parts,
                f"VENDORED_FRAMEWORKS.sha256 line {line_number} must contain a unique repository-relative path",
                failures)
        manifest_entries[relative_path] = digest
    require(set(manifest_entries) == expected_vendored_paths,
            "vendored framework integrity manifest must cover exactly the committed framework executables and installer",
            failures)
    for relative_path, expected_digest in manifest_entries.items():
        artifact = ROOT / relative_path
        if artifact.is_file():
            actual_digest = hashlib.sha256(artifact.read_bytes()).hexdigest()
            require(actual_digest == expected_digest,
                    f"vendored artifact digest mismatch: {relative_path}", failures)
    require("Main.storyboard" in project and "LaunchScreen.xib" in project and "Images.xcassets" in project,
            "Xcode project must keep storyboard, launch screen, and asset catalog references",
            failures)

    require("TweetShakeHasConfiguredTwitterCredentials()" in app_delegate and "Fabric.with([Twitter()])" in app_delegate,
            "AppDelegate must gate Fabric/Twitter startup on configured credentials",
            failures)
    require("func TweetShakeHasConfiguredTwitterCredentials(fabric: NSDictionary?) -> Bool" in app_delegate and
            'guard let kitName = kit["KitName"] as? String where kitName == "Twitter" else' in app_delegate and
            'guard let kitInfo = kit["KitInfo"] as? NSDictionary else' in app_delegate,
            "credential helper must require an explicitly named Twitter kit before accepting KitInfo credentials",
            failures)
    require("TweetShakeHasConfiguredCredentialValue" in app_delegate and "rangeOfString(\"$(\")" in app_delegate,
            "credential helper must reject unresolved build-setting placeholders",
            failures)
    require("guard let credential = value else" in app_delegate and "value!" not in app_delegate,
            "credential helper must avoid force-unwrapping optional credential values",
            failures)
    require("testCredentialHelperRejectsMissingAndPlaceholderValues" in tests and
            "testCredentialHelperAcceptsTrimmedCredentialValues" in tests and
            "testTwitterCredentialHelperRequiresNamedTwitterKit" in tests and
            "testTwitterCredentialHelperRejectsMissingFabricAPIKey" in tests and
            "testTwitterCredentialHelperRejectsMissingConsumerSecret" in tests and
            "testTwitterCredentialHelperAcceptsNamedTwitterKit" in tests and
            "XCTAssertFalse" in tests and "XCTAssertTrue" in tests and
            "XCTAssert(true" not in tests and "testPerformanceExample" not in tests,
            "tweetshakeTests must replace template tests with credential helper assertions",
            failures)
    require("showCredentialSetupMessage" in login_controller and "session != nil && error == nil" in login_controller,
            "login controller must show setup state and require successful login before segueing",
            failures)
    require("func showCredentialSetupMessage()" in login_controller and
            "if self.credentialSetupMessageLabel != nil" in login_controller and
            "return" in login_controller and
            "self.credentialSetupMessageLabel = messageLabel" in login_controller,
            "login controller must avoid stacking duplicate credential setup messages",
            failures)
    require("showLoginRequiredMessage" in login_controller and "performSegueWithIdentifier(\"shake\"" in login_controller,
            "login controller must preserve the shake segue behind a login guard",
            failures)
    require("showLoginRequiredMessage" in login_controller and "presentedViewController != nil" in login_controller,
            "login controller must avoid stacking duplicate login-required alerts",
            failures)
    require("var logInButton: TWTRLogInButton?" in login_controller and
            "var credentialSetupMessageLabel: UILabel?" in login_controller and
            "override func viewDidLayoutSubviews()" in login_controller and
            "centerLoginButton()" in login_controller and
            "layoutCredentialSetupMessage()" in login_controller and
            "CGRectGetMidX(self.view.bounds)" in login_controller and
            "CGRectGetMidY(self.view.bounds)" in login_controller and
            "CGRectInset(self.view.bounds, 24.0, 0.0)" in login_controller,
            "login controller must recenter and reframe login/setup UI after layout changes",
            failures)
    require("isShowingComposer" in shake_controller and "motion == UIEventSubtype.MotionShake && !isShowingComposer" in shake_controller,
            "shake controller must avoid stacking multiple composer presentations",
            failures)
    require("func hasTwitterSession() -> Bool" in shake_controller and
            "Twitter.sharedInstance().session() != nil" in shake_controller and
            "if !hasTwitterSession()" in shake_controller,
            "shake controller must verify a local Twitter session before composing",
            failures)
    require("func showLoginRequiredMessage()" in shake_controller and "Twitter Login Required" in shake_controller and
            "presentedViewController != nil" in shake_controller,
            "shake controller must show one local login-required message when the session is missing",
            failures)
    require("composer.setText(\"I just shook my phone\")" in shake_controller and "composer.showWithCompletion" in shake_controller,
            "shake controller must preserve user-confirmed composer behavior",
            failures)
    composer_completion_index = shake_controller.find("composer.showWithCompletion { [weak self]")
    main_dispatch_index = shake_controller.find("dispatch_async(dispatch_get_main_queue())", composer_completion_index)
    composer_reset_index = shake_controller.find("self?.isShowingComposer = false", main_dispatch_index)
    require(composer_completion_index != -1 and main_dispatch_index != -1 and composer_reset_index != -1 and
            composer_completion_index < main_dispatch_index < composer_reset_index,
            "composer completion must restore presentation state on the main thread",
            failures)
    require(not re.search(r"\b(?:print|println|NSLog)\s*\(", swift_sources),
            "first-party Swift must not log Twitter session or compose outcomes",
            failures)
    for forbidden in ["TWTRAPIClient", "setURL", "upload", "analytics", "NSUserDefaults", "UserDefaults", "lastComposeResult", "loginStatus"]:
        require(forbidden not in swift_sources,
                f"Tweet-shake sample must not add background API, upload, analytics, persistence, or outcome storage behavior: {forbidden}",
                failures)

    require("Info.plist" not in [line.strip() for line in gitignore.splitlines()],
            ".gitignore must not ignore every target Info.plist",
            failures)
    require(not git_ignores("tweetshake/Info.plist") and not git_ignores("tweetshakeTests/Info.plist"),
            "app and test Info.plist files must be trackable",
            failures)
    require("*.local.xcconfig" in gitignore and "*.secrets.xcconfig" in gitignore and ".env" in gitignore,
            ".gitignore must exclude local credential and environment files",
            failures)
    require(".PHONY: build check lint test" in makefile and "lint test build: check" in makefile,
            "Makefile must expose lint, test, build, and check verification gates",
            failures)
    require("make lint" in readme and "make test" in readme and "make build" in readme and
            "make check" in readme and "FABRIC_API_KEY" in readme and "TWITTER_CONSUMER_KEY" in readme,
            "README must document static verification gates and local credential build settings",
            failures)
    require("credential setup message" in readme and "user-confirmed" in readme and
            "credential helper" in readme and "credential helper tests" in readme and "session" in readme.lower() and
            "duplicate login failure alerts" in readme and "Twitter kit name" in readme and
            "incomplete credentials" in readme and "credential setup message guard" in readme and "login layout" in readme,
            "README must document credential helper, session, login layout, login alert, and composer guardrails",
            failures)
    require("scripts/check-baseline.py" in vision and "make lint" in vision and "make test" in vision and
            "make build" in vision and "failed or cancelled login" in vision and
            "credential helper" in vision and "credential helper tests" in vision and
            "duplicate login failure alerts" in vision and "Twitter kit name" in vision and
            "incomplete credentials" in vision and "credential setup message guard" in vision and "login layout" in vision,
            "VISION must describe the current tweet-shake baseline",
            failures)
    require("TwitterKit" in security and "make check" in security and
            "placeholder" in security and "credential helper tests" in security and
            "duplicate login failure alerts" in security and "Twitter kit name" in security and
            "incomplete credentials" in security and "credential setup message guard" in security,
            "SECURITY must document Twitter privacy and credential-placeholder guardrails",
            failures)
    require("Info.plist" in changes and "failed or cancelled login" in changes and
            "credential helper" in changes and "credential helper tests" in changes and
            "duplicate login failure alerts" in changes and "Twitter kit name" in changes and
            "incomplete credentials" in changes and "credential setup message guard" in changes and "login layout" in changes and
            "session" in changes.lower() and "make check" in changes,
            "CHANGES must record plist, login, credential helper, session, and baseline hardening",
            failures)
    require("make lint" in changes and "make test" in changes and "make build" in changes,
            "CHANGES must record the standard local gate aliases",
            failures)
    require("Swift 1-era" in readme and "iOS 8.3" in readme and "TwitterCore" in readme and "current SDK" in readme,
            "README must document the legacy SDK modernization boundary",
            failures)
    require("Swift 1-era" in vision and "iOS 8.3" in vision and "modernization" in vision.lower(),
            "VISION must document the legacy SDK modernization sequence",
            failures)
    require("retired" in security and "TwitterCore" in security and "current SDK" in security,
            "SECURITY must identify retired SDK and current-toolchain risk",
            failures)
    require("legacy SDK modernization boundary" in changes,
            "CHANGES must record the legacy SDK modernization boundary",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in session_guard_plan and
            "status: completed" in credential_helper_plan and "status: completed" in credential_test_plan and
            "status: completed" in login_alert_guard_plan and "status: completed" in kit_name_guard_plan,
            "plans must be marked completed",
            failures)
    require("status: completed" in incomplete_credential_plan,
            "incomplete credential plan must be marked completed",
            failures)
    require("status: completed" in login_layout_plan,
            "login layout plan must be marked completed",
            failures)
    require("status: completed" in make_gates_plan,
            "make gate aliases plan must be marked completed",
            failures)
    require("status: completed" in credential_setup_message_plan,
            "credential setup message guard plan must be marked completed",
            failures)
    require("status: completed" in modernization_plan and "Swift 1-era" in modernization_plan and "iOS 8.3" in modernization_plan,
            "legacy SDK modernization boundary must be completed and version-specific",
            failures)
    require("status: completed" in hosted_validation_plan and "make check" in hosted_validation_plan,
            "hosted validation plan must be completed", failures)
    require("status: completed" in vendored_integrity_plan and "does not establish" in vendored_integrity_plan,
            "vendored SDK integrity plan must be completed and state its trust boundary", failures)
    require("status: completed" in composer_main_thread_plan and "mutation" in composer_main_thread_plan.lower(),
            "main-thread composer completion plan must record completed mutation verification", failures)
    workflow_files = sorted(str(path.relative_to(ROOT)) for path in (ROOT / ".github/workflows").rglob("*") if path.is_file())
    require(workflow == EXPECTED_WORKFLOW and workflow_files == [".github/workflows/check.yml"],
            "Check workflow must remain the sole pinned, credential-free, read-only macOS gate", failures)
    require(read(".github/CODEOWNERS").strip() == "* @garethpaul",
            "CODEOWNERS must assign repository-wide ownership to @garethpaul", failures)

    if shutil.which("xcodebuild"):
        result = subprocess.run(["xcodebuild", "-list", "-project", "tweetshake.xcodeproj"], cwd=ROOT,
                                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        require(result.returncode == 0,
                "xcodebuild could not parse tweetshake.xcodeproj: " + result.stderr.strip(), failures)
    else:
        print("xcodebuild unavailable; static iOS baseline only.")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("ios-tweet-shake baseline checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
