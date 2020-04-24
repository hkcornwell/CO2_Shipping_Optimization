"""
static_co2.py

Get view for static CO2 Emission vs Epsilon graph
"""

def get_figure(df):
    layout = dict(
        autosize=True,
        automargin=True,
        margin=dict(l=70, r=30, b=50, t=40),
        hovermode="closest",
        plot_bgcolor="#F9F9F9",
        paper_bgcolor="#F9F9F9",
        legend=dict(font=dict(size=10), orientation="h"),
        title="Overall Optimal Epsilon vs CO2 Emissions",
        xaxis=dict(
            title="Cluster Size (Epsilon)",
                ),
        yaxis=dict(
            title="CO2 Emissions (kT)",
        )
    )

    data = [
        dict(
            type='scatter',
            mode='lines+markers',
            name='Epsilon vs CO2 Total',
            x=df['epsilons'],
            y=df['Carbon Emmissions'],
            xaxis_title_text="Cluster Size (Epsilon)",
            line=dict(
                shape="spline",
                smoothing=2,
                width=1,
                color='#92d8d8'
            ),
            marker=dict(symbol='diamond-open')
        )
    ]
    figure = dict(data=data, layout=layout)
    return figure
