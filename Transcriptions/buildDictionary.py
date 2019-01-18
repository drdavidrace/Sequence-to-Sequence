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
from embed_defaults.seq_seq_defaults import seq_seq_defaults
from nltk.tokenize import sent_tokenize

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("-c",dest="clean_trans",action='store_true', \
  help='Cleans the transcipt directories')
parser.add_argument("-s",dest="split_sentences",action='store_true', \
  help='Cleans the transcipt directories')
#
args = parser.parse_args()
clean_trans = args.clean_trans
split_sentences = args.split_sentences
simplify_math = True
#
defaults = seq_seq_defaults()
transcript_directories = defaults.get_transcript_dirs()
#
def basic_math_changes(inSentence=None):
    new_line = inSentence.lower().encode("ascii",errors="ignore").decode()
    new_line = new_line.replace("=", " equals ")
    new_line = new_line.replace("^", " to the power of ")
    #Other basic math changes here
    new_line = re.sub('  +',' ',new_line) #replace multiple spaces with a single space
    new_line = new_line.strip()
    return new_line
#
if __name__ == '__main__':
    print('Start of dictionary build.')
    dictionary_set = set()
    #Clean the subdirectories
    if clean_trans:
        print("Cleaning the text subdirectories.")
        for d in transcript_directories:
            p_files = os.listdir(d)
            for f in p_files:
                if (not f.startswith("Cal")) and (not f.startswith(".git")):
                    full_name = os.path.join(d,f)
                    os.remove(full_name)
    #Create the sentence files
    if split_sentences:
        print("Updating the text subdirectories for sentences.")
        for d in transcript_directories:
            p_files = os.listdir(d)
            for f in p_files:
                if f.startswith("Cal"):
                    work_name = os.path.join(d,f)
                    print("WORK FILE:  {:s}".format(work_name))
                    f_name = "S_" + f
                    full_name = os.path.join(d,f_name)
                    #sn = open(full_name,'w')
                    # fn.write("{:s}\n".format(full_name))
                    with open(work_name,'r',encoding='ISO-8859-1') as fn, open(full_name,'w') as sn:
                        for line in fn:
                            line_ascii = line.encode("ascii",errors="ignore").decode()
                            sentences = sent_tokenize(line_ascii)
                            for s in sentences:
                                sn.write("{:s}\n".format(s))
                    # f_name = "S_" + f
                    # full_name = os.path.join(d,f_name)
                    # fn = open(full_name,'w')
                    # fn.write("{:s}\n".format(full_name))
                    # sn.close()
    #Simplify Math
    if simplify_math:
        print("Simplifying the math in sentences.")
        for d in transcript_directories:
            p_files = os.listdir(d)
            for f in p_files:
                if f.startswith("S_"):
                    work_name = os.path.join(d,f)
                    print("WORK FILE:  {:s}".format(work_name))
                    f_name = "M_" + f
                    full_name = os.path.join(d,f_name)
                    mn = open(full_name,'w')
                    # fn.write("{:s}\n".format(full_name))
                    with open(work_name,'r',encoding='ISO-8859-1') as fn:
                        for line in fn:
                            work_line = basic_math_changes(line)
                            mn.write("{:s}\n".format(work_line))
                    # f_name = "S_" + f
                    # full_name = os.path.join(d,f_name)
                    # fn = open(full_name,'w')
                    # fn.write("{:s}\n".format(full_name))
                    mn.close()
    # cur_dir = '.'
    # sub_dirs = [os.path.join(cur_dir,d) for d in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir,d))]
    # print(sub_dirs)
    # #Clean the directories
    # #replace the spaces in the names with -
    # for sd in sub_dirs:
    #     if os.path.basename(sd).upper().startswith("CAL"):
    #         p_files = os.listdir(sd)
    #         for f in p_files:
    #             if f.startswith("PH"):
    #                 f0 = os.path.join(sd,f)
    #                 fn = open(f0,'r')
    #                 for cur_line in fn:
    #                     work_line = cur_line.strip()
    #                     work_line = re.sub(r'(\.|\?|\!)\s*$',"",work_line)
    #                     words = work_line.split()
    #                     for word in words:
    #                         word = word.strip()
    #                         word = re.sub("([\.\?\!\,\[\(\)\]])*([a-zA-Z]+)([\.\?\!\,\[\]\)\(])*",r"\2",word)
    #                         word.strip()
    #                         if len(word) > 0:
    #                             dictionary_set.add(word)
    #                 fn.close()
    # #build the histogram
    # text_set = sorted(dictionary_set)
    # text_hist = {}
    # for t in text_set:
    #     text_hist[t] = 0
    # for sd in sub_dirs:
    #     if os.path.basename(sd).upper().startswith("CAL"):
    #         p_files = os.listdir(sd)
    #         for f in p_files:
    #             if f.startswith("PH"):
    #                 f0 = os.path.join(sd,f)
    #                 fn = open(f0,'r')
    #                 for cur_line in fn:
    #                     work_line = cur_line.strip()
    #                     work_line = re.sub(r'(\.|\?|\!)\s*$',"",work_line)
    #                     words = work_line.split()
    #                     for word in words:
    #                         word = word.strip()
    #                         word = re.sub("([\.\?\!\,\[\(\)\]])*([a-zA-Z]+)([\.\?\!\,\[\]\)\(])*",r"\2",word)
    #                         word.strip()
    #                         if len(word) > 0:
    #                             text_hist[word] = text_hist[word] + 1
    #                 fn.close()
    # text_list =[(k,text_hist[k]) for k in sorted(text_hist, key=text_hist.get,reverse=True)]
    # #Save the text_hist in a pickle
    # hist_file_name = os.path.join(cur_dir,"video.hist.pkl")
    # print(len(text_hist))
    # if os.path.isfile(hist_file_name):
    #     os.remove(hist_file_name)
    # with open(hist_file_name, 'wb') as fn:
    #     pickle.dump(text_hist, fn, protocol=pickle.HIGHEST_PROTOCOL)
