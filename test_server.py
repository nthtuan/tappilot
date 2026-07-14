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

async def main():
    start_server = await websockets.serve(handle_client, "0.0.0.0", 8080)
    print("Test server running on ws://localhost:8080")
    await start_server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
