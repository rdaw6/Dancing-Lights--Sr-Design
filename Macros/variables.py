import csv
import time
from pathlib import Path

# Initialize variables
macro_select = None
Brightness = None
speed = None
colors = [(51, 0, 0), (0, 51, 0), (0, 0, 51)]
pixel_num = [100, 100, 100, 100]
# Function to load variables from CSV file
def load_variables_from_csv(csv_file_path):
    global macro_select, Brightness, speed

    variable_names = ["macro_select", "Brightness", "speed"]
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for i, row in enumerate(reader):
            variable_name = variable_names[i]
            value = row[0]
            if variable_name == "macro_select" or variable_name == "Brightness":
                value = int(value)
            else:
                value = float(value)

            if variable_name == "macro_select":
                macro_select = value
            elif variable_name == "Brightness":
                Brightness = value
            elif variable_name == "speed":
                speed = value


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