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

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    override func motionEnded(motion: UIEventSubtype, withEvent event: UIEvent) {
        if motion == UIEventSubtype.MotionShake && !isShowingComposer {
            isShowingComposer = true
            let composer = TWTRComposer()

            composer.setText("I just shook my phone")

            composer.showWithCompletion { [weak self] (result) -> Void in
                self?.isShowingComposer = false
            }
        }
    }
}
