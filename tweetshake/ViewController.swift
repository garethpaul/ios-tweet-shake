//
//  ViewController.swift
//  tweetshake
//
//  Created by Gareth Jones  on 5/23/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import TwitterKit

class ViewController: UIViewController {

    var isShowingComposer = false
    var isShakeViewVisible = false
    var shakeViewGeneration = 0
    var composerAttemptGeneration = 0
    var activeComposerAttemptGeneration: Int?

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        isShakeViewVisible = true
        shakeViewGeneration += 1
        activeComposerAttemptGeneration = nil
        isShowingComposer = false
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        isShakeViewVisible = false
        activeComposerAttemptGeneration = nil
        isShowingComposer = false
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func motionEnded(motion: UIEventSubtype, withEvent event: UIEvent) {
        if motion == UIEventSubtype.MotionShake {
            if !hasTwitterSession() {
                showLoginRequiredMessage()
                return
            }

            let appearanceGeneration = shakeViewGeneration
            guard let attemptGeneration = beginComposerPresentation() else {
                return
            }
            let composer = TWTRComposer()

            composer.setText("I just shook my phone")

            composer.showWithCompletion { [weak self] (result) -> Void in
                dispatch_async(dispatch_get_main_queue()) {
                    if let viewController = self {
                        viewController.reserveComposerCompletion(
                            appearanceGeneration,
                            attemptGeneration: attemptGeneration
                        )
                    }
                }
            }
        }
    }

    func beginComposerPresentation() -> Int? {
        guard isShakeViewVisible &&
              activeComposerAttemptGeneration == nil &&
              presentedViewController == nil else {
            return nil
        }

        composerAttemptGeneration += 1
        activeComposerAttemptGeneration = composerAttemptGeneration
        isShowingComposer = true
        return composerAttemptGeneration
    }

    func reserveComposerCompletion(appearanceGeneration: Int, attemptGeneration: Int) -> Bool {
        guard isShakeViewVisible &&
              appearanceGeneration == shakeViewGeneration &&
              activeComposerAttemptGeneration == attemptGeneration else {
            return false
        }

        activeComposerAttemptGeneration = nil
        isShowingComposer = false
        return true
    }

    func hasTwitterSession() -> Bool {
        return Twitter.sharedInstance().session() != nil
    }

    func showLoginRequiredMessage() {
        if self.presentedViewController != nil {
            return
        }

        let alert = UIAlertController(title: "Twitter Login Required", message: "Sign in with Twitter before composing a tweet.", preferredStyle: UIAlertControllerStyle.Alert)
        let action = UIAlertAction(title: "OK", style: UIAlertActionStyle.Default, handler: nil)
        alert.addAction(action)
        self.presentViewController(alert, animated: true, completion: nil)
    }
}
