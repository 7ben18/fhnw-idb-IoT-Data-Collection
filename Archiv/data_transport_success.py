import board
import busio
import digitalio
import time
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_socket
import adafruit_requests

# dht
import time
import adafruit_dht
import board

# TODO: Set your Wi-Fi ssid, password
WIFI_SSID = "Ben's Hotspot"
WIFI_PASSWORD = "Trebolsan4201+"

# ThingSpeak settings
TS_WRITE_API_KEY = "KRG0E2AZQI30SBBO"
TS_HTTP_SERVER = "api.thingspeak.com"

# FeatherWing ESP32 AirLift, nRF52840
cs = digitalio.DigitalInOut(board.D13)
rdy = digitalio.DigitalInOut(board.D11)
rst = digitalio.DigitalInOut(board.D12)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, cs, rdy, rst)

while not esp.is_connected:
    print("\nConnecting to Wi-Fi...")
    try:
        esp.connect_AP(WIFI_SSID, WIFI_PASSWORD)
    except ConnectionError as e:
        print("Cannot connect to Wi-Fi", e)
        continue

print("Wi-Fi connected to", str(esp.ssid, "utf-8"))
print("IP address", esp.pretty_ip(esp.ip_address))


# Initialize HTTP POST client
adafruit_requests.set_socket(adafruit_esp32spi_socket, esp)

# Constants
INTERVAL = 30 # need to change time to 30 or 45....

# Setup
dht = adafruit_dht.DHT11(board.A4)  # nRF52840, Grove D4

# Setup server url
post_url = "https://" + TS_HTTP_SERVER + "/update"

# Main Loop
while True:
    start = time.time()
    t = time.localtime(start)
    try:
        # Read the temperature and convert it to integer
        temperature = int(round(dht.temperature))
        # Read the humidity and convert it to integer
        humidity = int(round(dht.humidity))

        # Print timestamp, temperatur, humidity
        print("{:d}:{:02d}:{:02d},{:g},{:g}".format(
            t.tm_hour, t.tm_min, t.tm_sec, temperature, humidity))

        print("print succes")

        payload = "api_key=" + TS_WRITE_API_KEY + "&field1=" + \
            str(temperature) + "&field2=" + str(humidity)

        # Send a single message
        print(payload)
        response = adafruit_requests.post(post_url, data=payload)

        # Print the http status code; should be 200
        print(response.status_code)

        response.close()

    except RuntimeError as e:
        # Reading doesn't always work! Just print error and we'll try again
        print("{:d}:{:02d}:{:02d},{:g},{:g}".format(
            t.tm_hour, t.tm_min, t.tm_sec, -1, -1))

    end = time.time()
    # Wait for the remaining time
    time.sleep(INTERVAL - (end - start))

