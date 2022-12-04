#!/usr/bin/env python3

# import libraries
import re
import json
import os


# Build the default map for a specific location

# Constants
FILE = 'location_history.json'


# Main
FILE = open('location_history.json')
file = json.load(FILE)

print('hi')
list_of_points = []
points = {
    "Time": "",
    "Latitude, Longitude": "",
}

count = 0
for point in file["Location History"]:
    points["Time"] = point["Time"]
    points["Latitude, Longitude"] = (point["Latitude, Longitude"].split(" ")[0], point["Latitude, Longitude"].split(" ")[4])
    list_of_points.append(points.copy())

count=0
for x in list_of_points:
    count+=1

print(count)