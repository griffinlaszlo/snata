#!/usr/bin/env python3

# import libraries
import os
import sys
import re
import json
import datetime
# Constants


def main():
    
    #print_username()
    first_firend()

    

def print_username():

    FILE = open('uploads/json/account.json', encoding="utf8")
    file = json.load(FILE)

    # FILE = open('json/account.json')
    # file = json.load(FILE)
    print(file["Basic Information"]["Username"])

# def first_memory():

#     FILE = open('../mydata_1669823359244/json/memories_history.json')
#     file = json.load(FILE)

#     #print(file[][])



# def saved_sna(file):
#     first
#      print(file[][])
    
def first_firend():
    FILE = open('uploads/json/account.json', encoding="utf8")
    file = json.load(FILE)
    username = file["Basic Information"]["Username"]

    FILE = open('uploads/json/friends.json', encoding="utf8")
    file = json.load(FILE)

    print(username)
    #print(file["Friends"][0]["Creation Timestamp"])
    the_min = [int(file["Friends"][0]["Creation Timestamp"][0:4]), int(file["Friends"][0]["Creation Timestamp"][5:7]), int(file["Friends"][0]["Creation Timestamp"][8:10]),  int(file["Friends"][0]["Creation Timestamp"][11:13]),  int(file["Friends"][0]["Creation Timestamp"][14:16]), int(file["Friends"][0]["Creation Timestamp"][17:19]), file["Friends"][0]["Username"], file["Friends"][0]["Display Name"]]
    the_min_username = file["Friends"][0]["Username"]
    #print(the_min)
    the_min_array = []
    for i in file["Friends"]:
        count = 0
        current = [int(i["Creation Timestamp"][0:4]), int(i["Creation Timestamp"][5:7]), int(i["Creation Timestamp"][8:10]), int(i["Creation Timestamp"][11:13]),  int(i["Creation Timestamp"][14:16]), int(i["Creation Timestamp"][17:19]), i["Username"], i["Display Name"]]
        #print(current)
        the_min_array.append(current)

        # year is less than
        if (current[0] < the_min[0] and not current[6] == "teamsnapchat" and not current[6] == username):
            the_min = current
        # year is equal
        elif (current[0] == the_min[0]):
            # month is less than
            if (current[1] < the_min[1] and not current[6] == "teamsnapchat" and not current[6] == username):
                the_min = current
            # month is equal
            elif (current[1] == the_min[1]):
                # day is less than
                if (current[2] < the_min[2] and not current[6] == "teamsnapchat" and not current[6] == username):
                    the_min = current
                # day is equal
                elif (current[2] == the_min[2]):
                    # if hour is less than
                    if (current[3] < the_min[3] and not current[6] == "teamsnapchat" and not current[6] == username):
                        the_min = current
                    # hour is equal
                    elif (current[3] == the_min[3]):
                        # minute is less than
                        if (current[4] < the_min[4] and not current[6] == "teamsnapchat" and not current[6] == username):
                            the_min = current
                        # minute is equal
                        elif (current[4] == the_min[4]):
                            # seconds is less than
                            if (current[5] < the_min[5] and not current[6] == "teamsnapchat" and not current[6] == username):
                                the_min = current

        # for k, val in enumerate(current):
        #     if current[k] <= the_min[k]:
        #         count += 1
        #         continue
        #     else:
        #         break
        # if count == 6:
        #     the_min = current
        #     the_min_username = i["Username"]
    
    the_min_array = sorted(the_min_array)
    print(the_min_array[2:7])
    
    the_min_username = the_min[6]
    the_min_display = the_min[7]
    print(the_min_username, the_min_display)

if __name__ == '__main__':
    main()

