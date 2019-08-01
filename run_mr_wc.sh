#!/bin/bash

# make a directory in hdfs and copy the processed data to hadoop
hadoop fs -mkdir -p /user/dic
hadoop fs -mkdir -p /user/dic/input /user/dic/input/tw /user/dic/input/nyt /user/dic/input/cc

# command to remove input files from hdfs if present
hadoop fs -rm -r -f -skipTrash /user/dic/input/cc/* /user/dic/input/tw/* /user/dic/input/nyt/*

# put the input files at corresponding directory
hadoop fs -put /src/data/cc/processedData/*.txt /user/dic/input/cc
hadoop fs -put /src/data/tw/processedData/*.txt /user/dic/input/tw
hadoop fs -put /src/data/nyt/processedData/*.txt /user/dic/input/nyt

# command to remove result files from hdfs
hadoop fs -rm -r -f -skipTrash /user/dic/output*
rm -rf /src/data/MR_output/wc/*

# run the MR processing for word count for all the data source
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper.py -mapper /src/MRProcessing/mapper.py -file /src/MRProcessing/reducer.py -reducer /src/MRProcessing/reducer.py -input /user/dic/input/cc/* -output /user/dic/output_cc
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper.py -mapper /src/MRProcessing/mapper.py -file /src/MRProcessing/reducer.py -reducer /src/MRProcessing/reducer.py -input /user/dic/input/tw/* -output /user/dic/output_tw
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper.py -mapper /src/MRProcessing/mapper.py -file /src/MRProcessing/reducer.py -reducer /src/MRProcessing/reducer.py -input /user/dic/input/nyt/* -output /user/dic/output_nyt

# get the output for all the data source word count result from reducer 
hadoop fs -get /user/dic/output_cc /src/data/MR_output/wc
hadoop fs -get /user/dic/output_tw /src/data/MR_output/wc
hadoop fs -get /user/dic/output_nyt /src/data/MR_output/wc
