#!/usr/bin/env python
"""
This processes a set of mathematical transcriptions that rely on words and compares the words in the dictionary to the 
words in a standard embedding



"""

import os, sys
import subprocess
import argparse
import re
import shutil
import pickle
import bcolz
import numpy as np
from embed_defaults.build_glove_names import seq_seq_defaults

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("-c",dest="create_word_vector",action='store_true')

args = parser.parse_args()
create_word_vector = args.create_word_vector
#
#  Defaults
#
#  Working directories
defaults = seq_seq_defaults()
glove_dir_name = defaults.get_glove_dir_name()
work_glove_dir = defaults.get_work_glove_dir()
work_dir = defaults.get_work_dir_name()
if not os.path.isdir(work_dir):
    print("The working directory path {:s} does not exist.  Exiting".format(work_dir))
    sys.exit()
if not os.path.isdir(work_glove_dir):
    os.makedirs(work_glove_dir,mode=0o777,exist_ok=True)
#  Glove Information
vec_len = defaults.get_vec_len()
glove_vector_name = defaults.get_glove_vector_name()
glove_word_pickle_name = "glove." + glove_vector_name + "_word.pkl"
glove_idx_pickle_name = "glove." + glove_vector_name + "_idx.pkl"
glove_vector_dat = "glove." + glove_vector_name + ".dat"
#  Existing Files
glove_dir = os.path.join(cur_dir,glove_dir_name)
glove_file = os.path.join(glove_dir,glove_file_name)
working_glove_file = os.path.join(work_glove_dir,glove_file_name)
if not os.path.isfile(working_glove_file):
    if not os.path.isfile(glove_file):
        print("The glove file {:s} does not exist.  Exiting".format(glove_file))
        sys.exit()
    else:
        shutil.copy2(glove_file,working_glove_file)
#
working_glove_vectors = os.path.join(work_glove_dir,glove_vector_dat)
working_glove_word_pickle = os.path.join(work_glove_dir,glove_word_pickle_name)
working_glove_idx_pickle = os.path.join(work_glove_dir,glove_idx_pickle_name)
video_data_pickle = os.path.join(cur_dir,"video.hist.pkl")
#
def create_base_words():
    """Create the basic glove information in the working directory.
    This isn't very smart.  Ideally it would check the dates and only do the work
    if the dates are out of alignment, but this is quick and dirty.
    """
    words = []
    idx = 0
    word2idx = {}
    if os.path.isfile(working_glove_vectors):
        os.remove(working_glove_vectors)
    if os.path.isfile(working_glove_word_pickle):
        os.remove(working_glove_word_pickle)
    if os.path.isfile(working_glove_idx_pickle):
        os.remove(working_glove_idx_pickle)
    vectors = bcolz.carray(np.zeros(1), rootdir=working_glove_vectors, mode='w')
    with open(working_glove_file, 'rb') as fn:
        for l in fn:
            line = l.decode().split()
            try:
                vect = np.array(line[1:]).astype(np.float)
                if vect.shape[0] == vec_len:
                    word = line[0]
                    words.append(word)
                    word2idx[word] = idx
                    idx += 1
                    vectors.append(vect)
            except:
                print(line)
                print(idx)
                print(len(line))

    num_entries = int(vectors.shape[0] / vec_len)
    print(num_entries)
    vectors = bcolz.carray(vectors[1:].reshape((num_entries, vec_len)), rootdir=working_glove_vectors, mode='w')
    vectors.flush()
    pickle.dump(words, open(working_glove_word_pickle, 'wb'))
    pickle.dump(word2idx, open(working_glove_idx_pickle, 'wb'))

def get_word_vector():
    vectors = bcolz.open(working_glove_vectors)[:]
    words = pickle.load(open(working_glove_word_pickle, 'rb'))
    word2idx = pickle.load(open(working_glove_idx_pickle, 'rb'))
    glove = {w: vectors[word2idx[w]] for w in words}
    return glove

if __name__ == "__main__":
    if create_word_vector:
        create_base_words()
    glove = get_word_vector()
    video_hist = pickle.load(open(video_data_pickle,'rb'))
    number_in = 0
    number_not_in = 0
    not_in = set()
    for k in video_hist.keys():
        if k in glove:
            number_in += 1
        else:
            number_not_in += 1
            not_in.add(k)
    print("Number in {:d}".format(number_in))
    print("Number not in {:d}".format(number_not_in))
    print(not_in)
    print(glove['start'])
    print(glove['non-increasing'])
    print(glove['1234'])

    print(np.linalg.norm(glove['start']-glove['starts']))
    print(np.linalg.norm(glove['start']-glove['base']))
    print(np.linalg.norm(glove['calc']-glove['calculus']))
    print(np.linalg.norm(glove['catholic']-glove['calculus']))
