###################################
# Backend for Inspector 
###################################

import sys
sys.path.append("../lib")
sys.path.append("../")
from dataframe_preprocessor import DataframePreprocessor
from util import plotter
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from GTD_Config import * 

# CONSTANTS
gtd_csv = "../../data/GTD/{}".format(gtd_file_name)
# gtd_csv = "../../data/GTD/generated/GTD_sub_Taliban.csv"
preprocessor = DataframePreprocessor.init_from_file(gtd_csv)
df = preprocessor.get_dataframe()
