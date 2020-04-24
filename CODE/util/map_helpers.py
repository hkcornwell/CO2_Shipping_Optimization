"""
map_helpers.py

Contains helper functions to process post-processed trips dataframe.
"""

# Import required libraries
import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

import math
import plotly.graph_objects as go
import plotly.express as px


"""
Generates the data needed to funnel trip data into a plotly geoscatter map
"""
def gen_df_spokes_start(df_full_trips):
    df = df_full_trips[['MMSI',
                         'BaseDateTime_Start',
                         'LAT_SPOKEStartPort', 
                         'LON_SPOKEStartPort']].copy()
    df['color'] = 'green'
    df.columns = ['mmsi', 'time', 'lat', 'lon', 'color']
    df['size'] = 8
    df['text'] = (df[['mmsi', 'time']].apply(lambda x: "MMSI: %s<br>Time: %s" % (x[0],x[1]), axis=1))
    df['name'] = 'Spoke Start'
    df.head()
    return df

def gen_df_hub_start(df_full_trips):
    df = df_full_trips[['MMSI', 
                        'StartHUBPORT_PortID', 
                        'StartHUBPORT_LON',
                        'StartHUBPORT_LAT']].copy()

    df['count'] = df['StartHUBPORT_PortID']
    df = df.groupby(['StartHUBPORT_PortID', 
                        'StartHUBPORT_LON',
                       'StartHUBPORT_LAT'], as_index=False).agg({'count': 'count'})
    df.sort_values(by='count', ascending=False)
    df.columns = ['port_id', 'lon', 'lat', 'count']
    df['color'] = 'orange'
    df['text'] = df['port_id'].apply(lambda x: """Hub ID: %s""" % x)
    df['name'] = 'Hub Start'
    df['size'] = 8 + np.log(df['count'])
    return df

def gen_df_hub_end(df_full_trips):
    df = df_full_trips[['MMSI', 
                         'ENDHUBPORT_PortID', 
                         'ENDHUBPORT_LON',
                         'ENDHUBPORT_LAT']].copy()


    df['count'] = df['ENDHUBPORT_PortID']
    df = df.groupby(['ENDHUBPORT_PortID', 
                        'ENDHUBPORT_LON',
                       'ENDHUBPORT_LAT'], as_index=False).agg({'count': 'count'})
    df.sort_values(by='count', ascending=False)
    df['color'] = 'blue'
    df.columns = ['port_id', 'lon', 'lat', 'count', 'color']
    df['text'] = df['port_id'].apply(lambda x: """Hub ID: %s""" % x)
    df['name'] = 'Hub End'
    df['size'] = 8 + np.log(df['count'])
    return df

def gen_df_spoke_end(df_full_trips):
    df = df_full_trips[['MMSI', 
                         'LAT_SPOKEEndPort',
                         'LON_SPOKEEndPort',
                         'BaseDateTime_TripEnd']].copy()
    df.columns = ['mmsi', 'lat', 'lon', 'time']
    df['color'] = 'red'
    df['size'] = 8
    df['text'] = (df[['mmsi', 'time']].apply(lambda x: "MMSI: %s<br>Time: %s" % (x[0],x[1]), axis=1))
    df['name'] = 'Spoke End'
    return df
