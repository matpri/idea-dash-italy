import json

import dash_mantine_components as dmc
import geojson
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

from components import ids

from profiles.copper_output.visualization_scripts.input_utils import transmission_cost, cost, extant_capacity, demand, \
    vre, params, extant_transmission, policy


def render_plot(p_type, df, vre_variable=None, season=None, vre_scenario=None,
                _policy_scenarios=None, _p_variable=None, _p_scenario=None,
                _t_cost_scenarios=None,
                e_p_type=None, e_scenarios=None, e_region=None, e_year=None,
                _c_type=None, _c_scenario=None, _c_region=None,
                _demand_plot_type=None, _demand_region=None, _demand_multi_scenario=None,
                _demand_scenario=None, _demand_year=None, _demand_month=None, _demand_date=None, _demand_time_step=None,
                t_p_type=None, t_scenarios=None, t_year=None
                ):
    data = df.copy()
    data['class'], data['variable'] = data['variable'].apply(lambda x: x.split('|')[0]), data['variable'].apply(
        lambda x: '|'.join(x.split('|')[1:]))
    data = data[data['class'] == p_type]
    if p_type == 'Vre Capacity Factors':
        title = 'Vre Capacity Factors'
        x_label = 'Year'
        y_label = 'Capacity Factor'
        name = 'Capacity Factor'
        unit = '%'
        return vre.render(data, vre_variable, season, title, x_label, y_label, vre_scenario, name, unit)
    elif p_type == 'Extant Transmission':
        return extant_transmission.render(t_p_type, data, t_scenarios, t_year)
    elif p_type == 'Extant Capacity':
        return extant_capacity.render(e_p_type, data, False, e_scenarios, e_region, e_year, e_scenarios)
    elif p_type == 'Demand':
        return demand.render(_demand_plot_type, data, _demand_scenario, _demand_multi_scenario, _demand_region, _demand_year, _demand_month, _demand_date, 'Demand', 'Time',
                             'Demand (MW)', time_size=_demand_time_step)
    elif p_type == 'Cost':
        return cost.render(data, _c_type, _c_scenario, _c_region)
    elif p_type == 'Transmission Costs':
        return transmission_cost.render(data, _t_cost_scenarios)
    elif p_type == 'Technology Parameter':
        data = data[data['variable'].str.startswith(_p_variable)]
        return params.render(data, _p_scenario)
    elif p_type == 'Policy':
        return policy.render(data, _policy_scenarios, True)
    else:
        return go.Figure()


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting inputs')
    classes = df['variable'].apply(lambda x: x.split('|')[0]).unique()
    print(classes)

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value='',
            id={
                'type': 'copper-inputs-plot-select',
                'index': window_id
            },
        ),
        vre.create_widgets(df, classes, window_id),
        extant_capacity.create_widgets(df, classes, window_id),
        demand.create_widgets(df, classes, window_id),
        cost.create_widgets(df, classes, window_id),
        transmission_cost.create_widgets(df, classes, window_id),
        params.create_widgets(df, classes, window_id),
        extant_transmission.create_widgets(df, classes, window_id),
        policy.create_widgets(df, classes, window_id),
        dmc.Button('Download Data', id={'type': 'copper-inputs-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'copper-inputs-download', 'index': window_id}),
    ])

    fig = go.Figure()
    fig.add_annotation(text='Select a plot type to visualize the data', showarrow=False, xref='paper', yref='paper',
                       x=0.5, y=0.5, font=dict(size=20), align='center', ax=0, ay=0)

    plot_layout = dcc.Graph(
        figure=fig,
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'copper_output',
            'viz': 'inputs'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
