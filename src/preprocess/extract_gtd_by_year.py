################################################
# Extract GTD by Year 
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
output_dir = "../../data/GTD/generated/gtd_by_year"

df_preprocessor = get_full_gtd()

for year in year_range:
    print("--- {} ---".format(year))
    curr = df_preprocessor.get_subframe_by_condition(COL_year, lambda x : x == year)
    output = os.path.join(output_dir, "{}.csv".format(year))
    curr.to_csv(open(output, "w"), index=True)

