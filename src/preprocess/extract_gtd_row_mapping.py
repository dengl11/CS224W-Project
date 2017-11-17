###################################
# Extract GTD Feature mapping 
###################################
# Dump to file {
#                num2txt: {feature: {key: i}} 
#                txt2num: {feature: [...]}
#              }
####################################

import sys
sys.path.append("../lib")
sys.path.append("../")
from dataframe_preprocessor import DataframePreprocessor
from util import plotter
import pandas as pd 
from GTD_Config import * 
import pickle 
import numpy as np 

# CONSTANTS

preprocessor = get_full_gtd()
df = preprocessor.get_dataframe()
output = "../../data/GTD/generated/row_mapping.pkl"

id2row = {}
row2id = {}

row = -1

for ind, _ in df.iterrows():
    row += 1
    if ind in id2row: continue
    id2row[ind] = row
    row2id[row] = ind 


data = {"id2row": id2row, "row2id": row2id}
with open(output, 'wb') as f:
    pickle.dump(data, f, protocol=2)
