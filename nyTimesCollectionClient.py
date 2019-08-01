#####################################################################################
#######################       CSE 587 Lab 2       #  ################################
####################### UBITName - aayushku and smishra9 ############################
#####################################################################################

import os
import requests
import argparse
import jsonpickle
import json
import datetime
import numpy
import time
from bs4 import BeautifulSoup
count = 0

def get_file():
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    rel_path = 'data/nyt/raw_nyt.txt'
    #For accessing the file in a folder contained in the current folder
    file_name = os.path.join(fileDir, rel_path)
    return file_name

def get_ny_data(ny_api):
    global count
    filename = get_file()
    f=open(filename,'a')
    headers = {'Content-type': 'application/json'}
    for a in range(0,10):
        try:
            links = []
            url = ny_api+'&page='+str(a)
            print("API endpoint:",url)
            #articles = api.search(q="shooting", begin_date=20180406,end_date=20180407,page=a)
            articles = requests.get(url,headers=headers)
            ny_data = json.loads(articles.content)
            for i in range(0,len(ny_data['response']['docs'])):
                web_url = ny_data['response']['docs'][i]['web_url']
                links.append(web_url)
                count = count + 1
            print("URLS----: ",links)
            print("\n")
            for url in links:
                data = requests.get(url)
                soup = BeautifulSoup(data.content, 'html.parser')
                soup.prettify()
                for j in range((len(soup.find_all('p')))-3):
                    f.write(soup.find_all('p')[j].get_text())
                f.write("\n")
        except Exception as e:
            time.sleep(60)
            print(count," articles collected for selected period with error")
    f.close()
    print(count," articles collected for selected period")

# writing to the json file
def save_ny_data(query, data):
    file = query + '_ny.json'
    with open(file, 'a', encoding='utf8') as ny_json:
        ny_json.write(data)

phrases = ['nasdaq', 'exchange', 'trading', 'trader', 'share', 'stocks', 'retailers',
    'money', 'commodity', 'diet', 'disease', 'hospital', 'patient',
    'fitness', 'health', 'analysis', 'blockchain', 'technology', 'microsoft',
    'digital', 'corruption', 'crime', 'alcohol', 'fraud', 'government', 'judicial',
    'authority', 'drugs', 'conspiracy', 'felony']

def main():
    try:
        current_date = datetime.datetime.now()
        date =current_date.strftime("%Y%m%d")
        begin = "20190310"
        print("date check:",date)
        for phrase in phrases:
            #url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?fq='+phrase+'&facet_field=day_of_week&facet=true&begin_date='+begin+'&end_date='+date+'&api-key=k1XrMtD4XfjX4IU7MKuxITJA1vpGgTZX'
            #https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=news_desk:(%22technology%22)&glocations:(%22USA%22)&api-key=k1XrMtD4XfjX4IU7MKuxITJA1vpGgTZX
            url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?fq='+phrase+'&facet_field=day_of_week&facet=true&begin_date='+begin+'&end_date='+date+'&glocations:("USA")&api-key=q54vgEeqyyr2xPubZrlsK0PBkAyDzJN1'
            get_ny_data(url)

    except KeyboardInterrupt:
        print ("Disconnecting from NY Times... ")
        print ("Done")      

if __name__ == '__main__':
    main() 

'''U.S Economy 
1. Health care
2. Technology
3. Trading
4. crime
''' 