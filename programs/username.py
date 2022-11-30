#!/usr/bin/env python3

# import libraries
import os
import sys
import re
import json

# Constants

FILE = open('json/friends.json')
file = json.load(FILE)

def main():
    print_username()
    


def print_username():

    FILE = open('json/account.json')
    file = json.load(FILE)
    print(file["Basic Information"]["Username"])


# def saved_sna(file):
#     first
#      print(file[][])
    
def first_firend():

    FILE = open('../mydata_1669823359244/json/friends.json')
    file = json.load(FILE)
    print(file["Friends"][0]["Creation Timestamp"])
    the_min = [int(file["Friends"][0]["Creation Timestamp"][0:4]), int(file["Friends"][0]["Creation Timestamp"][5:7]), int(file["Friends"][0]["Creation Timestamp"][8:10]),  int(file["Friends"][0]["Creation Timestamp"][11:13]),  int(file["Friends"][0]["Creation Timestamp"][14:16]), int(file["Friends"][0]["Creation Timestamp"][17:19])]
    print(the_min)
    for i in file["Friends"]:
        count = 0
        current = [int(i["Creation Timestamp"][0:4]), int(i["Creation Timestamp"][5:7]), int(i["Creation Timestamp"][8:10]), int(i["Creation Timestamp"][11:13]),  int(i["Creation Timestamp"][14:16]), int(i["Creation Timestamp"][17:19])]
        print(current)
        whiole
        # for :
        #     count += 1
        # print(i["Creation Timestamp"])
        
    #     if int() == :
    






if __name__ == '__main__':
    main()
