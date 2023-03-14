import random
import time
import board
import neopixel

# Setup the neopixel string
pixels = neopixel.NeoPixel(board.D18, 300)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
# Twinkle loop
while True:
    pixels_to_light = random.randint(125, 175)
    pixels_on = random.sample(range(300), pixels_to_light)
    for i in range(300):
        if i in pixels_on:
            pixels[i] = RED
        else:
            pixels[i] = GREEN
    pixels.show()
    time.sleep(0.5)
