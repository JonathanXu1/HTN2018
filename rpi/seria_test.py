import serial
import socket
import asyncio
import datetime
import random
import websockets
try:
    import thread
except ImportError:
    import _thread as thread
import time

# ser = serial.Serial('/dev/ttyACM0',9600)

async def hello():
    async with websockets.connect(
            'ws://10.21.62.43:8765') as websocket:
        name = input("What's your name? ")

        await websocket.send(name)

asyncio.get_event_loop().run_until_complete(hello())


while True:
    data = ser.readline()
    print(data)
