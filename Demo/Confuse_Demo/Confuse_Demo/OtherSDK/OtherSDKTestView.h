//
//  OtherSDKTestView.h
//  Confuse_Demo
//
//  Created by qinly on 2018/3/5.
//  Copyright © 2018年 coderap. All rights reserved.
//

#import <UIKit/UIKit.h>

@interface OtherSDKTestView : UIView
- (NSString *)OtherSDKPublicFunctionWithoutParameters;

- (NSString *)OtherSDKPublicFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2;
@end
