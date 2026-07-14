#import "TPLogger.h"
#import "TPAgentCommon.h"

@implementation TPLogger

+ (instancetype)sharedLogger {
    static TPLogger *sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        [self setupLogDirectory];
    }
    return self;
}

- (void)setupLogDirectory {
    NSFileManager *fm = [NSFileManager defaultManager];
    NSString *logDir = @"/var/mobile/Library/Logs/TappilotAgent";
    if (![fm fileExistsAtPath:logDir]) {
        [fm createDirectoryAtPath:logDir withIntermediateDirectories:YES attributes:nil error:nil];
    }
}

- (void)log:(NSString *)message {
    TP_LOG(@"%@", message);
    [self writeToFile:message type:@"INFO"];
}

- (void)logError:(NSString *)message {
    TP_LOG(@"ERROR: %@", message);
    [self writeToFile:message type:@"ERROR"];
}

- (void)logWarning:(NSString *)message {
    TP_LOG(@"WARNING: %@", message);
    [self writeToFile:message type:@"WARNING"];
}

- (void)writeToFile:(NSString *)message type:(NSString *)type {
    NSDateFormatter *df = [[NSDateFormatter alloc] init];
    [df setDateFormat:@"yyyy-MM-dd"];
    NSString *logFileName = [NSString stringWithFormat:@"%@.log", [df stringFromDate:[NSDate date]]];
    NSString *logPath = [NSString stringWithFormat:@"/var/mobile/Library/Logs/TappilotAgent/%@", logFileName];

    [df setDateFormat:@"yyyy-MM-dd HH:mm:ss"];
    NSString *timestamp = [df stringFromDate:[NSDate date]];
    NSString *logLine = [NSString stringWithFormat:@"[%@] [%@] %@\n", timestamp, type, message];

    NSFileHandle *fh = [NSFileHandle fileHandleForWritingAtPath:logPath];
    if (!fh) {
        [[NSFileManager defaultManager] createFileAtPath:logPath contents:nil attributes:nil];
        fh = [NSFileHandle fileHandleForWritingAtPath:logPath];
    }
    [fh seekToEndOfFile];
    [fh writeData:[logLine dataUsingEncoding:NSUTF8StringEncoding]];
    [fh closeFile];
}

@end
