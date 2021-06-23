#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import networkx as nx
import plotly.graph_objs as go

import pandas as pd
from colour import Color
from datetime import datetime
from textwrap import dedent as d
import json
import tqdm 
from scipy import stats
import numpy as np

from scatter_app_utils import *


# Variables #

TOPIC = ['05', '19', '20', '22', '29'] # Individuals
COLOR = "cdr3_num_nts"


# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Transaction Network"


# styles: for right side hover/click component
styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    #########################Title
    html.Div(html.H1("Edit Distance & PHATE"),
             className="header",
             style={'textAlign': "center"}),
    #############################################################################################define the row
    html.Div(
        className="row",
        children=[
            ##############################################left side two input components
            html.Div(
                className="two columns",
                style={'max-width':'400px'},
                children=[
                    dcc.Markdown(d("""
                            **Topics to Include**
                            """)),
                    html.Div(
                        className="twelve columns",
                        children=[
                            dcc.Checklist(
                                id='my-range-slider',
                                options=[
                                    {'label': 'Individual 5', 'value': '05'},
                                    {'label': 'Individual 19', 'value': '19'},
                                    {'label': 'Individual 20', 'value': '20'},
                                    {'label': 'Individual 22', 'value': '22'},
                                    {'label': 'Individual 29', 'value': '29'},
                                ],
                                value=['05', '19', '20', '22', '29']
                            ),
                            html.Br(),
                            html.Div(id='output-container-range-slider')
                        ],
                        style={'height': '200px'}
                    ),
                    html.Div(
                        id="output",
                        children=[
                            dcc.Markdown(d("""
                                **Color**
                            """)),
                            dcc.Dropdown(
                                id='color',
                                options=[
                                    {'label': 'CDR3 Length', 'value': 'cdr3_num_nts'},
                                    {'label': 'Unique Seqs', 'value': 'uniques'},
                                    {'label': 'Copies', 'value': 'copies'},
                                    {'label': 'J Gene', 'value': 'j_gene'},
                                ],
                                value='cdr3_num_nts'
                            ),
                            html.Br(),
                        ]
                    )
                ]
            ),

            ############################################middle graph component
            html.Div(
                className="eight columns",
                children=[dcc.Graph(id="my-graph",
                                    figure=network_graph(TOPIC, COLOR))],
                style={'max-width': '800px'}
            ),

            #########################################right side two output component
            html.Div(
                className="two columns",
                children=[
                    html.Div(
                        className='twelve columns',
                        children=[
                            dcc.Markdown(d("""
                            **Node Data**

                            Hover to view
                            """)),
                            html.Pre(id='hover-data', style=styles['pre'])

                        ],
                        style={'height': '400px'}),
                    dcc.Markdown(d("""
                            **More Clone Information**
                                """)),
                    html.Div(id='click-data')
                ],
                style={'max-width':'400px'}
            )
        ]
    )
])

###################################callback for left side components
@app.callback(
    dash.dependencies.Output('my-graph', 'figure'),
    [dash.dependencies.Input('my-range-slider', 'value'), 
    dash.dependencies.Input('color', 'value')])
def update_output(value,color):
    TOPIC = value
    COLOR = color
    return network_graph(value, color)

################################callback for right side components
@app.callback(
    dash.dependencies.Output('hover-data', 'children'),
    [dash.dependencies.Input('my-graph', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    dash.dependencies.Output('click-data', 'children'),
    [dash.dependencies.Input('my-graph', 'clickData')])
def display_click_data(clickData):
    # DUMMY CLICK DATA, should be more clone info but placeholder for now
    if clickData :
        video = html.Iframe()
    else : 
        video = html.Iframe()
    return video# json.dumps(clickData, indent=2)



if __name__ == '__main__':
    app.run_server(debug=True)
