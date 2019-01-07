#!/usr/bin/env python
import os, sys
import subprocess

if __name__ == '__main__':
    print('Start of processing.')
    #Get the directories
    cur_dir = '.'
    sub_dirs = [os.path.join(cur_dir,d) for d in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir,d))]
    print(sub_dirs)
    #Clean the directories
    for sd in sub_dirs:
        p_files = os.listdir(sd)
        for f in p_files:
            f_new = f.replace(" ","-")
            os.rename(os.path.join(sd,f),os.path.join(sd,f_new))
