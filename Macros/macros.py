import sacn
import time
import sys
import math
import variables as v
import base_functions as b

wait = v.speed #speed from UI

sender = sacn.sACNsender()
sender.start()
sender.bind_address = '169.254.149.221'

sender.activate_output(16) #'universes' 1-4 (aka light strings 1-4)
sender.activate_output(20)
sender.activate_output(24)
sender.activate_output(28) 

lights = [sender[16], sender[20], sender[24], sender[28]] #right now l[3] is GRB, not RGB

sender[16].multicast = True
sender[20].multicast = True
sender[24].multicast = True
sender[28].multicast = True 



def macro1(lights):
    #b.alternate(lights, 50)
    #b.fade(lights, 1)
    #b.shootDownLine(lights, 2, 2, True)
    #b.strobe(lights, 100)
    #b.collide(lights, 2, 2) 
    #b.wrap(lights, 3, 2, space = 2)
    #b.single_wrap(lights, 3)
    b.combine(lights, 2)

#def macro2(lights):
    #b.alternate(lights, 50)
    #b.fade(lights, 1)
    #b.shootDownLine(lights, 2, 2, True)
    #b.strobe(lights, 100)
    #b.collide(lights, 2, 2) 
    #b.wrap(lights, 3, 2, space = 2)
    #b.single_wrap(lights, 3)
    #b.combine(lights, 2)

#def macro3(lights):
    #b.alternate(lights, 50)
    #b.fade(lights, 1)
    #b.shootDownLine(lights, 2, 2, True)
    #b.strobe(lights, 100)
    #b.collide(lights, 2, 2) 
    #b.wrap(lights, 3, 2, space = 2)
    #b.single_wrap(lights, 3)
    #b.combine(lights, 2)

macro1(lights)