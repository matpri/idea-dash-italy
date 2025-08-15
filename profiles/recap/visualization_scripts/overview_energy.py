# import dash_mantine_components as dmc
# import plotly.graph_objects as go
# from dash import html, dcc
# from components import ids
# from profiles.recap.visualization_scripts import requested_quantities

# def plot(df, window_id):
#     '''
#     Energy Demand-only overview visualization
#     :param df: pandas Dataframe containing the data to visualize
#     :param window_id: window id to use when registering components to dash
#     :return: html.Div([widgets]), dcc.Graph(plot)
#     '''
#     # Filter for only Energy Demand data
#     df = df[df['tab'] == 'Energy Demand']
    
#     _w, _fig = requested_quantities.widgets(df, window_id)
    
#     widget_layout = html.Div([
#         html.Div(_w,
#                 id={
#                     'type': 'recap-overview-demand',
#                     'index': window_id
#                 }),
#         html.Button('recap-DEMAND',
#                    id={
#                        'type': 'recap-demand-update',
#                        'index': window_id
#                    }, style={'display': 'none'})
#     ])
    
#     plot_layout = dcc.Graph(
#         figure=_fig,
#         id={
#             'type': 'figure',
#             'index': window_id,
#             'profile': 'recap',
#             'viz': 'Overview Energy'
#         },
#         style={
#             'width': '100%',
#             'height': '100%'
#         }
#     )
    
#     return widget_layout, plot_layout

import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from profiles.recap.visualization_scripts import requested_quantities

def plot(df, window_id):
    '''
    Energy demand-only overview visualization
    :param df: pandas Dataframe containing the energy demand data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # Since this is already filtered to energy demand only, we can directly use it
    # No need to filter by tab since the processing already did that
    
    # Use the requested_quantities visualization for energy demand
    _w, _fig = requested_quantities.widgets(df, window_id)
    
    widget_layout = html.Div([
        html.Div(_w,
                id={
                    'type': 'recap-overview-energy',
                    'index': window_id
                }),
        html.Button('recap-ENERGY',
                   id={
                       'type': 'recap-demand-update',
                       'index': window_id
                   }, style={'display': 'none'})
    ])
    
    plot_layout = dcc.Graph(
        figure=_fig,
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'recap',
            'viz': 'Overview Energy'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    
    return widget_layout, plot_layout