#Author: Emma Klinzing
#Class: ECE Capstone Design
#   Team: SD23P04: Dancing Lights
#Last Modified: 04/25/2023

#This file manages the member functions for the device and its different modes
#   It also calls the controls fuctions relevant to each mode of the device

import csv
import controls
import time

"""CSV = (0)MACRO_SEL,(1)BRIGHT_CTRL,(2)SPEED_CTRL,(3)SCHEME_SEL,(4)COLOR_SEL"""
MACRO_INDEX = 0
SPECIAL_MACRO_COL_INDEX = 1

BRIGHT_INDEX = 1
SPEED_INDEX = 2
SCHEME_INDEX = 3
SCHEME_COLORS_INDEX = 4 #Index of the first scheme's list of colors

SCHEME_EDIT_LED_PIN = 13

NUM_MACROS = 3
NUM_SCHEMES = 4
NUM_COL_PER_SCHEME = 4

#Number of colors options available when editing color in scheme
NUM_COLOR_OPTS = 6 

#csv_filename = "variables.csv" - FIX THIS PATH IF THE FILE MOVES ON THE LATTEPANDA (This path is only correct for our prototype's LattePanda)
csv_filename = "C:\\Users\\LattePanda\\Desktop\\Dancing-Lights--Sr-Design-main\\Macros\\variables.csv"

#Class object for prototype modes to be sub-classes of
class Mode:
    #Code that occurs for both state types
    def scan(self):
        #Code
        print("Scanning Mode") #placeholder print statement


