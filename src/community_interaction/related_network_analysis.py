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
group = GROUP_Taliban
min_nkill = 1 
max_nkill = 100 
excluded_groups = set(["Unknown"])

data = "../../data/GTD/generated/GTD_sub_{}.csv"

# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)

dataframe_preprocessor.filter_rows_by_condition(COL_nkill, lambda x: x >= min_nkill and x <= max_nkill)

dataframe_preprocessor.filter_rows_by_condition(COL_gname, lambda x: x not in excluded_groups)

df = dataframe_preprocessor.get_dataframe()
column_map = get_column_map() 

# Connection Feature
conn_feature = COL_gname


events_by_type = defaultdict(list) # {feature_value: [event_id]}
for index, row in df.iterrows():
    events_by_type[row[conn_feature]].append(index)

############### Plot ########################

title = "Community Analysis for {}".format(country)
#make figure

# plot data
scl = [[0, green], [0.1, yellow], [0.12, pink], [0.2, pink], [1, red]]
nodes = dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df[COL_log],
        lat = df[COL_lat],
        text = df[COL_nkill],
        mode = 'markers',
        name = "Event",
        marker = dict(
            size = 10,
            autocolorscale = 1,
            line = dict(
                width=.5,
                color='white'
            ),
            colorscale = scl,
            cmin = 0,
            color = df[COL_nkill],
            cmax = df[COL_nkill].max(),
            colorbar=dict(
                title="Number of People Killed"
            )
        ))

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

# Figure1: map 
map_figure = {
    'data': [nodes] ,
    'layout': layout,
    'frames': [],
    'config': {'scrollzoom': True}
}


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
        colorscale=scl,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='N-kill',
            xanchor='left',
        ),
        line=dict(width=2)))

for _, node in df.iterrows():
    x, y = node[COL_log], node[COL_lat]
    nkill = int(node[COL_nkill])
    node_trace['x'].append(x)
    node_trace['y'].append(y)
    node_trace['marker']['color'].append(nkill)
    node_info = 'nKill = {}'.format(nkill)
    node_trace['text'].append(node_info)

# links 
edge_traces = []
edge_colors = [gray, blue, purple, green, pink]

i = 0
for conn_type, arr in events_by_type.items():
    events = [df.loc[k] for k in arr]
    edge_trace = Scatter(
        x=[],
        y=[],
        text=[],
        name = conn_type,
        line=Line(width=0.5,color=edge_colors[i]),
        hoverinfo='text',
        mode='lines')
    for (e1, e2) in combinations(events, 2):
        x1, y1 = e1[COL_log], e1[COL_lat]
        x2, y2 = e2[COL_log], e2[COL_lat]
        edge_trace['x'] += [x1, x2, None]
        edge_trace['y'] += [y1, y2, None]
        edge_trace['text'].append(conn_type)
    edge_traces.append(edge_trace)
    i = (i + 1)%len(edge_colors)

network_layout=Layout(
    width = 1400,
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
    'data': [node_trace] + edge_traces,
    'layout': network_layout,
    'config': {'scrollzoom': True}
}
py.sign_in('dengl11', 'hrDwKpc7egWbsZPccRHi')
py.image.save_as(network_figure, filename='../../out/fig/usa.png')
py.image.save_as(map_figure, filename='../../out/fig/usa_map.png')

