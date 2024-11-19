import json

import dash_mantine_components as dmc
import plotly.graph_objects as go
import shapely
from dash import html, dcc
from components import ids

def render_plot(p_type, df, can=True):
    data = df.copy()
    data['class'], data['variable'] = data['variable'].apply(lambda x: x.split('|')[0]), data['variable'].apply(lambda x: '|'.join(x.split('|')[1:]))
    data = data[data['class'] == p_type]
    if p_type == 'Vre Capacity Factors':
        title = 'Vre Capacity Factors'
        x_label = 'Year'
        y_label = 'Capacity Factor'
        name = 'Capacity Factor'
        unit = '%'
        return plot_vre(data, 'Wind', 'Winter', title, x_label, y_label, name, unit)
    else:
        return go.Figure()


def plot_vre(grid, variable, season, title, x_label, y_label, name, unit):
    grid = grid[grid['variable'] == variable]
    grid = grid[grid['time'] == season]
    # convert the polygons to json
    grid['geometry_json'] = grid['geometry'].apply(lambda x: json.loads(json.dumps(shapely.geometry.mapping(x))))
    grid['geometry_json'] = grid['geometry'].apply(lambda x: shapely.geometry.mapping(x))
    grid_geojson = grid['geometry_json'].to_list()
    # create choropleth map
    fig = go.Figure(go.Choroplethmapbox(geojson=grid_geojson, locations=grid.index, z=grid['value'],
                                        customdata=grid['prov'],
                                        colorscale='Inferno',
                                        marker_line_width=0,  # Add this line here to remove grid outlines
                                        hovertemplate=f"Variable: {variable}<br>Season: {season}<br>" + 'Value: %{z}' + f'{unit}' + '<extra></extra>'
                                        ))

    # update layout
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129},
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
    #print('plotting inputs')
    classes = df['variable'].apply(lambda x: x.split('|')[0]).unique()

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