"""Class for manual mode of device"""
class ManMode(Mode):

    """Constructor"""
    def __init__(self, device):
        
        #Attaches device to this mode (so we can manage device vars, etc from this class obj)
        self.device = device

        #Set device's mode to manual ("M")
        self.mode = 'M'

    """method for toggling modes"""
    def toggle_mode(self):
        #Switching to automatic mode so set special_macro to 1
        self.device.set_special_macro(1)

        #Switch device to automatic mode
        self.device.mode = self.device.automode

    #Function to switch to Scheme Edit Mode
    def toggle_seMode(self):

        global SCHEME_EDIT_LED_PIN

        #Switching device to scheme edit mode so set special_macro to 2
        self.device.set_special_macro(2)

        #Switch device mode to scheme edit
        self.device.mode = self.device.semode

        #Turn on scheme edit led
        self.device.controls.led_on()


    #Function to check the relevant controls for manual mode
    def check_controls(self):
        """Check MS, AS, BC, SC, SS, SE"""
        
        #Mode select switch is checked in main (for all modes)

        #Check macro select button
        if(self.device.controls.check_macro_sel_pb()):
            #Button has been released

            if(self.device.macro < (NUM_MACROS - 1)):
                #Device is not on last macro in the list, so incremement macro number by 1
                new_val = self.device.macro + 1
                
                #Save new value to the device object's vars list
                self.device.vars[MACRO_INDEX][0] = new_val
                
                #Update the CSV with new val
                self.device.update_csv()
                
                #Update the device obj's member variable for macro num
                self.device.macro = new_val
                
            else:
                #Device is on last macro in the list, so loop back to the first

                #Update device obj's var list with new macro 
                self.device.vars[MACRO_INDEX][0] = 0

                #Update CSV with new macro number
                self.device.update_csv()

                #Update device's member var for macro num
                self.device.macro = 0
                
        
        #check brightness control (should return int between 1 and 5)
        brt_val = self.device.controls.check_bright_ctrl()

        #Check if the brightness value has changed by comparing it to device obj's member var for brightness
        if((brt_val != 0) and (brt_val != int(self.device.brightness))):
            #Brightness has changed and isn't an invalid number (0)
            
            #Update device obj's vars list
            self.device.vars[BRIGHT_INDEX] = brt_val
            
            #Updates CSV with new val
            self.device.update_csv()
            
            #Update device obj's member var for brightness 
            self.device.brightness = brt_val

        #Sleep to give sys time to catch up (after analog read)
        time.sleep(0.1)

        #check speed control (should return int between 1 and 10)
        speed_val = self.device.controls.check_speed_ctrl()

        if((speed_val != 0) and (speed_val != int(self.device.speed))):
            #Speed value has changed and isn't invalid input (0)

            #Update device obj's vars list
            self.device.vars[SPEED_INDEX] = speed_val

            #Update CSV with new val for speed
            self.device.update_csv()

            #Update device obj's member var for speed
            self.device.speed = speed_val

        #Check scheme select button
        if(self.device.controls.check_scheme_sel_pb()):
            print("Editing scheme number")
            #Button has been released
            
            if(self.device.scheme < NUM_SCHEMES - 1):
                #Not on last scheme in list, so increment scheme num val by 1
                new_val = self.device.scheme + 1

                #Update device obj's var list with new val for scheme num
                self.device.vars[SCHEME_INDEX] = new_val

                #Update CSV with new val for scheme num
                self.device.update_csv()

                #Update device obj's member val for scheme num 
                self.device.scheme = new_val
                
            else:
                #On last scheme num in scheme list, so loop back to beginning

                #Update device obj's var list with new scheme num
                self.device.vars[SCHEME_INDEX] = 0

                #Updte CSV
                self.device.update_csv()

                #Update device var's member var for scheme num
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
        self.device.controls.led_off()

        #Set pb prev states to zero in case it was pressed during mode switch
        self.device.controls.next_color_pb_prev_state = 0
        self.device.controls.change_color_pb_prev_state = 0

        #Set on color back to zero so when we re-enter edit mode we can start back at beginning
        self.on_color = 0

        #Going to manual so special macro is 0
        self.device.set_special_macro(0)

        #Go to manual mode
        self.device.mode = self.device.manmode

    def toggle_mode(self):
        global SCHEME_EDIT_LED_PIN
        
        #Mode switch has been flicked so turn off led
        self.device.controls.led_off()

        #Going to automatic mode so set special_macro to 1
        self.device.set_special_macro(1)

        #go to automatic mode
        self.device.mode = self.device.automode

    def check_controls(self):
        
        if(self.device.controls.check_edit_mode_pb()):
            #EDIT_SEL PB was pressed so toggle back to manual mode
            self.toggle_seMode()

        #check COLOR_SEL button
        if(self.device.controls.check_change_color_pb()):
            
            #COLOR_SEL button was pressed so move to the next color in the current scheme
            print("Edit next color in scheme")
            
            if(self.on_color < (NUM_COL_PER_SCHEME - 1)):
                #Not on the last color in the scheme, so incremenet by one
                self.on_color += 1
                
            else:
                #On last color in scheme so loop back to beginning of list
                self.on_color = 0 
                

        #check NEXT_COLOR_SEL pushbutton
        if(self.device.controls.check_next_color_pb()):

            #NEXT_COLOR_SEL was pressed
            print("Changing a color")
            print("Color #: " + str(self.on_color))
            print("Change to next color option")

            #Get the current scheme of the device (as an integer/index value)
            curr_scheme = self.device.scheme
            
            print("Current Scheme: " + str(curr_scheme))

            #Get the current color of the color number we're editing in the scheme
            curr_color = self.device.scheme_colors[curr_scheme][self.on_color]
            
            if(curr_color < (NUM_COLOR_OPTS - 1)):
                #Not on last color in list of color options so increment current color in current scheme by 1
                #Replace color with the next color option

                #Update the device obj's var list
                self.device.vars[SCHEME_COLORS_INDEX + self.device.scheme][self.on_color] = curr_color + 1

                #Update CSV
                self.device.update_csv()

                #Update the device obj's member var for the scheme (list of each scheme color's color index)
                self.device.scheme_colors[curr_scheme][self.on_color] = curr_color + 1
                
            else:
                #On last value in list of color options, so loop back to beginning

                #Update device obj's vars list with new value for the color in the scheme
                self.device.vars[SCHEME_COLORS_INDEX + self.device.scheme][self.on_color] = 0

                #Update CSV
                self.device.update_csv()

                #Update device obj's member func for the current scheme and it's current color
                self.device.scheme_colors[curr_scheme][self.on_color] = 0

"""Class for automatic/audio mode of device"""
class AutoMode(Mode):
    
    """Constructor"""
    def __init__(self, device):

        #Attach device obj to this mode so we can edit the device's variables, etc
        self.device = device

        #Set device's mode to automatic/audio
        self.mode = 'A'

    """method for toggling modes"""
    def toggle_mode(self):
        
        #Going to manual mode so set special_macro to 0
        self.device.set_special_macro(0)

        #Set device mode to manual
        self.device.mode = self.device.manmode

        #whenever manual mode is activated, need to check all controls
        self.device.mode.check_controls()


