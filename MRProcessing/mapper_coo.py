#!/usr/bin/env python
import sys
import re

def read_input(file):
    for line in file:
        # split the line into words
        yield line.split()

def main(separator='\t'):
    # input comes from STDIN (standard input)
    lines = read_input(sys.stdin)
    topwords = ["financi", "invest", "technolog", "market", "stock", "manual", "servic", "compani", "us", "releas", "report", "presid", "trump", "campaign", "state", "year", "investig", "us", "also", "time", "money", "share", "govern", "health", "trump", "peopl", "like", "crime", "pleas", "year"]
    for line in lines:
        print("line check:",line)
        for topword in topwords:
            if(topword in line):
                for word in line:
                    if (topword == word):
                        continue
                    print ("%s|%s\t%s" % (topword, word, 1))

if __name__ == "__main__":
    main()