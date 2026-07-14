#import "TPLuaManager.h"
#import "TPLogger.h"

@implementation TPLuaManager

+ (instancetype)sharedManager {
    static TPLuaManager *sharedInstance = nil;
    static dispatch_once_t onceToken;
    dispatch_once(&onceToken, ^{
        sharedInstance = [[self alloc] init];
    });
    return sharedInstance;
}

- (instancetype)init {
    self = [super init];
    if (self) {
        [self setupScriptDirectory];
    }
    return self;
}

- (void)setupScriptDirectory {
    NSFileManager *fm = [NSFileManager defaultManager];
    NSString *scriptDir = @"/var/mobile/Library/TappilotAgent/scripts";
    if (![fm fileExistsAtPath:scriptDir]) {
        [fm createDirectoryAtPath:scriptDir withIntermediateDirectories:YES attributes:nil error:nil];
    }
}

- (NSString *)scriptPathForName:(NSString *)name {
    return [NSString stringWithFormat:@"/var/mobile/Library/TappilotAgent/scripts/%@", name];
}

- (BOOL)uploadScript:(NSString *)name content:(NSString *)content {
    @try {
        NSString *path = [self scriptPathForName:name];
        [content writeToFile:path atomically:YES encoding:NSUTF8StringEncoding error:nil];
        [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Uploaded script: %@", name]];
        return YES;
    } @catch (NSException *exception) {
        [[TPLogger sharedLogger] logError:[NSString stringWithFormat:@"Failed to upload script %@: %@", name, exception.reason]];
        return NO;
    }
}

- (BOOL)deleteScript:(NSString *)scriptName {
    @try {
        NSString *path = [self scriptPathForName:scriptName];
        [[NSFileManager defaultManager] removeItemAtPath:path error:nil];
        [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Deleted script: %@", scriptName]];
        return YES;
    } @catch (NSException *exception) {
        [[TPLogger sharedLogger] logError:[NSString stringWithFormat:@"Failed to delete script %@: %@", scriptName, exception.reason]];
        return NO;
    }
}

- (NSArray<NSString *> *)listScripts {
    NSString *scriptDir = @"/var/mobile/Library/TappilotAgent/scripts";
    NSFileManager *fm = [NSFileManager defaultManager];
    NSArray *files = [fm contentsOfDirectoryAtPath:scriptDir error:nil];
    NSMutableArray *luaScripts = [NSMutableArray array];
    for (NSString *file in files) {
        if ([file.pathExtension isEqualToString:@"lua"]) {
            [luaScripts addObject:file];
        }
    }
    return [luaScripts copy];
}

- (BOOL)runScript:(NSString *)scriptName {
    // Implement Lua runtime execution here
    [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Running script: %@", scriptName]];
    return YES;
}

- (BOOL)stopScript:(NSString *)scriptName {
    [[TPLogger sharedLogger] log:[NSString stringWithFormat:@"Stopping script: %@", scriptName]];
    return YES;
}

- (BOOL)restartScript:(NSString *)scriptName {
    [self stopScript:scriptName];
    return [self runScript:scriptName];
}

@end
