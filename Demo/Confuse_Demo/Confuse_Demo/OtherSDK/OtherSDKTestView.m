//
//  OtherSDKTestView.m
//  Confuse_Demo
//
//  Created by qinly on 2018/3/5.
//  Copyright © 2018年 coderap. All rights reserved.
//

#import "OtherSDKTestView.h"

@implementation OtherSDKTestView

- (NSString *)OtherSDKPublicFunctionWithoutParameters {
    return @"OtherSDKPublicFunctionWithoutParameters";
}

- (NSString *)OtherSDKPublicFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2 {
    return @"OtherSDKPublicFunctionWithParameter1:parameter2:";
}

- (void)OtherSDKFunctionWithoutParameters {
    NSLog(@"OtherSDKFunctionWithoutParameters");
}

- (void)OtherSDKFunctionWithParameter1:(NSString *)parameter1 parameter2:(NSInteger)parameter2 {
    NSLog(@"OtherSDKFunctionWithParameter1:parameter2:");
}
@end
