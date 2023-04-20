#!/usr/bin/env python3

import pyfirmata
import time

if __name__ == '__main__':
    # Initiate communication with Arduino
    board = pyfirmata.Arduino('COM3')

    button = board.digital[8]
    
    previous_button_state = 0
    
    # Start iterator to receive input data
    it = pyfirmata.util.Iterator(board)
    it.start()

    # Setup LEDs and button
    button.mode = pyfirmata.INPUT
    

    # The "void loop()"
    while True:
        
        # Get button current state
        button_state = button.read()
        
        # Check if button has been released
        if((button_state != None) and (previous_button_state != None) and (button_state != previous_button_state)):
            if button_state == 0:
                print("Button released")
            
        # Save current button state as previous
        # for the next loop iteration
        previous_button_state = button_state
