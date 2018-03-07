//
//  ViewController.m
//  Confuse_Demo
//
//  Created by LennonChin on 2018/3/5.
//  Copyright © 2018年 coderap. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
/** testName */
@property (nonatomic, strong) NSString *testName;
@end

@implementation ViewController

- (void)setTestName:(NSString *)testName {
    _testName = testName;
}

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view, typically from a nib.
}


- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

- (NSString *)thisIsAPublicFunctionWithoutParameters {
    NSLog(@"thisIsAPublicFunctionWithoutParameters");
    return @"thisIsAPublicFunctionWithoutParameters";
}

- (NSString *)thisIsAPublicFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2 {
    NSLog(@"thisIsAPublicFunctionWithParameter1:parameter2:");
    return @"thisIsAPublicFunctionWithParameter1:parameter2:";
}

- (void)thisIsATestFunctionWithoutParameters {
    NSLog(@"thisIsATestFunctionWithoutParameters");
}

- (void)thisIsATestFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2 {
    NSLog(@"thisIsATestFunctionWithParameter1:parameter2:");
}
@end
