"""
app.py

Application entry point for Team NYC's dashboard
"""

import copy
import pathlib
import dash
import math
import datetime as dt
import pandas as pd
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import flask
import warnings
warnings.filterwarnings("ignore")

# Custom Team NYC imports
from util import map_helpers
from views import filter, metrics, co2_scatter, orig_mapbox, static_co2
from views import map as map_view
from model.trips import Trips

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
REPORT_PATH = PATH.joinpath("notebooks").resolve()

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", 
                          "content": "width=device-width"}]
)
server = app.server

# Load data
trips = Trips(DATA_PATH) 


# Create app layout
"""
Configuration for entire dashboard layout. Pulls in figures from functions modularized from
the views/ directory.
"""
app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div([metrics.get_metrics(),
                 filter.get_filter(trips)],
                 className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="main_graph",config={'displayModeBar': False})],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="teu_graph", config={'displayModeBar': False})],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    [dcc.Graph(id="original_graph", config={'displayModeBar': False})],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    [dcc.Graph(id="individual_graph", config={'displayModeBar': False})],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        
        ),
       # dcc scatter mapbox
       html.Div(
            [
                html.Div(
                    [dcc.Graph(id="static_graph", config={'displayModeBar': False})],
                    className="pretty_container twelve columns",
                )
            ],
        ),    
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)

@app.callback(
    [
        Output("num_trips_text", "children"),
        Output("num_hubs_text", "children"),
        Output("actual_text", "children"),
        Output("optimized_text", "children"),
    ],
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
    ],
)
def update_metrics(zone_types, vessel_types, cluster_slider):
    def agg_metrics(df_full_trips, df_raw_trips):
        df = df_full_trips 
        data = {
            'number_of_trips': len(df_full_trips),
            'number_of_hubs': len(set(df_full_trips['StartHUBPORT_PortID'].unique()).union(
                                set(df_full_trips['ENDHUBPORT_PortID'].unique()))),
            'actual_co2_emission': df_raw_trips['co2_total'].sum(),
            'optimized_co2_emission': df_full_trips['co2_total'].sum()
        }

        return data

    df_raw_trips = trips.get_trips(cluster_size=0.001,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)                       

    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)
    metrics = agg_metrics(df_full_trips, df_raw_trips)
    metrics['actual_co2_emission'] /= 1000000000
    metrics['actual_co2_emission'] = metrics['actual_co2_emission'].round(2)
    metrics['actual_co2_emission'] = f"{metrics['actual_co2_emission']} kT"
    metrics['optimized_co2_emission'] /= 1000000000
    metrics['optimized_co2_emission'] = metrics['optimized_co2_emission'].round(2)
    metrics['optimized_co2_emission'] = f"{metrics['optimized_co2_emission']} kT"
    return metrics['number_of_trips'], metrics['number_of_hubs'], metrics['actual_co2_emission'], metrics['optimized_co2_emission']


@app.callback(
    Output("main_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
    ],
    [State("main_graph", "relayoutData")],
)
def make_hub_and_spoke_figure(zone_types, vessel_types, cluster_slider, main_graph_layout):
    layout = dict(
        margin=dict(l=0, r=0, b=10, t=35),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        title=dict(
            text="Hub and Spoke Optimized Traffic Network",
            xanchor='center',
            x=0.5
        ),
        legend_orientation='h',
        legend_y=-0.05,
        legend_x=0.3
    )

    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)
    figure = map_view.gen_map(df_full_trips, 
                              zone_types=zone_types)
    figure.update_layout(layout)
    return figure

"""
## Mapbox graph plotting start port by port ID assigned
"""
@app.callback(
    Output("original_graph", "figure"),
    [
        Input("zone_types", "value"),
        Input("vessel_types", "value"),
        Input("cluster_slider", "value"),
    ],
    [State("original_graph", "relayoutData")],
)
def make_mapbox_figure(
    zone_types, vessel_types, cluster_slider, main_graph_layout
):
    df = trips.get_trips(cluster_size=cluster_slider,
                         zone_types=zone_types,
                         vessel_types=vessel_types)                       
    figure = orig_mapbox.get_figure(df)
    return figure

