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

# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)
dataframe_preprocessor.filter_rows_by_condition(COL_nwound, lambda x : x >= 5)

df = dataframe_preprocessor.get_dataframe()


############### Plot ########################

title = "World-wide Related Network Analysis"

# plot data
scl = [[0, green], [0.1, yellow], [0.12, pink], [0.2, pink], [1, red]]
# plot layout 
layout = {}
layout['legend']=dict(x=-.1, y=1.2)
layout['title'] = title 
# figure['layout']['autoscale'] = 0 
layout['geo'] = dict(
            autosize=True,
            showland = True,
            scope="world",
            showcoastlines = 0,
            landcolor = '#242426',
            subunitwidth=1,
            countrywidth=1,
            margin=dict(b=0,l=0,r=0,t=40),
            showframe = 1,
        )

measure = df[COL_nwound] + df[COL_nkill]
### node trace 
nodes = dict(
        type = 'scattergeo',
        lon = df['longitude'],
        lat = df['latitude'],
        text = measure,
        marker = dict(
            color = np.log(measure),
            colorscale='Viridis',
            colorbar=dict(
                thickness=15,
                title='N-kill',
                xanchor='left',
                ),
            line = dict(width=0.5),
            sizemode = 'area'),
        )


# Figure1: map 
network_figure = {
    'data': [nodes] ,
    'layout': layout,
    'frames': [],
    'config': {'scrollzoom': True}
}

# py.sign_in('dengl11', 'hrDwKpc7egWbsZPccRHi')
# py.image.save_as(network_figure, filename='../../out/fig/usa.png')
# py.image.save_as(map_figure, filename='../../out/fig/usa_map.png')

