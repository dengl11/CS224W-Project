################################################
# Backend for Notebook: Related Network 
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
data = "../../data/GTD/generated/GTD_sub_related.csv"
output = "../../data/GTD/generated/USA_related.tsv"

# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)
dataframe_preprocessor.filter_rows_by_condition(COL_country, lambda x : x == 217)

df = dataframe_preprocessor.get_dataframe()

row_map = get_row_map() 
id2row = row_map["id2row"]

edges = []

for i, node in df.iterrows():
    related = [int(x) for x in node[COL_related].split(",")]
    for n in related:
        if n != i:
            try:
                edges.append([id2row[i], id2row[n]])
            except:
                pass


with open(output, "w") as f:
    print("Event1 Event2", file = f)
    for e in edges:
        print(" ".join([str(x) for x in e]), file = f)

