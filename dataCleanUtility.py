#####################################################################################
#######################       CSE 587 Lab 2       #  ################################
####################### UBITName - aayushku and smishra9 ############################
#####################################################################################
import json
import os
import numpy
import sys
import os.path
import re
import emoji
import nltk
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from stemming.porter2 import stem

def clean_tweet_url(tweet):
    tweet = re.sub('http\S+\s*', '', tweet)  # remove URLs
    return tweet

emoticons_str = """
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "]+", flags=re.UNICODE)

def extract_emojis(str):
    listE = [c for c in str if c in emoji.UNICODE_EMOJI]
    return listE

def clean_tweet(tweet):
    tweet = re.sub('RT|cc', '', tweet)  # remove RT and cc if any. Though it will come to this in case of retweet
    tweet = re.sub('#\S+', '', tweet)  # remove hashtags
    tweet = re.sub('@\S+', '', tweet)  # remove mentions
    tweet = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), '', tweet)  # remove punctuations
    tweet = re.sub('\s+', ' ', tweet)  # remove extra whitespace
    tweet = re.sub('^\s', '', tweet) 
    return tweet

DATA_PARENT_DIR='data'
fileDir = os.path.dirname(os.path.realpath('__file__'))
#for sourceDir in ['nyt', 'tw', 'cc']:
for sourceDir in ['nyt']:
    input_path = os.path.join(fileDir, DATA_PARENT_DIR, sourceDir)
    for filename in os.listdir(input_path):
        if filename.endswith(".txt"):
            try:
                input_file = os.path.join(fileDir, DATA_PARENT_DIR, sourceDir, filename)
                output_file = os.path.join(fileDir, DATA_PARENT_DIR, sourceDir, 'processedData', filename)

                textOutFile = open(output_file, 'w', encoding='utf-8')
                with open(input_file, 'r', encoding='utf-8') as file:
                    for text in file:
                        text = re.sub(r"^AdvertisementSupported.*— ", '', text)
                        text = ''.join([i for i in text if not i.isdigit()])

                        if 'RT @' in text:
                            text = text[4:]
                        
                        text = clean_tweet_url(text)
                        text = re.sub(r"([:=;X][oO\-]?[D\)\]\(\]/\\OpP]) ", '', text)
                        emojis = extract_emojis(text)
                        tweet_xx = clean_tweet(text)

                        for em in emojis[:]:
                            tweet_xx = re.sub(em,'',tweet_xx)
                        tweet_xx=re.sub(emoji_pattern,'',tweet_xx)

                        stop = set(stopwords.words('english'))
                        sentence =  " ".join([word.lower() for word in word_tokenize(tweet_xx) if word.lower() not in stop])
                        sentence =  " ".join([word for word in word_tokenize(sentence) if wordnet.synsets(word)])
                        sentence = " ".join([stem(word) for word in word_tokenize(sentence)])
                        textOutFile.writelines(sentence + '\n')
                    
                textOutFile.close()
            except BaseException as e:
                print('processing file: %s' % filename)
                print("Error while search: %s" % str(e))
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                continue