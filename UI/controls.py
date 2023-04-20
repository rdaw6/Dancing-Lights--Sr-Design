import pyfirmata
from pyfirmata import Arduino, util
import states
import math

#declare pins
MODE_SEL_PIN = 7
MACRO_SEL_PIN = 8
#BRIGHT_CTRL_PIN = 11
#SPEED_CTRL_PIN = 12
SCHEME_SEL_PIN = 4
SCHEME_EDIT_PIN = 5

SCHEME_EDIT_LED_PIN = 20

board = Arduino('COM3')

MODE_SEL = board.digital[MODE_SEL_PIN]
MACRO_SEL = board.digital[MACRO_SEL_PIN]
#BRIGHT_CTRL = board.digital[BRIGHT_CTRL_PIN]
BRIGHT_CTRL = board.get_pin('a:0:i')
#SPEED_CTRL = board.digital[SPEED_CTRL_PIN]
SPEED_CTRL = board.get_pin('a:1:i')
SCHEME_SEL = board.digital[SCHEME_SEL_PIN]
SCHEME_EDIT = board.digital[SCHEME_EDIT_PIN]

MODE_SEL.mode = pyfirmata.INPUT
MACRO_SEL.mode = pyfirmata.INPUT
BRIGHT_CTRL.mode = pyfirmata.INPUT
SPEED_CTRL.mode = pyfirmata.INPUT
SCHEME_SEL.mode = pyfirmata.INPUT
SCHEME_EDIT.mode = pyfirmata.INPUT

iterator = util.Iterator(board)
iterator.start() 

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
        print("Checking mode switch")

        #Read in the MODE_SEL Switch value
        val = MODE_SEL.read()

        print("MODE_SEL Switch reads as " + str(val))

        try:
            return int(val) #Will eventually return 1 for manual and 1 for automatic

        except:
            print("invalid input...returning 0")
            return 1

    def check_bright_ctrl(self):
        val = BRIGHT_CTRL.read()

        if(val == None):
            return 0

        val = val*5

        if(val == 0):
            val = 1

        val = math.ceil(val)
        
        return val

    def check_speed_ctrl(self):
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
                
                print("Button released")
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
                
                print("Button released")
                self.scheme_edit_pb_prev_state = button_state
                return True
            
        self.scheme_edit_pb_prev_state = button_state
        return False

    def led_on(self,pin_num):
        print("Turning LED " + str(pin_num) + " on.")

    def led_off(self,pin_num):
        print("Turning LED " + str(pin_num) + " off.")

