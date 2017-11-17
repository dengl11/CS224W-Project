##########################################
# Backend for Notebook: Temporal Evolution 
##########################################
# Reference:
# https://www.kaggle.com/dengl11/global-terrorism-plotly-animations-47ef6a/editnb
##########################################

import sys
sys.path.append("../lib")
sys.path.append("..")
from GTD_Config import *
import pandas as pd
import numpy as np
from plotly.graph_objs import *
from dataframe_preprocessor import DataframePreprocessor

# Param
group = GROUP_Taliban
# group = GROUP_ISIL
data = "../../data/GTD/generated/GTD_sub_{}.csv".format(group)
selected_cols = [COL_year,'imonth','iday','country_txt','region_txt','provstate','city','latitude','longitude','attacktype1_txt','targtype1_txt','gname','weaptype1_txt','nkill','nwound'] 
title = "Temporal Distribution of Terrorist Event by {}".format(group)


# Read data 
dataframe_preprocessor = DataframePreprocessor.init_from_file(data)
df = dataframe_preprocessor.get_dataframe()

# Using only important columns 
df = df[selected_cols]

# data range 
geo_margin = 5
lat_range = dataframe_preprocessor.num_feature_range(COL_lat)
print("Latitude: {}".format(lat_range))
lat_range = (lat_range[0]- geo_margin, lat_range[1] + geo_margin)

# longitude 
log_range = dataframe_preprocessor.num_feature_range(COL_log)
print("Longitude: {}".format(log_range))
log_range = (log_range[0]- geo_margin, log_range[1] + geo_margin)

year_range = dataframe_preprocessor.num_feature_range(COL_year)
years  = list(range(year_range[0], year_range[1] + 1))
print("Years: {}".format(year_range))

df['text'] = df['city'] + '<br>' + df['country_txt'] + '<br>' + df['gname'] + '<br>' + df['iyear'].apply(str) + '<br>' + 'Killed:  ' + abs(df['nkill']).apply(str)

limits = [(0,200),(200,400),(400,1000),(1000,2000)]
colors = ["rgb(252,187,161)","rgb(251,106,74)","rgb(203,24,29)","rgb(103,0,13)","lightgrey"]
events = []


#make figure
figure = {
    'data': [],
    'layout': {
    },
    'frames': [],
    'config': {'scrollzoom': True}
}


figure['layout']['title'] = title 
# figure['layout']['autoscale'] = 0 
figure['layout']['geo'] = dict(
            autosize=True,
            showland = True,
            scope="asia",
            showcoastlines = 0,
            landcolor = '#242426',
            subunitwidth=1,
            countrywidth=1,
            # center = {'lat': np.mean(lat_range),
                      # 'log': np.mean(log_range)}, 
            # lonaxis = dict( range= log_range, showgrid=1 ),
            # lataxis = dict( range= lat_range ), 
            # xaxis=XAxis(range=[-100, 100]),
            showframe = 1,
        )


# config menu buttons 
figure['layout']['updatemenus'] = [
    {
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 500, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 300, 'easing': 'quadratic-in-out'}}],
                'label': 'Play',
                'method': 'animate'
            },
            {
                'args': [[None], {'frame': {'duration': 0, 'redraw': False}, 'mode': 'immediate',
                'transition': {'duration': 0}}],
                'label': 'Pause',
                'method': 'animate'
            }
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'top'
    }
]

# config slider 
figure['layout']['sliders'] = {
    'args': [
        'sliders.value', {
            'duration': 400,
            'ease': 'cubic-in-out'
        }
    ],
    'initialValue': '1952',
    'plotlycommand': 'animate',
    'values': years,
    'visible': True
}
sliders_dict = {
    'active': 0,
    'yanchor': 'top',
    'xanchor': 'left',
    'currentvalue': {
        'font': {'size': 20},
        'prefix': 'Year:',
        'visible': True,
        'xanchor': 'right'
    },
    'transition': {'duration': 500, 'easing': 'cubic-in-out'},
    'pad': {'b': 10, 't': 50},
    'len': 0.9,
    'x': 0.1,
    'y': 0,
    'steps': []
}


#Make data
year = 2005
for i in range(len(limits)):
    lim = limits[i]
    df_sub = df[(df.nkill >= lim[0]) & (df.nkill < lim[1])]
    #for year in years:
    df_sub_byyear = df_sub[df_sub.iyear == year]
    data_dict = dict(
        type = 'scattergeo',
        lon = df_sub_byyear['longitude'],
        lat = df_sub_byyear['latitude'],
        text = df_sub_byyear['text'] ,
        marker = dict(
                    size = df_sub_byyear['nkill'],
                    color = colors[i],
                    line = dict(width=0.5),
                    sizemode = 'area'),
                    name = '{0} - {1}'.format(lim[0],lim[1]) 
                    )
    figure['data'].append(data_dict)

#Make Frames
for year in years:
        frame = {'data': [], 'name': str(year)}
        for i in range(len(limits)):
            lim = limits[i]
            df_sub = df[(df.nkill >= lim[0]) & (df.nkill < lim[1])]
            df_sub_byyear = df_sub[df_sub.iyear == year]
            data_dict = dict(
                type = 'scattergeo',
                lon = df_sub_byyear['longitude'],
                lat = df_sub_byyear['latitude'],
                text = df_sub_byyear['text'] ,
                marker = dict(
                    size = df_sub_byyear['nkill'],
                    color = colors[i],
                    line = dict(width=0.5),
                    sizemode = 'area'),
                    name = '{0} - {1}'.format(lim[0],lim[1]) )
            frame['data'].append(data_dict)
        figure['frames'].append(frame)
        slider_step = {'args': [
            [year],
            {'frame': {'duration': 500, 'redraw': False},
             'mode': 'immediate',
             'transition': {'duration': 500}}
             ],
             'label': year,
             'method': 'animate'}
        sliders_dict['steps'].append(slider_step)

figure['layout']['sliders'] = [sliders_dict]
