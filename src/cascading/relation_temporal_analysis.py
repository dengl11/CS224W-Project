##########################################################
# Temporal Analysis of GTD Relation Network 
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
base_year = 1970
year_range = range(base_year, 2016 + 1)
top_group_file = "../../out/data/top_lethality_group.pkl"
relation_type = 1 # 0: all | 1: external 
relation_type_str = "all" if relation_type == 0 else "external"
tmp_file = "./tmp/relation_by_year_{}.pkl".format(relation_type_str)

fig_path = "../../out/fig/relation_by_year_{}.png".format(relation_type_str)

with open(top_group_file, "rb") as f:
    top_group_data = pickle.load(f)
    top_groups = [x[0] for x in top_group_data]



def preprocess_by_year():
    """
    Return: 
    """
    df_preprocessor = get_gtd_relation()
    df = df_preprocessor.get_dataframe().fillna(0)

    n_group = len(top_groups)
    group_lookup = dict((v, k) for (k, v) in enumerate(top_groups))
    # [nyear x ngroup]
    relation_by_year = np.zeros((len(year_range), n_group))

    for id, row in df.iterrows():
        name, year = row[COL_gname], row[COL_year]
        index = group_lookup.get(name, None)
        if index is None: continue
        if name == "Unknown": continue

        neighbors = [int(x) for x in row[COL_related].replace('and', ',').replace('\\', '').replace(' ', ',').split(',') if x and x != id]
        if relation_type == 0:
            curr = len(neighbors) 
        else:
            curr = 0
            for n in neighbors:
                try:
                    nbr_name = df.loc[n][COL_gname]
                    if nbr_name == name or nbr_name == "Unknown": continue 
                    curr += 1
                except: continue 
        relation_by_year[year - base_year][index] += curr 


    with open(tmp_file, "wb") as f:
        pickle.dump(relation_by_year, f)

if preprocess: preprocess_by_year()

with open(tmp_file, "rb") as f:
    data_by_year = pickle.load(f, encoding='latin1')
    data_by_year = np.array(data_by_year).T
    data_by_year = np.log2(data_by_year + 1)

sns_heatmap(data_by_year,
            save_path=fig_path,
            title="Relation Evolution by Year ({})".format(relation_type_str.title()),
            size=(16, 8),
            xlabel="Year",
            ylabel="Number of Relations",
            xtick_rot=45,
            ytick_rot=45,
            yticklabels=top_groups,
            xticklabels=list(year_range))
