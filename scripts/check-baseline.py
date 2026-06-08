#!/usr/bin/env python3
"""Static baseline checks for the legacy Tweet Shake sample."""

from __future__ import print_function

import json
import plistlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FAILURES = []


def rel(path):
    return ROOT / path


def expect(condition, message):
    if not condition:
        FAILURES.append(message)


def read_text(path):
    target = rel(path)
    expect(target.exists(), "{} is missing".format(path))
    if not target.exists():
        return ""
    return target.read_text(encoding="utf-8")


def parse_xml(path):
    target = rel(path)
    expect(target.exists(), "{} is missing".format(path))
    if not target.exists():
        return None
    try:
        return ET.parse(str(target))
    except ET.ParseError as exc:
        FAILURES.append("{} is not valid XML: {}".format(path, exc))
        return None


def parse_json(path):
    target = rel(path)
    expect(target.exists(), "{} is missing".format(path))
    if not target.exists():
        return None
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except ValueError as exc:
        FAILURES.append("{} is not valid JSON: {}".format(path, exc))
        return None


def parse_plist(path):
    target = rel(path)
    expect(target.exists(), "{} is missing".format(path))
    if not target.exists():
        return None
    try:
        with target.open("rb") as handle:
            return plistlib.load(handle)
    except Exception as exc:
        FAILURES.append("{} is not a valid plist: {}".format(path, exc))
        return None


def strip_swift_comments(text):
    lines = []
    for line in text.splitlines():
        lines.append(line.split("//", 1)[0])
    return "\n".join(lines)


def git_ls_files():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=str(ROOT),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        FAILURES.append("git ls-files failed: {}".format(result.stderr.strip()))
        return set()
    return set(result.stdout.splitlines())


def check_required_files():
    required = [
        ".gitignore",
        "CHANGES.md",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "VISION.md",
        "docs/plans/2026-06-08-tweet-shake-baseline.md",
        "docs/readme-overview.svg",
        "Fabric.framework/Fabric",
        "Fabric.framework/Headers/Fabric.h",
        "TwitterCore.framework/TwitterCore",
        "TwitterCore.framework/Headers/TWTRAuthSession.h",
        "TwitterKit.framework/TwitterKit",
        "TwitterKit.framework/Headers/TWTRComposer.h",
        "TwitterKit.framework/Headers/TWTRLogInButton.h",
        "TwitterKit.framework/Versions/A/Resources/TwitterKitResources.bundle",
        "tweetshake.xcodeproj/project.pbxproj",
        "tweetshake.xcodeproj/project.xcworkspace/contents.xcworkspacedata",
        "tweetshake/AppDelegate.swift",
        "tweetshake/Base.lproj/LaunchScreen.xib",
        "tweetshake/Base.lproj/Main.storyboard",
        "tweetshake/Images.xcassets/AppIcon.appiconset/Contents.json",
        "tweetshake/Images.xcassets/logo.imageset/Contents.json",
        "tweetshake/Images.xcassets/logo.imageset/logo.png",
        "tweetshake/Info.plist.example",
        "tweetshake/LoginViewController.swift",
        "tweetshake/ViewController.swift",
        "tweetshakeTests/Info.plist",
        "tweetshakeTests/tweetshakeTests.swift",
    ]

    for path in required:
        expect(rel(path).exists(), "{} is missing".format(path))


def check_parsable_resources():
    parse_xml("docs/readme-overview.svg")
    parse_xml("tweetshake.xcodeproj/project.xcworkspace/contents.xcworkspacedata")
    parse_xml("tweetshake/Base.lproj/Main.storyboard")
    parse_xml("tweetshake/Base.lproj/LaunchScreen.xib")

    app_icon = parse_json("tweetshake/Images.xcassets/AppIcon.appiconset/Contents.json")
    logo = parse_json("tweetshake/Images.xcassets/logo.imageset/Contents.json")

    if app_icon:
        images = app_icon.get("images", [])
        filenames = {image.get("filename") for image in images if image.get("filename")}
        expect(len(images) >= 6, "AppIcon asset should list the existing iPhone icon variants")
        expect("Icon-60@3x (1).png" in filenames, "AppIcon asset should include the 60pt @3x icon")
        for filename in filenames:
            expect(
                rel("tweetshake/Images.xcassets/AppIcon.appiconset/{}".format(filename)).exists(),
                "AppIcon asset references missing file {}".format(filename),
            )

    if logo:
        images = logo.get("images", [])
        filenames = {image.get("filename") for image in images if image.get("filename")}
        expect("logo.png" in filenames, "logo asset should reference logo.png")


