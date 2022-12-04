#!/usr/bin/env python3

# import libraries
import os
import sys
import re
import json
import datetime
# Constants


def main():
    
    print_username()
    first_friend()
    first_memory()
    total_snaps()
    user_profile_info()
    display_name_changes()
    num_of_subscriptions()


    

def print_username():

    FILE = open('../mydata_1669823359244/json/account.json')
    file = json.load(FILE)

    # FILE = open('json/account.json')
    # file = json.load(FILE)
    print(file["Basic Information"]["Username"])


def total_snaps():
    FILE = open('../mydata_1669823359244/json/chat_history.json')
    file = json.load(FILE)
    snaps_received_saved = len(file["Received Saved Chat History"])
    snaps_received_unsaved = len(file["Received Unsaved Chat History"])
    total_snaps_received = snaps_received_unsaved + snaps_received_saved
    snaps_sent_saved = len(file["Sent Saved Chat History"])
    snaps_sent_unsaved = len(file["Sent Unsaved Chat History"])
    total_snaps_sent = snaps_received_unsaved + snaps_received_saved

    text_snaps = 0
    media_snaps = 0
    share_snaps = 0
    note_snaps = 0


    for i in file["Received Saved Chat History"]:
        if i["Media Type"] == "TEXT":
            text_snaps += 1
        elif i["Media Type"] == "MEDIA":
            note_snaps += 1
        elif i["Media Type"] == "NOTE":
            note_snaps += 1
        elif i["Media Type"] == "SHARE":
            share_snaps += 1


    for i in file["Received Unsaved Chat History"]:
        if i["Media Type"] == "TEXT":
            text_snaps += 1
        elif i["Media Type"] == "MEDIA":
            note_snaps += 1
        elif i["Media Type"] == "NOTE":
            note_snaps += 1
        elif i["Media Type"] == "SHARE":
            share_snaps += 1

    for i in file["Sent Unsaved Chat History"]:
        if i["Media Type"] == "TEXT":
            text_snaps += 1
        elif i["Media Type"] == "MEDIA":
            note_snaps += 1
        elif i["Media Type"] == "NOTE":
            note_snaps += 1
        elif i["Media Type"] == "SHARE":
            share_snaps += 1

    for i in file["Sent Saved Chat History"]:
        if i["Media Type"] == "TEXT":
            text_snaps += 1
        elif i["Media Type"] == "MEDIA":
            note_snaps += 1
        elif i["Media Type"] == "NOTE":
            note_snaps += 1
        elif i["Media Type"] == "SHARE":
            share_snaps += 1
    

def display_name_changes():

    FILE = open('../mydata_1669823359244/json/account_history.json')
    file = json.load(FILE)
    the_list = []
    for i in file["Display Name Change"]:
        the_list.append([i["Date"], i["Display Name"]])

    return the_list


def num_of_subscriptions():

    FILE = open('../mydata_1669823359244/json/subscriptions.json')
    file = json.load(FILE)

    public_users = len(file["Public Users"])
    publishers = len(file["Public Users"])
    stories = len(file["Stories"])
    total_subs = stories + public_users + publishers

    return total_subs

def user_profile_info():

    FILE = open('../mydata_1669823359244/json/user_profile.json')
    file = json.load(FILE)
    
    breakdown = []
    for i in file["Breakdown of Time Spent on App"]:
        breakdown.append(i)

    engagement_list = []
    for i in file["Engagement"]:
        engagement_list.append([i["Event"], i["Occurences"]])

    num_of_interest_categories = len(file["Interest Categories"])

    return breakdown


def first_memory():

    FILE = open('../mydata_1669823359244/json/memories_history.json')
    file = json.load(FILE)
    print(f"Your first memory was taken at {file['Saved Media'][-1]['Date']}, it was a {file['Saved Media'][-1]['Media Type']}")
    link_to_memory = file["Saved Media"][-1]["Download Link"]


def first_friend():

    FILE = open('../mydata_1669823359244/json/friends.json')
    file = json.load(FILE)
    print(file["Friends"][0]["Creation Timestamp"])
    the_min = [int(file["Friends"][0]["Creation Timestamp"][0:4]), int(file["Friends"][0]["Creation Timestamp"][5:7]), int(file["Friends"][0]["Creation Timestamp"][8:10]),  int(file["Friends"][0]["Creation Timestamp"][11:13]),  int(file["Friends"][0]["Creation Timestamp"][14:16]), int(file["Friends"][0]["Creation Timestamp"][17:19])]
    the_min_username = file["Friends"][0]["Username"]
    #print(the_min)
    for i in file["Friends"]:
        count = 0
        current = [int(i["Creation Timestamp"][0:4]), int(i["Creation Timestamp"][5:7]), int(i["Creation Timestamp"][8:10]), int(i["Creation Timestamp"][11:13]),  int(i["Creation Timestamp"][14:16]), int(i["Creation Timestamp"][17:19])]
        #print(current)
        
        for k, val in enumerate(current):
            if current[k] <= the_min[k]:
                count += 1
                continue
            else:
                break
        if count == 6:
            the_min = current
            the_min_username = i["Username"]
    
    print(the_min_username)

if __name__ == '__main__':
    main()


