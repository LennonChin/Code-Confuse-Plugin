//
//  ViewController.h
//  Confuse_Demo
//
//  Created by LennonChin on 2018/3/5.
//  Copyright © 2018年 coderap. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface ViewController : UIViewController

- (NSString *)thisIsAPublicFunctionWithoutParameters;

- (NSString *)thisIsAPublicFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2;
@end

