#import <Foundation/Foundation.h>
#import <objc/runtime.h>

#define TP_LOG(fmt, ...) NSLog(@"[TappilotAgent] " fmt, ##__VA_ARGS__)

typedef NS_ENUM(NSInteger, TPCommandType) {
    TPCommandTypePing = 0,
    TPCommandTypeStatus,
    TPCommandTypeUpload,
    TPCommandTypeRun,
    TPCommandTypeStop,
    TPCommandTypeRestart,
    TPCommandTypeDeleteScript,
    TPCommandTypeListScripts,
    TPCommandTypeHeartbeat
};

typedef NS_ENUM(NSInteger, TPAgentStatus) {
    TPAgentStatusIdle = 0,
    TPAgentStatusRunning,
    TPAgentStatusError
};
