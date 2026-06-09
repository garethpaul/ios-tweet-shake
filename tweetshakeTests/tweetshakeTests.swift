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

}
