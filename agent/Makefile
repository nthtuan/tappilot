export ARCHS = arm64 arm64e
export TARGET = iphone:clang:14.5:13.0

INSTALL_TARGET_PROCESSES = tappilot-agent

include $(THEOS)/makefiles/common.mk

TOOL_NAME = tappilot-agent

tappilot-agent_FILES = $(wildcard src/*.mm)
tappilot-agent_CFLAGS = -fobjc-arc -std=c++17
tappilot-agent_CCFLAGS = -std=c++17
tappilot-agent_FRAMEWORKS = Foundation
tappilot-agent_INSTALL_PATH = /usr/bin

include $(THEOS_MAKE_PATH)/tool.mk