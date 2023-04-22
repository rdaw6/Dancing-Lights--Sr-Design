#Loosely based on code found at
#   https://forum.arduino.cc/t/using-a-rotary-encoder-simple-tutorial/252331/4
# in comment by StefanL38

import pyfirmata
from pyfirmata import Arduino, util
import time
import math

R_PIN_1 = 9
R_PIN_2 = 10
G_PIN_1 = 11
G_PIN_2 = 12
B_PIN_1 = 5
B_PIN_2 = 6

board = Arduino('COM3')

r_dt = board.digital[R_PIN_1]
r_clk = board.digital[R_PIN_2]
g_dt = board.digital[G_PIN_1]
g_clk = board.digital[G_PIN_2]
b_dt = board.digital[B_PIN_1]
b_clk = board.digital[B_PIN_2]

r_dt.mode = pyfirmata.INPUT
r_clk.mode = pyfirmata.INPUT
g_dt.mode = pyfirmata.INPUT
g_clk.mode = pyfirmata.INPUT
b_dt.mode = pyfirmata.INPUT
b_clk.mode = pyfirmata.INPUT

iterator = util.Iterator(board)
iterator.start()
time.sleep(0.1)

"""r_val = 0
g_val = 0
b_val = 0

r_state = 0
g_state = 0
b_state = 0"""
    

class EncMode:
    STATE_LOCKED = 0
    STATE_TURN_RIGHT_START = 1
    STATE_TURN_RIGHT_MIDDLE = 2
    STATE_TURN_RIGHT_END = 3
    STATE_TURN_LEFT_START = 4
    STATE_TURN_LEFT_MIDDLE = 5
    STATE_TURN_LEFT_END = 6
    STATE_UNDECIDED = 7

class RotaryEnc:
    def __init__(self,a_ctrl,b_ctrl):
        self.a_ctrl = a_ctrl
        self.b_ctrl = b_ctrl
        self.state = EncMode.STATE_LOCKED
        self.val = 0
    
    def check_state(self):
        a = not self.a_ctrl.read()
        b = not self.b_ctrl.read()
        
        delta = 0
        
        match self.state:
            case EncMode.STATE_LOCKED:
                if (a and b):
                    self.state = EncMode.STATE_UNDECIDED
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_RIGHT_START
                else:
                    self.state = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_RIGHT_START:
                if (a and b):
                    self.state = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_RIGHT_START
                else:
                    self.state = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_RIGHT_MIDDLE:
                if (a and b):
                    self.state = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_RIGHT_START
                else:
                    self.state = EncMode.STATE_LOCKED
                    delta = -1
            case EncMode.STATE_TURN_RIGHT_END:
                if (a and b):
                    self.state = EncMode.STATE_TURN_RIGHT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_RIGHT_END
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_RIGHT_START
                else:
                    self.state = EncMode.STATE_LOCKED
                    delta = -1
            case EncMode.STATE_TURN_LEFT_START:
                if (a and b):
                    self.state = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_LEFT_END
                else:
                    self.state = EncMode.STATE_LOCKED
            case EncMode.STATE_TURN_LEFT_MIDDLE:
                if (a and b):
                    self.state = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_LEFT_END
                else:
                    self.state = EncMode.STATE_LOCKED
                    delta = 1
            case EncMode.STATE_TURN_LEFT_END:
                if (a and b):
                    self.state = EncMode.STATE_TURN_LEFT_MIDDLE
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_LEFT_START
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_LEFT_END
                else:
                    self.state = EncMode.STATE_LOCKED
                    delta = 1
            case EncMode.STATE_UNDECIDED:
                if (a and b):
                    self.state = EncMode.STATE_UNDECIDED;
                
                elif ((not a) and b):
                    self.state = EncMode.STATE_TURN_RIGHT_END
                
                elif (a and not b):
                    self.state = EncMode.STATE_TURN_LEFT_END
                
                else:
                    self.state = EncMode.STATE_LOCKED

        return delta

    def check_val(self):
        delta = self.check_state()
        if (delta == -1):
            print("<-- ")
            if(self.val > 0):
                self.val -= 5
        elif (delta == 1):
            print(" -->")
            if(self.val < 50):
                self.val += 5
        if((delta == 1) or (delta == -1)):
            print(str(self.val))

if __name__ == '__main__':

    print("Initializing")
    r_ctrl = RotaryEnc(r_dt,r_clk)
    g_ctrl = RotaryEnc(g_dt,g_clk)
    b_ctrl = RotaryEnc(b_dt,b_clk)
    
    while True:
        r_ctrl.check_val()
        g_ctrl.check_val()
        b_ctrl.check_val()

        #print("(" + str(r_ctrl.val) + "," + str(g_ctrl.val) + "," + str(b_ctrl.val) + ")")

