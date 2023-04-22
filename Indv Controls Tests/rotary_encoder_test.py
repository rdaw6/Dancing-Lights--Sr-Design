import pyfirmata
from pyfirmata import Arduino, util
import time
import math

board = Arduino('COM3')

dt_pin = board.digital[9]
clk_pin = board.digital[10]

dt_pin.mode = pyfirmata.INPUT
clk_pin.mode = pyfirmata.INPUT

prev_clk_state = clk_pin.read()

counter = 0

iterator = util.Iterator(board)
iterator.start()
time.sleep(0.1)


try:
    
    print("starting")
    while True:
        curr_clk_state = clk_pin.read()

        if((curr_clk_state != prev_clk_state) and (curr_clk_state == 1)):
            print("Turning")
            curr_state_dt = dt_pin.read()
            if(curr_state_dt != curr_clk_state):
                #roatating CW so increment
                if(counter < 51):
                    counter += 1
            else:
                #rotating CCW so decrement
                if(counter > 0):
                    counter -= 1
            print(str(counter))
        prev_clk_state = curr_clk_state
                
        

except KeyboardInterrupt:
    board.exit()
