##########################################################
# Lethality Evolution Pattern Analysis of GTD Group Attacks 
##########################################################
from __future__ import print_function, division 
import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import *
from GTD_Config import *
from util import plotter, df_ops 
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
fig_path = "../../out/fig/lethality_evolution.png"
tmp_file = "./tmp/group_by_year.pkl"

kill_wound_ratio = 3
data_by_year = [] 

with open(top_group_file, "rb") as f:
    top_group_data = pickle.load(f)
    top_groups = [x[0] for x in top_group_data]

def increment_matrix(matrix):
    """ get the increment matrix for matrix 
    Return: 
    """
    nr, nc = matrix.shape
    ans = np.zeros((nr-1, nc))
    for r in range(1, nr):
        ans[r-1] = matrix[r,:] - matrix[r-1,:]
    return ans 
    

with open(tmp_file, "rb") as f:
    data_by_year = pickle.load(f, encoding='latin1')
    data_by_year = np.array(data_by_year)
    data_by_year = np.log2(data_by_year + 1)
    inc_mat = increment_matrix(data_by_year)

inc_df = df_ops.mat2df(inc_mat, columns=top_groups)
top_groups = simplity_gnames(top_groups)
sns_clustermap(inc_df,
            save_path=fig_path,
            title="Lethality Evolution by Year",
            size=(16, 12),
            xeabel="Group",
            ylabel="Group",
            xtick_rot=45,
            ytick_rot=45,
            yticklabels=top_groups,
            xticklabels=top_groups
            )
