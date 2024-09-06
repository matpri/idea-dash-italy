import dash_mantine_components as dmc
import geojson
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from dash import html, dcc
import matplotlib.pyplot as plt

from profiles.silver_output.visualization_scripts.utils import total_plot, region_plot

regions = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick',
           'Nova Scotia', 'Prince Edward Island', 'Newfoundland and Labrador', 'Yukon', 'Northwest Territories',
           'Nunavut']
with open('profiles/copper_output/visualization_scripts/utils/canada.geojson') as f:
    canada = geojson.load(f)


def render_plot(type, df, scenario, selected_time, time_size='hourly'):
    print('updating map plot', selected_time)
    scen_df = df[(df['scenario'] == scenario) & (df['classes'] == type)].copy()
    scen_df['time'] = pd.to_datetime(scen_df['time'])
    scen_df = scen_df.dropna(axis=1, how='all')
    # groupby time based on time_size
    if time_size == 'daily':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d')
    elif time_size == 'monthly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m')
    elif time_size == 'yearly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y')
    else:
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    cols = scen_df.columns.tolist()
    # remove value column
    cols.remove('value')
    scen_df = scen_df.groupby(cols).sum(numeric_only=True).reset_index()

    choropleth_layer = px.choropleth(
        geojson=canada, locations=regions, featureidkey="properties.name", color=regions,
        color_discrete_map={'British Columbia': 'lightgrey', 'Alberta': 'lightgrey', 'Saskatchewan': 'lightgrey',
                            'Manitoba': 'lightgrey', 'Ontario': 'lightgrey', 'Quebec': 'lightgrey',
                            'New Brunswick': 'lightgrey',
                            'Nova Scotia': 'lightgrey', 'Prince Edward Island': 'lightgrey',
                            'Newfoundland and Labrador': 'lightgrey',
                            'Yukon': 'lightgrey', 'Northwest Territories': 'lightgrey', 'Nunavut': 'lightgrey'},
        scope='north america',
    ).data

    for i in range(len(choropleth_layer)):
        choropleth_layer[i].showlegend = False

    fig = go.Figure()

    for trace in choropleth_layer:
        fig.add_trace(trace)

    if 'Line Flow' not in type:

        techs = scen_df['variable'].unique()
        scen_df['latitude'] = scen_df['latitude'].astype(float)
        scen_df['longitude'] = scen_df['longitude'].astype(float)
        scen_df['value'] = scen_df['value'].astype(float)

        scen_df['time'] = pd.to_datetime(scen_df['time'])
        scen_df = scen_df[scen_df['time'] == selected_time]

        for tech in techs:
            tech_df = scen_df[(scen_df['variable'] == tech)]
            fig.add_trace(go.Scattergeo(
                lon=tech_df['longitude'],
                lat=tech_df['latitude'],
                text=tech_df['variable'],
                name=tech,
                mode='markers',
                marker=dict(
                    size=tech_df['value'] / 30,
                    opacity=0.8,
                    line=dict(width=0)
                ),
                hovertemplate='<b>Technology: %{text}</b><br> Capacity: %{marker.size:.2f} MW<br>',
                showlegend=True
            ))

    else:
        # Initialize frames list and convert data types
        # frames = []
        scen_df['latitude_from'] = scen_df['latitude_from'].astype(float)
        scen_df['latitude_to'] = scen_df['latitude_to'].astype(float)
        scen_df['longitude_from'] = scen_df['longitude_from'].astype(float)
        scen_df['longitude_to'] = scen_df['longitude_to'].astype(float)
        scen_df['value'] = scen_df['value'].astype(float)
        scen_df['time'] = pd.to_datetime(scen_df['time'])

        # Calculate min and max values for color scaling
        min_value = scen_df['value'].min()
        max_value = scen_df['value'].max()

        time_df = scen_df[scen_df['time'] == selected_time]
        for i, row in time_df.iterrows():
            # Calculate color based on value
            color = plt.cm.viridis((row['value'] - min_value) / (max_value - min_value))
            rgba_color = f'rgba({int(color[0] * 255)},{int(color[1] * 255)},{int(color[2] * 255)},{color[3]})'

            fig.add_trace(
                go.Scattergeo(
                    lat=[row['latitude_from'], row['latitude_to']],
                    lon=[row['longitude_from'], row['longitude_to']],
                    mode='lines',
                    line=dict(
                        width=1 + (row['value'] - min_value) / (max_value - min_value) * 10,
                        color=rgba_color
                    ),
                    name=row['region'] + ' Import from ' + row['variable'],
                    showlegend=True,
                )
            )

    fig.update_geos(projection_type="orthographic")
    fig.update_layout(
        title_text='Generator Locations',
        geo=dict(
            showcountries=False, showcoastlines=False, showland=False,
            fitbounds="locations", showlakes=False,
            showrivers=False,
            subunitcolor='white',
            # Enable zoom
            projection_scale=1,
            center=dict(lat=56.1304, lon=-106.3468),
            visible=True,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        # Set legend position using dict format
        legend=dict(y=0.2),
    )
    fig.layout.autosize = True
    fig.update_layout(legend={'itemsizing': 'constant'})
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    classes = df['classes'].unique().tolist()

    scen_df = df[(df['scenario'] == scenarios[0]) & (df['classes'] == classes[0])].copy()

    dates = scen_df['time'].dt.strftime('%Y-%m-%d').unique().tolist()
    time_step = 'hourly'

    date = dates[0]

    # Get the unique values of the time column during the date and sort them
    unique_times = sorted(scen_df[scen_df['time'].dt.strftime('%Y-%m-%d') == date]['time'].unique().tolist())

    date_marks = {
        i: {'label': time.strftime('%H:%M'), 'style': {'transform': 'rotate(90deg) translate(20px, -10px)'}}
        for i, time in enumerate(unique_times)
        if i % 4 == 0  # Show every 4th mark
    }

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'silver-map_plots-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'silver-map_plots-scenario-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value=time_step,
            id={
                'type': 'silver-map_plots-time_step-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Select(
            label='Date',
            data=[{'label': date, 'value': date} for date in dates],
            value=dates[0],
            id={
                'type': 'silver-map_plots-date-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),

        html.Div(id={'type': 'silver-map_plots-time-slider-output', 'index': window_id},
                 children=[dcc.Slider(
                     id={'type': 'silver-map_plots-time-slider', 'index': window_id},
                     min=0,
                     max=len(unique_times) - 1,
                     step=1,
                     value=0,
                     marks=date_marks,
                     tooltip={"placement": "bottom", "always_visible": True},
                     updatemode='drag',
                 )],
                    style={'display': 'block'}
                 ),

        # Add padding div
        html.Div(style={'padding-bottom': '30px'}),

        dmc.Button('Download Data', id={'type': 'silver-map_plots-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-map_plots-download', 'index': window_id}),
    ])

    selected_time = dates[0] + ' ' + unique_times[0].strftime('%H:%M:%S')

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, scenarios[0], selected_time, time_step),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'silver_output',
            'viz': 'map_plots'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
