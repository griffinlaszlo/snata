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
    first_firend()

    

def print_username():

    FILE = open('uploads/account.json')
    file = json.load(FILE)

    # FILE = open('json/account.json')
    # file = json.load(FILE)
    print(file["Basic Information"]["Username"])

def first_memory():

    FILE = open('../mydata_1669823359244/json/memories_history.json')
    file = json.load(FILE)

    #print(file[][])



# def saved_sna(file):
#     first
#      print(file[][])
    
def first_firend():

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

# if __name__ == '__main__':
#     main()

