import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from profiles.recap.callbacks.ghg import emissions_mapping
from profiles.recap.visualization_scripts import requested_quantities, stock_lcc, ghg


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    tabs = df['tab'].unique().tolist()

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
    if 'Energy Demand' in tabs:
        _w, _fig = requested_quantities.widgets(df[df['tab'] == 'Energy Demand'], window_id)
        widgets.append(html.Div(_w,
                                id={
                                    'type': 'recap-overview-demand',
                                    'index': window_id
                                },
                                style={'display': 'block'} if tabs[0] == 'Energy Demand' else {'display': 'none'}
                                )
                       )
        widgets.append(html.Button('recap-DEMAND',
                                   id={
                                       'type': 'recap-demand-update',
                                       'index': window_id
                                   }, style={'display': 'none'}))
        if tabs[0] == 'Energy Demand':
            fig = _fig
    if 'Technology Stocks' in tabs:
        _w, _fig = stock_lcc.widgets(df[df['tab'] == 'Technology Stocks'], window_id)
        widgets.append(html.Div(
            _w,
            id={
                'type': 'recap-overview-stocks',
                'index': window_id
            },
            style={'display': 'block'} if tabs[0] == 'Technology Stocks' else {'display': 'none'}
        )
        )
        widgets.append(html.Button('recap-STOCKS',
                                   id={
                                       'type': 'recap-stocks-update',
                                       'index': window_id
                                   }, style={'display': 'none'}))
        if tabs[0] == 'Technology Stocks':
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
        figure=fig,
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'Summary',
            'viz': 'Overview'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
