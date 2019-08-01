#####################################################################################
#######################       CSE 587 Lab 2       #  ################################
####################### UBITName - aayushku and smishra9 ############################
#####################################################################################
import os
import argparse
import pandas as pd

def get_frequent_words(type):
    DATA_PARENT_DIR='data/MR_output/' + type + '/'
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    for sourceDir in ['tw', 'cc', 'nyt']:
        mid = DATA_PARENT_DIR + 'output_'+ sourceDir
        input_path = os.path.join(fileDir,mid)
        for filename in os.listdir(input_path):
            if filename.startswith("part"):
                input_file = os.path.join(fileDir,mid, filename)
                output_file = os.path.join(fileDir,mid,'WCloud_' + sourceDir + '.txt')
                data = pd.read_csv(input_file, sep="\t", header=None)
                data.columns = ['word', 'count']                    
                df_sort=data.sort_values('count',ascending=False)
                top50=df_sort.head(50)
                top50.to_csv(output_file, header=True, index=False, sep='\t', mode='a')

def main():
    # input filename should end with "WCount"
    ap = argparse.ArgumentParser() 
    ap.add_argument("-operation","--operation_type",required=True,help="word count or word courrence summarization") 
    args = vars(ap.parse_args()) 
    ops = args["operation_type"] 
    get_frequent_words(ops)
    
if __name__ == "__main__":
    main()

#  command to run: python frequentWords.py -operation wc/coo