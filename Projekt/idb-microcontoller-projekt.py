# Libraries
import board
import digitalio
import time
import adafruit_dht
import analogio

# LED library
from ChainableLED import ChainableLED

from lib import tm1637lib
# Librarie random for display
import random

# Libraries for data transport
import busio
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_socket
import adafruit_requests

# --------------------------------------------------------------------------

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

# FeatherWing ESP32 AirLift, nRF52840
cs = digitalio.DigitalInOut(board.D13)
rdy = digitalio.DigitalInOut(board.D11)
rst = digitalio.DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, rdy, rst)

# TODO: Set your Wi-Fi ssid, password
WIFI_SSID = "LeaLan" #"LeaLan"
WIFI_PASSWORD = "AllesPoebel" #"AllesPoebel"

# ThingSpeak settings
TS_WRITE_API_KEY = "HJWGPNGYS1DS5609"
TS_HTTP_SERVER = "api.thingspeak.com"

# while loop for wlan connection
while not esp.is_connected:
    print("\nConnecting to Wi-Fi...")
    try:
        esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
        rgb_led.setColorRGB(0, 0, 0, 225)
    except ConnectionError as e:
        print("Cannot connect to Wi-Fi", e)
        rgb_led.setColorRGB(0, 255, 165, 0)
        continue

# print connection status
print("Wi-Fi connected to", str(esp.ssid, "utf-8"))
print("IP address", esp.pretty_ip(esp.ip_address))

# Initialize HTTP POST client
adafruit_requests.set_socket(adafruit_esp32spi_socket, esp)

# print microcontroller status
print("Successfull connected, press button to start meassure")

# Setup server url to ThingSpeak
post_url = "https://" + TS_HTTP_SERVER + "/update"

# --------------------------------------------------------------------

# Constants for meassurement
dht_INTERVAL = 10

# Variable for Measurement start
measurement_on = False

# Main loop
while True:

    # check if button is pressed once
    if sensor_button.value == True and not measurement_on:
        # start measurment
        measurement_on = True

        while measurement_on:
            # Take a measurement
            start = time.time()
            t = time.localtime(start)

            # Read the temperature and convert it to integer
            temperature = int(round(dht.temperature))

            # Read the humidity and convert it to integer
            humidity = int(round(dht.humidity))

            # Read the light_value and voltage and convert it to integer
            light_value = sensor_light.value
            voltage = round((light_value * 3.3) / 65536)

            # create a  list of measurement
            measures = [str(temperature) + " C", str(humidity) + " H", str(light_value // 100) + "L", " " + str(voltage // 1) + "V"]

            # select random measurement
            value = random.choice(measures)

            # display them on hardware
            display.show(value)

            # Print timestamp, temperatur, humidity
            output = ("|Timestamp {:d}:{:02d}:{:02d} | Temperature {:g} | Humidity {:g} | Light_value {:g} | Voltage {:g} |".format(t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity, light_value, voltage))

            print(output)

            try:
                # Create payload
                payload = "api_key=" + TS_WRITE_API_KEY + \
                    "&field1=" + str(temperature) +\
                    "&field2=" + str(humidity) +\
                    "&field3=" + str(light_value) + \
                    "&field4=" + str(voltage)

                # Send a single message
                response = adafruit_requests.post(post_url, data=payload)

                # Print the http status code; should be 200
                print("Data succesfully transported to ThingSpeak, response status: " + str(response.status_code))
                #print("Successfull data transport to thingspeak! Status")

                response.close()

            except RuntimeError as e:
                # Reading doesn't always work! Just print error and we'll try again
                print("|Timestamp {:d}:{:02d}:{:02d} | Temperature {:g} | Humidity {:g} | Light_value {:g} | Voltage {:g} |"
                .format(t.tm_hour, t.tm_min, t.tm_sec, -1, -1, -1, -1))

            end = time.time()
            # Wait for the remaining time
            time.sleep(dht_INTERVAL - (end - start))


# --------------------------------------------------------------------------
