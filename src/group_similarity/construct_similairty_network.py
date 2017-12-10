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
sim_threshold = 5

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
# print(n_group)

for i in range(n_group):
    for j in range(i+1, n_group):
        v = sim_mat[i][j]
        if v == 0: continue
        edges.append((i, j , v))

with open(sim_network_tsv, "w") as f:
    print("Group1\tGroup2\tSimilarity", file = f)
    for g1, g2, s in edges:
        print("{}\t{}\t{}".format(g1, g2, s), file = f)

def get_3d_sim_network():
    """return the plotly object for 3D similarity network
    Return: 
    """
    Xn, Yn, Zn = [np.zeros(n_group) for _ in range(3)]
    for i, name in enumerate(groups):
        # features = ["lethality", "peak_year", "attack_type", "h2a", "log", "lat"]
        v = group_vecs[name]
        Xn[i] = v[-2]
        Zn[i] = v[-1]
        Yn[i] = v[1]
    # construct graph nodes 
    nodes=Scatter3d(x=Xn,
               y=Yn,
               z=Zn,
               mode='markers',
               name='actors',
               marker=Marker(symbol='dot',
                             size=6,
                             colorscale='Viridis',
                             line=Line(color='rgb(50,50,50)', width=0.5)
                             ),
               hoverinfo='text'
               )
    # construct edges
    Xe, Ye, Ze, edge_weights = [], [], [], []
    for g1, g2, s in edges:
        v1 = group_vecs[groups[g1]]
        v2 = group_vecs[groups[g2]]
        Xe += [v1[-2], v2[-2], None]
        Ze += [v1[-1], v2[-1], None]
        Ye += [v1[1], v2[1], None]
        edge_weights.append(s)

    edges_trace=Scatter3d(x=Xe,
               y=Ye,
               z=Ze,
               mode='lines',
               line=Line(color='rgb(125,125,125)', width=1),
               hoverinfo=edge_weights
               )



    # config axis 
    axis=dict(showbackground=False,
          showline=True,
          zeroline=True,
          showgrid=False,
          showticklabels=True,
          title=''
          )
    # layout
    layout = Layout(
         title="3D Similarity Network",
         width=1200,
         height=1000,
         showlegend=False,
         scene=Scene(
         xaxis=XAxis(axis),
         yaxis=YAxis(axis),
         zaxis=ZAxis(axis),
        ),
     margin=Margin(
        t=100
    ),
    hovermode='closest',
    )
    fig=Figure(data=[nodes, edges_trace], layout=layout)
    return fig
    

py.sign_in('dengl11', 'hrDwKpc7egWbsZPccRHi')
sim_fig = get_3d_sim_network() 
