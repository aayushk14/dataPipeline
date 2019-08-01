#####################################################################################
#######################       CSE 587 Lab 2       #  ################################
####################### UBITName - aayushku and smishra9 ############################
#####################################################################################


#-----------------------------------------------------------------------
# To get Twitter data using tweepy Stream API
#-----------------------------------------------------------------------

from twitter import *

import sys
import random
import json
import os.path
import time
import datetime
import numpy
import pytz
import os

#Import from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

access_key = ""
access_secret =  ""
consumer_key =  ""
consumer_secret =  ""

# USA Economy is our main topic and we have subtopics:
# healthcare, technology, treding, crime
# We feel these subtopics will have impact on USA Economy in some way
topicsSearch = ['nasdaq', 'exchange', 'trading', 'trader', 'share', 'stocks', 'retailers',
    'money', 'commodity', 'diet', 'disease', 'hospital', 'patient',
    'fitness', 'health', 'analysis', 'blockchain', 'technology', 'microsoft',
    'digital', 'corruption', 'crime', 'alcohol', 'fraud', 'government', 'judicial',
    'authority', 'drugs', 'conspiracy', 'felony']

max_iter = 30

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

class UBListener(StreamListener):
    def __init__(self, file, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        self.fileHandle = file
        super(UBListener, self).__init__() 

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            try:
                jsonData = json.loads(data, encoding='utf-8')
                #If its a retweet text then discard
                if 'RT @' in jsonData["text"]:
                    return True
                self.fileHandle.writelines(jsonData["text"])
                self.fileHandle.writelines('\n')
            except BaseException as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print("Error on_data: %s" % str(e))
                print(exc_type, fname, exc_tb.tb_lineno)        
            return True
        else:
            return False
    
    def on_error(self, status):
        print(status)
        return True


fileDir = os.path.dirname(os.path.realpath('__file__'))
input_path = os.path.join(fileDir, 'data', 'tw')

while 1:
    r = random.randint(1, 10000)
    outfile = os.path.join(input_path,
                'tweeter_' + str(r) + '.txt')
    filejson = open(outfile, 'w', encoding='utf-8')
    last_id = None
    iter_count = 0

    while iter_count < max_iter:
        #Get any one key word randomly from the topic at each 1 min and get the tweet
        topicsIndex = numpy.random.choice(numpy.arange(0, len(topicsSearch)))
        hashTagToSearch = topicsSearch[topicsIndex]
        twitter_stream = Stream(auth, UBListener(file=filejson))
        #To search only in usa and language in english
        twitter_stream.filter(track=[hashTagToSearch, 'usa'], languages=['en'])
        iter_count += 1

    filejson.close()