import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc


def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'

def render_plot(df, *args, **kwargs):
    # Create a Plotly table
    db = df.copy()
    db = db[db.region == 'CAN']
    db = db[['scenario', 'variable', 'value']]
    df_pivot = db.pivot(index='variable', columns='scenario', values='value')
    # fill na with ''
    df_pivot = df_pivot.fillna('')
    # Create a Plotly Table
    header_values = [''] + list(df_pivot.columns)
    cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

    min_value = df['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
    max_value = df['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

    def normalize(value):
        if isinstance(value, (int, float)):
            return (value - min_value) / (max_value - min_value)
        return None

    colors = []

    for col in df_pivot.columns:
        normalized_data = [normalize(val) for val in df_pivot[col]]
        colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in normalized_data])]


    colors_by_row = [['#ffffff', '#e5eeec' ] * (len(df_pivot.index) //2)] + colors# Determine font colors based on the background color
    font_colors = [['#000000'] * len(df_pivot.index)]
    for column in colors:
        font_colors.append([get_contrasting_font_color(color) for color in column])
    # Calculate the width for each column
    column_width = []
    column_width.append(max(df_pivot.index.str.len()) * 8)
    for col in df_pivot.columns:
        column_width.append(max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8)


    print(column_width)


    # Create Plotly table
    fig = go.Figure(data=[go.Table(
        columnorder = [i+1 for i in range(len(df_pivot.columns) + 1)],
        columnwidth=column_width,
        header=dict(values=header_values,
                    fill_color=['#ffffff', '#248ce6', '#248ce6'],
                    font=dict(color='white'),
                    align='center'),
        cells=dict(values=cell_values,
                   fill_color=colors_by_row,
                   line_color= colors_by_row,
                   font=dict(color=font_colors),

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
