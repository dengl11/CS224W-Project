################################################
# Backend for Notebook: Community Construction 
################################################

import sys
sys.path.append("../lib")
sys.path.append("..")
from util.plotter import gray, red, blue, purple, green, pink
from GTD_Config import *
from collections import defaultdict 
from itertools import combinations
import pandas as pd
from plotly.graph_objs import *
import numpy as np
import pickle 
from dataframe_preprocessor import DataframePreprocessor

# Param
group = GROUP_Taliban
min_nkill = 28 

# group = GROUP_ISIL
data = "../../data/GTD/generated/GTD_sub_{}.csv".format(group)

# load mapping 
mapping_path = "../../data/GTD/generated/column_mapping.pkl"
with open(mapping_path, "rb") as f:
    column_map = pickle.load(f)


# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data, index_col = COL_eventid)
dataframe_preprocessor.filter_rows_by_condition(COL_nkill, lambda x: x >= min_nkill)
df = dataframe_preprocessor.get_dataframe()


# Connection Feature
conn_feature = COL_attacktype1


events_by_type = defaultdict(list)
for index, row in df.iterrows():
    events_by_type[row[conn_feature]].append(index)


############### Plot ########################

import plotly.plotly as py
from plotly.graph_objs import *

### set nodes 
node_trace = Scatter(
    x=[],
    y=[],
    text=[],
    mode='markers',
    name = "event",
    hoverinfo='text',
    marker=Marker(
        showscale=True,
        # colorscale options
        # 'Greys' | 'Greens' | 'Bluered' | 'Hot' | 'Picnic' | 'Portland' |
        # Jet' | 'RdBu' | 'Blackbody' | 'Earth' | 'Electric' | 'YIOrRd' | 'YIGnBu'
        colorscale='YIGnBu',
        reversescale=True,
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


edge_traces = []
edge_colors = [gray, blue, purple, green, pink]

i = 0
for conn_type, arr in events_by_type.items():
    conn_type = column_map['num2txt'][conn_feature][conn_type]
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

fig = Figure(data=Data([node_trace] + edge_traces),
             layout=Layout(
                title='<br>Events by {}'.format(conn_feature),
                titlefont=dict(size=16),
                showlegend=1,
                legend=dict(x=-.1, y=1.2),
                hovermode='closest',
                margin=dict(b=20,l=5,r=50,t=40),
                xaxis=XAxis(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=YAxis(showgrid=False, zeroline=False, showticklabels=False)))
