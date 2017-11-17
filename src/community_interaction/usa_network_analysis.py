################################################
# Backend for Notebook: Related Network 
################################################ 
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

nodes = Graph.Nodes()
print("\n------ 1 ------")
(outs, counts) = snap_util.nodes_count_by_out(nodes)
log_outs, log_counts = np.log10(outs), np.log10(counts)

ax = plotter.curve_plot(log_outs, log_counts, xlabel="$log_{10}$(OutDeg)", ylabel="$log_{10}$(NodeCount)", show=False)

def convert_to_eventId(arr):
    """
    Args:
        arr: 

    Return: 
    """
    return [row2id[x] for x in arr]


print("\n------ 2 ------")
# coefficients
p = np.polyfit(x = log_outs, y = log_counts, deg = 1)
print("a = {:.2f}\nb = {:.2f}".format(*p))

fn = np.poly1d(p)
# regression line
fits = fn(log_outs)
fig = plt.plot(log_outs, fits)
plt.legend(["Count Plot", "Regression"])
ax_set_title(plt.gca(), "Degree Distribution of USA Relation Network")

# save fig
plt.savefig(fig_path)

print("\n------ 1 ------")
wcc = snap.TCnComV()
snap.GetWccs(Graph, wcc)
nwcc = len(wcc)
print("# of weakly connected components: {}".format(nwcc))

print("\n------ 2 ------")
MxWcc = snap.GetMxWcc(Graph)
print("# of edges in MxWcc {}".format(len(list(MxWcc.Edges()))))
print("# of nodes in MxWcc {}".format(len(list(MxWcc.Nodes()))))


print("Number of Nodes: {}".format(Graph.GetNodes()))
print("Number of Edges: {}".format(Graph.GetEdges()))

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
