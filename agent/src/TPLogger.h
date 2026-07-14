#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface TPLogger : NSObject

+ (instancetype)sharedLogger;

- (void)log:(NSString *)message;
- (void)logError:(NSString *)message;
- (void)logWarning:(NSString *)message;

@end

NS_ASSUME_NONNULL_END
