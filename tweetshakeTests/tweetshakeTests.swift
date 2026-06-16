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

}
