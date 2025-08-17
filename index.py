#!/usr/bin/python3

import time
from enum import IntEnum

### Customisation ###

# File containing the measures
database = "measures"
# URL of the "home" button
url = "http://localhost"
# Displayed program version
version = "Version 1.1"

### Definitions ###


class Type(IntEnum):
    time = 0
    processor = 1
    memory = 2
    disk = 3


# Index of the measure inside the displayed array
index = 0
# Quantity of measures read from file
measures_quantity = 0
# Default value to be displayed
no_data = -1
# Error message
error = ""
# Lists of values that will be displayed
processor = [no_data]*60
memory = [no_data]*60
disk = [no_data]*60

### Functions ###

# Imports data from file into a list
def ImportData():
    measures = list()
    measures_quantity = 0
    with open(database, 'r') as file:
        for line in file:
            try:
                content_txt = line.split(';')
                content_int = [int(content_txt[Type.time]), int(content_txt[Type.processor]),
                            int(content_txt[Type.memory]), int(content_txt[Type.disk])]
            except:
                content_int = [no_data, no_data, no_data, no_data]
                global error
                error = " - Unexpected measure value"
            measures.append(content_int)
            measures_quantity += 1
    return measures, measures_quantity

# Skips measures older than 1 hour
def SkipOldMeasures(measures, index):
    now = int(time.time())
    minute = 60
    hour = 60*minute
    measures_where_skipped = False
    while measures[index][Type.time] < now - hour and index < 60:
        index += 1
        measures_where_skipped = True
    if measures_where_skipped:
        index += 1
    return index

# Assigns measures to display arrays
def AssignMeasures(measures, measures_quantity, index):
    minute = 60
    for counter in range(index, measures_quantity):
        # Skipping slots if measures are not consecutive
        if counter > 0:
            quantity_of_skips = 0
            while measures[counter][Type.time] > measures[counter-1][Type.time] + minute + 3 + quantity_of_skips*minute and index < 60:
                quantity_of_skips += 1
                index += 1
        # Assigning measures to respective lists
        if index < measures_quantity:
            processor[index] = measures[counter][Type.processor]
            memory[index] = measures[counter][Type.memory]
            disk[index] = measures[counter][Type.disk]
            index += 1
        else:
            break
    return index

# Prints graphs in HTML
def DrawGraph(values, input_type):
    max_height = 100
    color = ["black", "black"]
    if input_type == Type.processor:
        color = ["lightblue", "blue"]
    if input_type == Type.memory:
        color = ["pink", "purple"]
    if input_type == Type.disk:
        color = ["lightgreen", "green"]
    for x in range(len(values)):
        value = values[x]
        if value == no_data:
            print('''<div class="no_data"></div>''')
        if value == 0:
            print('''<div class="bar" style="height: 0; margin-top: ''' +
                  str(max_height) + '''px; background: ''' + str(color[0]) + '''; border-color: ''' + str(color[1]) + '''"></div>''')
        if value > 0:
            height = (value/100) * max_height
            margin = max_height - height
            print('''<div class="bar" style="height:''' + str(height) + '''px; margin-top: ''' +
                  str(margin) + '''px; background: ''' + str(color[0]) + '''; border-color: ''' + str(color[1]) + '''"></div>''')


### Body ###


try:
    measures, measures_quantity = ImportData()
except:
    error = " - Could not retrieve data"
else:
    try:
        index = SkipOldMeasures(measures, index)
        index = AssignMeasures(measures, measures_quantity, index)
    except:
        error = " - Something went wrong while handling data"


print("Content-type: text/html\n\n")
print('''
<!DOCTYPE html>

<head>
    <title>
        Performances
    </title>
    <link rel="stylesheet" type="text/css" href="style.css">
</head>

<body>
    <div class="winwow">
        <div class="window_header">
        ''' + version + '''<span style="color: red;">''' + error + '''</span>
            <button class="reload_button" onClick="window.location.reload(true)"><b class="reload">&#8634;</b></button>
            <button class="home_button"><a href="''' + url + '''"><b class="reload">&#x2302;</b></a></button>
        </div>
        <div class="window_content">
            <div class="metric">
                Processor: ''' + str(processor[index-1]) + '''%
                <div class="graph">
                ''')
DrawGraph(processor, Type.processor)
print('''</div>
            </div>
            <div class="metric">
                Memory: ''' + str(memory[index-1]) + '''%
                <div class="graph">
                ''')
DrawGraph(memory, Type.memory)
print('''</div>
            </div>
            <div class="metric">
                Disk: ''' + str(disk[index-1]) + '''%
                <div class="graph">
                ''')
DrawGraph(disk, Type.disk)
print('''</div>
            </div>
        </div>
    </div>
</body>
''')
