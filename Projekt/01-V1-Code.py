# Libraries
import board
import digitalio
import time
import adafruit_dht
import analogio
from ChainableLED import ChainableLED
from lib import tm1637lib
import random

# setup: RED_LED on pin D3
led = digitalio.DigitalInOut(board.RED_LED)  # general-purpose RED LED on Pin D3
led.direction = digitalio.Direction.OUTPUT

# setup: button sensor
sensor_button = digitalio.DigitalInOut(board.A0) # nRF52840, Grove A0
sensor_button.direction = digitalio.Direction.INPUT
sensor_button.pull = digitalio.Pull.UP

# setup: Temperature and Humidity sensor
dht = adafruit_dht.DHT11(board.A4)  # nRF52840, Grove D4

# setup: Lightsensor
sensor_light = analogio.AnalogIn(board.A2) # nRF52840 A2, Grove A2

# setup: RGB-LED
CLK_PIN = board.D5 # nRF5840 D5, Grove D2
DATA_PIN = board.D6
NUMBER_OF_LEDS = 1
# create rgb_led objecct
rgb_led = ChainableLED(CLK_PIN, DATA_PIN, NUMBER_OF_LEDS)
# set color of rgb_led to red
rgb_led.setColorRGB(0, 255, 0, 0)

# setup: display
display = tm1637lib.Grove4DigitDisplay(board.D9, board.D10) # nRF52840 D9, D10, Grove D4

# Constants for meassurement
dht_INTERVAL = 1

# Variables
measurement_on = False

# Main loop
while True:

    # Check if button is pressed once
    if sensor_button.value == True and not measurement_on:
        # Start measurement
        measurement_on = True

        for _ in range(10):
            led.value = True
            rgb_led.setColorRGB(0, 0, 0, 0)
            time.sleep(0.1)
            led.value = False
            rgb_led.setColorRGB(0, 255, 0, 0)
            time.sleep(0.1)

        rgb_led.setColorRGB(0, 0, 0, 255)

        while measurement_on:
            # Take a measurement
            start = time.time()
            t = time.localtime(start)

            try:
                # Read the temperature and convert it to integer
                temperature = int(round(dht.temperature))
                # Read the humidity and convert it to integer
                humidity = int(round(dht.humidity))
                # Read the light_value and voltage and convert it to integer
                light_value = sensor_light.value
                voltage = (light_value * 3.3) / 65536

                measures = [str(temperature) + " C", str(humidity) + " H", str(light_value // 100) + "L", " " + str(voltage // 1) + "V"]
                value = random.choice(measures)
                display.show(value)

                # Print timestamp, temperatur, humidity
                output = ("|Timestamp {:d}:{:02d}:{:02d} | Temperature {:g} | Humidity {:g} | Light_value {:g} | Voltage {:g} |"
                .format(t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity, light_value, voltage))
                print(output)

            except RuntimeError as e:
                # Reading doesn't always work! Just print error and we'll try again
                print("|Timestamp {:d}:{:02d}:{:02d} | Temperature {:g} | Humidity {:g} | Light_value {:g} | Voltage {:g} |"
                .format(t.tm_hour, t.tm_min, t.tm_sec, -1, -1, -1, -1))

            end = time.time()
            # Wait for the remaining time
            time.sleep(dht_INTERVAL - (end - start))

    # Check if button is pressed again
    elif sensor_button.value == True and measurement_on:
        # Stop measurement
        measurement_on = False

        for _ in range(10):
            led.value = True
            time.sleep(0.1)
            led.value = False
            time.sleep(0.1)

        led.value = False
        time.sleep(5)  # Add a small delay to avoid accidental double-clicks# Write your code here :-)
        print("End of meassurement")
