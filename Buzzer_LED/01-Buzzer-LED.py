import board
import digitalio
import time

actuator = digitalio.DigitalInOut(board.D5) # nRF52840, Grove D2
actuator.direction = digitalio.Direction.OUTPUT

# setup
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT

sensor = digitalio.DigitalInOut(board.D9) # nRF52840, Grove D4
sensor.direction = digitalio.Direction.INPUT
sensor.pull = digitalio.Pull.UP

while True:
    if sensor.value == True:

        actuator.value = True
        led.value = True
        time.sleep(0.01)

        actuator.value = False
        led.value = False
        print("Akusignal")

