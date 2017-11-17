###################################
# Extract Sub-Dataset from GTD 
###################################

import sys
sys.path.append("../lib")
sys.path.append("..")
from dataframe_preprocessor import DataframePreprocessor
from util import plotter
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from GTD_Config import *

# CONSTANTS
gtd_csv = "../../data/GTD/globalterrorismdb_0617dist.csv"

# Construct dataframe preprocessor 
preprocessor = DataframePreprocessor.init_from_file(gtd_csv)
column_map = get_column_map()


#########  Select by Group #################
# COL_gname = "gname"
# selected_group = GROUP_ISIL 
# # selected_group = GROUP_Taliban
# output = "../../data/GTD/generated/GTD_sub_{}.csv".format(selected_group)

# # select data by selected_group
# preprocessor.filter_rows_by_condition(COL_gname, lambda x: x == selected_group)

# preprocessor.filter_rows_by_condition(COL_gname, lambda x: x == selected_group)


######### Select by Country #################

# country = 'United States'
# country_num = column_map['txt2num'][COL_country][country]
# output = "../../data/GTD/generated/GTD_sub_{}_1970_1979.csv".format(country.replace(' ', '_'))
# preprocessor.filter_rows_by_condition(COL_country, lambda x: x == country_num)
# preprocessor.filter_rows_by_condition(COL_year, lambda x: x >= 1970 and x <= 1979)


######### Select by Related #################

output = "../../data/GTD/generated/GTD_sub_related.csv"
preprocessor.filter_rows_by_nonempty_column(COL_related)

######### Shared Method #################
# dump to file 
preprocessor.dump(output)

