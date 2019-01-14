import os, sys

def get_defaults_file():
    cur_dir = "."
    json_default_file_name = 'defaults.json'
    return os.path.join(cur_dir,json_default_file_name)
