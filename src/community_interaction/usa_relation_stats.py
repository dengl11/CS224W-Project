##########################################################
# Basic Statistics Computation for USA Relation Network 
##########################################################
from __future__ import print_function, division 
import sys
sys.path.append("../lib")
sys.path.append("..")
import snap_util
from util.plotter import *
from GTD_Config import *
from util import plotter
from collections import defaultdict 
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np
import pickle 
from dataframe_preprocessor import DataframePreprocessor
import snap

# Param
data = "../../data/GTD/generated/USA_related.tsv"
fig_path = "../../out/fig/usa_network.png"

dataframe_preprocessor = get_full_gtd()
df = dataframe_preprocessor.get_dataframe()

Graph = snap.LoadEdgeList(snap.PUNGraph, data, 0, 1)
# clustering_coef = snap.GetClustCf(usa_graph)
row_map = get_row_map()
row2id = row_map["row2id"]
id2row = row_map["id2row"]

nodes = Graph.Nodes()
n_nodes = Graph.GetNodes()
############################# Nodes & Edges  #############################

def convert_to_eventId(arr):
    return [row2id[x] for x in arr]

def plot_degree_dist():
    (outs, counts) = snap_util.nodes_count_by_out(nodes)
    log_outs, log_counts = np.log10(outs), np.log10(counts/n_nodes)
    # log_outs, log_counts = np.log10(outs), np.log10(counts)

    # ax = plotter.curve_plot(log_outs, log_counts, xlabel="$log_{10}$(OutDeg)", ylabel="", show=False)
    ax = plotter.curve_plot(log_outs, log_counts, xlabel="$log_{10}$(OutDeg)", ylabel="$log_{10}$(Node Ratio)", show=False)
    # print("\n------ 1-2 Fitting Degree Dist. ------")

    # coefficients
    # p = np.polyfit(x = log_outs, y = log_counts, deg = 1)
    # print("a = {:.2f}\nb = {:.2f}".format(*p))

    # fn = np.poly1d(p)
# # regression line
    # fits = fn(log_outs)
    # fig = plt.plot(log_outs, fits)
    # plt.legend(["Count Plot", "Regression"])
    ax_set_title(plt.gca(), "Degree Distribution of USA Relation Network")

    # save fig
    plt.savefig(fig_path)

def basic_stats():
    print("\n------ 1-1 Basic Stats ------")

    print("Number of Nodes: {}".format(n_nodes))
    print("Number of Edges: {}".format(Graph.GetEdges()))
    clus_coef = snap.GetClustCf(Graph)
    print("Clustering Coefficient: {}".format(clus_coef))







############################# WCC  #############################

def wcc():
    print("\n------ 3-0 WCC ------")
    wcc = snap.TCnComV()
    snap.GetWccs(Graph, wcc)
    nwcc = len(wcc)
    print("# of weakly connected components: {}".format(nwcc))

    print("\n------ 3-1 MxWCC ------")
    MxWcc = snap.GetMxWcc(Graph)
    print("# of edges in MxWcc {}".format(len(list(MxWcc.Edges()))))
    print("# of nodes in MxWcc {}".format(len(list(MxWcc.Nodes()))))



############################# Severity vs Degree  #############################

def severity_relation():
    """
    Return: 
    """
    k = 100
    top_nodeIds = snap_util.top_nodes_by_deg(Graph, k)
    top_events = convert_to_eventId(top_nodeIds)
    top_nodes = [snap_util.getNodebyID(Graph, x) for x in top_nodeIds]
    top_degs = [x.GetDeg() for x in top_nodes]
# top_nodes = [snap_util.node_by_id(Graph, x) for x in top_nodes]
# events = [df.loc[x] for x in top_nodes ]
    top_df = df.loc[top_events]

    alpha = 10
# plt.figure(figsize=(600, 300))
    plt.plot(range(k), top_degs)
    plt.plot(range(k), top_df[COL_nkill])
    plt.plot(range(k), top_df[COL_nwound])
    plt.plot(range(k), top_df[COL_nkill] * alpha + top_df[COL_nwound])
    plt.legend(["Node Degree", "nKill", "nWound", "{} * nKill + nWound".format(alpha)])
    ax = plt.gca()
    ax.set_xlabel("Rank of Node by Degree", fontsize=10)
    ax.set_ylabel("", fontsize=10)
    ax_set_title(plt.gca(), "Correlation between Degree Distribution and Severity in USA Relation Network")
    plt.savefig("../../out/fig/usa_corr.png")

############################# Severity vs Degree  #############################
def extract_community(topK = 10):
    """community analysis
    Return: [[eventID] x topK]
    """
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(Graph, CmtyV)
    communities = []
    for Cmty in CmtyV:
        if topK <= 0: break 
        curr = []
        topK -= 1
        for NI in Cmty:
            curr.append(row2id[NI])
        communities.append(curr)
    print("The modularity of the network is %f" % modularity)
    return communities

def get_community(events):
    """show the sub-dataframe for a community
    Args:
        events: 

    Return: 
    """ 
    Nodes = snap.TIntV()
    for nodeId in events:
        Nodes.Add(id2row[nodeId])
    edges_inout = snap.GetEdgesInOut(Graph, Nodes)
    print("EdgesIn: %s EdgesOut: %s" % (edges_inout[0], edges_inout[1]))
    return df.loc[events]
    

############################# Main  #############################
communities = extract_community()

# for c in communities:
    # show_community(c)
# basic_stats()
