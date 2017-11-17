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
gtd_csv = "../../data/GTD/{}".format(gtd_file_name)
output = "../../data/GTD/generated/column_mapping.pkl"


preprocessor = DataframePreprocessor.init_from_file(gtd_csv)
df = preprocessor.get_dataframe()

features = ['country', 'weaptype1', 'targtype1', 'attacktype1']

num2txt = {} # {feature: {key: i}}
txt2num = {} # {feature: [...]}


for f in features:
    f_txt = f + "_txt"
    num_arr = df[f]
    txt_arr = df[f_txt]
    curr_txt2num = dict(zip(txt_arr, num_arr)) # {txt: num}
    n = max(curr_txt2num.values()) + 1
    curr_num2txt = [None] * n
    for k, i in curr_txt2num.items():
        curr_num2txt[i] = k
    num2txt[f] = curr_num2txt 
    txt2num[f] = curr_txt2num 


data = {
        'num2txt': num2txt,
        'txt2num': txt2num
        }

with open(output, 'wb') as f:
    pickle.dump(data, f)
