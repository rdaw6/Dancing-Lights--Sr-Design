import time
import board
import neopixel

# Setup the neopixel string
pixels = neopixel.NeoPixel(board.D18, 300)

# Rainbow loop
while True:
    for i in range(300):
        pixel_index = (i * 256 // 300) + 1
        pixels[i] = (255, 0, 0) if pixel_index < 85 else \
                    (255 - (pixel_index - 85), pixel_index - 85, 0) if pixel_index < 170 else \
                    (0, 255 - (pixel_index - 170), pixel_index - 170)
        pixels.show()
        time.sleep(0.01)