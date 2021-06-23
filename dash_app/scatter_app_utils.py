#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import plotly.graph_objs as go

import pandas as pd
from colour import Color
import json
from scipy import stats
import numpy as np


def network_graph(topics, color):
    if topics == None or topics == [] : 
        topics = ['05', '19', '20', '22', '29']
    if color == None : 
        color = "cdr3_num_nts"
    
    data = pd.read_csv('multi_individuals_phate.tsv', sep = '\t')

    # Filter by timepoint selected
    data = data[(data['subject'].isin(['IHCV2020-0' + t for t in topics]))].reset_index(drop=True)

    num_nodes = len(data['clone_id'])


    traceRecode = []  # contains node_trace, middle_node_trace

    # use the phate diffusion constant as specified by filt
    x_axis = 'phate1'
    y_axis = 'phate2'
    x = data[x_axis]
    y = data[y_axis]

    ########################################################################################
    ##### DEALING WITH COLOR NONSENSE ###########

    marker_colors = []

    if color in ['cdr3_num_nts', 'uniques', 'copies'] :
        # special color arrangement
        c = np.asarray(data[color])
        temp = c.argsort()
        ranks = np.empty_like(temp)
        ranks[temp] = np.arange(len(c))
        ranks = ranks.astype('int')

        colors = list(Color('lightcoral').range_to(Color('darkred'), num_nodes))
        # colors = list(Color('LightSkyBlue').range_to(Color('darkred'), num_nodes))
        colors = np.asarray(['rgb' + str(tuple(np.around(x.rgb, 3))) for x in colors])

        marker_colors = colors[ranks]
    elif color == 'j_gene' : 
        marker_colors = [int(n[4]) for n in np.asarray(data[color])]

    else : 
        marker_colors = np.asarray(data[color])

    # Small fix for allowing equal rank sorting
    '''
    rank_copy = np.array(ranks)
    for i in range(len(ranks)-1) : 
        r1 = ranks[i]
        r2 = ranks[i+1]
        if np.greater_equal(data[color][r1], data[color][r2]) : 
            rank_copy[r2] = rank_copy[r1]
    ranks = rank_copy
    '''
    ############################################################################################################################################################

    node_trace = go.Scatter(x=x, y=y, ids=data['clone_id'], hovertext=data['j_gene'], 
                            mode='markers+text', textposition="bottom center",
                            hoverinfo="text", 
                            marker=dict(color=marker_colors))
                            # marker={'size': 10, 'color': 'LightSkyBlue'}) # text=data['Title'],

    traceRecode.append(node_trace)

    #################################################################################################################################################################
    figure = {
        "data": traceRecode,
        "layout": go.Layout(title='PHATE', showlegend=False, hovermode='closest',
                            margin={'b': 20, 'l': 20, 'r': 20, 't': 80},
                            xaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            yaxis={'showgrid': False, 'zeroline': False, 'showticklabels': False},
                            height=600,
                            # annotations=[annotation],
                            clickmode='event+select'
                            )}

    return figure
    