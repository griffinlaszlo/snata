#!/usr/bin/env python3

# python headers
import sys
import os
import re
import json

# open chat_history.json file
FILE = open('uploads/json/story_history.json')
file = json.load(FILE)

# for key, value in file.items():
#     print(key)

total_story_views = 0
total_story_replies = 0
story_count = 0
for x in file["Your Story Views"]:
    story_views = x["Story Views"]
    story_replies = x["Story Replies"]
    total_story_views = total_story_views + story_views
    total_story_replies = total_story_replies + story_replies
    story_count += 1


if story_count <= 100:
    print('You like to keep things lowkey..')
    print(f"You've only posted to your story {story_count} times")
    print(f'Still racking up the views though!')
    print(f'You have {total_story_views} views across all your stories')
elif story_count >= 100 and story_count <= 300:
    print("You could write a book with all these stories...")
    print(f"You've posted to your story {story_count} times")
    print(f'Lotta eyes on them too!')
    print(f'You have {total_story_views} views across all your stories')
elif story_count >= 300 and story_count <= 500:   
    print("You're a story teller!")
    print(f"You've posted to your story {story_count} times")
    print(f'Lotta eyes on them too!')
    print(f'You have {total_story_views} views across all your stories')
elif story_count > 500:
    print("You're an open book!")
    print(f"You've posted to your story {story_count} times")
    print(f"with {total_story_views} total views across all your stories")


viewer = {}
count = 0
for x in file["Friend and Public Story Views"]:
    for key, value in x.items():
        if key == 'View':
            viewer[value] = viewer.get(value, 0) + 1
print("Here are your favorite creators from the Discovery Page!")
print("You've viewed...")
for k, v in sorted(viewer.items(), key=lambda x: x[1], reverse=True):
    if k != '' and k != 'no name':
        count += 1
        print(f"@{k}'s story {v} times")
    if count == 5:
        break

