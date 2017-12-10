################################################
# Home-Aroad Atack Analysis for All Groups 
################################################ 
from __future__ import division
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
tmp_file = "../../out/data/h2a.pkl"
preprocess = 0

def preprocess_h2a():
    df_preprocessor = get_full_gtd()
    df = df_preprocessor.get_dataframe()
    # replace na as 0
    df.fillna(0, inplace = True)
    group_lookup = get_top_group_index()
    h2a = defaultdict(lambda : [0, 0, 0]) # group -> (n_attack, n_home_attack, h2a_ratio) 
    for _, row in df.iterrows():
        name, nation, country  = row[COL_gname], row[COL_nation], row[COL_country]
        index = group_lookup.get(name, None)
        if index is None: continue
        h2a[name][0] += 1 
        if country == nation:
            h2a[name][1] += 1   
    for k, v in h2a.items():
        if v[0] > 0:
            h2a[k][2] = v[1]/v[0]
    with open(tmp_file, "wb") as f:
        pickle.dump(dict(h2a), f)


def plot_h2a(h2a):
    save_path = "../../out/fig/h2a.png"
    h2a_ratio = [x[1] for x in h2a]
    # distribution_plot(h2a_ratio, save_path=save_path, xlim=(0, 1), ylim=(0, 1),)
    sns_dist_plot(h2a_ratio,
                  save_path=save_path,
                  normalize=True,
                  cumulative=False,
                  title="Distribution of H2A Ratio",
                  xlabel="H2A",
                  ylabel="Probabilty Density Value",
                  xlim=(0, 1),
                  # ylim=(0, 4)
                  )
    # sns.distplot(h2a_ratio, kde=False)
    # plt.show()
    # h2a.reverse()
    # names = [x[0] for x in h2a]
    # hbar_plot(names, h2a_ratio, "Home Attacking Ratio", "Groups", "Home Attacking Ratio", 


if preprocess: preprocess_h2a()

with open(tmp_file, "rb") as f:
    h2a = pickle.load(f)

h2a_list = sorted(
        [(k, v[1] / v[0]) for (k, v) in h2a.items()], 
        lambda x, y: 1 if x[1] > y[1] else -1,
        reverse = 0)

# table = tabulate([(str(y[0]), y[1], y[2], y[3]) for y in h2a_list[:10]], headers=["Group", "Kill", "Wound", "Severity"], tablefmt='orgtbl')
# print(table)
plot_h2a(h2a_list)