def check_project_wiring():
    pbxproj = read_text("tweetshake.xcodeproj/project.pbxproj")

    for framework in ("Fabric.framework", "TwitterCore.framework", "TwitterKit.framework"):
        expect(framework in pbxproj, "{} should remain referenced in the Xcode project".format(framework))
        expect(
            "{} in Frameworks".format(framework) in pbxproj,
            "{} should be linked in the app target".format(framework),
        )

    expect(
        "TwitterKitResources.bundle in Resources" in pbxproj,
        "TwitterKit resource bundle should remain copied into app resources",
    )
    expect("Main.storyboard in Resources" in pbxproj, "Main.storyboard should be an app resource")
    expect("LaunchScreen.xib in Resources" in pbxproj, "LaunchScreen.xib should be an app resource")
    expect("Images.xcassets in Resources" in pbxproj, "Images.xcassets should be an app resource")
    expect(
        "INFOPLIST_FILE = tweetshake/Info.plist;" in pbxproj,
        "app target should still point at the local ignored app Info.plist",
    )
    expect(
        "INFOPLIST_FILE = tweetshakeTests/Info.plist;" in pbxproj,
        "test target should still point at the local ignored test Info.plist",
    )
    expect("IPHONEOS_DEPLOYMENT_TARGET = 8.3;" in pbxproj, "legacy deployment target should remain visible")
    expect("LastUpgradeCheck = 0630;" in pbxproj, "legacy Xcode project version should remain visible")


def check_storyboard_contract():
    storyboard = read_text("tweetshake/Base.lproj/Main.storyboard")
    expect('customClass="LoginViewController"' in storyboard, "storyboard should start at LoginViewController")
    expect('customClass="ViewController"' in storyboard, "storyboard should keep the shake composer screen")
    expect('identifier="shake"' in storyboard, "storyboard should keep the shake segue identifier")
    expect('text="Shake To Tweet"' in storyboard, "storyboard should keep the user-facing shake prompt")
    expect('image="logo"' in storyboard, "storyboard should keep the logo image view")


def check_sanitized_plist_template():
    plist = parse_plist("tweetshake/Info.plist.example")
    test_plist = parse_plist("tweetshakeTests/Info.plist")
    if not plist:
        return

    fabric = plist.get("Fabric", {})
    kits = fabric.get("Kits", [])
    kit = kits[0] if kits else {}
    kit_info = kit.get("KitInfo", {})
    url_types = plist.get("CFBundleURLTypes", [])
    schemes = []
    for url_type in url_types:
        schemes.extend(url_type.get("CFBundleURLSchemes", []))

    expect(fabric.get("APIKey") == "YOUR_FABRIC_API_KEY", "Fabric API key should be a placeholder")
    expect(kit.get("KitName") == "Twitter", "Info.plist.example should document the Twitter kit")
    expect(
        kit_info.get("consumerKey") == "YOUR_TWITTER_CONSUMER_KEY",
        "Twitter consumer key should be a placeholder",
    )
    expect(
        kit_info.get("consumerSecret") == "YOUR_TWITTER_CONSUMER_SECRET",
        "Twitter consumer secret should be a placeholder",
    )
    expect(
        "twitterkit-YOUR_TWITTER_CONSUMER_KEY" in schemes,
        "Info.plist.example should document the TwitterKit callback scheme placeholder",
    )
    expect(plist.get("UIMainStoryboardFile") == "Main", "Info.plist.example should point at Main storyboard")
    expect(plist.get("UILaunchStoryboardName") == "LaunchScreen", "Info.plist.example should point at launch screen")

    if test_plist:
        expect(test_plist.get("CFBundlePackageType") == "BNDL", "test Info.plist should be bundle metadata")
        expect("Fabric" not in test_plist, "test Info.plist should not contain Fabric credentials")

    tracked = git_ls_files()
    expect("tweetshake/Info.plist" not in tracked, "real app Info.plist should remain untracked")


