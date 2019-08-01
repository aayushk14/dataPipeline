#####################################################################################
#######################       CSE 587 Lab 2       #  ################################
####################### UBITName - aayushku and smishra9 ############################
#####################################################################################

import requests
import argparse
import time
import json
import gzip
from io import BytesIO
from bs4 import BeautifulSoup
import sys
import csv
from glob import glob
import warc
import urllib
import urllib.request
import re
from langdetect import detect

# List of available indices and we are taking for two months i.e. Feb and March 2019
index_list = ["2019-09", "2019-13"]

# USA Economy is our main topic and we have subtopics:
# healthcare, technology, treding, crime
# We feel these subtopics will have impact on USA Economy in some way
keywords = 'nasdaq' or 'exchange' or 'trading' or 'trader' or 'share' or 'stocks' or 'retailers' or 'money' or 'commodity' or 'diet' or 'disease' or 'hospital' or 'patient' or 'fitness' or 'health' or 'analysis' or 'blockchain' or 'technology' or 'microsoft' or 'digital' or 'corruption' or 'crime' or 'alcohol' or 'fraud' or 'government' or 'judicial' or 'authority' or 'drugs' or 'conspiracy' or 'felony'

def search_domain(domain):
    record_list = []
    print ("[*] Trying target domain: %s" % domain)
    
    for index in index_list:
        print ("[*] Trying index %s" % index)
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s/&filter=mime:text/html&limit=600&output=json" % domain

        response = requests.get(cc_url)
        
        if response.status_code == 200:
            records = response.content.splitlines()
            for record in records:
                record_list.append(json.loads(record))  
            print ("[*] Added %d results." % len(records))
    print ("[*] Found a total of %d hits." % len(record_list))
    return record_list     

def download_page(records):
    # We'll get the file via HTTPS so we don't need to worry about S3 credentials
    prefix = 'https://commoncrawl.s3.amazonaws.com/'
    fcc=open("data/cc/cc_economy.txt",'w', encoding='utf-8')
    c = 1
    link_count = 0
    for record in records:
        offset, length = int(record['offset']), int(record['length'])
        offset_end = offset + length - 1
        dummy = record['filename'].replace('/warc/','/wet/').replace('.warc.','.warc.wet.')
        link = prefix + dummy
        print("check done:",link)
        holder = "data/cc/cc_data/" + str(c) + ".warc.wet.gz"
        try:
            if(urllib.request.urlretrieve(link,holder)):
                c = c + 1
            warc_files = glob(holder)
            # Process each of the WARC files we found
            for fn in warc_files:
                f = warc.open(fn)
                for record in f:
                    url = record.header.get('warc-target-uri', None)
                    if not url:
                        continue
                    text = record.payload.read()
                    if(detect(text.decode("utf-8")) == 'en'):
                        if  keywords in text.decode("utf-8").lower():
                            fcc.write(str(text, 'utf-8'))
                            fcc.write('\n')
                            link_count = link_count + 1
        except Exception:
            pass
    fcc.close()
    print("number of links parsed:",link_count)

if __name__ == '__main__':
    print("Starting CommonCrawl Search")
    #Finds domains related to wikipedia
    domain = "*.wikipedia.org"
    record_list = search_domain(domain)
    download_page(record_list)