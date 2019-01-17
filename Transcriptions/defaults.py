#!/usr/bin/env python
"""
This is a script that sets some of the defaults for the embedding processing and
saves the values to defaults.json.

Nothing fancy here, but may add additional capabilities in the future.
"""
import os, sys
import json
from pprint import pprint
from embed_defaults.seq_deq_defaults import seq_seq_defaults

defaults = seq_seq_defaults()
json_default_file = defaults.get_json_default_file()
#  Define basic defaults
defaults = {}
defaults['vec_len'] = 50
defaults['size'] = 6
defaults["glove_dir_name"] = "glove-base"
defaults["work_dir"] = "/work-temp"
defaults["glove_sizes"]= [6, 42, 840]
defaults["vector_lengths"] = [50,300]
defaults["text_dirs"] = ["Cal2Texts"]
# process the defaults
json_defaults = json.dumps(defaults)

if os.path.isfile(json_default_file):
    os.remove(json_default_file)
with open(json_default_file,'w') as fn:
    fn.write(json_defaults)
#open and print the results
in_json = None
with open(json_default_file,'r') as fn:
    in_json = json.load(fn)
    pprint(in_json)
print(type(in_json))
pprint(in_json['vec_len'])
pprint(in_json['size'])