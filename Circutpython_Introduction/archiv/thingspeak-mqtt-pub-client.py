import board
import busio
import digitalio
import time
from lib import adafruit_esp32spi as adafruit_esp32spi
from lib import adafruit_esp32spi as adafruit_esp32spi_socket
from lib import adafruit_minimqtt as adafruit_minimqtt

# TODO: Set your Wi-Fi ssid, password
WIFI_SSID = "Ben's Hotspot" # "MY_SSID"
WIFI_PASSWORD = "Trebolsan4201+" # "MY_PASSWORD"

# ThingSpeak settings
TS_CHANNEL_ID = "2049970" #"MY_CHANNEL_ID"
TS_WRITE_API_KEY = "HJWGPNGYS1DS5609" # "MY_WRITE_API_KEY" # https://api.thingspeak.com/update?api_key=HJWGPNGYS1DS5609&field1=0
TS_MQTT_BROKER = "mqtt.thingspeak.com"

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
    except RuntimeError as e:
        print("Cannot connect to Wi-Fi", e)
        continue

print("Wi-Fi connected to", str(esp.ssid, "utf-8"))
print("IP address", esp.pretty_ip(esp.ip_address))


def handle_connect(client, userdata, flags, rc):
    print("Connected to {0}".format(client.broker))


def handle_publish(client, userdata, topic, pid):
    print("Published to {0} with PID {1}".format(topic, pid))


adafruit_minimqtt.set_socket(adafruit_esp32spi_socket, esp)

mqtt_client = adafruit_minimqtt.MQTT(broker=TS_MQTT_BROKER, is_ssl=False)

# Set callback handlers
mqtt_client.on_connect = handle_connect
mqtt_client.on_publish = handle_publish

try:
    # Connect to ThingSpeak
    print("Connecting to {0}".format(TS_MQTT_BROKER))
    mqtt_client.connect()

    # Some test data
    humidity = 55
    temperature = 25

    # Setup topic (see https://ch.mathworks.com/help/thingspeak/publishtoachannelfeed.html)
    topic = "channels/" + TS_CHANNEL_ID + "/publish/" + TS_WRITE_API_KEY
    # Create payload
    payload = "field1="+str(temperature)+"&field2="+str(humidity)

    # Publish a single message
    mqtt_client.publish(topic, payload)

    # Give some seconds to publish before exiting
    time.sleep(5)

except MQTT.MMQTTException as error:
    print(error)
