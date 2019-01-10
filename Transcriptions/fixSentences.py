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
from copy import copy
from math import fabs

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
    new_line = new_line.replace(" cal "," calculus ")
    new_line = new_line.replace("sine"," sin ")
    new_line = new_line.replace("sub"," sub ")
    new_line = new_line.replace("sub stitue","substitue")
    new_line = new_line.replace("sub trac","subtrac")
    new_line = new_line.replace("youre", " you are ")
    new_line = new_line.replace("youve", " you have ")
    new_line = new_line.replace("y'all", " you all ")
    new_line = new_line.replace("'s","s")
    new_line = new_line.replace("'ll"," will ")
    new_line = new_line.replace("woll"," will ")
    new_line = new_line.replace("'m"," am ")
    new_line = new_line.replace("'re"," are ")
    new_line = new_line.replace(","," , ")
    new_line = new_line.replace("costheta","cos(theta)")
    new_line = new_line.replace("cos2theta","cos(2theta)")
    new_line = new_line.replace("cos4theta","cos(4theta)")
    new_line = new_line.replace("cos0","cos(0)")
    new_line = new_line.replace("cosx","cos(x)")
    new_line = new_line.replace("cosu","cos(u)")
    new_line = new_line.replace("sintheta","sin(theta)")
    new_line = new_line.replace("sin2theta","sin(2theta)")
    new_line = new_line.replace("sin4theta","sin(4theta)")
    new_line = new_line.replace("sin0","sin(0)")
    new_line = new_line.replace("sin2pi","sin(2pi)")
    new_line = new_line.replace("sinpi","sin(pi)")
    new_line = new_line.replace("sinx","sin(x)")
    new_line = new_line.replace("sinu","sin(u)")
    new_line = re.sub('  +',' ',new_line)
    new_line = new_line.strip()
    return new_line

def choose_int_words(inString=None):
    t_float = float(inString)
    t_int = int(t_float)
    if fabs(float(t_int) - t_float) < 1e-12:
        return num2words(t_int)
    else:
        return num2words(inString)

def first_number_replace_words(inSentence=None):
    p_numbers = inSentence.split()
    out_string = ""
    found = False
    for p in p_numbers:
        q = p.rstrip().rstrip(".").rstrip()
        try:
            t_number = num2words(q)
            t_number = choose_int_words(q)
            out_string = out_string + " " + t_number
        except:
            out_string = out_string + " " + q
    if found:
        print(out_string)
    return out_string

def fraction_replace_words(inSentence=None):
    op = re.compile(r"([\+\-]*[0-9\.]+)([\/]+)([\+\-]*[0-9\.])")
    out_string = ""
    start_pt = 0
    for p in op.finditer(inSentence):
        out_string = out_string + inSentence[start_pt:p.start()] + " " + choose_int_words(p.group(1)) + \
        " over " + choose_int_words(p.group(3)) + " "
        start_pt = p.end()
    if(start_pt > 0):
        out_string = out_string + " " + inSentence[start_pt:]
    else:
        out_string = inSentence
    return out_string

def ordered_pair_replace_words(inSentence=None):
    p_numbers = inSentence.split()
    out_string = ""
    for p in p_numbers:
        cur_match = re.match(r"([\(]+)([\+\-\ ]*[0-9\.]+)([\ \,]+)([\+\-\ ]*[0-9\.]+)([\ ]*)([\)]+)",p)
        if cur_match:
            print("FOUND ORDERED PAIR")
            out_string = out_string + " the ordered pair " + num2words(cur_match.group(2)) + \
            " comma " + num2words(cur_match.group(4))
        else:
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
        if os.path.basename(sd).upper().startswith("CAL"):
            for f in p_files:
                f_new = f.replace(" ","-")
                os.rename(os.path.join(sd,f),os.path.join(sd,f_new))
                new_file = os.path.join(sd,f_new)
                if f_new.startswith("PH"):
                    os.remove(new_file)
    #filter the text to replace the = with equals
    if process_subs:
        if os.path.basename(sd).upper().startswith("CAL"):
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
                                new_line = first_number_replace_words(new_line)
                                new_line = fraction_replace_words(new_line)
                                #new_line = ordered_pair_replace_words(new_line)
                                split_lines = re.split(r"[\.\!\?]\s+",new_line)
                                for s in split_lines:
                                    s1 = s.replace(r"[\?\.\!]$","").strip()
                                    s1 = re.sub(r'\s\s+',' ',s1)
                                    #The following makes the substitution f(x) to f of x, kinda cute
                                    s1 = re.sub(r"(\S+)\((.+?)\)",r"\1 of \2",s1)
                                    s1 = re.sub(r"(\d+)(pi)", r"\1pi ",s1)
                                    s1 = re.sub(r"(pi)[\/]", r" pi over ",s1)
                                    s1 = re.sub(r"(pi)[\+]", r" pi plus ",s1)
                                    s1 = re.sub(r"(pi)[\-]", r" pi minus ",s1)
                                    s1 = re.sub(r"(pi)[\*]", r" pi times ",s1)
                                    s1 = re.sub(r"(pi)[\^]", r" pi to the power of  ",s1)
                                    s1 = s1.rstrip().rstrip(".").rstrip("?").rstrip("!").rstrip()
                                    s1 = s1.strip()
                                    s1 = s1.replace(")/", " over ")
                                    s1 = first_number_replace_words(s1)
                                    s1 = fraction_replace_words(s1)
                                    words = s1.split()
                                    out_str = ""
                                    for w in words:
                                        word = re.sub("([\.\?\!\,\[\(\)\]])*([\-\+0-9a-zA-Z]+)([\.\?\!\,\[\]\)\(])*",r"\2",w)
                                        out_str = out_str + " " + word
                                    if len(out_str) > 0:
                                        fm.write("{:s} .\n".format(out_str))
                        fn.close()
                        fm.close()
            curr_phase_count += 1
    print(curr_phase_count)
