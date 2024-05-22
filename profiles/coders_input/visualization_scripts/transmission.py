import dash_mantine_components as dmc
import geojson
from dash import html, dcc

import plotly.express as px
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


with open('profiles/copper_output/visualization_scripts/utils/canada.geojson') as f:
    canada = geojson.load(f)

regions = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick',
           'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories',
           'Nunavut']
def render_plot(df):
    df['latitude_start'] = df['latitude_start'].astype(float)
    df['longitude_start'] = df['longitude_start'].astype(float)
    df['latitude_end'] = df['latitude_end'].astype(float)
    df['longitude_end'] = df['longitude_end'].astype(float)
    df['summer_capacity'] = df['summer_capacity'].astype(float)
    df = create_color_map(df)
    fig_base = px.choropleth(
        geojson=canada, locations=regions, featureidkey="properties.name", color=regions,
        color_discrete_map={'British Columbia': 'lightgrey', 'Alberta': 'lightgrey', 'Saskatchewan': 'lightgrey',
                            'Manitoba': 'lightgrey', 'Ontario': 'lightgrey', 'Quebec': 'lightgrey',
                            'New Brunswick': 'lightgrey',
                            'Nova Scotia': 'lightgrey', 'Prince Edward Island': 'lightgrey',
                            'Newfoundland and Labrador': 'lightgrey',
                            'Yukon': 'lightgrey', 'Northwest Territories': 'lightgrey', 'Nunavut': 'lightgrey'},
        scope='north america',
    )
    fig_base.update_geos(projection_type="natural earth")

    fig = go.Figure(
        data=fig_base.data,
        layout=go.Layout(
        )
    )
    for i, row in df.iterrows():
        fig.add_trace(go.Scattergeo(
            lon=[row['longitude_start'], row['longitude_end']],
            lat=[row['latitude_start'], row['latitude_end']],
            mode='lines',
            line=dict(
                color=row['color'],
            ),
            hovertemplate=f'<b>Capacity: {row["summer_capacity"]} MW</b><extra></extra>'
        ))

    fig.update_geos(projection_type="natural earth")
    fig.update_layout(
        title_text='Transmission Lines',
        showlegend=False,
        geo=dict(
            showcountries=False, showcoastlines=False, showland=False,
            fitbounds="locations", showlakes=False,
            showrivers=False,
            subunitcolor='white'
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''

    widget_layout = html.Div([
        dmc.Button('Download Data', id={'type': 'coders_input-transmission-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'coders_input-transmission-download', 'index': window_id}),
    ], style={'textAlign': 'center'})

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
