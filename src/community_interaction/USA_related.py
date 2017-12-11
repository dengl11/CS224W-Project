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
dataframe_preprocessor.filter_rows_by_condition(COL_country, lambda x : x == 217)

df = dataframe_preprocessor.get_dataframe()


############### Plot ########################

title = "Related Network Analysis"

# plot layout 
layout = {}
layout['legend']=dict(x=-.1, y=1.2)
layout['title'] = title 
# figure['layout']['autoscale'] = 0 
layout['geo'] = dict(
            autosize=True,
            showland = True,
            scope="usa",
            showcoastlines = 0,
            landcolor = '#242426',
            subunitwidth=1,
            countrywidth=1,
            margin=dict(b=0,l=0,r=0,t=40),
            showframe = 1,
        )

measure = df[COL_nwound] + 3 * df[COL_nkill]
measure[measure>0] = np.log10(measure[measure>0])

colorbar_title = "log10[3 * N-kill + N-Wound]"

### node trace 
nodes = dict(
        type = 'scattergeo',
        lon = df['longitude'],
        lat = df['latitude'],
        text = measure,
        marker = dict(
            color = measure,
            colorscale='Viridis',
            colorbar=dict(
                thickness=15,
                title=colorbar_title,
                xanchor='left',
                ),
            line = dict(width=0.5),
            sizemode = 'area'),
        )


# Figure1: map 
map_figure = {
    'data': [nodes] ,
    'layout': layout,
    'frames': [],
    'config': {'scrollzoom': True}
}

# py.sign_in('dengl11', 'hrDwKpc7egWbsZPccRHi')
# py.image.save_as(network_figure, filename='../../out/fig/usa.png')
# py.image.save_as(map_figure, filename='../../out/fig/usa_map.png')


##########################################################

### node trace 
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    name = "Event",
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        color=[],
        size=10,
        colorscale='Viridis',
        colorbar=dict(
            thickness=15,
            title=colorbar_title,
            xanchor='left',
        ),
        line=dict(width=2)))

for i, node in df.iterrows():
    x, y = node[COL_log], node[COL_lat]
    nkill = (node[COL_nkill])
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    node_trace['marker']['color'].append(measure[i])
    node_info = 'Severity = {}'.format(measure[i])
    node_trace['text'].append(node_info)

# links 
edge_trace = Scatter(
    x=[],
    y=[],
    text=[],
    name = "Relation",
    line=Line(width=0.5),
    hoverinfo='text',
    mode ='lines')

for _, node in df.iterrows():
    related = [int(x) for x in node[COL_related].split(",")]
    for n in related:
        try:
            nbr = df.loc[n]
            x1, y1 = node[COL_log], node[COL_lat]
            x2, y2 = nbr[COL_log], nbr[COL_lat]
            edge_trace['x'] += [x1, x2, None]
            edge_trace['y'] += [y1, y2, None]
            # edge_trace['text'].append("{}-{}".format(node[COL_eventid], nbr[COL_eventid]))
        except Exception as e:
            # print("{} not in network!".format(n))
            pass 


network_layout=Layout(
    width = 1000,
    title=title, 
    titlefont=dict(size=16),
    showlegend=1,
    legend=dict(xanchor="center", yanchor="top",x=-.1, y=0.5),
    hovermode='closest',
    margin=dict(b=20,l=5,r=50,t=40),
    xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False))

# Figure2: network  
network_figure = {
    'data': [node_trace, edge_trace],
    'layout': network_layout,
    'config': {'scrollzoom': True}
}


