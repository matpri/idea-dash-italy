import dash_mantine_components as dmc
from dash import html, dcc

import pandas as pd
import plotly.graph_objects as go

import matplotlib

def create_color_map(df, cmap='viridis'):
    max_capacity = df['summer_capacity'].max()
    min_capacity = df['summer_capacity'].min()
    df['color'] = (df['summer_capacity'] - min_capacity) / (max_capacity - min_capacity)

    # apply color map viridis
    df['color'] = df['color'].apply(lambda x: matplotlib.cm.get_cmap(cmap)(x))
    # make color to string with rgba
    df['color'] = df['color'].apply(lambda x: f'rgba({int(x[0] * 255)}, {int(x[1] * 255)}, {int(x[2] * 255)}, 0.8)')
    return df


def render_plot(df):
    df['latitude_start'] = df['latitude_start'].astype(float)
    df['longitude_start'] = df['longitude_start'].astype(float)
    df['latitude_end'] = df['latitude_end'].astype(float)
    df['longitude_end'] = df['longitude_end'].astype(float)
    df['summer_capacity'] = df['summer_capacity'].astype(float)

    df = create_color_map(df)
    fig = go.Figure()
    for i, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row['longitude_start'], row['longitude_end']],
            lat=[row['latitude_start'], row['latitude_end']],
            mode='lines',
            line=dict(
                color=row['color'],
            )

        ))

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        title_text='Transmission Lines',
        showlegend=False,
        geo=dict(
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
    )

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''

    widget_layout = html.Div(['No widgets available for this visualization.'], style={'textAlign': 'center'})

    plot_layout = dcc.Graph(
        figure=render_plot(df),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'coders_input',
            'viz': 'transmission'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
