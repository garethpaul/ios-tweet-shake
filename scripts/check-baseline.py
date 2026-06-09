#!/usr/bin/env python3
from pathlib import Path
import json
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASELINE_PLAN = ROOT / "docs/plans/2026-06-08-tweet-shake-baseline.md"
SESSION_GUARD_PLAN = ROOT / "docs/plans/2026-06-08-compose-session-guard.md"
CREDENTIAL_HELPER_PLAN = ROOT / "docs/plans/2026-06-08-credential-helper-unwrap.md"
CREDENTIAL_TEST_PLAN = ROOT / "docs/plans/2026-06-08-credential-helper-tests.md"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


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
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
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
    baseline_plan = BASELINE_PLAN.read_text(encoding="utf-8") if BASELINE_PLAN.exists() else ""
    session_guard_plan = SESSION_GUARD_PLAN.read_text(encoding="utf-8") if SESSION_GUARD_PLAN.exists() else ""
    credential_helper_plan = CREDENTIAL_HELPER_PLAN.read_text(encoding="utf-8") if CREDENTIAL_HELPER_PLAN.exists() else ""
    credential_test_plan = CREDENTIAL_TEST_PLAN.read_text(encoding="utf-8") if CREDENTIAL_TEST_PLAN.exists() else ""

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
    require("Main.storyboard" in project and "LaunchScreen.xib" in project and "Images.xcassets" in project,
            "Xcode project must keep storyboard, launch screen, and asset catalog references",
            failures)

    require("TweetShakeHasConfiguredTwitterCredentials()" in app_delegate and "Fabric.with([Twitter()])" in app_delegate,
            "AppDelegate must gate Fabric/Twitter startup on configured credentials",
            failures)
    require("TweetShakeHasConfiguredCredentialValue" in app_delegate and "rangeOfString(\"$(\")" in app_delegate,
            "credential helper must reject unresolved build-setting placeholders",
            failures)
    require("guard let credential = value else" in app_delegate and "value!" not in app_delegate,
            "credential helper must avoid force-unwrapping optional credential values",
            failures)
    require("testCredentialHelperRejectsMissingAndPlaceholderValues" in tests and
            "testCredentialHelperAcceptsTrimmedCredentialValues" in tests and
            "XCTAssertFalse" in tests and "XCTAssertTrue" in tests and
            "XCTAssert(true" not in tests and "testPerformanceExample" not in tests,
            "tweetshakeTests must replace template tests with credential helper assertions",
            failures)
    require("showCredentialSetupMessage" in login_controller and "session != nil && error == nil" in login_controller,
            "login controller must show setup state and require successful login before segueing",
            failures)
    require("showLoginRequiredMessage" in login_controller and "performSegueWithIdentifier(\"shake\"" in login_controller,
            "login controller must preserve the shake segue behind a login guard",
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
    require("make check" in readme and "FABRIC_API_KEY" in readme and "TWITTER_CONSUMER_KEY" in readme,
            "README must document static verification and local credential build settings",
            failures)
    require("credential setup message" in readme and "user-confirmed" in readme and
            "credential helper" in readme and "credential helper tests" in readme and "session" in readme.lower(),
            "README must document credential helper, session, and composer guardrails",
            failures)
    require("scripts/check-baseline.py" in vision and "failed or cancelled login" in vision and
            "credential helper" in vision and "credential helper tests" in vision,
            "VISION must describe the current tweet-shake baseline",
            failures)
    require("TwitterKit" in security and "make check" in security and
            "placeholder" in security and "credential helper tests" in security,
            "SECURITY must document Twitter privacy and credential-placeholder guardrails",
            failures)
    require("Info.plist" in changes and "failed or cancelled login" in changes and
            "credential helper" in changes and "credential helper tests" in changes and
            "session" in changes.lower() and "make check" in changes,
            "CHANGES must record plist, login, credential helper, session, and baseline hardening",
            failures)
    require("status: completed" in baseline_plan and "status: completed" in session_guard_plan and
            "status: completed" in credential_helper_plan and "status: completed" in credential_test_plan,
            "plans must be marked completed",
            failures)

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a scheme-specific Xcode test on macOS before release.")
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
