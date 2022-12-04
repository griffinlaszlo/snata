#!/usr/bin/env python3

# python headers
import sys
import os
import re
import json

# open chat_history.json file
FILE = open('json/memories_history.json')
file = json.load(FILE)

total_count = 0
image_count = 0
video_count = 0
image_years = []
video_years = []
days = []

for x in file['Saved Media']:
    if x['Media Type'] == 'Image':
        image_count+= 1
        image_years = []
        
    elif x['Media Type'] == 'Video':
        video_count += 1

    total_count += 1

if image_count > video_count:
    print('You are ')
    print('You look at life from a stand still...')
    print('You capture life at a stand still')
else:
    print('You like to watch life fly-by')

# Think of funny ad voices


print(total_count)
print(image_count)
print(video_count)

