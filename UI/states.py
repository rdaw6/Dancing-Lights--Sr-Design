import csv
import controls
import time

"""CSV = (0)MACRO_SEL,(1)BRIGHT_CTRL,(2)SPEED_CTRL,(3)SCHEME_SEL,(4)COLOR_SEL"""
MACRO_INDEX = 0
BRIGHT_INDEX = 1
SPEED_INDEX = 2
SCHEME_INDEX = 3
SCHEME_COLORS_INDEX = 4 #Index of the first scheme's list of colors

SCHEME_EDIT_LED_PIN = 20

NUM_MACROS = 4
NUM_SCHEMES = 4
NUM_COL_PER_SCHEME = 4

#Number of colors options available when editing color in scheme
NUM_COLOR_OPTS = 6 

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
                self.device.update_csv(MACRO_INDEX)
                self.device.macro = new_val
            else:
                #Loops back to beginning of macro "list"
                self.device.vars[MACRO_INDEX] = 1
                self.device.update_csv(MACRO_INDEX)
                self.device.macro = 1
            #print("Macro number changed")
                
        
        #check brightness control (should return int between 1 and 5)
        brt_val = self.device.controls.check_bright_ctrl()

        if((brt_val != 0) and (brt_val != int(self.device.brightness))):
            self.device.vars[BRIGHT_INDEX] = brt_val
            self.device.update_csv(BRIGHT_INDEX)
            self.device.brightness = brt_val

        time.sleep(0.1)

        #check speed control (should return int between 1 and 10)
        speed_val = self.device.controls.check_speed_ctrl()

        if((speed_val != 0) and (speed_val != int(self.device.speed))):
            #print("New speed value!")
            self.device.vars[SPEED_INDEX] = speed_val
            self.device.update_csv(SPEED_INDEX)
            self.device.speed = speed_val

        #Check scheme select button
        if(self.device.controls.check_scheme_sel_pb()):
            print("Editing scheme number")
            #Button has been released
            if(self.device.scheme < NUM_SCHEMES - 1):
                new_val = self.device.scheme + 1
                self.device.vars[SCHEME_INDEX] = new_val
                self.device.update_csv(SCHEME_INDEX)
                self.device.scheme = new_val
            else:
                #Loops back to beginning of macro "list"
                self.device.vars[SCHEME_INDEX] = 0
                self.device.update_csv(SCHEME_INDEX)
                self.device.scheme = 0

        #Check edit mode pb
        if(self.device.controls.check_edit_mode_pb()):
            self.toggle_seMode()