# Main graph -> individual graph
@app.callback(Output("individual_graph", "figure"), 
                [
                    Input("zone_types", "value"),
                    Input("vessel_types", "value"),
                    Input("cluster_slider", "value"),
                ]
             )
def make_scatter_figure(zone_types, vessel_types, cluster_slider):
    df_full_trips = trips.get_trips(cluster_size=cluster_slider,
                                    zone_types=zone_types,
                                    vessel_types=vessel_types)
    figure = co2_scatter.get_figure(df_full_trips)
    return figure

# Main graph -> individual graph
@app.callback(Output('teu_graph', 'figure'),
              [Input("zone_types", "value"), 
                Input("vessel_types", "value"),
                Input('main_graph', 'hoverData')])
def make_teu_figure(zone_types, vessel_types, main_graph_hover):
    layout_individual = dict(
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend_orientation='h',
        legend_y=-0.15
    )

    df = trips.get_trips(cluster_size=None,
                        zone_types='All',
                        vessel_types=vessel_types)

    data = []
    if main_graph_hover:
        points_data = main_graph_hover['points'][0]
        if 'text' in points_data:
            text = points_data['text']
            if 'MMSI' in text:
                text = text.split("<br>")
                mmsi = text[0].split()[-1]
                dt = text[1].split()[-1]
                df = df[df['MMSI'] == int(mmsi)]
                df = df[df['BaseDateTime_Start'] == dt]
                df = df[(df['LON_SPOKEStartPort'] == points_data['lon']) |
                        (df['LON_SPOKEEndPort'] == points_data['lon'])]

                df = df[(df['LAT_SPOKEEndPort'] == points_data['lat']) |
                        (df['LAT_SPOKEStartPort'] == points_data['lat'])]

                df = df.sort_values(by=['cluster_size'], ascending=True)
                data = [
                    dict(
                        type='scatter',
                        mode='lines+markers',
                        name='Epsilon vs CO2 Total',
                        x=df['cluster_size'],
                        y=df['co2_total'],
                        xaxis_title="Cluster Size (Epsilon)",
                        yaxis_title="CO2 Efficiency (TEU)",
                        line=dict(
                            shape="spline",
                            smoothing=2,
                            width=1,
                            color='#92d8d8'
                        ),
                        marker=dict(symbol='diamond-open')
                    )
                ]
                
                layout_individual["title"] = "Cluster Size vs CO2 Emissions (Spoke)"
                layout_individual["xaxis_title"] = "Cluster Size (Epsilon)"
                layout_individual["yaxis_title"] = "CO2 Efficiency (TEU)"
                figure = dict(data=data, layout=layout_individual)
                return figure
            elif 'Hub' in text:
                hub_id = text.split()[-1]
    df = trips.get_static_graph()
    df = df.sort_values(by=['epsilons'], ascending=True)
    figure = static_co2.get_figure(df)
    return figure

@app.callback(Output('static_graph', 'figure'),
              [Input("zone_types", "value")])
def make_static_graph(zone_types):
    layout_individual = dict(
        margin=dict(l=30, r=30, b=20, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        title="Hub and Spoke CO2 Map",
        legend_orientation='h',
        legend_y=-0.15,
    )

    df = trips.get_static_graph()
    df = df.sort_values(by=['epsilons'], ascending=True)
    figure = static_co2.get_figure(df)
    return figure


@app.server.route("/data_notebook")
def get_report():
    return flask.send_from_directory(REPORT_PATH, "data_notebook.html")

@app.server.route("/data_co2_notebook")
def get_co2_report():
    return flask.send_from_directory(REPORT_PATH, "co2_calculations.html")

# Main
if __name__ == "__main__":
    app.run_server(debug=False, dev_tools_props_check=False)
