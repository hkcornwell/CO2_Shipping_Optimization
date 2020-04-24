"""
orig_mapbox.py

Figure view to get original vessel data
"""

def get_figure(df):
    figure = {
        'data': [{
            'lat': df['LAT_SPOKEStartPort'],
            'lon': df['LON_SPOKEStartPort'],
            'marker':{
                'color': df['StartHUBPORT_PortID'],
                'size': 10,
                'opacity': 1,
                'colorscale':'Jet'
            },
            'customdata': df['StartHUBPORT_PortID'],
            'type':'scattermapbox' ## Different types of mapbox is available
        },
        {
            'lat': df['LAT_SPOKEEndPort'],
            'lon': df['LON_SPOKEEndPort'],
            'marker':{
                'color': df['ENDHUBPORT_PortID'],
                'size': 10,
                'opacity': 1,
                'colorscale':'Jet'
            },
            'customdata': df['ENDHUBPORT_PortID'],
            'type':'scattermapbox' ## Different types of mapbox is available
        }
        ],
        'layout':{
            'mapbox':{
                'accesstoken':'pk.eyJ1IjoiY2hyaWRkeXAiLCJhIjoiY2ozcGI1MTZ3MDBpcTJ3cXR4b3owdDQwaCJ9.8jpMunbKjdq1anXwU5gxIw',
                'center': dict(lon= -75.629536, lat= 24.619554)
            }, ##Access token is taken from https://github.com/plotly/dash-recipes/blob/master/walmart-hover.py
            'hovermode': 'closest',
                'margin':{'l':30, 'r':30, 'b':30, 't':50},
                'title': "Original Freight Traffic Network",
                'showlegend': False
        },
    }
    return figure
