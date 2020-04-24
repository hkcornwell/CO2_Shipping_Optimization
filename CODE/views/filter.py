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
from controls import CLUSTERS 

def gen_options(vals, b=False):
    """
    generate options via not the black-scholes equation
    """
    if b:
        return [{"label": v, "value": v} for v in vals]
    return [{"label": v, "value": v} for v in vals]

def get_filter(trips):
    df = trips.get_trips()    

    # Gen vessel options
    vessel_types = list(df['VesselType'].unique())
    vessel_options = gen_options(vessel_types)

    # Gen zones options
    zone_types = list(set(df['StartHUBPORT_PortID'].unique()).union(set(df['ENDHUBPORT_PortID'].unique())))
    zone_options = gen_options(zone_types)
    zone_options.append({"label": "All", "value": "All"})

    return html.Div(
        [
        html.H4("Filters"),
        html.P(
            "Filter by cluster size (epsilon):",
            className="control_label",
            ),
        html.Br(),
        dcc.Slider(
            id="cluster_slider",
            min=0,
            max=1.25,
            value=0.35,
            step=None,
            className="dcc_control",
            marks={k:"" for k in CLUSTERS},
            tooltip = { 'always_visible': True }
            ),
        html.P("Select individual hub to display:", className="control_label"),
        dcc.Dropdown(
                id="zone_types",
                options=zone_options,
                multi=False,
                value="All",
                className="dcc_control",
                ),
        html.P("Filter by vessel type:", className="control_label"),
        dcc.Dropdown(
                id="vessel_types",
                options=vessel_options,
                multi=True,
                value=vessel_types,
                className="dcc_control",
                ),
        ],
        className="pretty_container four columns",
        id="cross-filter-options",
        )
