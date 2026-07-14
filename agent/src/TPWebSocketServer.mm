#import "TPWebSocketServer.h"
#import "TPLogger.h"
#import "TPCommandDispatcher.h"
#include <sys/socket.h>
#include <netinet/in.h>

@interface TPWebSocketServer ()
@property (nonatomic, assign) NSUInteger port;
@property (nonatomic, strong) NSFileHandle *serverHandle;
@property (nonatomic, strong) NSMutableArray<NSFileHandle *> *clientHandles;
@end

@implementation TPWebSocketServer

- (instancetype)initWithPort:(NSUInteger)port {
    self = [super init];
    if (self) {
        _port = port;
        _clientHandles = [NSMutableArray array];
    }
    return self;
}

- (void)start {
    if (_isRunning) return;
    _isRunning = YES;
    
    [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Starting server on port %lu", (unsigned long)_port]];
    
    // Create a simple socket server
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        [[TPLogger sharedLogger] logError:@"Socket create failed"];
        return;
    }
    
    int yes = 1;
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes));
    
    struct sockaddr_in serv_addr;
    memset(&serv_addr, 0, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(_port);
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    
    if (bind(sockfd, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        [[TPLogger sharedLogger] logError:@"Bind failed"];
        close(sockfd);
        return;
    }
    
    listen(sockfd, 5);
    
    _serverHandle = [[NSFileHandle alloc] initWithFileDescriptor:sockfd closeOnDealloc:YES];
    [NSNotificationCenter.defaultCenter addObserver:self selector:@selector(acceptClient:) name:NSFileHandleConnectionAcceptedNotification object:_serverHandle];
    [_serverHandle acceptConnectionInBackgroundAndNotify];
    
    if ([_delegate respondsToSelector:@selector(webSocketServerDidStart:)]) {
        [_delegate webSocketServerDidStart:self];
    }
}

- (void)stop {
    if (!_isRunning) return;
    _isRunning = NO;
    
    [[TPLogger sharedLogger] log:@"Stopping server"];
    
    [NSNotificationCenter.defaultCenter removeObserver:self];
    [_serverHandle closeFile];
    for (NSFileHandle *handle in _clientHandles) {
        [handle closeFile];
    }
    [_clientHandles removeAllObjects];
    
    if ([_delegate respondsToSelector:@selector(webSocketServerDidStop:)]) {
        [_delegate webSocketServerDidStop:self];
    }
}

- (void)broadcastMessage:(NSDictionary *)message {
    NSError *err = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:message options:0 error:&err];
    if (jsonData == nil) return;
    
    for (NSFileHandle *client in _clientHandles) {
        [client writeData:jsonData];
    }
}

- (void)acceptClient:(NSNotification *)notification {
    NSFileHandle *clientHandle = notification.userInfo[NSFileHandleNotificationFileHandleItem];
    if (!clientHandle) return;
    
    [_clientHandles addObject:clientHandle];
    [NSNotificationCenter.defaultCenter addObserver:self selector:@selector(readData:) name:NSFileHandleReadCompletionNotification object:clientHandle];
    [clientHandle readInBackgroundAndNotify];
}

- (void)readData:(NSNotification *)notification {
    NSFileHandle *clientHandle = notification.object;
    NSData *data = notification.userInfo[NSFileHandleNotificationDataItem];
    
    if (data.length == 0) {
        [_clientHandles removeObject:clientHandle];
        [clientHandle closeFile];
        return;
    } else {
        // Try to parse JSON data
        NSError *err = nil;
        NSDictionary *json = [NSJSONSerialization JSONObjectWithData:data options:0 error:&err];
        if (json) {
            [[TPCommandDispatcher sharedDispatcher] dispatchCommand:json];
            if ([_delegate respondsToSelector:@selector(webSocketServer:didReceiveMessage:fromClient:)]) {
                [_delegate webSocketServer:self didReceiveMessage:json fromClient:clientHandle];
            }
        }
        [clientHandle readInBackgroundAndNotify];
    }
}

@end
