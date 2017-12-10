################################################
# Location Analysis for All Groups 
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
analysis_type = "geo_location"
tmp_file = "../../out/data/{}.pkl".format(analysis_type)
fig_path = "../../out/fig/{}.png".format(analysis_type)
preprocess = 1

def preprocess_analysis():
    df_preprocessor = get_full_gtd()
    df = df_preprocessor.get_dataframe()
    # replace na as 0
    # df.fillna(0, inplace = True)
    group_lookup = get_top_group_index()
    n_group = len(group_lookup)
    lats = defaultdict(list)
    logs = defaultdict(list)
    for _, row in df.iterrows():
        name, lat, log  = row[COL_gname], row[COL_lat], row[COL_log]
        index = group_lookup.get(name, None)
        if index is None or np.isnan(lat): continue
        lats[index].append(lat)
        logs[index].append(log)
    output = {}
    for name, index in group_lookup.items():
        output[name] = (np.median(logs[index]), np.median(lats[index]))


    with open(tmp_file, "wb") as f:
        pickle.dump(output, f)



if preprocess: preprocess_analysis()

with open(tmp_file, "rb") as f:
    data = pickle.load(f, encoding="latin1")
    print(data)

# table = tabulate([(str(y[0]), y[1], y[2], y[3]) for y in h2a_list[:10]], headers=["Group", "Kill", "Wound", "Severity"], tablefmt='orgtbl')
# print(table)
# plot_h2a(h2a_list)
