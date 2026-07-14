#import <Foundation/Foundation.h>
#import "TPAgentCommon.h"
#import "TPLogger.h"
#import "TPConfig.h"
#import "TPWebSocketServer.h"
#import "TPCommandDispatcher.h"
#import "TPLuaManager.h"

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        TP_LOG(@"Tappilot Agent starting...");
        [[TPLogger sharedLogger] log:@"Agent started"];
        
        TPConfig *config = [TPConfig sharedConfig];
        TPWebSocketServer *server = [[TPWebSocketServer alloc] initWithPort:config.port];
        
        [server start];
        
        [[NSRunLoop mainRunLoop] run];
    }
    return 0;
}