"""Class for the device itself"""
class Device:

    #The user interface device (The Lattepanda and attached controls)

    def __init__(self):
        #Assign controls object (attaches the controls to this device so we can call those member funcs)
        self.controls = controls.Controls(self)
        
        #There are three possible states: manual, automatic/audio, and scheme edit -> declare those class objects
        self.automode = AutoMode(self)
        self.manmode = ManMode(self)
        self.semode = SchemeEditMode(self)

        #Upon initialization of this device, determine the mode (manual or automatic) based on the MODE_SEL switch
        #Can't start in SCHEME_EDIT mode
        if self.controls.check_mode_switch() == 1:
            #Manual Mode

            #Set device's var for mode to manual 
            self.mode = self.manmode

            #Set var for special_macro to 0 (since we're not in automatic or scheme edit mode)
            self.special_macro = 0
            
        else:
            #In automatic/audio mode

            #Set device's var for mode to automatic.audio
            self.mode = self.automode

            #Set var for SPECIAL_MACRO to 1 since we're in automatic mode
            self.special_macro = 1

        #Read in the CSV values (See design notebook for the format)
        with open(csv_filename, newline='') as f:
            r = csv.reader(f)
            var_list = list(r)

            i = 0
            #Loop through the lines of the CSV
            for line in var_list:
                if((i < SCHEME_COLORS_INDEX) and (i != MACRO_INDEX)):
                    #The current row has only one value
                    #Read in the row as a value
                    var_list[i] = int(line[0])
                    
                else:
                    #The current row has multiple columns of values
                    #Read in the row as a list
                    var_list[i] = line
                i+=1

        #Ensure macro number is stored as integer
        var_list[MACRO_INDEX][0] = int(var_list[MACRO_INDEX][0])

        #Ensure the colors in the schemes are stored as ints in the var_list
        j=0
        while(j<NUM_SCHEMES):
            k=0
            while(k<NUM_COL_PER_SCHEME):
                var_list[SCHEME_COLORS_INDEX+j][k] = int(var_list[SCHEME_COLORS_INDEX+j][k])
                k+=1
            j+=1

        #Set special_macros to correct value based on starting mode
        if self.mode.mode == "A":
            #Automatic mode is special_macro 1
            self.special_macro = 1

            #Update the device's var list with the proper SPECIAL_MACRO value
            var_list[MACRO_INDEX][SPECIAL_MACRO_COL_INDEX] = 1
            
        else:
            #If it's not in automatic mode at start, it's in manual - no special_macro
            self.special_macro = 0

            #Update the device's var list with the peroper SPECIAL_MACRO value
            var_list[MACRO_INDEX][SPECIAL_MACRO_COL_INDEX] = 0
                    
        print("Var list after init: ")
        print(var_list)

        #Assign the read in CSV values to the device's var list 
        self.vars = var_list

        #assign the device variables (Note: Speical macro already assigned above)
        self.macro = var_list[MACRO_INDEX][0]
        self.brightness = var_list[BRIGHT_INDEX]
        self.speed = var_list[SPEED_INDEX]
        self.scheme = var_list[SCHEME_INDEX]

        #Create a list where the first scheme's color list is the first entry
        #Assign that list of lists (with one entry) to the device's scheme_colors var
        self.scheme_colors = [var_list[SCHEME_COLORS_INDEX]]

        #Go through and append all the other schemes' color lists to the device's scheme_colors var (list of lists)
        index = 1
        while(index < NUM_SCHEMES):
            self.scheme_colors.append(var_list[SCHEME_COLORS_INDEX + index])
            index += 1

        print(self.scheme_colors)

        #Update the CSV to reflect the device's var list 
        self.update_csv()

        #Close the CSV
        f.close()
        

    """method for toggling mode switch"""
    def toggle_mode(self):
        #Set the device's toggle mode func to call the toggle_mode func for whatever mode it's in
        #this way we can call the same func for any mode but get the right action for that specific mode
        print("Toggling mode")
        self.mode.toggle_mode()

    #
    # Func to change value in csv when var is changed
    #
    # param[in]  spot     number of var in CSV list
    # param[in]  val      new val or var
    #
    def update_csv(self):
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

        #Keep trying to open the CSV until it works
        fail = True
        while(fail):
            try:
                with open(csv_filename,'w',newline='') as f:
                    w = csv.writer(f)

                    #Loop through all the entries in teh device's vars list
                    i = 0
                    while(i < SCHEME_COLORS_INDEX + NUM_SCHEMES):
                        
                        if((i < SCHEME_COLORS_INDEX) and (i != MACRO_INDEX)):
                            
                            #Current list entry is an integer -> write it to the CSV properly
                            w.writerow([self.vars[i]])
                            
                        else:
                            
                            #Current list entry is a list -> write it to the CSV properly
                            w.writerow(self.vars[i])

                        #Increment the index
                        i += 1

                #Close the CSV    
                f.close()

                #Was able to successfully write to the CSV so end the loop by setting fail to false
                fail = False
                
            except:
                #Failed so try again
                continue

    #Func to switch the device's special macro val
    #
    #param[in]  val   New value for special_macro
    #
    def set_special_macro(self,val):

        #Update the device's var for SPECIAL_MACRO
        self.special_macro = val

        #Update the device's var list entry for SPECIAL_MACRO
        self.vars[MACRO_INDEX][SPECIAL_MACRO_COL_INDEX] = val

        #Update the CSV
        self.update_csv()

    
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
        val = vars[spot] #Read the CSV value for the requested spot from the list
        f.close() #Close the CSV
        
        return val #Return requested val


