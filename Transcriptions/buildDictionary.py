#!/usr/bin/env python
"""
This processes a set of mathematical transcriptions that rely on words (rather than a lot of symbols)
to build a dictionary.

The dictionary is then saved as a python object


"""

import os, sys
import subprocess
import argparse
import re
import pickle

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
# parser.add_argument("--subs",dest="subs",action='store_true')

# args = parser.parse_args()

# curr_phase_count = 0
# process_subs = args.subs


if __name__ == '__main__':
    print('Start of dictionary build.')
    dictionary_set = set()
    #Get the directories
    cur_dir = '.'
    sub_dirs = [os.path.join(cur_dir,d) for d in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir,d))]
    print(sub_dirs)
    #Clean the directories
    #replace the spaces in the names with -
    for sd in sub_dirs:
        if os.path.basename(sd).upper().startswith("CAL"):
            p_files = os.listdir(sd)
            for f in p_files:
                if f.startswith("PH"):
                    f0 = os.path.join(sd,f)
                    fn = open(f0,'r')
                    for cur_line in fn:
                        work_line = cur_line.strip()
                        work_line = re.sub(r'(\.|\?|\!)\s*$',"",work_line)
                        words = work_line.split()
                        for word in words:
                            word = word.strip()
                            word = re.sub("([\.\?\!\,\[\(\)\]])*([a-zA-Z]+)([\.\?\!\,\[\]\)\(])*",r"\2",word)
                            word.strip()
                            if len(word) > 0:
                                dictionary_set.add(word)
                    fn.close()
    #build the histogram
    text_set = sorted(dictionary_set)
    text_hist = {}
    for t in text_set:
        text_hist[t] = 0
    for sd in sub_dirs:
        if os.path.basename(sd).upper().startswith("CAL"):
            p_files = os.listdir(sd)
            for f in p_files:
                if f.startswith("PH"):
                    f0 = os.path.join(sd,f)
                    fn = open(f0,'r')
                    for cur_line in fn:
                        work_line = cur_line.strip()
                        work_line = re.sub(r'(\.|\?|\!)\s*$',"",work_line)
                        words = work_line.split()
                        for word in words:
                            word = word.strip()
                            word = re.sub("([\.\?\!\,\[\(\)\]])*([a-zA-Z]+)([\.\?\!\,\[\]\)\(])*",r"\2",word)
                            word.strip()
                            if len(word) > 0:
                                text_hist[word] = text_hist[word] + 1
                    fn.close()
    text_list =[(k,text_hist[k]) for k in sorted(text_hist, key=text_hist.get,reverse=True)]
    #Save the text_hist in a pickle
    hist_file_name = os.path.join(cur_dir,"video.hist.pkl")
    print(len(text_hist))
    if os.path.isfile(hist_file_name):
        os.remove(hist_file_name)
    with open(hist_file_name, 'wb') as fn:
        pickle.dump(text_hist, fn, protocol=pickle.HIGHEST_PROTOCOL)
