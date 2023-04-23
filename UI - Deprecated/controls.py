import pyfirmata
from pyfirmata import Arduino, util
import states
import math
import time

#declare pins
MODE_SEL_PIN = 7
MACRO_SEL_PIN = 8

BRIGHT_CTRL_PIN = 0 #analog
SPEED_CTRL_PIN = 1 #analog

SCHEME_SEL_PIN = 4
SCHEME_EDIT_PIN = 2

R_PIN_1 = 9
R_PIN_2 = 10
G_PIN_1 = 11
G_PIN_2 = 12
B_PIN_1 = 5
B_PIN_2 = 6

SCHEME_EDIT_LED_PIN = 20

board = Arduino('COM3')

MODE_SEL = board.digital[MODE_SEL_PIN]
MACRO_SEL = board.digital[MACRO_SEL_PIN]
BRIGHT_CTRL = board.analog[BRIGHT_CTRL_PIN]
SPEED_CTRL = board.analog[SPEED_CTRL_PIN]
SCHEME_SEL = board.digital[SCHEME_SEL_PIN]
SCHEME_EDIT = board.digital[SCHEME_EDIT_PIN]
r_dt = board.digital[R_PIN_1]
r_clk = board.digital[R_PIN_2]
g_dt = board.digital[G_PIN_1]
g_clk = board.digital[G_PIN_2]
b_dt = board.digital[B_PIN_1]
b_clk = board.digital[B_PIN_2]

MODE_SEL.mode = pyfirmata.INPUT
MACRO_SEL.mode = pyfirmata.INPUT
BRIGHT_CTRL.mode = pyfirmata.INPUT
SPEED_CTRL.mode = pyfirmata.INPUT
SCHEME_SEL.mode = pyfirmata.INPUT
SCHEME_EDIT.mode = pyfirmata.INPUT
r_dt.mode = pyfirmata.INPUT
r_clk.mode = pyfirmata.INPUT
g_dt.mode = pyfirmata.INPUT
g_clk.mode = pyfirmata.INPUT
b_dt.mode = pyfirmata.INPUT
b_clk.mode = pyfirmata.INPUT

iterator = util.Iterator(board)
iterator.start()
time.sleep(3)

class EncMode:
    STATE_LOCKED = 0
    STATE_TURN_RIGHT_START = 1
    STATE_TURN_RIGHT_MIDDLE = 2
    STATE_TURN_RIGHT_END = 3
    STATE_TURN_LEFT_START = 4
    STATE_TURN_LEFT_MIDDLE = 5
    STATE_TURN_LEFT_END = 6
    STATE_UNDECIDED = 7

#Class object to represent the set of controls on this device
class Controls():

    """Constructor"""
    def __init__(self, device):

        self.device = device
        self.macro_pb_prev_state = 0
        self.scheme_sel_pb_prev_state = 0
        self.scheme_edit_pb_prev_state = 0
    

    def check_macro_sel_pb(self):
        # Get button current state
        button_state = MACRO_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.macro_pb_prev_state != None) and (button_state != self.macro_pb_prev_state)):
            
            if button_state == 0:
                
                print("Button released")
                self.macro_pb_prev_state = button_state
                return True
            
        self.macro_pb_prev_state = button_state
        return False

    def check_mode_switch(self):
        #print("Checking mode switch")

        #Read in the MODE_SEL Switch value
        val = MODE_SEL.read()

        #print("MODE_SEL Switch reads as " + str(val))

        try:
            return int(val) #Will eventually return 1 for manual and 1 for automatic

        except:
            print("invalid input...returning 0")
            return 1

    def check_bright_ctrl(self):
        BRIGHT_CTRL.enable_reporting()
        val = BRIGHT_CTRL.read()

        if(val == None):
            return 0

        val = val*5

        if(val == 0):
            val = 1

        val = math.ceil(val)
        
        return val

    def check_speed_ctrl(self):
        SPEED_CTRL.enable_reporting()
        val = SPEED_CTRL.read()

        if(val == None):
            return 0

        val = val*10

        if(val == 0):
            val = 1

        val = math.ceil(val)

        return val

    def check_scheme_sel_pb(self):
        # Get button current state
        button_state = SCHEME_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.scheme_sel_pb_prev_state != None) and (button_state != self.scheme_sel_pb_prev_state)):
            
            if button_state == 0:
                
                self.scheme_sel_pb_prev_state = button_state
                return True
            
        self.scheme_sel_pb_prev_state = button_state
        return False

    def check_edit_mode_pb(self):
        # Get button current state
        button_state = SCHEME_EDIT.read()
        
        # Check if button has been released
        if((button_state != None) and (self.scheme_edit_pb_prev_state != None) and (button_state != self.scheme_edit_pb_prev_state)):
            
            if button_state == 0:
                
                self.scheme_edit_pb_prev_state = button_state
                return True
            
        self.scheme_edit_pb_prev_state = button_state
        return False

    def led_on(self,pin_num):
        print("Turning LED " + str(pin_num) + " on.")

    def led_off(self,pin_num):
        print("Turning LED " + str(pin_num) + " off.")

class RotaryEnc(Controls):
    def __init__(self,a_ctrl,b_ctrl):
        self.ctrl_1 = a_ctrl
        self.ctrl_2 = b_ctrl
        self.state = EncMode.STATE_LOCKED
        self.val = 0

    """def rgb_checks(self):
        print("Initializing")
        r_ctrl = RotaryEnc(r_dt,r_clk)
        g_ctrl = RotaryEnc(g_dt,g_clk)
        b_ctrl = RotaryEnc(b_dt,b_clk)

        while True:
            r_ctrl.check_val()
            g_ctrl.check_val()
            b_ctrl.check_val()"""
    
    def check_state(self):
        a = not self.ctrl_1.read()
        #print("a = " + str(a))
        b = not self.ctrl_2.read()
        #print("b = " + str(b))
        
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
        #print("Delta is: " + str(delta))
        #time.sleep(0.01)
        if (delta == -1):
            print("delta is -1")
            print("<-- ")
            if(self.val > 0):
                self.val -= 5
        elif (delta == 1):
            print("delta is 1")
            print(" -->")
            if(self.val < 50):
                self.val += 5
        if((delta == 1) or (delta == -1)):
            print(str(self.val))

