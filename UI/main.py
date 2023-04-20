#Import necessary files
import csv
import states
import controls
import time

#import necessary libraries
#import pyfirmata


def main():
    device = states.Device()

    while True:
        #Run loop at 100Hz
        time.sleep(0.01)

        #Check the mode toggle switch
        #Let's say 1 is manual and 0 is automatic
        if device.controls.check_mode_switch() == 1:
            
            #Should be in manual mode
            if device.mode.mode == 'A':
                device.toggle_mode()

        else:
            
            #Should be in automatic mode
            if device.mode.mode != 'A':
                device.toggle_mode()
        
        
        #Check which mode the device is in to check input
        if device.mode.mode == "M":

            """Check MS, AS, BC, SC, SS, SE"""
            device.mode.check_controls()
            
        elif device.mode.mode == "E":

            """Check CS, R, G, B"""
            device.mode.check_controls()
            
        else:

            """Check MS"""
            print("Automatic mode")

        #Print the controls from csv
        print("Printing CSV vals")
        device.print_csv_vals()

        #Print the controls from variables
        print("Printing variables vals")
        print(device.macro)
        print(device.brightness)
        print(device.speed)
        print(device.scheme)


if __name__ == '__main__':
    main()


