#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@protocol TPWebSocketServerDelegate;

@interface TPWebSocketServer : NSObject

@property (nonatomic, weak, nullable) id<TPWebSocketServerDelegate> delegate;
@property (nonatomic, assign, readonly) BOOL isRunning;

- (instancetype)initWithPort:(NSUInteger)port;
- (void)start;
- (void)stop;
- (void)sendMessage:(NSDictionary *)message;

@end

@protocol TPWebSocketServerDelegate <NSObject>

@optional
- (void)webSocketServer:(TPWebSocketServer *)server didReceiveMessage:(NSDictionary *)message;
- (void)webSocketServerDidStart:(TPWebSocketServer *)server;
- (void)webSocketServerDidStop:(TPWebSocketServer *)server;

@end

NS_ASSUME_NONNULL_END
