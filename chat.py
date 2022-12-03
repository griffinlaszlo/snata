#!/usr/bin/env python3

# python headers
import sys
import os
import re
import json

# open chat_history.json file
FILE = open('chat_history.json')
file = json.load(FILE)

for key, value in file.items():
    # print only the first key and value
    # if key is received saved chat history
    if key == 'Received Saved Chat History':
        # dict for received usernames
        received = {}
        media = {}
        text = {}
        for n in value:
            for k, v in n.items():
                if k == 'From':
                    # append v to received dict with count
                    received[v] = received.get(v, 0) + 1
                if k == 'Media Type':
                    media[v] = media.get(v, 0) + 1
                if k == 'Text':
                    text[v] = text.get(v, 0) + 1


        print()
        print('Top 5 Received Saved Chat History:')
        print()
        for k, v in sorted(received.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(k, v)

        # rank media types by count
        print()
        print('Media Types:')
        print()
        for k, v in sorted(media.items(), key=lambda x: x[1], reverse=True):
            print(k, v)

        print()
        print('Top 10 Text Sayings:')
        print()
        count=0
        for k, v in sorted(text.items(), key=lambda x: x[1], reverse=True):
            if k != '':
                count += 1
                print(k, v)
            if count == 10:
                break

            



'''
    # if key is sent saved chat history
    if key == 'Sent Saved Chat History':
        # dict for sent usernames
        sent = {}
        for n in value:
            for k, v in n.items():
                if k == 'To':
                    # append v to sent dict with count
                    sent[v] = sent.get(v, 0) + 1
        # print out top 5 sent usernames and count in a print statement
        print('Top 5 Sent Saved Chat History:')
        print()
        for k, v in sorted(sent.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(k, v)

    # if key is received unsaved chat history
    print()
    if key == 'Received Unsaved Chat History':
        # dict for received usernames
        received = {}
        for n in value:
            for k, v in n.items():
                if k == 'From':
                    # append v to received dict with count
                    received[v] = received.get(v, 0) + 1

            # create ratio of sent to received
        ratio = {}
        for k, v in sent.items():
            if k in received:
                ratio[k] = v / received[k]
        # print out top 5 ratio of sent to received

        print('Top 5 Ratio of Sent to Received:')
        print()
        for k, v in sorted(ratio.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(k, v)
        print()




        # print out top 5 received usernames and count in a print statement
        print('Top 5 Received Unsaved Chat History:')
        print()
        for k, v in sorted(received.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(k, v)

    # if key is sent unsaved chat history
    if key == 'Sent Unsaved Chat History':
        # dict for sent usernames
        sent = {}
        for n in value:
            for k, v in n.items():
                if k == 'To':
                    # append v to sent dict with count
                    sent[v] = sent.get(v, 0) + 1
        # print out top 5 sent usernames and count in a print statement

        print('Top 5 Sent Unsaved Chat History:')
        print()
        for k, v in sorted(sent.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(k, v)

        # create ratio of sent to received
        ratio = {}
        for k, v in sent.items():
            if k in received:
                ratio[k] = v / received[k]

    
'''

