import board
import digitalio
import time

sensor = digitalio.DigitalInOut(board.A0) # nRF52840, Grove A0
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP

while True:
    print(sensor.value)
    time.sleep(0.1)# Write your code here :-)
