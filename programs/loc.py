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
    if key == 'Frequent Locations':
        for n in value:
            n['City'] = n['City'].title()
            n['Region'] = n['Region'].upper()
            n['Country'] = n['Country'].upper()
            print('You are frequently found in ' + n['City'], n['Region'], n['Country'])
            break
    if key == 'Latest Location':
        value = dict( value[0])
        for x,y in value.items():
            if x == 'City':
                city = y
                city = city.title()
            if x == 'Country':
                country = y
                country = country.upper()
            if x == 'Region':
                region = y
                region = region.upper()
        print()
        print(f'You were last seen in {city}, {region}, {country}\n')
    if key == 'Home & Work':
        continue
    # if key == 'Daily Top Locations':
    #     print(value)
#     if key == 'Top Locations Per Six-Day Period':
#         print(value)
#     if key == 'Location History':
#         print(value) 
    # declare a dictionary with date and name 
    dictionary = {
        'date': "",
        'name': "",
    }
    if key == 'Businesses and public places you may have visited':
        for n in value:
            for x,y in n.items():
                if x == 'Name':
                    dictionary['name'] = y
                if x == 'Date':
                    dictionary['date'] = y
                
            print('You were at ' + dictionary['name'] + ' on ' + dictionary['date'])
        
        # print you were at the business on the date
        # change date to a string
        # print(f'You were at {dictionary["name"]} on {dictionary["date"]}')
    
    
    # count how many times the name appears in the dictionary

        #     if key == 'Areas you may have visited in the last two years':
#         print(value)
# print()


