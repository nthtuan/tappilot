#import "TPConfig.h"
#import "TPLogger.h"

@implementation TPConfig

+ (instancetype)sharedConfig {
    static TPConfig *sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        _port = 8080;
        _heartbeatInterval = 5.0;
        _serverHost = @"127.0.0.1";
        [self loadConfig];
    }
    return self;
}

- (void)loadConfig {
    NSString *configPath = @"/var/mobile/Library/Preferences/com.tappilot.agent.plist";
    NSDictionary *config = [NSDictionary dictionaryWithContentsOfFile:configPath];
    if (config) {
        if (config[@"port"]) {
            _port = [config[@"port"] unsignedIntegerValue];
        }
        if (config[@"heartbeatInterval"]) {
            _heartbeatInterval = [config[@"heartbeatInterval"] doubleValue];
        }
        if (config[@"serverHost"]) {
            _serverHost = config[@"serverHost"];
        }
        [[TPLogger sharedLogger] log:@"Config loaded"];
    }
}

- (void)saveConfig {
    NSString *configPath = @"/var/mobile/Library/Preferences/com.tappilot.agent.plist";
    NSDictionary *config = @{
        @"port": @(_port),
        @"heartbeatInterval": @(_heartbeatInterval),
        @"serverHost": _serverHost
    };
    [config writeToFile:configPath atomically:YES];
    [[TPLogger sharedLogger] log:@"Config saved"];
}

@end
