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

    var loginStatus = "not started"

    override func viewDidLoad() {
        super.viewDidLoad()
        let logInButton = TWTRLogInButton(logInCompletion: { [weak self] (session: TWTRSession!, error: NSError!) in
            if session != nil && error == nil {
                if let viewController = self {
                    viewController.loginStatus = "authenticated"
                    viewController.performSegueWithIdentifier("shake", sender: viewController)
                }
            } else {
                if let viewController = self {
                    viewController.loginStatus = "authentication failed"
                }
            }
        })
        logInButton.center = self.view.center
        self.view.addSubview(logInButton)

        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

}
