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
import asyncio
import websockets
import orjson

async def handle_client(websocket, path):
    print("Client connected!")
    try:
        async for message in websocket:
            data = orjson.loads(message)
            print(f"Received: {data}")
            response = {"type": "pong", "received": data}
            await websocket.send(orjson.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "0.0.0.0", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
print("Test server running on ws://localhost:8080")
asyncio.get_event_loop().run_forever()import asyncio
import websockets
import orjson

async def handle_client(websocket, path):
    print("Client connected!")
    try:
        async for message in websocket:
            data = orjson.loads(message)
            print(f"Received: {data}")
            response = {"type": "pong", "received": data}
            await websocket.send(orjson.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

start_server = websockets.serve(handle_client, "0.0.0.0", 8080)
asyncio.get_event_loop().run_until_complete(start_server)
print("Test server running on ws://localhost:8080")
asyncio.get_event_loop().run_forever()