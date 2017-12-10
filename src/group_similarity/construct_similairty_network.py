################################################
# Constructor for Similarity Network 
################################################ 
from __future__ import division
import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import *
from util import num_ops 
from GTD_Config import *
from collections import defaultdict 
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np
from numpy import sign 
from tabulate import tabulate 
import pickle 
from dataframe_preprocessor import DataframePreprocessor

# Param
sim_pkl = "../../out/data/similarity_100.pkl"
group_vec_pkl = "../../out/data/group_vectors.pkl"
sim_network_tsv = "../../data/GTD/generated/sim_network.tsv"
sim_threshold = 2

with open(sim_pkl, "rb") as f:
    dic = pickle.load(f, encoding="latin1")
    groups = dic["group"] # list of group name 
    sim_mat = dic["matrix"] # np 2d array 

with open(group_vec_pkl, "rb") as f:
    # {name : [...]}
    group_vecs = pickle.load(f, encoding="latin1")

edges = [] # [(g1, g2, weight)]
sim_mat[sim_mat < sim_threshold] = 0

# prepare edges
n_group = len(groups)
for i in range(n_group):
    for j in range(i+1, n_group):
        v = sim_mat[i][j]
        if v == 0: continue
        edges.append((i, j , v))

with open(sim_network_tsv, "w") as f:
    print("Group1\tGroup2\tSimilarity", file = f)
    for g1, g2, s in edges:
        print("{}\t{}\t{}".format(g1, g2, s), file = f)
