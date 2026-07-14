#import <Foundation/Foundation.h>
#import "TPAgentCommon.h"

NS_ASSUME_NONNULL_BEGIN

@interface TPCommandDispatcher : NSObject

+ (instancetype)sharedDispatcher;
- (void)dispatchCommand:(NSDictionary *)command;

@end

NS_ASSUME_NONNULL_END
