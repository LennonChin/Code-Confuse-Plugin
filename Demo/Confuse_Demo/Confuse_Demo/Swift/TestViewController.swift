//
//  TestViewController.swift
//  Confuse_Demo
//
//  Created by qinly on 2018/3/5.
//  Copyright © 2018年 coderap. All rights reserved.
//
import UIKit

class TestViewController: UIViewController {
    
    override func viewDidLoad() {
        super.viewDidLoad()
        self.title = "TestViewController"
    }
    
    func TestFunction() -> [String] {
        
        return "TestFunction"
    }
    
}

extension TestViewController {
    
    func TestFunction2() -> [String] {
        
        return "TestFunction2"
    }
    
    func TestFunction3() -> [UIViewController] {
        
        
        return UIViewController()
    }
}

