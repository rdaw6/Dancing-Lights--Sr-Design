#Import necessary files
import csv
import states
import controls
import time

#import necessary libraries
#import pyfirmata


def main():
    #Create a device object (Represents LattePanda) (Attaches Controls and Modes to obj)
    device = states.Device()

    while True:
        #Run loop at 100Hz
        time.sleep(0.1)

        #Ensure the device obj is in the correct mode by checking MODE_SEL control
        #Check the mode toggle switch (1 is manual, 1 is automatic)
        if device.controls.check_mode_switch() == 1:
            #MODE_SEL is in manual position

            #Check if device obj mode is currently automatic
            if device.mode.mode == 'A':
                #device currently in automatic mode

                #toggle to manual
                device.toggle_mode()

        else:
            #MODE_SEL switch in automatic position
            
            if device.mode.mode != 'A':
                #device is in manual or edit mode

                #toggle to automatic
                device.toggle_mode()
        
        
        #Check necessary controls based on mode of device
        if device.mode.mode == "M":
            #Device is in manual mode

            """Check MS, AS, BC, SC, SS, SE"""
            device.mode.check_controls()
            
        elif device.mode.mode == "E":
            #Device is in scheme edit mode

            """Check CS, R, G, B"""
            device.mode.check_controls()
            
        else:
            #Device is in automatic mode (no controls to check)
            print("Automatic mode")


if __name__ == '__main__':
    main()


