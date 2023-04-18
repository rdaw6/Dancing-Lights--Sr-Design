import pyfirmata
import states

#declare pins
MODE_SEL_PIN = 7
MACRO_SEL_PIN = 8
BRIGHT_CTRL_PIN = 11
SPEED_CTRL_PIN = 12
SCHEME_SEL_PIN = 4

SCHEME_EDIT_LED_PIN = 20

"""
board = Arduino('COM3')

MODE_SEL = board.digital[MODE_SEL_PIN]
MACRO_SEL = board.digital[MACRO_SEL_PIN]
BRIGHT_CTRL = board.digital[BRIGHT_CTRL_PIN]
SPEED_CTRL = board.digital[SPEED_CTRL_PIN]
SCHEME_SEL = board.digital[SCHEME_SEL_PIN]

MODE_SEL.mode = pyfirmata.INPUT
MACRO_SEL.mode = pyfirmata.INPUT
BRIGHT_CTRL.mode = pyfirmata.INPUT
SPEED_CTRL.mode = pyfirmata.INPUT
SCHEME_SEL.mode = pyfirmata.INPUT

iterator = util.Iterator(board)#This might go in main
iterator.start() #Might go in main????
"""

#Class object to represent the set of controls on this device
class Controls():

    """Constructor"""
    def __init__(self, device):
        self.device = device

    def check_bright_ctrl(self):
        val = input("Brightness value 1 to 5: ")
        return int(val)

    def check_speed_ctrl(self):
        val = input("Speed value 1 to 10: ")
        return int(val)

    def check_edit_mode_pb(self):
        val = input("Edit Mode? y=1 or n=0: ")
        return int(val)

    def led_on(self,pin_num):
        print("Turning LED " + str(pin_num) + " on.")

    def led_off(self,pin_num):
        print("Turning LED " + str(pin_num) + " off.")