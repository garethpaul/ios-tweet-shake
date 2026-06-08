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

    override func viewDidLoad() {
        super.viewDidLoad()

        if !TweetShakeHasConfiguredTwitterCredentials() {
            showCredentialSetupMessage()
            return
        }

        let logInButton = TWTRLogInButton(logInCompletion: { [weak self] (session: TWTRSession!, error: NSError!) in
            if session != nil && error == nil {
                if let viewController = self {
                    viewController.performSegueWithIdentifier("shake", sender: viewController)
                }
            } else {
                if let viewController = self {
                    viewController.showLoginRequiredMessage()
                }
            }
        })
        logInButton.center = self.view.center
        self.view.addSubview(logInButton)

        // Do any additional setup after loading the view, typically from a nib.
    }

    func showCredentialSetupMessage() {
        let messageLabel = UILabel(frame: CGRectInset(self.view.bounds, 24.0, 0.0))
        messageLabel.text = "Configure Twitter credentials before signing in."
        messageLabel.textAlignment = NSTextAlignment.Center
        messageLabel.textColor = UIColor.whiteColor()
        messageLabel.numberOfLines = 0
        self.view.addSubview(messageLabel)
    }

    func showLoginRequiredMessage() {
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
