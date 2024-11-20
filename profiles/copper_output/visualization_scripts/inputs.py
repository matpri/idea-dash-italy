import json

import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from dash import html, dcc
from components import ids


def render_plot(p_type, df, vre_variable=None, season=None):
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
        return plot_vre(data, vre_variable, season, title, x_label, y_label, name, unit)
    else:
        return go.Figure()


def plot_vre(grid, variable, season, title, x_label, y_label, name, unit):
    grid = grid[grid['variable'] == variable]
    grid = grid[grid['time'] == season]

    # Check if grid is empty after filtering
    if grid.empty:
        fig = go.Figure()
        # add annotations
        fig.add_annotation(
            text="No data available for the selected variable and season",
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            font=dict(size=20),
            align='center',
            ax=0,
            ay=0,
        )
        return fig

    # convert the polygons to json
    grid = grid[['geometry', 'value', 'prov', 'region']]

    gdf = gpd.GeoDataFrame(grid, geometry='geometry')

    # Convert GeoDataFrame to GeoJSON
    geojson = gdf.__geo_interface__
    fig = go.Figure(
        go.Choroplethmapbox(
            geojson=geojson, locations=gdf['region'], z=gdf['value'],
            featureidkey="properties.region",
            customdata=gdf['prov'],
            colorscale='Inferno',
            marker_line_width=0,  # Add this line here to remove grid outlines
            hovertemplate=f"Variable: {variable}<br>Season: {season}<br>" + 'Value: %{z}<extra></extra>'
        )
    )

    # update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=2.5, mapbox_center={"lat": 540902, "lon": -95.7129},
        geo=dict(
            showframe=False,
            bgcolor='rgba(0,0,0,0)'),

    )


    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)

    fig.update_geos(projection_type="orthographic")
    fig.layout.template = None
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting inputs')
    classes = df['variable'].apply(lambda x: x.split('|')[0]).unique()
    print(classes)
    seasons = []
    vre_variables = []
    if 'Vre Capacity Factors' in classes:
        seasons = ['Winter', 'Summer']
        vre_variables = ['Wind', 'Solar']



    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'copper-inputs-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Season',
            data=[{'label': season, 'value': season} for season in seasons],
            value=seasons[0] if seasons else '',
            id={
                'type': 'copper-inputs-season-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='VRE Variable',
            data=[{'label': vre_variable, 'value': vre_variable} for vre_variable in vre_variables],
            value=vre_variables[0] if vre_variables else '',
            id={
                'type': 'copper-inputs-vre-variable-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Button('Download Data', id={'type': 'copper-inputs-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'copper-inputs-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df),
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
