################################################
# Extract USA Related Network by Year 
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
import pickle 
from dataframe_preprocessor import DataframePreprocessor

# Param
year_range = range(1970, 2016 + 1)
data = "../../data/GTD/generated/USA_related.csv"
output_dir = "../../data/GTD/generated/usa_related_by_year"

def get_related_edges_from_df(df):
    edges = []
    for i, node in df.iterrows():
        related = [int(x) for x in node[COL_related].split(",")]
        for n in related:
            if n != i:
                try:
                    edges.append([id2row[i], id2row[n]])
                except:
                    pass
    return edges 

# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)

df = dataframe_preprocessor.get_dataframe()

row_map = get_row_map() 
id2row = row_map["id2row"]

for year in year_range:
    print("--- {} ---".format(year))
    curr = dataframe_preprocessor.get_subframe_by_condition(COL_year, lambda x : x == year)
    output = os.path.join(output_dir, "{}.tsv".format(year))
    edges = get_related_edges_from_df(curr)
    with open(output, "w") as f:
        print("Event1 Event2", file = f)
        for e in edges:
            print(" ".join([str(x) for x in e]), file = f)

