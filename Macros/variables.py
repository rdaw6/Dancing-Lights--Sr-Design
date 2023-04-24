import csv
import time
from pathlib import Path

# Initialize variables
macro_select = None
Brightness = None
speed = None
color_scheme = None
#color_options = [(0, 0, 0), (0, 0, 51), (0, 51, 0), (0, 51, 51), (51, 0, 0), (51, 0, 51), (51, 17, 0), (51, 17, 51), (51, 34, 0), (51, 34, 51), (51, 51, 0), (51, 51, 51)]
color_options  = [(51, 0, 0),   # dark red
                 (51, 17, 0),  # dark brown
                 (51, 34, 0),  # dark olive
                 (0, 51, 0),   # dark green
                 (0, 51, 51),  # dark cyan
                 (0, 0, 51),   # dark blue
                 (51, 0, 51),# dark magenta
                 (51, 51, 51)]  #white


colors = [0, 0, 0, 0]
scheme_1 = None
scheme_2 = None
scheme_3 = None
scheme_4 = None
pixel_num = [50, 100, 100, 100]
# Function to load variables from CSV file
def load_variables_from_csv(csv_file_path):
    global macro_select, Brightness, speed, color_scheme, colors, scheme_1, scheme_2, scheme_3, scheme_4, color_options

    variable_names = ["macro_select", "Brightness", "speed", "color_scheme", "scheme_1", "scheme_2", "scheme_3", "scheme_4"]
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            variable_name = variable_names[i]
            if i < 4:
                value = row[0]
                print(value)
            else:
                v1 = int(row[0])
                v2 = int(row[1])
                v3 = int(row[2])
                v4 = int(row[3])
                print(v1, v2, v3, v4)

            if variable_name == "macro_select" or variable_name == "Brightness" or variable_name == "color_scheme":
                value = int(value)
            elif variable_name == "speed":
                value = int(value)

            if variable_name == "macro_select":
                macro_select = value
            elif variable_name == "Brightness":
                Brightness = value
            elif variable_name == "speed":
                speed = value
            elif variable_name == "color_scheme":
                color_scheme = value
            elif variable_name == "scheme_1":
                scheme_1 = [v1, v2, v3, v4]
            elif variable_name == "scheme_2":
                scheme_2 = [v1, v2, v3, v4]
            elif variable_name == "scheme_3":
                scheme_3 = [v1, v2, v3, v4]
            elif variable_name == "scheme_4":
                scheme_4 = [v1, v2, v3, v4]
    schemes = [scheme_1, scheme_2, scheme_3, scheme_4]
    scheme = schemes[color_scheme]
    for i in range(0, 4):
        r, g, b = color_options[scheme[i]]
        colors[i] = (r*Brightness, g*Brightness, b*Brightness)
    print(f"macro: {macro_select}, Brightness: {Brightness}, speed: {speed}, scheme: {color_scheme}, colors: {colors}")


def monitor_csv_file(csv_file_path):
    file_path = Path(csv_file_path)
    last_modified_time = file_path.stat().st_mtime

    while True:
        current_modified_time = file_path.stat().st_mtime
        if current_modified_time != last_modified_time:
            load_variables_from_csv(csv_file_path)
            print(f'Variables updated: macro_select={macro_select}, Brightness={Brightness}, speed={speed}')
            last_modified_time = current_modified_time
        time.sleep(1)

# Set the initial values of the variables
csv_file_path = 'variables.csv'
load_variables_from_csv(csv_file_path)

# Start monitoring and updating variables
#monitor_csv_file(csv_file_path)


#number from 1 to 5, 5 is brightest
#Brightness = 5

#Array of RGB tuple from 0 to 51
#colors = [(51* Brightness, 0, 0), (0, 51* Brightness, 0), (0, 0, 51* Brightness)]

#select int of desired macro 
#macro_select = 1

# 0.03 for very gradual, 0.01 for medium, 0.005 for quick
#speed = .05

#number of pixels attached to universes 16, 20, 24, and 28 respectively
#pixel_num = [100, 9, 0, 170]