# -*- coding: utf-8 -*-
"""
Created on Thu Sep 09 10:22:20 2021

@author: aprsh
"""

import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import datetime
from datetime import timedelta
import krakenex
from pykrakenapi import KrakenAPI


api = krakenex.API()
k = KrakenAPI(api)  

fig = go.Figure()
app = dash.Dash(__name__)
  
app.layout = html.Div(
    [
        dcc.Graph(id = 'live-graph', animate = True),
        dcc.Interval(
            id = 'graph-update',
            interval = 60000,
            n_intervals = 0
        ),
    ]
)
  
@app.callback(
    Output('live-graph', 'figure'),
    [ Input('graph-update', 'n_intervals') ]
)
  
def update_live_graph(n):
    since = datetime.datetime.now() - datetime.timedelta(0, 900)
    price_data, last = k.get_recent_trades("BTCUSD", since=since, ascending=True)
    if price_data.empty:
        return
    go.Figure().update_layout(
    title="Plot Title",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend_title="Legend Title",
    font=dict(
        family="Courier New, monospace",
        size=18,
        color="RebeccaPurple"
    ))
    data = [go.Scatter(
            x=price_data.index,
            y=list(price_data['price']),
            name='High',
            line=dict(color="#00FF00"),
            mode= 'lines'
    )]
    
  
    return {'data': data,
            'layout' : go.Layout(yaxis = dict(range = [min(price_data['price']),max(price_data['price'])]),)}

  
if __name__ == '__main__':
    app.run_server()
    
  
