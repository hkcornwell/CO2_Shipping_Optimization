"""
trips.py

Trips ORM model.

Loads in all epsilon permutations of the model and stores in a persistent data frame.
All dashboard analytics is derived off this single dataframe.
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
from util import map_helpers
from controls import CLUSTERS

class Trips():
    def __init__(self, data_path):
        self.data_path = data_path
        self.df_clusters = []
        for c in CLUSTERS:
            c = np.format_float_positional(c)
            df = pd.read_csv(self.data_path.joinpath(f"clusteredDF_{(c)}.csv"), low_memory=False)
            df['cluster_size'] = (c)
            df['co2_total'] = df[['CO2_SpokeStart', 'CO2_SpokeEnd', 'CO2_Hub_Hub']].sum(axis=1)
            self.df_clusters.append(df)
        self.df_clusters = pd.concat(self.df_clusters)
        self.static_emissions = pd.read_csv(self.data_path.joinpath(f"staticgraph.csv"), low_memory=False)

    def get_trips(self, cluster_size=1, zone_types="All", vessel_types=None):
        df = self.df_clusters
        if cluster_size:
            cluster_size = np.format_float_positional(cluster_size)
            df = df[df['cluster_size'] == cluster_size]
        if zone_types != "All":
            df = df[(df['StartHUBPORT_PortID'] == zone_types) | (df['ENDHUBPORT_PortID'] == zone_types)]
        if vessel_types:
            df = df[df['VesselType'].isin(vessel_types)]

        return df

    def get_static_graph(self):
        return self.static_emissions
