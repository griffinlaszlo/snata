#!/usr/bin/env python3

# import libraries
import os
import sys
import re
import json

# Constants

FILE = open('friends.json')
file = json.load(FILE)

# Main

freq = {}

for user in file["Friends"]:
    src = user["Source"]
    if(src in freq):
        freq[src]+=1
    else:
        freq[src] = 1

friends = len(file["Friends"])
addedyou = friends - freq["added by added me back"]
print(f'You have {friends}  friends on Snapchat.')
print(f'You added {freq["added by added me back"]} of these friends')
print(f'{addedyou} of your friends added you first')

for key in freq:
    sep = "were"
    if freq[key] == 1: 
        sep = "was"
    print(f'{freq[key]} were {key}')

# generate a list of 10 random integers between 0 and 100

