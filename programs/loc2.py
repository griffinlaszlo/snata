#!/usr/bin/env python3

# import libraries
import os
import sys
import re
import json

# Constants
FILE = 'location_history.json'
# date = str(input("Date (XXXX/XX/XX): "))


# Main
FILE = open('location_history.json')
file = json.load(FILE)
# num =  'y'
# User input 
# while (num == 'y'):
#     print()
#     print("Menu:")
#     print("1: Frequest Locations")
#     print("2: Latest Location")
#     print("3: Home & Work")
#     print("4: Daily Top Locations")
#     print("5: Top Locations Per Six-Day Period")
#     print("6: Location History")
#     print("7: Businesses and public places you may have visited")
#     print("8: Areas you may have vsited in the last two years")
#     print()
#     num = input("What would you like to see? ")

print()
for key, value in file.items():

    # dictionary = {
    #     'region': "",
    #     'city': "",
    #     'time': "",
    # }

    if key == 'Areas you may have visited in the last two years':
        for n in value:
            for key,value in n.items():
                n['City'] = n['City'].title()
                n['Region'] = n['Region'].title()
                print('You were in ' + n['City']+', ' + n['Region'] + ' on ' + n['Time']+'.')
