import csv
import controls

"""CSV = (0)MACRO_SEL,(1)BRIGHT_CTRL,(2)SPEED_CTRL,(3)SCHEME_SEL,(4)COLOR_SEL"""
MACRO_INDEX = 0
BRIGHT_INDEX = 1
SPEED_INDEX = 2
SCHEME_INDEX = 3

SCHEME_EDIT_LED_PIN = 20

NUM_MACROS = 4

csv_filename = "variables.csv"

class Mode:
    #Insert code here
    #Code that occurs for both state types
    def scan(self):
        #Code
        print("Scanning Mode") #placeholder print statement


"""Class for manual mode of device"""
class ManMode(Mode):

    """Constructor"""
    def __init__(self, device):
        self.device = device
        self.mode = 'M'

    """method for toggling modes"""
    def toggle_mode(self):
        self.device.mode = self.device.automode

    #se = scheme edit
    def toggle_seMode(self):
        
        global SCHEME_EDIT_LED_PIN
        
        self.device.mode = self.device.semode

        #Turn on scheme edit led
        self.device.controls.led_on(SCHEME_EDIT_LED_PIN)


    def check_controls(self):
        """Check MS, AS, BC, SC, SS, SE"""

        #Mode select switch is checked in main (for all modes)

        #Check macro select button
        if(self.device.controls.check_macro_sel_pb()):
            #Button has been released
            if(self.device.macro < NUM_MACROS):
                new_val = self.device.macro + 1
                self.device.vars[MACRO_INDEX] = new_val
                self.device.update_csv(MACRO_INDEX,new_val)
                self.device.macro = new_val
            else:
                #Loops back to beginning of macro "list"
                self.device.vars[MACRO_INDEX] = 1
                self.device.update_csv(MACRO_INDEX,1)
                self.device.macro = 1
            print("Macro number changed")
                
        
        #check brightness control (should return int between 1 and 5)
        brt_val = self.device.controls.check_bright_ctrl()

        print("brt_val = " + str(brt_val))
        print("self.device.brightness = " + str(self.device.brightness))

        if((brt_val != 0) and (brt_val != int(self.device.brightness))):
            print("New brightness value!")
            self.device.vars[BRIGHT_INDEX] = brt_val
            self.device.update_csv(BRIGHT_INDEX,brt_val)
            self.device.brightness = brt_val

        #check speed control (should return int between 1 and 10)
        speed_val = self.device.controls.check_speed_ctrl()

        print("speed_val = " + str(speed_val))
        print("self.device.speed = " + str(self.device.speed))

        if((speed_val != 0) and (speed_val != int(self.device.speed))):
            print("New speed value!")
            self.device.vars[SPEED_INDEX] = speed_val
            self.device.update_csv(SPEED_INDEX,speed_val)
            self.device.speed = speed_val

        #Check scheme select button
        if(self.device.controls.check_scheme_sel_pb()):
            #Button has been released
            if(self.device.scheme < NUM_SCHEMES):
                new_val = self.device.scheme + 1
                self.device.vars[SCHEME_INDEX] = new_val
                self.device.update_csv(SHCEME_INDEX,new_val)
                self.device.scheme = new_val
            else:
                #Loops back to beginning of macro "list"
                self.device.vars[SCHEME_INDEX] = 1
                self.device.update_csv(SCHEME_INDEX,1)
                self.device.scheme = 1
            print("Scheme number changed")

        #Check edit mode pb
        if(self.device.controls.check_edit_mode_pb()):
            self.toggle_seMode()


"""Class for color scheme edit mode within manual mode"""
class SchemeEditMode(ManMode):

    """Constructor"""
    def __init__(self, device):
        
        self.device = device
        self.mode = 'E'

    def toggle_seMode(self):
        
        global SCHEME_EDIT_LED_PIN

        #Switching edit mode back to normal manual mode so turn off led
        self.device.controls.led_off(SCHEME_EDIT_LED_PIN)

        #Go to manual mode
        self.device.mode = self.device.manmode

    def toggle_mode(self):
        global SCHEME_EDIT_LED_PIN
        
        #Mode switch has been flicked so turn off led
        self.device.controls.led_off(SCHEME_EDIT_LED_PIN)

        #go to automatic mode
        self.device.mode = self.device.automode

    def check_controls(self):
        print("Check scheme select button")
        if(self.device.controls.check_edit_mode_pb()):
            self.toggle_seMode()
        

"""Class for automatic/audio mode of device"""
class AutoMode(Mode):
    
    """Constructor"""
    def __init__(self, device):
        self.device = device
        self.mode = 'A'

    """method for toggling modes"""
    def toggle_mode(self):
        self.device.mode = self.device.manmode

        #whenever manual mode is activated, need to check all controls
        self.device.mode.check_controls()


"""Class for the device itself"""
class Device:

    #The user interface device

    def __init__(self):
        #Assign controls object
        self.controls = controls.Controls(self)
        
        #There are three possible states: manual and automatic
        self.automode = AutoMode(self)
        self.manmode = ManMode(self)
        self.semode = SchemeEditMode(self)


        """This will actually need to be set based on which way mode switch is flipped"""
        self.mode = self.manmode #for now, default to manual mode

        """with open(csv_filename, newline='') as f:
            r = csv.reader(f)
            var_list = list(r)"""


        with open(csv_filename, newline='') as f:
            r = csv.reader(f)
            var_list = list(r)
            i=0
            for line in var_list:
                var_list[i] = line[0]
                i+=1
        
        print("Var list after init: ")
        print(var_list)

        self.vars = var_list
        
        self.macro = int(var_list[0][0])
        self.brightness = int(var_list[1][0])
        self.speed = int(var_list[2][0])
        self.scheme = int(var_list[3][0])
        
        f.close()
        

    """method for toggling mode switch"""
    def toggle_mode(self):
        print("Toggling mode")
        self.mode.toggle_mode()

    #
    # Func to change value in csv when var is changed
    #
    # param[in]  spot     number of var in CSV list
    # param[in]  val      new val or var
    #
    def update_csv(self,spot,val):
        print("Update CSV called")

        print("Val from vars is: " + str(val))

        """f = open(csv_filename,'w') #Read in CSV file
        w = csv.writer(f)
        w.writerows(self.vars)"""

        

        with open(csv_filename,'w',newline='') as f:
            w = csv.writer(f, delimiter=' ')

            for item in self.vars:
                w.writerow([item])
                
        f.close()

    #
    # Func to change value in csv when var is changed
    #
    # param[in]  spot     number of var in CSV list
    #
    # Return the value of the parameter in that spot in the csv list
    #
    def get_csv_val(self,spot):
        f = open(csv_filename) #Read in CSV file
        r = csv.reader(f)
        vars = list(r) # Store CSV as list
        val = vars[spot]
        f.close()
        
        return val

    def print_csv_vals(self):
        print("Printing csv vals: ")
        f = open('variables.csv') #Read in CSV file
        r = csv.reader(f)
        vars = list(r) # Store CSV as list
        f.close()

        # printing the list using loop
        print("Printing list")
        for i in range(len(vars)):
            print(vars[i])
        

