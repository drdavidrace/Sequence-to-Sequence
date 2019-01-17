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
import tables as tbl
import numpy as np
from embed_defaults.build_glove_names import *
from math import exp

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("-c",dest="create_word_vector",action='store_true', \
  help='Create the word table contents for the embedding words')
parser.add_argument("-b",dest="create_base_table",action="store_true", \
  help='Create the base pytable for the embedding words.')

args = parser.parse_args()
create_word_vector = args.create_word_vector
create_table = args.create_base_table
work_dir = get_work_dir_name()
work_glove_dir = get_work_glove_dir()
#
#  Defaults
#
if not os.path.isdir(work_dir):
    print("The working directory path {:s} does not exist.  Exiting".format(work_dir))
    sys.exit()
if not os.path.isdir(work_glove_dir):
    os.makedirs(work_glove_dir,mode=0o777,exist_ok=True)
#  Glove Information
vec_len = get_vec_len()
max_word_length = 0
num_data_points = 400000 
glove_file_name = get_glove_file_name()
glove_vector_dat = get_glove_vector_dta()
#  Existing Files
cur_dir = "."
glove_file = get_glove_file_name()
working_glove_file = get_working_glove_file_name()
#
working_glove_vectors = get_glove_vector_dta()
video_data_pickle = os.path.join(cur_dir,"video.hist.pkl")
# def max_len_word():
#     max_word_length = 0
#     with open(glove_file, 'rb') as fn:
#         for l in fn:
#             line = l.decode().split()
#             max_word_length = max(max_word_length,len(line[0]))
#     return max_word_length
#
# def create_base_table():
#     if os.path.isfile(working_glove_vectors):
#         os.remove(working_glove_vectors)
#     glove = tbl.open_file(working_glove_vectors,mode='w',title="Word Embedding Vectors",root_uep="/")
#     #Create the group
#     word_group = glove.create_group("/","word_vector",title="Word Details")
#     #Create the columns
#     max_len = max_len_word()
#     data_def = np.dtype([('word','S'+str(max_len)),('vector',np.float64,(vec_len,))])
#     word_table = glove.create_table(word_group,'word_vectors', \
#     description=data_def,title="Word Vectors",expectedrows=num_data_points)
#     word_row = word_table.row
#     print("Starting the word/vector storage")
#     #Add values to the table
#     word_count = 0
#     with open(glove_file, 'rb') as fn:
#         for l in fn:
#             line = l.decode().split()
#             w = line[0].lower().strip()
#             v = np.array(line[1:]).astype(np.float) 
#             if v.shape[0] == vec_len:
#                 word_count += 1  
#                 word_row['word'] = bytes(w.encode("ascii","ignore"))
#                 word_row['vector'] = v
#                 word_row.append()
#                 if word_count%10000 == 0:
#                     print("\tProcessed {:d} words.".format(word_count))
#     glove.flush()
#     # print(word_table)
#     # print(word_table[0])
#     # check = "word ==" + "'theta'"
#     # first_result = [row['vector'] for row in word_table.where(check) ]
#     # print(first_result)
#     glove.close()

    
# def create_base_words():
#     """Create the basic glove information in the working directory.
#     This isn't very smart.  Ideally it would check the dates and only do the work
#     if the dates are out of alignment, but this is quick and dirty.
#     """
#     words = []
#     idx = 0
#     word2idx = {}
#     if os.path.isfile(working_glove_vectors):
#         os.remove(working_glove_vectors)
#     if os.path.isfile(working_glove_word_pickle):
#         os.remove(working_glove_word_pickle)
#     if os.path.isfile(working_glove_idx_pickle):
#         os.remove(working_glove_idx_pickle)
#     vectors = bcolz.carray(np.zeros(1), rootdir=working_glove_vectors, mode='w')
#     with open(working_glove_file, 'rb') as fn:
#         for l in fn:
#             line = l.decode().split()
#             try:
#                 vect = np.array(line[1:]).astype(np.float)
#                 if vect.shape[0] == 300:
#                     word = line[0]
#                     words.append(word)
#                     word2idx[word] = idx
#                     idx += 1
#                     vectors.append(vect)
#             except:
#                 print(line)
#                 print(idx)
#                 print(len(line))
            

#     num_entries = int(vectors.shape[0] / vec_len)
#     vectors = bcolz.carray(vectors[1:].reshape((num_entries, vec_len)), rootdir=working_glove_vectors, mode='w')
#     vectors.flush()
#     pickle.dump(words, open(working_glove_word_pickle, 'wb'))
#     pickle.dump(word2idx, open(working_glove_idx_pickle, 'wb'))

# def get_word_vector():
#     vectors = bcolz.open(working_glove_vectors)[:]
#     words = pickle.load(open(working_glove_word_pickle, 'rb'))
#     word2idx = pickle.load(open(working_glove_idx_pickle, 'rb'))
#     glove = {w: vectors[word2idx[w]] for w in words}
#     return glove

if __name__ == "__main__":
    #open base table
    glove = tbl.open_file(working_glove_vectors,mode='r',title="Word Embedding Vectors",root_uep="/")
    table = glove.root.word_vector.word_vectors
    print(table[0])
    # check = "word ==" + "'calculus'"
    # first_result = [row['vector'] for row in table.where(check) ]
    # print(first_result)
    # check = "word ==" + "'derivative'"
    # first_result = [row['vector'] for row in table.where(check) ]
    # print(first_result)
    check = "word ==" + "'ice'"
    first_result = [row['vector'] for row in table.where(check) ][0]
    check = "word ==" + "'solid'"
    second_result = [row['vector'] for row in table.where(check) ][0]
    check = "word ==" + "'gas'"
    third_result = [row['vector'] for row in table.where(check) ][0]
    print(third_result)
    dp1 = np.dot(second_result,first_result)
    dp2 = np.dot(second_result,third_result)
    print('{:20.15f}\n'.format(dp1))
    print('{:20.15f}\n'.format(dp2))
    glove.close()

    # if create_word_vector:
    #     create_base_words()
    # glove = get_word_vector()
    # video_hist = pickle.load(open(video_data_pickle,'rb'))
    # number_in = 0
    # number_not_in = 0
    # not_in = set()
    # for k in video_hist.keys():
    #     if k in glove:
    #         number_in += 1
    #     else:
    #         number_not_in += 1
    #         not_in.add(k)
    # print("Number in {:d}".format(number_in))
    # print("Number not in {:d}".format(number_not_in))
    # print(not_in)
    # print(glove['start'])
    # print(glove['non-increasing'])
    # print(glove['1234'])

    # print(np.linalg.norm(glove['start']-glove['starts']))
    # print(np.linalg.norm(glove['start']-glove['base']))
    # print(np.linalg.norm(glove['calc']-glove['calculus']))
    # print(np.linalg.norm(glove['catholic']-glove['calculus']))
