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
num =  'y'
# User input 
while (num == 'y'):
    print()
    print("Menu:")
    print("1: Frequest Locations")
    print("2: Latest Location")
    print("3: Home & Work")
    print("4: Daily Top Locations")
    print("5: Top Locations Per Six-Day Period")
    print("6: Location History")
    print("7: Businesses and public places you may have visited")
    print("8: Areas you may have vsited in the last two years")
    print()
    num = input("What would you like to see? ")

    for key, value in file.items():
        if key == 'Frequent Locations' and num == '1':
            print(value)
        if key == 'Latest Location' and num == '2':
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
        if key == 'Home & Work' and num == '3':
            print(value)
        if key == 'Daily Top Locations' and num == '4':
            print(value)
        if key == 'Top Locations Per Six-Day Period' and num == '5':
            print(value)
        if key == 'Location History' and num == '6':
            print(value)
        if key == 'Businesses and public places you may have visited' and num == '7':
            print(value)
        if key == 'Areas you may have visited in the last two years' and num == '8':
            print(value)
    print()    
    num = input('continue? (y/n): ')


