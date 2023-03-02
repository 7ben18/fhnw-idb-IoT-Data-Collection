# Write your code here :-)
import analogio
import board
import time

sensor_light = analogio.AnalogIn(board.A2) # nRF52840 A2, Grove A2

while True:
    light_value = sensor_light.value
    voltage = (light_value * 3.3) / 65536
    print((light_value, voltage)) # serial plotter format
    time.sleep(1)
