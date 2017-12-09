##########################################################
# Group Interaction for USA Relation Network 
##########################################################
from __future__ import print_function, division 
import sys
sys.path.append("../lib")
sys.path.append("..")
import snap_util
from util.plotter import *
from GTD_Config import *
from util import plotter
from collections import defaultdict, Counter
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import plotly.plotly as py
import numpy as np
from pprint import pprint 
import pickle 
from dataframe_preprocessor import DataframePreprocessor
from tabulate import tabulate
import snap

# Param
preprocess = 0 # 1: first process | 0: just load generated data 
data = "../../data/GTD/generated/GTD_sub_related.csv"
tmp_file = "./tmp/connections.pkl"
# data = "../../data/GTD/generated/USA_related.csv"

if preprocess:
    df_processor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)
    df = df_processor.get_dataframe()

def preprocess_connections(): 
    connections = Counter() # (g1, g2) -> n_connection 

    for _, row in df.iterrows():
        curr_group = row[COL_gname]
        if curr_group == "Unknown": continue
        neighbors = [int(x) for x in row[COL_related].replace('and', ',').replace('\\', '').replace(' ', ',').split(',') if x]
        for n in neighbors: 
            try:
                nbr_name = df.loc[n][COL_gname]
                if nbr_name == curr_group or nbr_name == "Unknown": continue 
                pair = tuple(sorted((curr_group, nbr_name)))
                connections[pair] += 1
            except: continue 
    with open(tmp_file, "wb") as f:
        pickle.dump(connections, f)

if preprocess: preprocess_connections() 
with open(tmp_file, "rb") as f:
    connections = pickle.load(f)

table = tabulate([(str(x[0]), str(x[1]), y) for (x, y) in connections.most_common(5)], headers=["Group1", "Group2", "# Connections"], tablefmt='orgtbl')
print(table)
