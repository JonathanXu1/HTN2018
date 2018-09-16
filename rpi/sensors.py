import Adafruit_ADS1x15
import time
import socket
import pickle
import client
import math

# Matplotlib stuff
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.title("Sensor readings")
plt.legend()
fig = plt.figure()
ax = plt.axes(1,1,1)

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()
# Or create an ADS1015 ADC (12-bit) instance.
# adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
# adc = Adafruit_ADS1x15.ADS1015(address=0x49, bus=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

#Create lists to store everything
df = pd.DataFrame({'y1': 0, 'y2': 0, 'y3': 0})

def animate():
    for i in df:
        df[i] = exponential_smoothing(df[i], 0.05)
        plt.plot(df[i], label='mic %s' % i)

'''simple exponential smoothing go back to last N values
 y_t = a * y_t + a * (1-a)^1 * y_t-1 + a * (1-a)^2 * y_t-2 + ... + a*(1-a)^n * 
y_t-n'''
def exponential_smoothing(panda_series, alpha_value):
    output = sum([alpha_value * (1 - alpha_value) ** i * x for i, x in
                  enumerate(reversed(panda_series))])
    return output


print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*range(4)))
print('-' * 37)

# Calibrate
sum1 = sum2 = sum3 = 0
diff = [0] * 3
for i in range(1000):
    sum1 += adc.read_adc(0, gain=GAIN)
    sum2 += adc.read_adc(1, gain=GAIN)
    sum3 += adc.read_adc(2, gain=GAIN)
diff[0] = sum1/1000;
diff[1] = sum2/1000;
diff[2] = sum3/1000;

# Connecting to the server
ip = "138.197.235.123"
print("Connecting to " + ip)
client = socket.socket()
client.connect((ip, 80))
print("Pinging server:")
client.send("ping".encode())
print("Server says: " + client.recv(1024).decode())

# Main loop.
while True:
    # Read all the ADC channel values in a list.
    values = [0] * 3
    for i in range(3):
        # Read the specified ADC channel using the previously set gain value.
        values[i] = adc.read_adc(i, gain=GAIN) - diff[i]
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        # values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values))
    '''
    #Socket send
    message = '| {0:>6} | {1:>6} | {2:>6} | {3:>6} |'.format(*values)
    client.send("target:".encode())
    client.recv(1024).decode()
    client.send(pickle.dumps(message))
    '''

    #Plotting
    df2 = pd.DataFrame({'y1': values[0], 'y2': values[1], 'y3': values[2]})
    df.append(df2)
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

    # Find angle
    N2X = math.sin(1.0472) * df[1][-1] / math.sin(1.5708)
    N2Y = df[1][-1]

    N3X = math.sin(1.0472) * df[2][-1] / math.sin(1.5708)
    N3Y = df[2][-1]

    X = N3X - N2X
    # Serial.print("x: ")
    # Serial.println(X)

    Y = df[0][-1] - N2Y - N3Y
    # Serial.print("y: ")
    # Serial.println(Y)

    H = math.sqrt(math.pow(math.fabs(X), 2) + math.pow(math.fabs(Y), 2))
    # Serial.print("Hype")
    # Serial.println(H)

    AR = math.atan2(math.fabs(Y), math.fabs(X)) * 180 / 3.14

    # Serial.print("Relative angle: ")
    # Serial.println(AR)

    if Y > 0:# ar =180
        # Q1
        if X < 0:
            angle = 180+AR
        # Q2
        else:
            angle = 90+AR

    else: # ar=0
        # Q1
        if X < 0:
            angle = 270-AR
        # Q2
        else:
            angle = 90+AR
    print(angle)
    # Pause for half a second.
    time.sleep(0.01)
