import dash_mantine_components as dmc
import geojson
import plotly.graph_objects as go
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
from dash import html, dcc
from components import ids
import matplotlib.pyplot as plt

from profiles.cims_output.processing_scripts.inputs import extant_transmission
from profiles.silver_output.visualization_scripts.utils import total_plot, tech_plot

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
    time_format = '%Y-%m-%d %H:%M:%S'
    if time_size == 'daily':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d')
        time_format = '%Y-%m-%d'
    elif time_size == 'monthly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m')
        time_format = '%Y-%m'
    elif time_size == 'yearly':
        scen_df['time'] = scen_df['time'].dt.strftime('%Y')
        time_format = '%Y'
    else:
        scen_df['time'] = scen_df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    if isinstance(selected_time, str):
        selected_time = datetime.strptime(selected_time, time_format)

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
        techs = scen_df['variable'].dropna().unique()
        scen_df['latitude'] = scen_df['latitude'].astype(float)
        scen_df['longitude'] = scen_df['longitude'].astype(float)
        scen_df['value'] = scen_df['value'].astype(float)

        scen_df['time'] = pd.to_datetime(scen_df['time'])
        scen_df = scen_df[scen_df['time'] == selected_time]

        for tech in techs:
            tech_df = scen_df[(scen_df['variable'] == tech)]
            tech_df['size'] = tech_df['value'].apply(lambda x: max(x, 0)/30)  # Set negative values to 0 for sizing
            fig.add_trace(go.Scattergeo(
                lon=tech_df['longitude'],
                lat=tech_df['latitude'],
                text=tech_df['variable'],
                name=tech,
                customdata=tech_df['value'],
                mode='markers',
                marker=dict(
                    size=tech_df['size'],
                    opacity=0.8,
                    line=dict(width=0)
                ),
                hovertemplate='<b>%{text}</b><br>' +
                              'Capacity: %{customdata:.2f} MW<br>' +
                              f'Time: {selected_time.strftime(time_format)}<br>' +
                              '<extra></extra>',
                showlegend=True
            ))

    else:
        sub_df = df[(df['scenario'] == scenario)].copy()
        sub_df = sub_df.dropna(axis=1, how='all')
        if 'filename' in sub_df.columns:
            bus_locations = sub_df[sub_df['filename'] == 'model inputs|bus_location']
            existing_transmission = sub_df[sub_df['filename'] == 'model inputs|existing transmission']
            bus_locations = bus_locations[bus_locations['scenario'] == scenario][['bus', 'latitude', 'longitude']]
            existing_transmission = existing_transmission[existing_transmission['scenario'] == scenario][
                ['name', 'to bus', 'from bus', 'pmax', 'reactance']]

            # Merge bus locations with existing transmission
            existing_transmission = pd.merge(existing_transmission, bus_locations, left_on='from bus', right_on='bus',
                                             how='left')
            existing_transmission = existing_transmission.rename(
                columns={'latitude': 'latitude_from', 'longitude': 'longitude_from'})
            existing_transmission = pd.merge(existing_transmission, bus_locations, left_on='to bus', right_on='bus',
                                             how='left')
            existing_transmission = existing_transmission.rename(
                columns={'latitude': 'latitude_to', 'longitude': 'longitude_to'})
            existing_transmission = existing_transmission[
                ['name','to bus', 'from bus', 'latitude_from', 'longitude_from', 'latitude_to', 'longitude_to', 'pmax', 'reactance']]

        scen_df['line'] = scen_df.apply(lambda x: f"{x['region']}-{x['variable']}", axis=1)
        scen_df['pmax'] = None
        scen_df['reactance'] = None
        if 'filename' in sub_df.columns:
            existing_transmission['line'] = existing_transmission.apply(lambda x: f"{x['from bus']}-{x['to bus']}", axis=1)
            new_rows = []
            for i, transmission in existing_transmission.iterrows():
                if transmission['line'] in scen_df['line'].dropna().unique():
                    scen_df.loc[scen_df['line'] == transmission['line'], 'pmax'] = transmission['pmax']
                    scen_df.loc[scen_df['line'] == transmission['line'], 'reactance'] = transmission['reactance']
                else:
                    # If the line is not in scen_df, we can add it with a value of 0
                    new_row = {
                        'region': transmission['name'],
                        'variable': transmission['from bus'],
                        'latitude_from': transmission['latitude_from'],
                        'longitude_from': transmission['longitude_from'],
                        'latitude_to': transmission['latitude_to'],
                        'longitude_to': transmission['longitude_to'],
                        'value': 0,
                        'time': selected_time,
                        'line': transmission['line'],
                        'pmax': transmission['pmax'],
                        'reactance': transmission['reactance']
                    }
                    new_rows.append(new_row)

            if new_rows:
                new_rows_df = pd.DataFrame(new_rows)
                scen_df = pd.concat([scen_df, new_rows_df], ignore_index=True)

        scen_df['pmax'] = scen_df['pmax'].fillna(-1)
        scen_df['reactance'] = scen_df['reactance'].fillna(-1)

        # Initialize frames list and convert data types
        # frames = []
        scen_df['latitude_from'] = scen_df['latitude_from'].astype(float)
        scen_df['latitude_to'] = scen_df['latitude_to'].astype(float)
        scen_df['longitude_from'] = scen_df['longitude_from'].astype(float)
        scen_df['longitude_to'] = scen_df['longitude_to'].astype(float)
        scen_df['value'] = scen_df['value'].astype(float)
        scen_df['pmax'] = scen_df['pmax'].astype(float)
        scen_df['reactance'] = scen_df['reactance'].astype(float)
        scen_df['time'] = pd.to_datetime(scen_df['time'])

        # Calculate min and max values for color scaling
        min_value = scen_df['value'].abs().min()
        max_value = scen_df['value'].abs().max()

        time_df = scen_df[scen_df['time'] == selected_time]
        for i, row in time_df.iterrows():
            # Calculate color based on value
            # if max_value == min_value:
            #     color = plt.cm.viridis(0)
            # else:
            color = plt.cm.viridis((row['value'] / row['pmax'])) if row['pmax'] != -1 and row['pmax'] != 0 else plt.cm.viridis(
                (row['value'] - min_value) / (max_value - min_value))
            rgba_color = f'rgba({int(color[0] * 255)},{int(color[1] * 255)},{int(color[2] * 255)},{color[3]})'

            cap_hover = 'Capacity: ' + f'{row["pmax"]:.2f} MW<br>' if row['pmax'] != -1 else ''
            reactance_hover = 'Reactance: ' + f'{row["reactance"]:.2f} Ohm<br>' if row['reactance'] != -1 else ''

            fig.add_trace(
                go.Scattergeo(
                    lat=[row['latitude_from'], row['latitude_to']],
                    lon=[row['longitude_from'], row['longitude_to']],
                    mode='lines',
                    line=dict(
                        width=0.01 + (abs(row['value']) / row['pmax']) if row['pmax'] != -1 and row['pmax'] != 0
                        else 1 + (
                                    abs(row['value']) - min_value) / (
                                                                                                        max_value - min_value) * 10 if max_value != min_value else 1,
                        color=rgba_color
                    ),
                    name=str(row['region']) + ' Import from ' + str(row['variable']),
                    showlegend=True,
                    hovertemplate='<b>' + str(row['region']) + ' Import from ' + str(row['variable']) + '</b><br>' +
                                  'Flow: ' + f'{row["value"]:.2f} MW<br>' +
                                   cap_hover +
                                  reactance_hover +
                                  f'Time: {selected_time.strftime(time_format)}<br>' +
                                  '<extra></extra>',
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
    scenarios = df['scenario'].dropna().unique().tolist()
    classes = df['classes'].dropna().unique().tolist()

    scen_df = df[(df['scenario'] == scenarios[0]) & (df['classes'] == classes[0])].copy()

    dates = scen_df['time'].dt.strftime('%Y-%m-%d').dropna().unique().tolist()
    time_step = 'hourly'

    date = dates[0]

    # Get the unique values of the time column during the date and sort them
    unique_times = sorted(scen_df[scen_df['time'].dt.strftime('%Y-%m-%d') == date]['time'].dropna().unique().tolist())

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
                     updatemode='mouseup',
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
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'SILVER',
            'viz': 'Map Plots'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
