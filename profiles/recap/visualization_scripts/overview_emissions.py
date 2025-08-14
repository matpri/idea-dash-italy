import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from profiles.recap.visualization_scripts import ghg

def plot(df, window_id):
    '''
    Emissions-only overview visualization
    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # Filter for only Emissions data
    # df = df[df['tab'] == 'Emissions']
    
    # _w, _fig = ghg.widgets(df, window_id)
    
    # widget_layout = html.Div([
    #     html.Div(_w,
    #             id={
    #                 'type': 'recap-overview-emissions',
    #                 'index': window_id
    #             }),
    #     html.Button('recap-EMISSIONS',
    #                id={
    #                    'type': 'recap-emissions-update',
    #                    'index': window_id
    #                }, style={'display': 'none'})
    # ])
    tabs = df['tab'].unique().tolist()
    tabs = ['Emissions'] if 'Emissions' in tabs else tabs  # Ensure only Emissions tab is present

    widgets = []
    fig = go.Figure()
    if 'Emissions' in tabs:
        _w, _fig = ghg.widgets(df[df['tab'] == 'Emissions'], window_id)
        widgets.append(html.Div(_w,
                                id={
                                    'type': 'recap-overview-emissions',
                                    'index': window_id
                                },
                                style={'display': 'block'} if tabs[0] == 'Emissions' else {'display': 'none'}
                                )
                       )
        widgets.append(html.Button('recap-EMISSIONS',
                                   id={
                                       'type': 'recap-emissions-update',
                                       'index': window_id
                                   }, style={'display': 'none'}))
        if tabs[0] == 'Emissions':
            fig = _fig

    widget_layout = html.Div([
        dmc.Select(
            label='Reporting Variable',
            data=[{'label': plot, 'value': plot} for plot in tabs],
            value=tabs[0],
            id={
                'type': 'recap-overview-tabs-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        *widgets
    ])
    plot_layout = dcc.Graph(
        figure=_fig,
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'recap',
            'viz': 'Overview Emissions'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    
    return widget_layout, plot_layout