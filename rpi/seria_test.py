import serial
import tornado
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

ser = serial.Serial('/dev/ttyACM0',9600)



async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, '10.21.62.43', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


while True:
    data = ser.readline()
    print(data)
