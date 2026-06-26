//
//  tweetshakeTests.swift
//  tweetshakeTests
//
//  Created by Gareth Jones  on 5/23/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import XCTest
@testable import tweetshake

class tweetshakeTests: XCTestCase {

    func testShakeControllerCanBecomeFirstResponder() {
        let controller = ViewController()

        XCTAssertTrue(controller.canBecomeFirstResponder(), "The visible shake controller must be eligible for initial motion delivery")
    }

    func testCredentialHelperRejectsMissingAndPlaceholderValues() {
        XCTAssertFalse(TweetShakeHasConfiguredCredentialValue(nil), "Missing credentials should be rejected")
        XCTAssertFalse(TweetShakeHasConfiguredCredentialValue("  "), "Blank credentials should be rejected")
        XCTAssertFalse(TweetShakeHasConfiguredCredentialValue("$(TWITTER_CONSUMER_KEY)"), "Build setting placeholders should be rejected")
        XCTAssertFalse(TweetShakeHasConfiguredCredentialValue("REPLACE_SECRET"), "Replacement placeholders should be rejected")
    }

    func testCredentialHelperAcceptsTrimmedCredentialValues() {
        XCTAssertTrue(TweetShakeHasConfiguredCredentialValue("  local-consumer-key  "), "Non-placeholder credentials should be accepted after trimming")
    }

    func testTwitterCredentialHelperRequiresNamedTwitterKit() {
        let fabric: NSDictionary = [
            "APIKey": "fabric-api-key",
            "Kits": [
                [
                    "KitInfo": [
                        "consumerKey": "consumer-key",
                        "consumerSecret": "consumer-secret"
                    ]
                ]
            ]
        ]

        XCTAssertFalse(TweetShakeHasConfiguredTwitterCredentials(fabric), "Credential-looking kit info should be rejected unless it belongs to the Twitter kit")
    }

    func testTwitterCredentialHelperRejectsMissingFabricAPIKey() {
        let fabric: NSDictionary = [
            "Kits": [
                [
                    "KitName": "Twitter",
                    "KitInfo": [
                        "consumerKey": "consumer-key",
                        "consumerSecret": "consumer-secret"
                    ]
                ]
            ]
        ]

        XCTAssertFalse(TweetShakeHasConfiguredTwitterCredentials(fabric), "Fabric API key must be configured before Twitter startup")
    }

    func testTwitterCredentialHelperRejectsMissingConsumerSecret() {
        let fabric: NSDictionary = [
            "APIKey": "fabric-api-key",
            "Kits": [
                [
                    "KitName": "Twitter",
                    "KitInfo": [
                        "consumerKey": "consumer-key"
                    ]
                ]
            ]
        ]

        XCTAssertFalse(TweetShakeHasConfiguredTwitterCredentials(fabric), "Twitter consumer secret must be configured before Twitter startup")
    }

    func testTwitterCredentialHelperAcceptsNamedTwitterKit() {
        let fabric: NSDictionary = [
            "APIKey": "fabric-api-key",
            "Kits": [
                [
                    "KitName": "Twitter",
                    "KitInfo": [
                        "consumerKey": "consumer-key",
                        "consumerSecret": "consumer-secret"
                    ]
                ]
            ]
        ]

        XCTAssertTrue(TweetShakeHasConfiguredTwitterCredentials(fabric), "Named Twitter kit credentials should be accepted when all values are configured")
    }

    func testLoginCompletionRequiresCurrentVisibleAppearance() {
        let controller = LoginViewController()
        controller.isLoginViewVisible = true
        controller.loginViewGeneration = 2
        controller.activeLoginAttemptGeneration = 7

        XCTAssertFalse(controller.reserveLoginCompletion(1, attemptGeneration: 7), "A prior appearance completion should remain stale")
        XCTAssertFalse(controller.reserveLoginCompletion(2, attemptGeneration: 6), "A prior button attempt should remain stale")
        XCTAssertTrue(controller.reserveLoginCompletion(2, attemptGeneration: 7), "The current visible attempt should reserve its completion")
        XCTAssertFalse(controller.reserveLoginCompletion(2, attemptGeneration: 7), "A duplicate callback must not reserve a consumed attempt")
        XCTAssertNil(controller.activeLoginAttemptGeneration)
        XCTAssertNil(controller.logInButton)

        controller.activeLoginAttemptGeneration = 8
        controller.isLoginViewVisible = false
        XCTAssertFalse(controller.reserveLoginCompletion(2, attemptGeneration: 8), "A hidden controller should reject its current completion")
    }

    func testLoginCompletionIsInvalidatedWhenDisappearanceBegins() {
        let controller = LoginViewController()
        controller.isLoginViewVisible = true
        controller.loginViewGeneration = 3
        controller.activeLoginAttemptGeneration = 9

        controller.viewWillDisappear(false)
        XCTAssertFalse(controller.reserveLoginCompletion(3, attemptGeneration: 9), "A disappearing controller should reject its current completion")
        XCTAssertNil(controller.activeLoginAttemptGeneration)
    }

