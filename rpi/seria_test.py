import serial

ser = serial.Serial('/dev/ttyACM0',9600)

while True:
	bytesToRead = ser.inWaiting()
	data = ser.read(bytesToRead)
	print(data)