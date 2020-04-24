import pickle
import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

from util.map_helpers import *

"""
Add hub and spokes
"""

def gen_map(df_full_trips, lines=True, zone_types='All'):
    fig = go.Figure()

    if lines and not zone_types == 'All': 
        df_fig_arr = [gen_df_spokes_start(df_full_trips),
                     gen_df_hub_start(df_full_trips),
                     gen_df_hub_end(df_full_trips),
                     gen_df_spoke_end(df_full_trips)]
    elif zone_types == 'All':
        df_fig_arr = [gen_df_hub_start(df_full_trips),gen_df_hub_end(df_full_trips)]
    else:
        df_fig_arr = [gen_df_spokes_start(df_full_trips),
                     gen_df_spoke_end(df_full_trips)]

    # Add locations
    for df in df_fig_arr:
        df['shape'] = 'circle'
        fig.add_trace(go.Scattergeo(
            lon=df['lon'],
            lat=df['lat'],
            name=df['name'].values[0],
            text=df['text'],
            marker=dict(size=df['size'],
                        symbol=df['shape'],
                        color=df['color'],
                        line=dict(width=3, color='rgba(68, 68, 68, 0)')
                        )))

    """
    Add paths
    """
    if not zone_types == 'All':
        for row in df_full_trips.itertuples():
            fig.add_trace(go.Scattergeo(
                lon=[row.LON_SPOKEStartPort, row.StartHUBPORT_LON],
                lat=[row.LAT_SPOKEStartPort, row.StartHUBPORT_LAT],
                mode='lines',
                line=dict(width=0.3, color='gray'),
                opacity=0.8,
                showlegend=False,
                name=row.Segment
            ))
            
            fig.add_trace(go.Scattergeo(
                lon=[row.StartHUBPORT_LON, row.ENDHUBPORT_LON],
                lat=[row.StartHUBPORT_LAT, row.ENDHUBPORT_LAT],
                mode='lines',
                line=dict(width=0.3, color='gray'),
                opacity=0.8,
                showlegend=False,
                name=row.Segment
            ))
            
            fig.add_trace(go.Scattergeo(
                lon=[row.ENDHUBPORT_LON, row.LON_SPOKEEndPort],
                lat=[row.ENDHUBPORT_LAT, row.LAT_SPOKEEndPort],
                mode='lines',
                line=dict(width=0.3, color='gray'),
                opacity=0.8,
                showlegend=False,
                name=row.Segment
            ))

    layout = dict(showlegend=True,
                  geo=dict(
                      projection = go.layout.geo.Projection(
                          type='azimuthal equal area'
                        ),
                      center={'lat': df_full_trips['LAT_SPOKEStartPort'].mean(), 
                              'lon': df_full_trips['LON_SPOKEStartPort'].mean()},
                        scope="north america",
                        showland = False,
                        showlakes = False,
                        showocean = True,
                        resolution = 50,
                        landcolor = 'rgb(230, 145, 56)',
                        lakecolor = 'rgb(0, 255, 255)',
                        oceancolor = 'rgb(127,205,255)',
                        coastlinewidth = 3,
                  )
                 )
    fig.update_layout(layout)
    return fig
