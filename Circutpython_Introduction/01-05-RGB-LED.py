# Based on https://github.com/DexterInd/GrovePi/tree/master/Software/Python/grove_chainable_rgb_led licensed under MIT License

import board
import digitalio
import time
from ChainableLED import ChainableLED

CLK_PIN = board.D5 # nRF5840 D5, Grove D2
DATA_PIN = board.D6
NUMBER_OF_LEDS = 1

if __name__ == "__main__":
    rgb_led = ChainableLED(CLK_PIN, DATA_PIN, NUMBER_OF_LEDS)

    while True:
        # The first parameter: NUMBER_OF_LEDS - 1; Other parameters: the RGB values.
        rgb_led.setColorRGB(0, 255, 0, 0) # Rot
        time.sleep(2)
        rgb_led.setColorRGB(0, 0, 255, 0) # Gruen
        time.sleep(1)
        rgb_led.setColorRGB(0, 0, 0, 255) # Blau
        time.sleep(1)
