"""
This is currently a bunch of functions but should turn into an object 
so it doesn't have to open and close files so often
"""

import os, sys
import json
#default options
#
def get_defaults_file_name():
    cur_dir = "."
    json_default_file_name = 'defaults.json'
    return os.path.join(cur_dir,json_default_file_name)
#
def get_defaults_json():
    json_default_file = get_defaults_file_name()
    default_json = None
    with open(json_default_file,'r') as fn:
        default_json = json.load(fn)
    return default_json
#
def get_default_value(in_val=None):
    assert in_val is not None
    assert isinstance(in_val,str)
    work_val = in_val.lower().strip()
    defaults = get_defaults_json()
    work_keys = list(defaults.keys())
    assert work_val in work_keys
    return defaults[work_val]
#
def get_glove_dir_name():
    cur_dir = "."
    glove_dir_name = get_default_value("glove_dir_name")
    return os.path.join(cur_dir,glove_dir_name)
#
def get_vec_len():
    return get_default_value("vec_len")
#
def get_work_dir_name():
    return get_default_value("work_dir")
# 
def get_glove_sizes():
    return get_default_value("glove_sizes")
#
def get_vector_lengths():
    return get_default_value("vector_lengths")
#
def get_glove_vector_name():
    glove_size = get_default_value("size")
    vec_len = get_vec_len()
    if not glove_size in get_default_value("glove_sizes"):
        raise ValueError('glove size must be one of {}'.format(get_glove_sizes()))
    if not vec_len in get_default_value("vector_lengths"):
        raise ValueError('glove vector length must be one of {}'.format(get_vector_lengths()))
    return str(glove_size) + "B." + str(vec_len) + "d"
#
def _get_glove_file_name_():
    return "glove." + get_glove_vector_name() + ".txt"
def get_glove_file_name():
    return os.path.join(get_glove_dir_name(),_get_glove_file_name_())
def get_working_glove_file_name():
    return os.path.join(get_work_glove_dir(),_get_glove_file_name_())

def get_work_glove_dir():
    return os.path.join(get_work_dir_name(),get_glove_dir_name())
#
def get_glove_vector_dta():
    return os.path.join(get_work_glove_dir(), "glove." + get_glove_vector_name() + ".hd5")

