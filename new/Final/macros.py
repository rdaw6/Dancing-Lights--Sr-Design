import sacn
import time
import sys
import math
import csv
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from importlib import reload
import variables as v
import base_functions as b
from pyfirmata import Arduino, util

#wait = v.speed #speed from UI

sender = sacn.sACNsender()
sender.start()
sender.bind_address = '169.254.107.173'

sender.activate_output(16) #'universes' 1-4 (aka light strings 1-4)
sender.activate_output(20)
sender.activate_output(24)
sender.activate_output(28) 

lights = [sender[16], sender[20], sender[24], sender[28]] #right now l[3] is GRB, not RGB

sender[16].multicast = True
sender[20].multicast = True
sender[24].multicast = True
sender[28].multicast = True

csv_filename = "C:\\Users\\LattePanda\\Desktop\\Dancing-Lights--Sr-Design-main\\Final\\variables.csv"



def macro1(lights):
    b.alternate(lights, 50)
    #v.load_variables_from_csv('variables.csv')
    v.load_variables_from_csv(csv_filename)
    if v.macro_select[0] != 0:
        return 0
    b.fade(lights, 1)
    #b.shootDownLine(lights, 2, 2, True)
    #b.strobe(lights, 100)
    #b.collide(lights, 2, 2) 
    #b.wrap(lights, 3, 2, space = 2)
    #b.single_wrap(lights, 3)
    #b.combine(lights, 2)

def macro2(lights):
    #b.alternate(lights, 50)
    #b.fade(lights, 1)
    b.shootDownLine(lights, 2, 2, True)
    v.load_variables_from_csv(csv_filename)
    if v.macro_select[0] != 1:
        return 0
    #b.strobe(lights, 100)
    #b.collide(lights, 2, 2) 
    #b.wrap(lights, 3, 2, space = 2)
    b.single_wrap(lights, 3)
    v.load_variables_from_csv(csv_filename)
    if v.macro_select[0] != 1:
        return 0
    b.combine(lights, 2)

def macro3(lights):
    #b.alternate(lights, 50)
    #b.fade(lights, 1)
    #b.shootDownLine(lights, 2, 2, True)
    b.strobe(lights, 50)
    v.load_variables_from_csv(csv_filename)
    if v.macro_select[0] != 2:
        return 0
    b.collide(lights, 2, 2) 
    v.load_variables_from_csv(csv_filename)
    if v.macro_select[0] != 2:
        return 0
    b.wrap(lights, 3, 2, space = 2)
    #b.single_wrap(lights, 3)
    #b.combine(lights, 2)

def color_edit(lights):
    while(1):
        v.load_variables_from_csv(csv_filename)
        if v.macro_select[1] != 2:
            break
        t = (0,0,0)*2
        for i in range(0, len(lights)):
            lights[i].dmx_data = v.colors[0]*10 +t+ v.colors[1]*10 +t+ v.colors[2]*10+t+v.colors[3]*10
            time.sleep(.1)
        
def audio(t):
    #add values to output
    #t = (high, mid, low)
    
    lights[0].dmx_data = t * 100

    #repeat every 100 milliseconds
    time.sleep(.1)

def main():
    while(1):
        if v.macro_select == [0,0]:
            macro1(lights)

        if v.macro_select == [1,0]:
            macro2(lights)

        if v.macro_select == [2,0]:
            macro3(lights)

        if v.macro_select[1] == 2:
            color_edit(lights)

        if v.macro_select[1] == 1:
            
            while(1):
                v.load_variables_from_csv(csv_filename)
                if v.macro_select[1] != 1:
                    break

        v.load_variables_from_csv(csv_filename)

if __name__ == '__main__':
    main()
