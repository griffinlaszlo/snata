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
    print(key)
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
                print('It has been ' + str(int(time.strftime('%Y')) - int(year)) + ' years, ' + str(int(time.strftime('%m')) - int(month_num)) + ' months, ' + str(-1*(int(time.strftime('%d')) - int(day))) + ' days, ' + str(int(time.strftime('%H')) - int(hour)) + ' hours, ' + str(1*(int(time.strftime('%M')) - int(minute))) + ' minutes, and ' + str(-1*(int(time.strftime('%S')) - int(second))) + ' seconds since you created your account.')             

    

    if key == 'Engagement':
        # search through list
        print('In the last month or two, you...')
        for n in value:
            event = n["Event"]
            occurrences = n["Occurrences"]
            print(n)
            print(event)
            print(occurrences)            
            if event == 'Application Opens':
                text = '...have opened the app ' + str(occurrences) + ' times.'
            if event == 'Discover Snap Views':
                text = '...have viewed ' + str(occurrences) + ' Discover Snaps.'
                print(text)
            else:
                break
    '''
            if event == 'Discover Stories Views':
                text = '...have viewed ' + str(occurrences) + ' Discover Stories.'
            if event == 'Discover Stories Swipes':
                text = '...have swiped ' + str(occurrences) + ' Discover Stories.'
            if event == 'Discover Stories Taps':
                text = '...have tapped ' + str(occurrences) + ' Discover Stories.'
            if event == 'Discover Stories Long Presses':
                text = '...have long pressed ' + str(occurrences) + ' Discover Stories.'
            if event == 'Discover Stories Saves':
                text = '...have saved ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Shares':
                text = '...have shared ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Replies':
                text = '...have replied to ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Screenshots':
                text = '...have screenshot ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Mutes':
                text = '...have muted ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Unmutes':
                text = '...have unmuted ' + str(occurrences) + ' Discover Stories.'
            elif event == 'Discover Stories Opens':
                text = '...have opened ' + str(occurrences) + ' Discover Stories.'
            print(text)

            # if event = Application Opens, print value

                #print('opened the application ' + str(n["Value"]) + ' times')
                   # print(f'{key}: {value}')         

'''