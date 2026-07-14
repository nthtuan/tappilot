#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface TPConfig : NSObject

@property (nonatomic, assign) NSUInteger port;
@property (nonatomic, assign) NSTimeInterval heartbeatInterval;
@property (nonatomic, copy) NSString *serverHost;

+ (instancetype)sharedConfig;
- (void)loadConfig;
- (void)saveConfig;

@end

NS_ASSUME_NONNULL_END
