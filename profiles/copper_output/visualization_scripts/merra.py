import json

import dash_mantine_components as dmc
import plotly.graph_objects as go
import shapely
from dash import html, dcc


def vre_plot(grid, variable, year):
    '''
    Creates a plot of VRE capacity factors as a heatmap. Using the latitude and longitude of the VRE generators in the df as the center of a square grid cell,
     the capacity factor of the VRE generator is used to color the grid cell.
    :param df:
    :return:
    '''
    grid = grid[grid['variable'] == variable]
    grid = grid[grid['time'] == year]
    # convert the polygons to json
    grid['geometry_json'] = grid['geometry'].apply(lambda x: json.loads(json.dumps(shapely.geometry.mapping(x))))
    grid_geojson = json.loads(grid.to_json())
    # create choropleth map
    fig = go.Figure(go.Choroplethmapbox(geojson=grid_geojson, locations=grid.index, z=grid['value'],
                                        customdata=grid['prov'],
                                        colorscale='Inferno',
                                        marker_line_width=0, # Add this line here to remove grid outlines
                                        hovertemplate=f"Variable: {variable}<br>Year: {year}<br>" + 'Value: %{z}<extra></extra>'
                                        ))

    # update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129},
        geo=dict(
            showframe=False,
            bgcolor='rgba(0,0,0,0)'),
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )
    fig.update_geos(projection_type="orthographic")
    fig.layout.template = None
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    variables = df['variable'].unique()
    years = df['time'].unique()

    widget_layout = html.Div(
        [
            dmc.Select(
                label='Select Variable',
                id={'type': 'copper_output-vre-variable-dropdown', 'index': window_id},
                data=[{'label': variable, 'value': variable} for variable in variables],
                value=variables[0]
            ),

            dmc.Select(
                label='Select Year',
                id={'type': 'copper_output-vre-year-dropdown', 'index': window_id},
                data=[{'label': year, 'value': year} for year in years],
                value=years[0]
            ),

            dmc.Button('Download Data', id={'type': 'copper_output-vre-download-button', 'index': window_id},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': 'copper_output-vre-download', 'index': window_id}),
        ],
        style={'textAlign': 'center'})
    plot_layout = dcc.Graph(
        figure=vre_plot(df, variables[0], years[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'copper_output',
            'viz': 'vre'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
