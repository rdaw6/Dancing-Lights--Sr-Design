from pyfirmata import Arduino, util
import time

board = Arduino('COM3')

pin = board.get_pin('a:0:i')            #analog pin 0 input

iterator = util.Iterator(board)
iterator.start()
time.sleep(0.1)

try:
    while True:

        val = pin.read()

        if(val == None):
            continue

        val = val*10

        if(val == 0):
            val = 1

        val = ceil(val)
        
        print(str(val))

        time.sleep(0.1)

except KeyboardInterrupt:
    board.exit()