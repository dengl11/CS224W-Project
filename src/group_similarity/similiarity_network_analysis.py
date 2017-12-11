################################################
# Analysis for Similarity Network 
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
import snap
from dataframe_preprocessor import DataframePreprocessor

# Param
sim_network_tsv = "../../data/GTD/generated/sim_network.tsv"
Graph = snap.LoadEdgeList(snap.PUNGraph, sim_network_tsv, 0, 1)
row_map = get_row_map()
row2id = row_map["row2id"]
id2row = row_map["id2row"]

nodes = Graph.Nodes()
n_nodes = Graph.GetNodes()

with open("../../out/data/top_lethality_group.pkl", "rb") as f:
    group_arr = pickle.load(f)

def basic_stats():

    print("Number of Nodes: {}".format(n_nodes))
    print("Number of Edges: {}".format(Graph.GetEdges()))
    clus_coef = snap.GetClustCf(Graph)
    print("Clustering Coefficient: {}".format(clus_coef))

def extract_community(topK = 5):
    """community analysis
    Return: [[eventID] x topK]
    """
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(Graph, CmtyV)
    communities = defaultdict(int) # {group index : community ID}
    arr = []
    for Cmty in CmtyV:
        if topK <= 0: break 
        curr = []
        for NI in Cmty:
            communities[NI] = topK
            curr.append(NI)
        topK -= 1
        arr.append(curr)
    print("The modularity of the network is %f" % modularity)
    return communities, arr 

def show_communities(community_arr):
    """
    Args:
    Return: 
    """
    txt_arr = []
    for arr in community_arr:
        txt_arr.append(simplity_gnames([group_arr[x][0] for x in arr]))
    summary = [", ".join(x) for x in txt_arr]
    table = tabulate(zip(range(1, len(txt_arr) +1), summary),
                     headers=["Community", "Groups"],
                     tablefmt='orgtbl')
    print(table)


print("\n------ 1-1 Basic Stats ------")
basic_stats()

print("\n------ 2-1 Community Detection ------")
communities, community_arr = extract_community()
show_communities(community_arr)

with open("../../out/data/similarity_community.pkl", "wb") as f:
    pickle.dump(communities, f)



