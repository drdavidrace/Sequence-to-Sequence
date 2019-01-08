#!/usr/bin/env python
import os, sys
import subprocess
import argparse
import re

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("--subs",dest="subs",action='store_true')

args = parser.parse_args()

curr_phase_count = 0
process_subs = args.subs


if __name__ == '__main__':
    print('Start of processing.')
    #Get the directories
    cur_dir = '.'
    sub_dirs = [os.path.join(cur_dir,d) for d in os.listdir(cur_dir) if os.path.isdir(os.path.join(cur_dir,d))]
    print(sub_dirs)
    #Clean the directories
    #replace the spaces in the names with -
    for sd in sub_dirs:
        p_files = os.listdir(sd)
        for f in p_files:
            f_new = f.replace(" ","-")
            os.rename(os.path.join(sd,f),os.path.join(sd,f_new))
            new_file = os.path.join(sd,f_new)
            if f_new.startswith("PH"):
                os.remove(new_file)
    #filter the text to replace the = with equals
    if process_subs:
        for sd in sub_dirs:
            p_files = os.listdir(sd)
            for f in p_files:
                f_new = "PH"+str(curr_phase_count) + "-" + f
                f0 = os.path.join(sd,f)
                f1 = os.path.join(sd,f_new)
                fn = open(f0,'r')
                fm = open(f1,'w')
                for cur_line in fn:
                    new_line = cur_line.replace("=", " equals ")
                    new_line = new_line.replace("minus"," minus ")
                    new_line = new_line.replace("plus", " plus ")
                    new_line = new_line.replace("times", " times ")
                    new_line = new_line.replace("*", " times ")
                    new_line = new_line.replace("+", " plus ")
                    new_line = new_line.replace("),(",") , (")
                    new_line = new_line.replace("^"," to the power of ")
                    new_line = new_line.replace("sub"," sub ")
                    re.sub('  +',' ',new_line)
                    split_lines = re.split(r"\.|\?\s*",new_line)
                    for s in split_lines:
                        s1 = s.replace(r"\n","").strip()
                        s1 = re.sub(r'\s\s+',' ',s1)
                        s1 = re.sub(r"(\S+)\((.+?)\)",r"\1 of \2",s1)
                        if len(s1) > 0:
                            fm.write("{:s}.\n".format(s1))
                fn.close()
                fm.close()
        curr_phase_count += 1
    print(curr_phase_count)
