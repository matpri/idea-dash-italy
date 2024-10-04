import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc


def render_plot(df, *args, **kwargs):
    # Create a Plotly table
    db = df.copy()
    db =  db[db.region == 'CAN']
    db = db[['scenario', 'variable', 'value']]
    df_pivot = db.pivot(index='variable', columns='scenario', values='value')
    # Create a Plotly Table
    header_values = ['Variable'] + list(df_pivot.columns)
    cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

    # Create Plotly table


    fig = go.Figure(data=[go.Table(
        header=dict(values=header_values,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=cell_values,
                   fill_color=[['#ffebcc'] * len(cell_values[0])] + [[('lavender' if v < 0 else '#ccffcc') for v in col] for
                                                                     col in cell_values[1:]],
                   align='left'))
    ])


    return fig




def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    classes = df['variable'].unique().tolist()

    scenarios = df['scenario'].unique().tolist()

    base_scenarios = list(set([scenario.split('|')[1] for scenario in scenarios]))
    base_scenarios = ['ALL'] + base_scenarios

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'energy_model-output_stats-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Group By',
            value=0,
            data=[
                {'label': 'No Grouping', 'value': 0},
                {'label': 'Group by Model', 'value': 1},
                {'label': 'Group by Scenario', 'value': 2},
                {'label': 'Group by Version', 'value': 3},
            ],
            id={
                'type': 'energy_model-output_stats-groupby-toggle',
                'index': window_id,
            },
        ),
        dmc.Select(
            label='Scenario Group',
            data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
            value='ALL',
            id={
                'type': 'energy_model-output_stats-scenario-group-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Region',
            value='CAN',
            data=[
                {'label': 'CAN', 'value': 'CAN'},
                {'label': 'AB+QC', 'value': 'AB+QC'},
            ],
            id={
                'type': 'energy_model-output_stats-region-toggle',
                'index': window_id,
            },
        ),
        dmc.Switch(
            label='Fill Area',
            checked=True,
            id={
                'type': 'energy_model-output_stats-fill-switch',
                'index': window_id,
            },
        ),

        dmc.Button('Download Data', id={'type': 'energy_model-output_stats-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-output_stats-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, False, False, False),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'output_stats'
        },
        style={
            'width': '100%',
            'height': '100%'
        }

    )

    return widget_layout, plot_layout