def check_first_party_swift():
    swift_paths = sorted(rel("tweetshake").glob("*.swift")) + sorted(rel("tweetshakeTests").glob("*.swift"))
    source_by_name = {}
    stripped_source = []
    for path in swift_paths:
        text = path.read_text(encoding="utf-8")
        stripped = strip_swift_comments(text)
        source_by_name[path.name] = stripped
        stripped_source.append(stripped)

    all_source = "\n".join(stripped_source)

    expect("Fabric.with([Twitter()])" in all_source, "AppDelegate should initialize Fabric/TwitterKit")
    expect(
        not re.search(r"\b(?:print|println|NSLog)\s*\(", all_source),
        "first-party Swift should not log login or compose state",
    )

    forbidden_terms = [
        "startWithConsumerKey",
        "consumerKey",
        "consumerSecret",
        "accessToken",
        "authToken",
        "apiKey",
        "APIKey",
        "OAuth",
        "oauth",
    ]
    for term in forbidden_terms:
        expect(term not in all_source, "first-party Swift should not include credential term {}".format(term))

    local_privacy_terms = [
        "http://",
        "https://",
        "NSURL",
        "NSURLConnection",
        "URLSession",
        "NSUserDefaults",
        "UserDefaults",
        "writeToFile",
        "NSKeyedArchiver",
        "analytics",
        "upload",
    ]
    lowered = all_source.lower()
    for term in local_privacy_terms:
        expect(term.lower() not in lowered, "first-party Swift should not add network or persistence term {}".format(term))

    login = source_by_name.get("LoginViewController.swift", "")
    expect("TWTRLogInButton" in login, "LoginViewController should still use TwitterKit login UI")
    expect("[weak self]" in login, "login completion should capture self weakly")
    expect("guard " not in login, "login completion should stay compatible with the older Swift style")
    expect("session != nil && error == nil" in login, "login completion should require a session and no error")
    expect("loginStatus" in login, "login completion should keep local-only status state")
    expect(
        'performSegueWithIdentifier("shake"' in login,
        "login completion should only open the shake flow after successful login",
    )

    view = source_by_name.get("ViewController.swift", "")
    expect("var lastComposeResult" in view, "ViewController should keep local-only compose status state")
    expect("motion == UIEventSubtype.MotionShake" in view, "shake detection should use the motion subtype parameter")
    expect("withEvent event: UIEvent)" in view, "motion override should keep the legacy non-optional event signature")
    expect("TWTRComposer()" in view, "ViewController should still use TwitterKit composer UI")
    expect('composer.setText("I just shook my phone")' in view, "compose text should remain the original sample text")
    expect("showWithCompletion" in view, "composer should still be user-confirmed through TWTRComposer")
    expect("[weak self]" in view, "composer completion should capture self weakly")
    expect("lastComposeResult" in view, "composer completion should update local-only status state")


def check_docs():
    readme = read_text("README.md")
    vision = read_text("VISION.md")
    security = read_text("SECURITY.md")
    changes = read_text("CHANGES.md")
    plan = read_text("docs/plans/2026-06-08-tweet-shake-baseline.md")
    gitignore = read_text(".gitignore")

    for text_name, text in (
        ("README.md", readme),
        ("VISION.md", vision),
        ("SECURITY.md", security),
    ):
        lowered = text.lower()
        expect("make check" in lowered, "{} should document the static verification command".format(text_name))
        expect("info.plist.example" in lowered, "{} should document the sanitized plist template".format(text_name))
        expect("credential" in lowered, "{} should document credential handling".format(text_name))
        expect("silent" in lowered, "{} should reject silent posting or background account actions".format(text_name))

    expect("user-confirmed" in readme.lower(), "README should describe user-confirmed compose behavior")
    expect("scripts/check-baseline.py" in vision, "VISION should name the baseline checker")
    expect("local configuration" in readme.lower(), "README should keep credentials in local configuration")
    expect("local configuration" in security.lower(), "SECURITY should keep credentials in local configuration")
    expect("login completion" in changes.lower(), "CHANGES should mention the login completion guard")
    expect("console logging" in changes.lower(), "CHANGES should mention removal of console logging")
    expect("Info.plist.example" in changes, "CHANGES should mention the sanitized plist template")
    expect("make check" in changes, "CHANGES should mention the new verification command")
    expect("status: completed" in plan, "baseline plan should be marked completed")

    for pattern in ("Info.plist", "*.local.xcconfig", "*.secrets.xcconfig", ".env", ".env.*", "__pycache__/", "*.pyc"):
        expect(pattern in gitignore, ".gitignore should keep {} out of git".format(pattern))


def main():
    check_required_files()
    check_parsable_resources()
    check_project_wiring()
    check_storyboard_contract()
    check_sanitized_plist_template()
    check_first_party_swift()
    check_docs()

    if shutil.which("xcodebuild"):
        print("xcodebuild is available; run a device/simulator build separately for legacy TwitterKit validation.")
    else:
        print("xcodebuild unavailable; skipping legacy iOS build/test and using static baseline checks.")

    if FAILURES:
        print("Static baseline failed:")
        for failure in FAILURES:
            print("- {}".format(failure))
        return 1

    print("Static baseline passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
