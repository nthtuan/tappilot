#import "TPCommandDispatcher.h"
#import "TPLogger.h"
#import "TPLuaManager.h"
#import "TPWebSocketServer.h"

@implementation TPCommandDispatcher

+ (instancetype)sharedDispatcher {
    static TPCommandDispatcher *sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
    }
    return self;
}

- (void)dispatchCommand:(NSDictionary *)command {
    NSString *type = command[@"type"];
    [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Received command: %@", type]];
    
    if ([type isEqualToString:@"ping"]) {
        [self handlePing];
    } else if ([type isEqualToString:@"status"]) {
        [self handleStatus];
    } else if ([type isEqualToString:@"upload"]) {
        [self handleUpload:command];
    } else if ([type isEqualToString:@"run"]) {
        [self handleRun:command];
    } else if ([type isEqualToString:@"stop"]) {
        [self handleStop:command];
    } else if ([type isEqualToString:@"restart"]) {
        [self handleRestart:command];
    } else if ([type isEqualToString:@"delete"]) {
        [self handleDelete:command];
    } else if ([type isEqualToString:@"list"]) {
        [self handleListScripts];
    } else if ([type isEqualToString:@"heartbeat"]) {
        [self handleHeartbeat];
    }
}

- (void)handlePing {
    NSDictionary *response = @{@"type": @"pong", @"timestamp": @([[NSDate date] timeIntervalSince1970])};
    // Send response via WebSocket server (placeholder)
    [[TPLogger sharedLogger] log:@"Responding to ping"];
}

- (void)handleStatus {
    NSDictionary *status = @{
        @"type": @"status",
        @"status": @"running",
        @"timestamp": @([[NSDate date] timeIntervalSince1970])
    };
    [[TPLogger sharedLogger] log:@"Sending status"];
}

- (void)handleUpload:(NSDictionary *)command {
    NSString *name = command[@"name"];
    NSString *content = command[@"content"];
    if (name && content) {
        [[TPLuaManager sharedManager] uploadScript:name content:content];
    }
}

- (void)handleRun:(NSDictionary *)command {
    NSString *name = command[@"name"];
    if (name) {
        [[TPLuaManager sharedManager] runScript:name];
    }
}

- (void)handleStop:(NSDictionary *)command {
    NSString *name = command[@"name"];
    if (name) {
        [[TPLuaManager sharedManager] stopScript:name];
    }
}

- (void)handleRestart:(NSDictionary *)command {
    NSString *name = command[@"name"];
    if (name) {
        [[TPLuaManager sharedManager] restartScript:name];
    }
}

- (void)handleDelete:(NSDictionary *)command {
    NSString *name = command[@"name"];
    if (name) {
        [[TPLuaManager sharedManager] deleteScript:name];
    }
}

- (void)handleListScripts {
    NSArray *scripts = [[TPLuaManager sharedManager] listScripts];
    NSDictionary *response = @{@"type": @"scripts", @"scripts": scripts};
    [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Listing %lu scripts", (unsigned long)scripts.count]];
}

- (void)handleHeartbeat {
    [[TPLogger sharedLogger] log:@"Heartbeat received"];
}

@end
