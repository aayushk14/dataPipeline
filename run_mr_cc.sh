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

for word in `cat /src/data/MR_output/wc/output_cc/WCloud_cc.txt | cut -f1 | head -n 11 | tail -n 10`
do
  if [ "x$wordlist" == "x" ]
  then
    export wordlist="\"$word\""
  else
    export wordlist="$wordlist, \"$word\""
  fi
done
sed -i 's;\(.*topwords = \)\[.*\];\1\['"$wordlist"'\];g' /src/MRProcessing/mapper_coo.py
# run the MR processing for word cooccurance for top 10 words received from MR word count for all the data source
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper_coo.py -mapper /src/MRProcessing/mapper_coo.py -file /src/MRProcessing/reducer_coo.py -reducer /src/MRProcessing/reducer_coo.py -input /user/dic/input/cc/* -output /user/dic/output_cc
for word in `cat /src/data/MR_output/wc/output_nyt/WCloud_nyt.txt | cut -f1 | head -n 11 | tail -n 10`
do
  if [ "x$wordlist" == "x" ]
  then
    export wordlist="\"$word\""
  else
    export wordlist="$wordlist, \"$word\""
  fi
done
sed -i 's;\(.*topwords = \)\[.*\];\1\['"$wordlist"'\];g' /src/MRProcessing/mapper_coo.py
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper_coo.py -mapper /src/MRProcessing/mapper_coo.py -file /src/MRProcessing/reducer_coo.py -reducer /src/MRProcessing/reducer_coo.py -input /user/dic/input/nyt/* -output /user/dic/output_nyt
for word in `cat /src/data/MR_output/wc/output_tw/WCloud_tw.txt | cut -f1 | head -n 11 | tail -n 10`
do
  if [ "x$wordlist" == "x" ]
  then
    export wordlist="\"$word\""
  else
    export wordlist="$wordlist, \"$word\""
  fi
done
sed -i 's;\(.*topwords = \)\[.*\];\1\['"$wordlist"'\];g' /src/MRProcessing/mapper_coo.py
hadoop jar /usr/lib/hadoop-mapreduce/hadoop-streaming-2.6.0-cdh5.7.0.jar -file /src/MRProcessing/mapper_coo.py -mapper /src/MRProcessing/mapper_coo.py -file /src/MRProcessing/reducer_coo.py -reducer /src/MRProcessing/reducer_coo.py -input /user/dic/input/tw/* -output /user/dic/output_tw

rm -rf /src/data/MR_output/coo/*

# get the output for all the data source word co-occurance result from reducer 
hadoop fs -get /user/dic/output_cc /src/data/MR_output/coo
hadoop fs -get /user/dic/output_tw /src/data/MR_output/coo
hadoop fs -get /user/dic/output_nyt /src/data/MR_output/coo