    func testLoginRetryRequiresSameVisibleAppearance() {
        let controller = LoginViewController()
        controller.isLoginViewVisible = true
        controller.loginViewGeneration = 4

        XCTAssertTrue(controller.canRetryLogin(4))
        XCTAssertFalse(controller.canRetryLogin(3))

        controller.isLoginViewVisible = false
        XCTAssertFalse(controller.canRetryLogin(4))
    }

    func testLoginRetryRestorationInstallsFreshAttempt() {
        let controller = LoginViewController()
        controller.loadViewIfNeeded()
        controller.isLoginViewVisible = true
        controller.loginViewGeneration = 5
        controller.loginAttemptGeneration = 10

        controller.restoreLoginAfterFailure(5)

        XCTAssertEqual(controller.loginAttemptGeneration, 11)
        XCTAssertEqual(controller.activeLoginAttemptGeneration, 11)
        XCTAssertNotNil(controller.logInButton)
    }

    func testLoginRetryRestorationRejectsStaleAppearance() {
        let controller = LoginViewController()
        controller.isLoginViewVisible = true
        controller.loginViewGeneration = 6
        controller.loginAttemptGeneration = 12

        controller.restoreLoginAfterFailure(5)

        XCTAssertEqual(controller.loginAttemptGeneration, 12)
        XCTAssertNil(controller.activeLoginAttemptGeneration)
        XCTAssertNil(controller.logInButton)
    }

    func testComposerCompletionRequiresCurrentVisibleAttempt() {
        let controller = ViewController()
        controller.isShakeViewVisible = true
        controller.shakeViewGeneration = 2
        controller.activeComposerAttemptGeneration = 7
        controller.isShowingComposer = true

        XCTAssertFalse(controller.reserveComposerCompletion(1, attemptGeneration: 7), "A prior appearance completion should remain stale")
        XCTAssertFalse(controller.reserveComposerCompletion(2, attemptGeneration: 6), "A prior composer attempt should remain stale")
        XCTAssertTrue(controller.reserveComposerCompletion(2, attemptGeneration: 7), "The current visible composer should reserve its completion")
        XCTAssertFalse(controller.reserveComposerCompletion(2, attemptGeneration: 7), "A duplicate composer callback must not reserve a consumed attempt")
        XCTAssertNil(controller.activeComposerAttemptGeneration)
        XCTAssertFalse(controller.isShowingComposer)
    }

    func testStaleComposerCompletionCannotClearNewAttempt() {
        let controller = ViewController()
        controller.isShakeViewVisible = true
        controller.shakeViewGeneration = 3
        controller.activeComposerAttemptGeneration = 10
        controller.isShowingComposer = true

        XCTAssertTrue(controller.reserveComposerCompletion(3, attemptGeneration: 10))
        controller.activeComposerAttemptGeneration = 11
        controller.isShowingComposer = true

        XCTAssertFalse(controller.reserveComposerCompletion(3, attemptGeneration: 10), "A duplicate old callback must not clear a newer composer")
        XCTAssertEqual(controller.activeComposerAttemptGeneration, 11)
        XCTAssertTrue(controller.isShowingComposer)
    }

    func testComposerCompletionIsInvalidatedWhenDisappearanceBegins() {
        let controller = ViewController()
        controller.isShakeViewVisible = true
        controller.shakeViewGeneration = 4
        controller.activeComposerAttemptGeneration = 12
        controller.isShowingComposer = true

        controller.viewWillDisappear(false)

        XCTAssertFalse(controller.isShakeViewVisible)
        XCTAssertFalse(controller.reserveComposerCompletion(4, attemptGeneration: 12), "A disappearing shake controller should reject its composer completion")
        XCTAssertNil(controller.activeComposerAttemptGeneration)
        XCTAssertFalse(controller.isShowingComposer)
    }

    func testComposerPresentationReservationRequiresVisibleIdleController() {
        let controller = ViewController()
        XCTAssertNil(controller.beginComposerPresentation(), "A hidden controller must not start a composer")

        controller.isShakeViewVisible = true
        XCTAssertEqual(controller.beginComposerPresentation(), 1)
        XCTAssertNil(controller.beginComposerPresentation(), "An active composer must block a second reservation")
        XCTAssertEqual(controller.activeComposerAttemptGeneration, 1)
        XCTAssertTrue(controller.isShowingComposer)
    }

    func testShakePresentationPreflightRequiresVisibleIdleController() {
        let controller = ViewController()
        XCTAssertFalse(controller.canBeginComposerPresentation(), "A hidden controller must not inspect account state for a shake")

        controller.isShakeViewVisible = true
        XCTAssertTrue(controller.canBeginComposerPresentation())

        controller.activeComposerAttemptGeneration = 1
        XCTAssertFalse(controller.canBeginComposerPresentation(), "An active composer must block account lookup for another shake")
    }

}
