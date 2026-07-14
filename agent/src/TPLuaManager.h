#import <Foundation/Foundation.h>

NS_ASSUME_NONNULL_BEGIN

@interface TPLuaManager : NSObject

+ (instancetype)sharedManager;

- (BOOL)runScript:(NSString *)scriptName;
- (BOOL)stopScript:(NSString *)scriptName;
- (BOOL)restartScript:(NSString *)scriptName;
- (NSArray<NSString *> *)listScripts;
- (BOOL)uploadScript:(NSString *)name content:(NSString *)content;
- (BOOL)deleteScript:(NSString *)scriptName;

@end

NS_ASSUME_NONNULL_END
