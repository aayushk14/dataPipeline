#####################################################################################
#######################       CSE 587 Lab 2 README        ###########################
####################### UBITName - aayushku and smishra9 ###########################
#####################################################################################

1. We have chosen a topic "Economy" for USA for our study as part of this Lab.

2. Then we carefully decided the subtopics - Crime, Health, Stock Market and Technology which impact USA economy in some way
   Again for these subtopic we have choosen some frequent words which we searched in all our data source to get usefull data.
   These words are:
	'nasdaq', 'exchange', 'trading', 'trader', 'share', 'stocks', 'retailers', 'drugs',
	'money', 'commodity', 'diet', 'disease', 'hospital', 'patient', 'felony', 'authority',
	'fitness', 'health', 'analysis', 'blockchain', 'technology', 'microsoft', 'judicial',
	'digital', 'corruption', 'crime', 'alcohol', 'fraud', 'government', 'conspiracy'


2. Data aggregation from three different source - twitter, NYTimes and Common Crawl data.

Files and Description
=================================
part1:
======
Data collection scripts:
	ccCollectionClient.py 		- To collect data under data/cc from Common Crawl.
	nyTimesCollectionClient.py      - To collect data under data/nyt from NYTimes.
	tweetCollectionClient.py	- To collect data under data/twt from twitter.

Data cleaning in all the data collection:
dataCleanUtility.py				- This utility cleans all text files present at
									data/cc
									data/tw
									data/nyt
								  and creates the processed files at
								    data/cc/processedData
									data/tw/processedData
									data/nyt/processedData
									
The code for Map and Reduce present at MRProcessing:
mapper.py      - Mapper for Word count
reducer.py     - Reducer for word count
mapper_coo.py  - Mapper for Word co-occurance
reducer_coo.py - Reducer for word co-occurance

The automated scripts to be used for running MR processing for word count and word co-occurance are:

1. run_mr_wc.sh - Takes input from data/cc/processedData, data/tw/processedData, data/nyt/processedData
               and generate the word count result at data/MR_output/wc.

2. run_mr_cc.sh - Takes input from data/cc/processedData, data/tw/processedData, data/nyt/processedData
               and generate the word co-occurance result at data/MR_output/coo.

python frequentWords.py -operations <wc/coo> - this command will sort the word count output present at data/MR_output/wc.

3.All the images and visualisation files are available at data/output_images.

Pre-requisite for running hadoop docker instance:
docker run --hostname=quickstart.cloudera --privileged=true -t -i -v /Users/apple/Documents/sem2/DIC/projects/lab2:/src --publish-all=true -p 8888 cloudera/quickstart /usr/bin/docker-quickstart
