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

if __name__ == '__main__':
    main()
