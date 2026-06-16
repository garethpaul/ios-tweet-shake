//
//  ViewController.swift
//  tweetshake
//
//  Created by Gareth Jones  on 5/23/15.
//  Copyright (c) 2015 gpj. All rights reserved.
//

import UIKit
import TwitterKit


class LoginViewController: UIViewController {

    var logInButton: TWTRLogInButton?
    var credentialSetupMessageLabel: UILabel?
    var isLoginViewVisible = false
    var loginViewGeneration = 0

    override func viewWillAppear(animated: Bool) {
        super.viewWillAppear(animated)
        isLoginViewVisible = true
        loginViewGeneration += 1

        if TweetShakeHasConfiguredTwitterCredentials() {
            installLoginButtonForCurrentAppearance()
        }
    }

    override func viewWillDisappear(animated: Bool) {
        super.viewWillDisappear(animated)
        isLoginViewVisible = false
        logInButton?.removeFromSuperview()
        logInButton = nil
    }

    override func viewDidLoad() {
        super.viewDidLoad()

        if !TweetShakeHasConfiguredTwitterCredentials() {
            showCredentialSetupMessage()
            return
        }

    }

    func installLoginButtonForCurrentAppearance() {
        logInButton?.removeFromSuperview()
        let generation = loginViewGeneration
        let logInButton = TWTRLogInButton(logInCompletion: { [weak self] (session: TWTRSession!, error: NSError!) in
            dispatch_async(dispatch_get_main_queue()) {
                if let viewController = self {
                    guard viewController.canHandleLoginCompletion(generation) else {
                        return
                    }

                    if session != nil && error == nil {
                        viewController.performSegueWithIdentifier("shake", sender: viewController)
                    } else {
                        viewController.showLoginRequiredMessage()
                    }
                }
            }
        })
        self.logInButton = logInButton
        self.view.addSubview(logInButton)
        centerLoginButton()
    }

    func canHandleLoginCompletion(generation: Int) -> Bool {
        return isLoginViewVisible && generation == loginViewGeneration
    }

    override func viewDidLayoutSubviews() {
        super.viewDidLayoutSubviews()

        centerLoginButton()
        layoutCredentialSetupMessage()
    }

    func centerLoginButton() {
        if let logInButton = self.logInButton {
            logInButton.center = CGPointMake(
                CGRectGetMidX(self.view.bounds),
                CGRectGetMidY(self.view.bounds)
            )
        }
    }

    func layoutCredentialSetupMessage() {
        if let messageLabel = self.credentialSetupMessageLabel {
            messageLabel.frame = CGRectInset(self.view.bounds, 24.0, 0.0)
        }
    }

    func showCredentialSetupMessage() {
        if self.credentialSetupMessageLabel != nil {
            return
        }

        let messageLabel = UILabel(frame: CGRectZero)
        messageLabel.text = "Configure Twitter credentials before signing in."
        messageLabel.textAlignment = NSTextAlignment.Center
        messageLabel.textColor = UIColor.whiteColor()
        messageLabel.numberOfLines = 0
        self.credentialSetupMessageLabel = messageLabel
        self.view.addSubview(messageLabel)
        layoutCredentialSetupMessage()
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

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
