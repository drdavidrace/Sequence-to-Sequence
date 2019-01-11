#!/usr/bin/env python
"""
This processes a set of mathematical transcriptions that rely on words and compares the words in the dictionary to the 
words in a standard embedding



"""

import os, sys
import subprocess
import argparse
import re
import pickle
import bcolz
import numpy as np

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("-c",dest="create_word_vector",action='store_true')

args = parser.parse_args()
create_word_vector = args.create_word_vector
#
#  Defaults
#
glove_dir_name = "glove-base"
vec_len = 300
glove_vector_name = "42B." + str(vec_len) + "d"
glove_file_name = "glove." + glove_vector_name + ".txt"
glove_word_pickle_name = "glove." + glove_vector_name + "_word.pkl"
glove_idx_pickle_name = "glove." + glove_vector_name + "_idx.pkl"
glove_vector_dat = "glove." + glove_vector_name + ".dat"
cur_dir = "."
glove_dir = os.path.join(cur_dir,glove_dir_name)
glove_file = os.path.join(glove_dir,glove_file_name)
glove_vectors = os.path.join(glove_dir,glove_vector_dat)
glove_word_pickle = os.path.join(glove_dir,glove_word_pickle_name)
glove_idx_pickle = os.path.join(glove_dir,glove_idx_pickle_name)
video_data_pickle = os.path.join(cur_dir,"video.hist.pkl")
#
def create_base_words():
    words = []
    idx = 0
    word2idx = {}
    if os.path.isfile(glove_vectors):
        os.remove(glove_vectors)
    if os.path.isfile(glove_word_pickle):
        os.remove(glove_word_pickle)
    if os.path.isfile(glove_idx_pickle):
        os.remove(glove_idx_pickle)
    vectors = bcolz.carray(np.zeros(1), rootdir=glove_vectors, mode='w')
    print(glove_file)
    with open(glove_file, 'rb') as fn:
        for l in fn:
            line = l.decode().split()
            word = line[0]
            words.append(word)
            word2idx[word] = idx
            idx += 1
            vect = np.array(line[1:]).astype(np.float)
            vectors.append(vect)

    num_entries = int(vectors.shape[0] / vec_len)
    vectors = bcolz.carray(vectors[1:].reshape((num_entries, vec_len)), rootdir=glove_vectors, mode='w')
    vectors.flush()
    pickle.dump(words, open(glove_word_pickle, 'wb'))
    pickle.dump(word2idx, open(glove_idx_pickle, 'wb'))
def get_word_vector():
    vectors = bcolz.open(glove_vectors)[:]
    words = pickle.load(open(glove_word_pickle, 'rb'))
    word2idx = pickle.load(open(glove_idx_pickle, 'rb'))
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
    print(glove['unincreasing'])

    print(np.linalg.norm(glove['start']-glove['starts']))
    print(np.linalg.norm(glove['start']-glove['base']))
    print(np.linalg.norm(glove['calc']-glove['calculus']))
    print(np.linalg.norm(glove['catholic']-glove['calculus']))
