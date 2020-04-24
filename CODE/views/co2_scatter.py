"""
co2_scatter.py

Plotly figure for scatter plot for individual trip emissions
"""

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

import plotly.express as px
import plotly.graph_objects as go

layout = dict(
    margin=dict(l=30, r=30, b=30, t=40),
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    title=dict(
        text="Vessel Dimensions vs CO2 Efficiency",
        xanchor='center',
        x=0.5
    ),
    legend_orientation='h',
    legend_y=-0.05,
    legend_x=0.6,
    legend_xanchor='center'
)

def _generate_scatter_df(df_full_trips):
    df = df_full_trips[['Length', 'Width', 'VesselType']]
    df['Vessel Type'] = df['VesselType']
    df['CO2 Efficiency'] = df_full_trips['Individual_TEU']
    return df

def get_figure(df_full_trips):
    fig = px.scatter_3d(_generate_scatter_df(df_full_trips), 
                        x='Length', 
                        y='Width', 
                        z='CO2 Efficiency',
                        color='Vessel Type')
    fig.update_layout(layout)
    #figure = dict(data=fig, layout=layout)
    return fig