"""Class for color scheme edit mode within manual mode"""
class SchemeEditMode(ManMode):

    """Constructor"""
    def __init__(self, device):
        
        self.device = device
        self.mode = 'E'
        self.on_color = 0

    def toggle_seMode(self):
        
        global SCHEME_EDIT_LED_PIN

        #Switching edit mode back to normal manual mode so turn off led
        self.device.controls.led_off(SCHEME_EDIT_LED_PIN)

        #Set pb prev states to zero in case it was pressed during mode switch
        self.device.controls.next_color_pb_prev_state = 0
        self.device.controls.change_color_pb_prev_state = 0

        #Set on color back to zero so when we re-enter edit mode we can start back at beginning
        self.on_color = 0

        #Go to manual mode
        self.device.mode = self.device.manmode

    def toggle_mode(self):
        global SCHEME_EDIT_LED_PIN
        
        #Mode switch has been flicked so turn off led
        self.device.controls.led_off(SCHEME_EDIT_LED_PIN)

        #go to automatic mode
        self.device.mode = self.device.automode

    def check_controls(self):
        #print("Checking edit mode controls")
        
        #print("Check scheme select button")
        if(self.device.controls.check_edit_mode_pb()):
            self.toggle_seMode()

        #check color number button
        if(self.device.controls.check_next_color_pb()):
            #Make sure we're not going out of range of num colors in scheme
            #subtract once since our first color indexes at 0
            print("Edit next color in scheme")
            if(self.on_color < (NUM_COL_PER_SCHEME - 1)):
                self.on_color += 1
            else:
                #Loop back to beginning of list
                self.on_color = 0 #on_color indexes from 0
                

        #check color selection button
        if(self.device.controls.check_change_color_pb()):
            print("Changing a color")
            print("Color #: " + str(self.on_color))
            #Button has been released
            print("Change to next color options")

            curr_scheme = self.device.scheme
            print("Current Scheme: " + str(curr_scheme))
            curr_color_as_int = int(self.device.scheme_colors[curr_scheme][self.on_color])
            #if(int(self.device.scheme_colors[curr_scheme-1][self.on_color]) < (NUM_COLOR_OPTS - 1)):
            if(curr_color_as_int < (NUM_COLOR_OPTS - 1)):
                #Replace color with next option
                self.device.vars[SCHEME_COLORS_INDEX + self.device.scheme][self.on_color] = str(curr_color_as_int + 1)
                self.device.update_csv(SCHEME_COLORS_INDEX + self.device.scheme)
                self.device.scheme_colors[curr_scheme][self.on_color] = str(curr_color_as_int + 1)
                
            else:
                #Replace color in scheme with first option
                self.device.vars[SCHEME_COLORS_INDEX + self.device.scheme][self.on_color] = str(0)
                self.device.update_csv(SCHEME_COLORS_INDEX + self.device.scheme)
                self.device.scheme_colors[curr_scheme][self.on_color] = str(0)

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
                if(i < SCHEME_COLORS_INDEX):
                    var_list[i] = int(line[0])
                else:
                    var_list[i] = line
                i+=1

        j=0
        while(j<NUM_SCHEMES):
            k=0
            while(k<NUM_COL_PER_SCHEME):
                #var_list[SCHEME_COLORS_INDEX+j][k] = int(var_list[SCHEME_COLORS_INDEX+j][k])
                var_list[SCHEME_COLORS_INDEX+j][k] = str(var_list[SCHEME_COLORS_INDEX+j][k])

                k+=1
            j+=1
        
        print("Var list after init: ")
        print(var_list)

        self.vars = var_list
        
        self.macro = var_list[MACRO_INDEX]
        self.brightness = var_list[BRIGHT_INDEX]
        self.speed = var_list[SPEED_INDEX]
        self.scheme = var_list[SCHEME_INDEX]

        self.scheme_colors = [var_list[SCHEME_COLORS_INDEX]]
        
        index = 1
        while(index < NUM_SCHEMES):
            self.scheme_colors.append(var_list[SCHEME_COLORS_INDEX + index])
            index += 1

        print(self.scheme_colors)
        
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
    def update_csv(self,spot):
        #print("Update CSV called")
        print("New values:")
        print("Macro #: " + str(self.vars[MACRO_INDEX]))
        print("Brightness: " + str(self.vars[BRIGHT_INDEX]))
        print("Speed: " + str(self.vars[SPEED_INDEX]))
        print("Scheme #: " + str(self.vars[SCHEME_INDEX]))

        #print the color schemes
        i=0
        while(i < NUM_SCHEMES):
            print(self.vars[SCHEME_COLORS_INDEX + i])
            i += 1

        fail = True
        while(fail):
            try:
                with open(csv_filename,'w',newline='') as f:
                    w = csv.writer(f)

                    """for item in self.vars:
                        try:
                            w.writerow(item.split(" ,"))
                        except:
                            w.writerow([item])"""

                    i = 0
                    while(i < SCHEME_COLORS_INDEX + NUM_SCHEMES):
                        if(i < SCHEME_COLORS_INDEX):
                            w.writerow([self.vars[i]])
                        else:
                            w.writerow(self.vars[i])
                        i += 1
                        
                f.close()
                fail = False
                
            except:
                continue

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
        

