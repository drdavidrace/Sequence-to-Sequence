#!/usr/bin/env python
"""
This processes a set of mathematical oriented transcriptions to create more word oriented 
transcriptions.  For instance, f(x) become f of x.


"""

import os, sys
import subprocess
import argparse
import re
from num2words import num2words

parser = argparse.ArgumentParser(description="Parse args for processing transcriptions")
parser.add_argument("--subs",dest="subs",action='store_true')

args = parser.parse_args()

curr_phase_count = 0
process_subs = args.subs
def basic_subs(inSentence=None):
    new_line = inSentence.replace("=", " equals ")
    new_line = new_line.lower()
    new_line = new_line.encode("ascii",errors="ignore").decode()
    new_line = new_line.replace("minus"," minus ")
    new_line = new_line.replace("plus", " plus ")
    new_line = new_line.replace("times", " times ")
    new_line = new_line.replace("*", " times ")
    new_line = new_line.replace("+", " plus ")
    new_line = new_line.replace("),(",") , (")
    new_line = new_line.replace("^"," to the power of ")
    new_line = new_line.replace("sub"," sub ")
    new_line = new_line.replace("sub stitue","substitue")
    new_line = new_line.replace("sub trac","subtrac")
    new_line = new_line.replace("youre", " you are ")
    new_line = new_line.replace("youve", " you have ")
    new_line = new_line.replace("'s","s")
    new_line = new_line.replace("'ll"," will ")
    new_line = new_line.replace("'m"," am ")
    new_line = new_line.replace("'re"," are ")
    new_line = re.sub('  +',' ',new_line)
    new_line = new_line.strip()
    return new_line

def first_replace_words(inSentence=None):
    p_numbers = inSentence.split()
    out_string = ""
    for p in p_numbers:
        try:
            t_number = num2words(p)
            out_string = out_string + " " + t_number
        except:
            out_string = out_string + " " + p
    return out_string

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
                if not re.match("^\.",f):
                    f_new = "PH"+str(curr_phase_count) + "-" + f
                    f0 = os.path.join(sd,f)
                    f1 = os.path.join(sd,f_new)
                    fn = open(f0,'r',encoding="ISO-8859-1")
                    fm = open(f1,'w')
                    for cur_line in fn:
                        if not re.match(r'^slide',cur_line,re.I):
                            new_line = basic_subs(cur_line)
                            new_line = first_replace_words(new_line)
                            split_lines = re.split(r"[.!?]\s+",new_line)
                            for s in split_lines:
                                s1 = s.replace(r"[?.!]$","").strip()
                                s1 = re.sub(r'\s\s+',' ',s1)
                                #The following makes the substitution f(x) to f of x, kinda cute
                                s1 = re.sub(r"(\S+)\((.+?)\)",r"\1 of \2",s1)
                                s1 = re.sub(r"(\d+)(pi)", r"\1 pi ",s1)
                                s1 = re.sub(r"(pi)[\/\+\-\*\^]", r" pi ",s1)
                                s1 = s1.rstrip().rstrip(".").rstrip("?").rstrip("!").rstrip()
                                s1 = s1.strip()
                                if len(s1) > 0:
                                    fm.write("{:s}.\n".format(s1))
                    fn.close()
                    fm.close()
        curr_phase_count += 1
    print(curr_phase_count)
