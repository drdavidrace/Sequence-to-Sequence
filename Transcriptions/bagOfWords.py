#!/usr/bin/env python
"""
This processes the text in a set of text files to create a bag of words embedding.
This makes extensive use of pytorch.

"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

if __name__ == "__main__":
    print("Start of bag of words.")
    #set the seed
    torch.manual_seed(1)