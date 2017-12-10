##########################################################
# Temporal Analysis of GTD Group Attacks 
##########################################################
from __future__ import print_function, division 
import sys
sys.path.append("../lib")
sys.path.append("..")
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

# Param
preprocess = 0 # preprocess lethality by year data 
year_range = range(1970, 2016 + 1)
top_group_file = "../../out/data/top_lethality_group.pkl"
input_dir = "../../data/GTD/generated/gtd_by_year"
fig_path = "../../out/fig/group_by_year.png"
tmp_file = "./tmp/group_by_year.pkl"

kill_wound_ratio = 3
data_by_year = [] 

with open(top_group_file, "rb") as f:
    top_group_data = pickle.load(f)
    top_groups = [x[0] for x in top_group_data]



def get_lethality_from_df(input):
    """get lethality for each group in given dataframe
    Args:
        input: 

    Return: 
    """
    df_preprocessor = DataframePreprocessor.init_from_file(input)
    df = df_preprocessor.get_dataframe().fillna(0)
    ans = np.zeros(n_group)
    for _, row in df.iterrows():
        name, nkill, nwound = row[COL_gname], row[COL_nkill], row[COL_nwound]
        index = group_lookup.get(name, None)
        if index is None: continue
        lethality = nkill * kill_wound_ratio + nwound 
        ans[index] += lethality 
    return ans  

def preprocess_by_year():
    """
    Return: 
    """
    global n_group, group_lookup 

    n_group = len(top_groups)
    group_lookup = dict((v, k) for (k, v) in enumerate(top_groups))
    for year in year_range:
        input = os.path.join(input_dir, "{}.csv".format(year))
        curr = get_lethality_from_df(input)
        data_by_year.append(curr)
    with open(tmp_file, "wb") as f:
        pickle.dump(data_by_year, f)

if preprocess: preprocess_by_year()

with open(tmp_file, "rb") as f:
    data_by_year = pickle.load(f, encoding='latin1')
    data_by_year = np.array(data_by_year).T
    data_by_year = np.log2(data_by_year + 1)

sns_heatmap(data_by_year,
            save_path="../../out/fig/lethality_by_year.png",
            title="Lethality Evolution by Year",
            size=(16, 8),
            xlabel="Year",
            ylabel="Lethality",
            xtick_rot=45,
            ytick_rot=45,
            yticklabels=top_groups,
            xticklabels=list(year_range))
