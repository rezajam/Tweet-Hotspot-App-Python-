"""
    This script connects to Twitter Streaming API, gets tweets with '#' and
    forwards them through a local connection in port 9009. That stream is
    meant to be read by a spark app for processing. Both apps are designed
    to be run in Docker containers.

    To execute this in a Docker container, do:
    
        docker run -it -v $PWD:/app --name twitter -p 9009:9009 python bash

    and inside the docker:

        pip install -U git+https://github.com/tweepy/tweepy.git
        python twitter_app.py

    (we don't do pip install tweepy because of a bug in the previous release)
    For more instructions on how to run, refer to final slides in tutorial 8

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Author: Tilemachos Pechlivanoglou

"""

# from __future__ import absolute_import, print_function

import socket
import sys
import json


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Stream
import tweepy
# import dataset
import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
nltk.download('vader_lexicon')
global word4
import csv
sia = SIA()
# SEP = ';'
# csv = open('OutputStreaming.csv','a')
# csv.write('Date' + SEP + 'Text' + SEP + 'Location' + SEP + 'Number_Follower' + SEP + 'User_Name' + SEP + 'Friends_count\n')

# Replace the values below with yours
consumer_key="XXXXXXXXX"
consumer_secret="XXXXXXXXX"
access_token="XXXXXXXXX"
access_token_secret="XXXXXXXXX"

with open('OutputStreaming6.csv', 'a') as f:
    writer = csv.writer(f)
    writer.writerow(['Id', 'Latitude', 'Longitude', 'Hashtag', 'Sentiment'])

class TweetListener(StreamListener):
    """ A listener that handles tweets received from the Twitter stream.

        This listener prints tweets and then forwards them to a local port
        for processing in the spark app.
    """
    def on_status(self, status):
        # print (status.author.id, status.geo, status.text)
        coord_dict = status.geo
        idd = status.author.id
        textt =  status.text
        textt = textt.replace('\n', ' ')
        temp = re.sub(r'[^a-zA-Z#]', ' ', textt)
        word = ''
        word4 = ''
        temp = re.sub(r'[\s]', ' ', temp)
        text = re.sub(r'[^a-zA-Z0-9\s#]', ' ', textt)
        senti = text
        sent = 0
        # temp = temp.split(' ')
        if textt.find('#') != -1:
            hashtags = text.split(" ")
            # temp2 = textt.split(" ")
            # word = ' '
            # if len(word) >0
            # print(hashtags)x
            for x in hashtags:
                if len(x) > 0:
                    if x[0] == '#':
                        word += x
            word3 = []
            word2 = word.split('#')
            if len(word2) > 1:
                for x in word2:
                    if x != '':
                        x = '#' + x
                        word3.append(x)
                # print(word2)

            word4 = ', '.join(word3)
            # print(temp)
            # for x in temp:
            #     if(x != '' and x[0] == '#'):b22
            #         word += x
        
        score = sia.polarity_scores(senti)
        corp = score.get('compound')
        if (corp > 0):
            sent = 1.0
        elif corp < 0:
            sent = -1.0
        else:
            sent = 0.0

        # print(temp)

        # Writing status data
        with open('OutputStreaming6.csv', 'a') as f:
            writer = csv.writer(f)
            if(coord_dict != None):
                if('coordinates' in coord_dict.keys() and len(word4)>0):
                    for hashtag in word3:
                        # print (hashtag)
                        writer.writerow([idd, float(coord_dict['coordinates'][0]),float(coord_dict['coordinates'][1]) , hashtag, float(sent)])

    def on_error(self, status):
        print(status)






# ==== setup local connection ====


# with open('OutputStreaming5.csv', 'a') as f:
#     writer = csv.writer(f)
#     writer.writerow(['ID',  'Lat',  'Long', 'Text', 'Sentiment'])
# IP and port of local machine or Docker

TCP_IP = socket.gethostbyname(socket.gethostname()) # returns local IP
TCP_PORT = 9009

# setup local connection, expose socket, listen for spark app
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))
# s.listen(1)
print("Waiting for TCP connection...")

# if the connection is accepted, proceed
# conn, addr = s.accept()
print("Connected... Starting getting tweets.")


# ==== setup twitter connection ====
listener = TweetListener()
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, listener)

language = ['en']
locations = [-130,-20,100,50]

# get filtered tweets, forward them to spark until interrupted
try:
    stream.filter(languages=language, locations = locations)
    # stream.filter(l)
except KeyboardInterrupt:
    csv.close()
    s.shutdown(socket.SHUT_RD)

