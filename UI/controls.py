#Author: Emma Klinzing
#Class: ECE Capstone Design
#   Team: SD23P04: Dancing Lights
#Last Modified: 04/25/2023

#This file manages reading and writing to the various controls on the physical device
#   It returns the relevant values to the device object documented in states.py

import pyfirmata
from pyfirmata import Arduino, util
import states
import math
import time

#declare pins - See design notebook for a pin diagram and more detail
MODE_SEL_PIN = 7
MACRO_SEL_PIN = 8

BRIGHT_CTRL_PIN = 0 #analog
SPEED_CTRL_PIN = 1 #analog

SCHEME_SEL_PIN = 4
SCHEME_EDIT_PIN = 2

NEXT_COLOR_PIN = 9
CHANGE_COLOR_PIN = 3

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

SCHEME_EDIT_LED = board.digital[SCHEME_EDIT_LED_PIN]


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

        #Set the initial state of all the PBs to zero 
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
        
        # Check if button has been released (& Ensure we're not reading/comparing to a None value which is common during startup)
        if((button_state != None) and (self.macro_pb_prev_state != None) and (button_state != self.macro_pb_prev_state)):
            
            if button_state == 0:
                #The button has been released
                print("Button released")

                #Set the previous state of the pb to be 0
                self.macro_pb_prev_state = button_state

                #Return true to notofy of button release
                return True

        #set previous state of button to match this read  
        self.macro_pb_prev_state = button_state

        #Return false to notify NO button release has occurred
        return False

    #Function to check the state of the MODE_SEL switch
    def check_mode_switch(self):

        #Read in the MODE_SEL Switch value
        val = MODE_SEL.read()
        time.sleep(0.01)

        #Try to return the value of the switch 
        try:
            #Return the value of the switch 
            return int(val)

        except:
            #Input was not an integer so default to manual mode by returning 1
            print("invalid input...returning 1")
            return 1

    #Check the BRIGHT_CTRL potentiometer
    def check_bright_ctrl(self):

        #Enable reporting for this analog control
        BRIGHT_CTRL.enable_reporting()
        print("Reading brightness")

        #Read the potentiometer value
        val = BRIGHT_CTRL.read()

        #Sleep after reading value
        time.sleep(0.01)

        if(val == None):
            #System booting or there's an error so return 0
            #   The device will handle this by retaining its previous value for the control (See states.py)
            return 0

        #The value will be a decimal between 0 and 1 -> we need a value between 1 and 5
        #Multiply by 5 to scale the value to our needed range
        val = val*5

        #If the value is zero, the knob is in the lowest position, so scale this to 1 (the lowest brightness)
        if(val == 0):
            val = 1

        #Otherwise, take the ceiling of the value (should be between 0 and 5) to get an integer value for brightness
        val = math.ceil(val)

        #Return the brightness value [1,5]
        return val

    #Check SPEED_CTRL potentiometer
    def check_speed_ctrl(self):

        #Enable reporting since it's an analog control
        SPEED_CTRL.enable_reporting()
        print("Reading speed")

        #Read the Speed value 
        val = SPEED_CTRL.read()
        time.sleep(0.01)

        #System booting or there's an error so return 0
        #   The device will handle this by retaining its previous value for the control (See states.py)
        if(val == None):
            return 0

        #The value will be a decimal between 0 and 1 -> we need a value between 1 and 10
        #Multiply by 10 to scale the value to our needed range
        val = val*10

        #If the value is zero, the knob is in the lowest position, so scale this to 1 (the lowest speed)
        if(val == 0):
            val = 1

        #Otherwise, take the ceiling of the value (should be between 0 and 10) to get an integer value for speed
        val = math.ceil(val)

        #Return the brightness value [1,10]
        return val

    #Check the SCHEME_SEL PB (Determines which scheme num we're on)
    def check_scheme_sel_pb(self):
        
        # Get button current state
        button_state = SCHEME_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.scheme_sel_pb_prev_state != None) and (button_state != self.scheme_sel_pb_prev_state)):
            #Button is in dufferent state than last read
            
            if button_state == 0:
                #Button is in released state

                #Set previous state of PB equal to current state (unpressed)
                self.scheme_sel_pb_prev_state = button_state

                #Return true bc the pb was just released
                return True

        #Set previous state of PB to be equal to current state
        self.scheme_sel_pb_prev_state = button_state

        #Return false bc pb was not just released
        return False

    def check_edit_mode_pb(self):
        # Get button current state
        button_state = SCHEME_EDIT.read()
        
        # Check if button has been released
        if((button_state != None) and (self.scheme_edit_pb_prev_state != None) and (button_state != self.scheme_edit_pb_prev_state)):
            
            if button_state == 0:
                #Button is in released state

                #Set prev state of pb equal to current state (unpressed)
                self.scheme_edit_pb_prev_state = button_state

                #Return true bc the pb was just released 
                return True

        #Set previous state of PB to be equal to current state
        self.scheme_edit_pb_prev_state = button_state

        #Return false bc pb was not just released
        return False


    def check_change_color_pb(self):
        # Get button current state
        button_state = CHANGE_COLOR_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.change_color_pb_prev_state != None) and (button_state != self.change_color_pb_prev_state)):
            
            if button_state == 0:
                #Button is in released state

                #Set prev state of pb equal to current state (unpressed)
                self.change_color_pb_prev_state = button_state

                #Return true bc the pb was just released
                return True

        #Set previous state of PB to be equal to current state
        self.change_color_pb_prev_state = button_state

        #Return false bc pb was not just released
        return False

    def check_next_color_pb(self):
        # Get button current state
        button_state = NEXT_COLOR_SEL.read()
        
        # Check if button has been released
        if((button_state != None) and (self.next_color_pb_prev_state != None) and (button_state != self.next_color_pb_prev_state)):
            
            if button_state == 0:
                #Button is in released state

                #Set prev state of pb equal to current state (unpressed)
                self.next_color_pb_prev_state = button_state

                #Return true bc the pb was just released
                return True

        #Set previous state of PB to be equal to current state
        self.next_color_pb_prev_state = button_state

        #Return false bc pb was not just released
        return False

    def led_on(self):
        #Turn SCHEME_EDIT_LED on by sending high signal
        SCHEME_EDIT_LED.write(1)

    def led_off(self,pin_num):
        #Tur SCHEME_EDIT_LED off by sending low signal
        SCHEME_EDIT_LED.write(0)


