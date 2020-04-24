# Import required libraries
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

def get_metrics():
    return html.Div(
            [
            html.Div(
                [
                html.H3(
                    "CO2 Emissions Optimization in Freight Traffic",
                    style={"margin-bottom": "0px"},
                    ),
                html.H5(
                    "42. Team NYC", style={"margin-top": "0px"}
                    ),
                html.P("This dashboard demonstrates how we can reduce CO2 emissions from maritime freight traffic by leveraging a hub-and-spoke model to aggregate vessel cargo. Toggle the controls on the right and interact with the charts to understand the various scenarios of optimizing freight traffic to reduce emissions. Below link(s) provide more information about our analysis."),
                html.A(html.Button("Data Notebook"), href="/data_notebook", target="_blank", style={"margin-right":"10px"}),
                html.A(html.Button("CO2 Notebook"), href="/data_co2_notebook", target="_blank", style={"margin-right":"10px"}),
                html.A(html.Button("DVA Requirements"), href="https://docs.google.com/document/d/e/2PACX-1vR5-8SC5dE30GdEohe69d-CA0QA45dPtBI43VYImQsqLKW7PjIVHPCGtA9fFlu98hAw6YWVF9Pyb-4n/pub", target="_blank")
                ],
                className="pretty_container"
                ),
            html.Div(
                [
                html.Div(
                    [html.H6(id="num_trips_text"), html.P("Total Trips")],
                    id="num_trips",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="num_hubs_text"), html.P("Total Hubs")],
                    id="num_hubs",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="actual_text"), html.P("CO2 Original Emissions")],
                    id="actual",
                    className="mini_container",
                    ),
                html.Div(
                    [html.H6(id="optimized_text"), html.P("CO2 Optimized Emissions")],
                    id="optimized",
                    className="mini_container",
                    ),
                ],
                id="info-container",
                className="row container-display",
                ),
                ],
                id="right-column",
                className="eight columns",
                )

"""
If we get the optimized co2 data, put this back in!

html.Div(
[dcc.Graph(id="count_graph")],
id="countGraphContainer",
className="pretty_container",
),
"""
