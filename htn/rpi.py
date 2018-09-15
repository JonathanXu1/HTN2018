import time
import grovepi

# Connect the Grove Sound Sensor to analog port A0
# SIG,NC,VCC,GND
sound_sensor = 0

grovepi.pinMode(sound_sensor,"INPUT")

# The threshold to turn the led on 400.00 * 5 / 1024 = 1.95v
threshold_value = 400

while True:
    try:
        # Read the sound level
        sensor_value = grovepi.analogRead(sound_sensor)

        print("sensor_value = %d" %sensor_value)
        time.sleep(.5)

    except IOError:
        print ("Error")