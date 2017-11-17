###################################
# Divide the GTD Dataset by Feature 
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
gtd_csv = "../../data/GTD/globalterrorismdb_0617dist.csv"

# param 
top_k = 20
# feature = COL_country_txt  
feature = COL_gname 
fig_output = "../../out/fig/gtd_by_{}.png".format(feature)

preprocessor = DataframePreprocessor.init_from_file(gtd_csv)
dataframe = preprocessor.get_dataframe()

print("dataframe.shape = {}".format(dataframe.shape))
print("dataframe columns:\n {}".format(list(dataframe.keys())))

events_by_group = dataframe[feature].value_counts()[1: 1+top_k]
print(events_by_group)
groups = set(events_by_group.keys())
groups_ordered_by_count = sorted(events_by_group.keys(), key = lambda x: events_by_group[x], reverse=True) 
print(groups)

preprocessor.filter_rows_by_condition(feature, lambda x: x in groups)
dataframe = preprocessor.get_dataframe()
print("dataframe.shape = {}".format(dataframe.shape))

# plot count by group 
plt.figure(figsize=(8, 10))
ax = sns.countplot(y = feature, data = preprocessor.get_dataframe(), linewidth=1, order = groups_ordered_by_count)
title = "Count of Terrorist Events by {}".format(feature)
plt.yticks(rotation=45, fontsize=14)
plt.yticks(fontsize=14)
ax.set_ylabel(feature, fontsize=16)
ax.set_xlabel("Number of Events", fontsize=16)
plotter.ax_set_title(ax, title, size=17)
plt.tight_layout() 
plt.savefig(fig_output)

