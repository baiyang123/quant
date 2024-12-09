import asyncio
import json

import websockets


# 订阅
async def main():
    async with websockets.connect("wss://wspap.okx.com:8443/ws/v5/public?brokerId=9999") as websocket:
        arg2 = {
                  "op": "subscribe",
                  "args":   [
                    {
                      "channel" : "instruments",
                      "instType": "SPOT"
                    }
                  ]
                }
        data_json = json.dumps(arg2)
        await websocket.send(data_json)
        print(f"Sent: {data_json}")

        response = await websocket.recv()
        print(f"Received: {response}")


asyncio.run(main())

# async def main():
#     async with websockets.connect("ws://localhost:8765") as websocket:
#         message = "Hello, server!"
#         await websocket.send(message)
#         print(f"Sent: {message}")
#
#         response = await websocket.recv()
#         print(f"Received: {response}")
#
#
# asyncio.run(main())
