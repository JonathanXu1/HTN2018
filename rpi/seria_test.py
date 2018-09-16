import serial
import socket
import asyncio
import datetime
import random
import socket

try:
    import thread
except ImportError:
    import _thread as thread
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("10.21.62.43", 80))
sock.listen(2)
(client,(ip,port))=sock.accept()
time.sleep(1)
client.send("HELLO")

# ser = serial.Serial('/dev/ttyACM0',9600)



#
# while True:
#     data = ser.readline()
#     print(data)
