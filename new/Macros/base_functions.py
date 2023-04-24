import time
import math
import variables as v
from importlib import reload

csv_filename = "C:\\Users\\LattePanda\\Desktop\\Dancing-Lights--Sr-Design-main\\Macros\\variables.csv"



def fade(lights, num_loops): #array of universes (strings of lights) and number of times to loop thru pattern
    sleep = [.1, .09, .08, .07, .06, .05, .04, .03, .02, .01]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = (51 * v.Brightness, x* v.Brightness , 0)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)
        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = ((51-x) * v.Brightness, 51 * v.Brightness, 0)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)
            
        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = (0, 51 * v.Brightness, x * v.Brightness)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)

        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = (0, (51-x) * v.Brightness, 51* v.Brightness)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)
        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = (x* v.Brightness, 0, 51* v.Brightness)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)
        for x in range(52):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [0,0]:
                return 0
            t = (51* v.Brightness, 0, (51-x)* v.Brightness )
            for n in range(0, len(lights)):
                lights[n].dmx_data = t*v.pixel_num[n]
            time.sleep(local_speed)

def shootDownLine(lights, num_loops, width, bounce = False): #edit once pixel count known
    sleep = [.2, .18, .16, .14, .12, .1, .08, .06, .04, .02]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        for x in range(0, v.pixel_num[0] - width):
            v.load_variables_from_csv(csv_filename)
            local_speed = sleep[v.speed - 1]
            if v.macro_select != [1,0]:
                return 0
            t = v.colors[0]*x + v.colors[1] * width + v.colors[0]*(v.pixel_num[0]-x-width)
            for n in range(0, len(lights)):
                lights[n].dmx_data = t
            time.sleep(local_speed)
        if bounce == True:
            for x in range(0, v.pixel_num[0] - width):
                v.load_variables_from_csv(csv_filename)
                local_speed = sleep[v.speed - 1]
                if v.macro_select != [1,0]:
                    return 0
                t = v.colors[0]*(v.pixel_num[0]-x-width) + v.colors[1] * width + v.colors[0]*x
                for n in range(0, len(lights)):
                    lights[n].dmx_data = t
                time.sleep(local_speed)
    return 0

def alternate(lights, num_loops):
    sleep = [1, .9, .8, .7, .6, .5, .4, .3, .2, .1]
    local_speed = sleep[v.speed - 1]
    colors = v.colors
    for i in range(0, num_loops):
        v.load_variables_from_csv(csv_filename)
        if v.macro_select != [0,0]:
                return 0
        t = ()
        for i in range(0, len(v.colors)):
            t += colors[i]
        temp = colors
        new_colors = temp[1:] + [temp[0]]
        colors = new_colors
        for i in range(0, len(lights)):
            lights[i].dmx_data = t * math.floor(v.pixel_num[0]/len(v.colors))
        time.sleep(local_speed)

def strobe(lights, num_loops):
    sleep = [1, .9, .8, .7, .6, .5, .4, .3, .2, .1]
    local_speed = sleep[v.speed - 1]
    for n in range(0, num_loops):
        v.load_variables_from_csv(csv_filename)
        if v.macro_select != [2,0]:
            return 0
        for x in range(0, len(v.colors)):
            for i in range(0, len(lights)):
                lights[i].dmx_data = v.colors[x] * v.pixel_num[i]
            time.sleep(local_speed)

def collide(lights, num_loops, width): #edit once pixel count is known
    sleep = [.2, .18, .16, .14, .12, .1, .08, .06, .04, .02]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        for x in range(0, v.pixel_num[0]//2 - width + 1):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [2,0]:
                return 0
            t1 = (10, 10, 10)*x + v.colors[0] * width + (10, 10, 10)*(v.pixel_num[0]//2-x-width)
            t2 = (10, 10, 10)*(v.pixel_num[0]//2-x-width) + v.colors[1] * width + (10, 10, 10)*x
            for z in range(0, len(lights)):
                lights[z].dmx_data = t1 + t2
            time.sleep(local_speed)
        #for y in range(0, width*2 - 1):

def wrap(lights, num_loops, width, space): #space is num of pixels between the series of lights
    sleep = [.2, .18, .16, .14, .12, .1, .08, .06, .04, .02]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        t=()
        for color in v.colors:
            t += color * width + (10, 10, 10)*space
        n = v.pixel_num[0] // (len(t)//3)
        mod = v.pixel_num[0] % (len(t)//3)
        t *= n
        t += t[:mod*3]
        for x in range(0, (len(t)//3)+1):
            v.load_variables_from_csv(csv_filename)
            if v.macro_select != [2,0]:
                return 0
            for z in range(0, len(lights)):
                lights[z].dmx_data = t[:x*3]
            time.sleep(local_speed)

def single_wrap(lights, num_loops):
    sleep = [.2, .18, .16, .14, .12, .1, .08, .06, .04, .02]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        for i in range(0, len(v.colors)):
            t = ()
            for z in range(0, v.pixel_num[0]):
                v.load_variables_from_csv(csv_filename)
                local_speed = sleep[v.speed - 1]
                if v.macro_select != [1,0]:
                    return 0
                t += v.colors[i]
                for x in range(0, len(lights)):
                    lights[x].dmx_data = t
                time.sleep(local_speed)

def combine(lights, num_loops): #edit once pixel count is known
    sleep = [.2, .18, .16, .14, .12, .1, .08, .06, .04, .02]
    local_speed = sleep[v.speed - 1]
    for i in range(0, num_loops):
        for y in range(0, len(v.colors)):
            t1 = v.colors[y] * (v.pixel_num[0]//2)
            if y==len(v.colors)-1:
                t2 = v.colors[0] * (v.pixel_num[0]//2)
                new_color = ((v.colors[y][0]+v.colors[0][0])//2, (v.colors[y][1]+v.colors[0][1])//2, (v.colors[y][2]+v.colors[0][2])//2)
            else:
                t2 = v.colors[y+1] * (v.pixel_num[0]//2)
                new_color = ((v.colors[y][0]+v.colors[y+1][0])//2, (v.colors[y][1]+v.colors[y+1][1])//2, (v.colors[y][2]+v.colors[y+1][2])//2)
            for x in range(0, (v.pixel_num[0]//2) + 1 ):
                v.load_variables_from_csv(csv_filename)
                if v.macro_select != [1,0]:
                    return 0
                for z in range(0, len(lights)):
                    lights[z].dmx_data = t1[:x*3] + (0, 0, 0)*(v.pixel_num[0]-(x*2)) + t2[:x*3]
                time.sleep(local_speed)
            time.sleep(local_speed)
            for z in range(0, len(lights)):
                lights[z].dmx_data = new_color * v.pixel_num[0]
            time.sleep(local_speed*12)
            
