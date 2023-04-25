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

NEXT_COLOR_PIN = 3
CHANGE_COLOR_PIN = 9

SCHEME_EDIT_LED_PIN = 13

board = Arduino('COM3')

MODE_SEL = board.digital[MODE_SEL_PIN]
MACRO_SEL = board.digital[MACRO_SEL_PIN]
BRIGHT_CTRL = board.analog[BRIGHT_CTRL_PIN]
SPEED_CTRL = board.analog[SPEED_CTRL_PIN]
SCHEME_SEL = board.digital[SCHEME_SEL_PIN]
SCHEME_EDIT = board.digital[SCHEME_EDIT_PIN]
NEXT_COLOR_SEL = board.digital[NEXT_COLOR_PIN]
CHANGE_COLOR_SEL = board.digital[CHANGE_COLOR_PIN]


MODE_SEL.mode = pyfirmata.INPUT
MACRO_SEL.mode = pyfirmata.INPUT
BRIGHT_CTRL.mode = pyfirmata.INPUT
SPEED_CTRL.mode = pyfirmata.INPUT
SCHEME_SEL.mode = pyfirmata.INPUT
SCHEME_EDIT.mode = pyfirmata.INPUT
NEXT_COLOR_SEL.mode = pyfirmata.INPUT
CHANGE_COLOR_SEL.mode = pyfirmata.INPUT

iterator = util.Iterator(board)
iterator.start()
time.sleep(3)

#Class object to represent the set of controls on this device
class Controls():

    """Constructor"""
    def __init__(self, device):

        self.device = device
        self.macro_pb_prev_state = 0
        self.scheme_sel_pb_prev_state = 0
        self.scheme_edit_pb_prev_state = 0
        self.next_color_pb_prev_state = 0
        self.change_color_pb_prev_state = 0
    

    def check_macro_sel_pb(self):
        # Get button current state
        button_state = MACRO_SEL.read()
        time.sleep(0.01)
        
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
        time.sleep(0.01)

        #print("MODE_SEL Switch reads as " + str(val))

        try:
            return int(val) #Will eventually return 1 for manual and 1 for automatic

        except:
            print("invalid input...returning 0")
            return 1

    def check_bright_ctrl(self):
        BRIGHT_CTRL.enable_reporting()
        print("Reading brightness")
        val = BRIGHT_CTRL.read()
        time.sleep(0.01)

        if(val == None):
            return 0

        val = val*5

        if(val == 0):
            val = 1

        val = math.ceil(val)
        
        return val

    def check_speed_ctrl(self):
        SPEED_CTRL.enable_reporting()
        print("Reading speed")
        val = SPEED_CTRL.read()
        time.sleep(0.01)

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

    def check_next_color_pb(self):
        # Get button current state
        button_state = NEXT_COLOR_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.next_color_pb_prev_state != None) and (button_state != self.next_color_pb_prev_state)):
            
            if button_state == 0:
                
                self.next_color_pb_prev_state = button_state
                return True
            
        self.next_color_pb_prev_state = button_state
        return False

    def check_change_color_pb(self):
        # Get button current state
        button_state = CHANGE_COLOR_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.change_color_pb_prev_state != None) and (button_state != self.change_color_pb_prev_state)):
            
            if button_state == 0:
                
                self.change_color_pb_prev_state = button_state
                return True
            
        self.change_color_pb_prev_state = button_state
        return False

    def led_on(self,pin_num):
        print("Turning LED " + str(pin_num) + " on.")

    def led_off(self,pin_num):
        print("Turning LED " + str(pin_num) + " off.")


