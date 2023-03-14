import random
import time
import board
import neopixel

# Setup the neopixel string
pixels = neopixel.NeoPixel(board.D18, 300)

# Fire loop
while True:
    for i in range(300):
        flicker = random.randint(0, 20)
        r = min(255, max(0, 255 - flicker * 10))
        g = min(150, max(0, 100 - flicker * 5))
        b = min(50, max(0, 50 - flicker * 2))
        pixels[i] = (r, g, b)
    pixels.show()
    time.sleep(0.01)