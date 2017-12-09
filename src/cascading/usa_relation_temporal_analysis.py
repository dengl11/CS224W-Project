##########################################################
# Temporal Analysis of USA Relation Network 
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
year_range = range(1970, 2016 + 1)
output_dir = "../../data/GTD/generated/usa_related_by_year"
fig_path = "../../out/fig/usa_network.png"

# clustering_coef = snap.GetClustCf(usa_graph)
# row_map = get_row_map()
# row2id = row_map["row2id"]
# id2row = row_map["id2row"]

# nodes = Graph.Nodes()
# n_nodes = Graph.GetNodes()

def get_modularity(Graph):
    CmtyV = snap.TCnComV()
    modularity = snap.CommunityGirvanNewman(Graph, CmtyV)
    return modularity


############################# Main  #############################
years = []
modularities = []
cluster_coefficients = []
nevents = []
for year in year_range:
    try:
        data = os.path.join(output_dir, "{}.tsv".format(year))
        Graph = snap.LoadEdgeList(snap.PUNGraph, data, 0, 1)
        n_nodes = Graph.GetNodes()
        clus = snap.GetClustCf(Graph)
        m = get_modularity(Graph)
        cluster_coefficients.append(clus)
        years.append(year)
        modularities.append(m)
        nevents.append(n_nodes)
    except: 
        m = None
    print(year, m, clus)
ax = plotter.curve_plot(years, modularities, xlabel="year", ylabel="Modularity", show=False)
ax_set_title(plt.gca(), "Evolution of Modularity of USA Relation Network")
plt.savefig("../../out/fig/usa_modularity_by_year.png")

plt.figure()
ax = plotter.curve_plot(years, cluster_coefficients, xlabel="year", ylabel="Clustering Coefficient", show=False)
ax_set_title(plt.gca(), "Evolution of Clustering Coefficient of USA Relation Network")
plt.savefig("../../out/fig/usa_clus_coeff_by_year.png")

plt.figure()
ax = plotter.curve_plot(years, nevents, xlabel="year", ylabel="Events", show=False)
ax_set_title(plt.gca(), "Evolution of Events of USA Relation Network")
plt.savefig("../../out/fig/usa_events_by_year.png")
