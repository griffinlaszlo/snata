#!/usr/bin/env python3
import os
import sys
import re
import json
import time
from tkinter import W

# Constants

FILE = open('user_profile.json')
file = json.load(FILE)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
for key, value in file.items():
    # print(key)
    if key == 'App Profile':
        for key, value in value.items():
            if key == 'Creation Time':
                year, month, day = value.split('-')
                day = day.split(' ')[0]
                hour, minute, second = value.split(' ')[1].split(':')
                if int(hour) >= 12:
                    hour = str(int(hour) - 12)
                    second += ' PM'
                elif int(hour) < 12:
                    second += ' AM'
                month = months[int(month) - 1]
                print('You created your account on ' + month + ' ' + day + ', ' + year + ' at ' + hour + ':' + minute + ':' + second)
                for n in months:
                    if n == month:
                        month_num = months.index(n) + 1
                        break
                second = second.split(' ')[0]
                print('It has been ' + str(int(time.strftime('%Y')) - int(year)) + ' years, ' + str(int(time.strftime('%m')) - int(month_num)) + ' months and ' + str(-1*(int(time.strftime('%d')) - int(day))) + ' days' + ' since you created your account.')             

    

    if key == 'Engagement':
        for n in value:
            event = n["Event"]
            occurrences = n["Occurrences"]
            if event == 'Application Opens':
                print('In the last month or two, you have...\n...opened the app ' + str(occurrences) + ' times')

            if event == 'Story Views':
                print('...viewed ' + str(occurrences) + ' Discover Stories.')

            if event == 'Snaps Posted to Story':
                print('...posted ' + str(occurrences) + ' Snaps to your Story.')

            if event == 'Snaps Viewed in a Story':
                print('...viewed ' + str(occurrences) + ' Snaps in a Story.')

            if event == 'Snap Views':
                print('...viewed ' + str(occurrences) + ' Snaps.')
            
            if event == 'Snap Sends':
                print('...sent ' + str(occurrences) + ' Snaps.')

            if event == 'Chats Sent':
                print('...sent ' + str(occurrences) + ' Chats.')

            if event == 'Chats Viewed':
                print('...viewed ' + str(occurrences) + ' Chats.')

            if event == 'Discover Editions Viewed':
                print('...viewed ' + str(occurrences) + ' Discover Editions.')
            
            if event == 'Discover Snap Views':
                print('...viewed ' + str(occurrences) + ' Discover Snaps.')
            
            if event == 'Direct Snaps Created':
                print('...created ' + str(occurrences) + ' Direct Snaps.')
            
            if event == 'Direct Snaps Viewed':
                print('...viewed ' + str(occurrences) + ' Direct Snaps.')

            if event == 'Geofilter Snap Sends':
                print('...sent ' + str(occurrences) + ' Geofilter Snaps.')
            
            if event == 'Geofilter Story Snaps Viewed':
                print('...viewed ' + str(occurrences) + ' Geofilter Story Snaps.')
            
            if event == 'Geolens Swipes':
                print('...swiped ' + str(occurrences) + ' Geolens Snaps.')
            
            if event == 'Geofilter Snaps Posted to Story':
                print('...posted ' + str(occurrences) + ' Geofilter Snaps to your Story.')

            if event == 'Geofilter Swipes':
                print('...swiped ' + str(occurrences) + ' Geofilter Snaps.')
            


