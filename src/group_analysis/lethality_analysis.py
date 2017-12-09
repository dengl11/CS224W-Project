################################################
# Lethality Analysis for All Groups 
################################################ 
import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import *
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
tmp_file = "./tmp/lethality.pkl"
preprocess = 0

def preprocess_lethality():
    df_preprocessor = get_full_gtd()
    df = df_preprocessor.get_dataframe()
    # replace na as 0
    df.fillna(0, inplace = True)
    lethality = defaultdict(lambda : [0, 0]) # group -> (n_kill, n_wound) 
    for _, row in df.iterrows():
        name, nkill, nwound = row[COL_gname], row[COL_nkill], row[COL_nwound]
        if name == "Unknown": continue
        lethality[name][0] += nkill 
        lethality[name][1] += nwound  
    with open(tmp_file, "wb") as f:
        pickle.dump(dict(lethality), f)


if preprocess: preprocess_lethality()

with open(tmp_file, "rb") as f:
    lethality = pickle.load(f)

lethality_list = sorted(lethality.items(), lambda x, y: 1 if x[1][0] > y[1][0] else -1, reverse = 1)

table = tabulate([(str(x), y[0], y[1]) for (x, y) in lethality_list[:10]], headers=["Group", "Kill", "Wound"], tablefmt='orgtbl')
print(table)
