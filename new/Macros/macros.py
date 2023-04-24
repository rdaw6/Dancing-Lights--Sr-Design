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

csv_filename = "C:\\Users\\LattePanda\\Desktop\\Dancing-Lights--Sr-Design-main\\Macros\\variables.csv"



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
        
def audio(lights):
    board = Arduino('COM3')
    it = util.Iterator(board)
    it.start()
    time.sleep(.05)
    board.analog[2].enable_reporting()
    board.analog[3].enable_reporting()
    board.analog[4].enable_reporting()
    board.analog[5].enable_reporting()
    i=0
    output = []
    while True:
        #read values from circuit
        volume = board.analog[3].read()
        hp = board.analog[4].read()
        lp = board.analog[5].read()
        bp = board.analog[2].read()
        if ((volume == None) or (hp == None) or (lp == None) or (bp == None)):
            continue
        #print("H " + str(hp) + " L " + str(lp) + " M " + str(bp))
        #invert low pass input
        
        lpmod = 1 - lp
        # normalize values 
        brightness = round(20 * volume)
        if (brightness > 5):
            brightness = 5
        high = round((hp - .815)*(255/.02))
        #print("High " + str(high))
        if (high < 0):
            high =0
        if (high > 255):
            high =255
        low = round((lpmod)*(255/.004))
        #print("Low " + str(low))
        if (low < 0):
            low =0
        if (low > 255):
            low =255
        mid = round((bp - .1)*(255/.42))
        #print("Mid " + str(mid))
        if (mid < 0) or (mid==0):
            mid =0
            low = 0
            high = 0
        if (mid > 255):
            mid =255

        #add values to output
        #output[i] = (brightness, high, mid, low)
        t = (high, mid, low)
        #print(t)
        #print("Brightness " + str(brightness))
        lights[0].dmx_data = t * 100
        #i += 1
        #repeat every 100 milliseconds
        time.sleep(.1)

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
        audio(lights)

    v.load_variables_from_csv(csv_filename)
