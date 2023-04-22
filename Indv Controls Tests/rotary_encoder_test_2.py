import pyfirmata
from pyfirmata import Arduino, util
import time
import math

ENCODER_A_PIN = 9;
ENCODER_B_PIN = 10;

board = Arduino('COM3')

dt_pin = board.digital[ENCODER_A_PIN]
clk_pin = board.digital[ENCODER_B_PIN]

dt_pin.mode = pyfirmata.INPUT
clk_pin.mode = pyfirmata.INPUT

iterator = util.Iterator(board)
iterator.start()
time.sleep(0.1)

count = 0

def loop():
    global count
    
    state = rotaryEncoder()

    print(state)
    
    if (state == -1):
        print("<-- ")
        if(count > 0):
            count -= 1
    if (state == 1):
        print(" -->")
        if(count < 51):
            count += 1

class EncMode:
    STATE_LOCKED = 0
    STATE_TURN_RIGHT_START = 1
    STATE_TURN_RIGHT_MIDDLE = 2
    STATE_TURN_RIGHT_END = 3
    STATE_TURN_LEFT_START = 4
    STATE_TURN_LEFT_MIDDLE = 5
    STATE_TURN_LEFT_END = 6
    STATE_UNDECIDED = 7

def rotaryEncoder():
    #enumerate(STATE_LOCKED, STATE_TURN_RIGHT_START, STATE_TURN_RIGHT_MIDDLE, STATE_TURN_RIGHT_END, STATE_TURN_LEFT_START, STATE_TURN_LEFT_MIDDLE, STATE_TURN_LEFT_END, STATE_UNDECIDED)
    encoderState = EncMode.STATE_LOCKED;

    delta = 0
    while(delta == 0):
        #print("State: " + str(encoderState))

        a = not dt_pin.read()
        b = not clk_pin.read()
        
        match encoderState:
            case EncMode.STATE_LOCKED:
                if (a and b):
                    encoderState = EncMode.STATE_UNDECIDED
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_RIGHT_START
                else:
                    encoderState = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_RIGHT_START:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_RIGHT_START
                else:
                    encoderState = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_RIGHT_MIDDLE:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_RIGHT_START
                else:
                    encoderState = EncMode.STATE_LOCKED
                    delta = -1
            case EncMode.STATE_TURN_RIGHT_END:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_RIGHT_START
                else:
                    encoderState = EncMode.STATE_LOCKED
                    delta = -1
            case EncMode.STATE_TURN_LEFT_START:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_LEFT_END
                else:
                    encoderState = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_LEFT_MIDDLE:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_LEFT_END
                else:
                    encoderState = EncMode.STATE_LOCKED
                    delta = 1
            case EncMode.STATE_TURN_LEFT_END:
                if (a and b):
                    encoderState = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_LEFT_END
                else:
                    encoderState = EncMode.STATE_LOCKED
                    delta = 1
            case EncMode.STATE_UNDECIDED:
                if (a and b):
                    encoderState = EncMode.STATE_UNDECIDED;
                
                elif ((not a) and b):
                    encoderState = EncMode.STATE_TURN_RIGHT_END
                
                elif (a and not b):
                    encoderState = EncMode.STATE_TURN_LEFT_END
                
                else:
                    encoderState = EncMode.STATE_LOCKED

    return delta

if __name__ == '__main__':
    count
    print("Initializing")
    while True:
        loop()
        print(count)
