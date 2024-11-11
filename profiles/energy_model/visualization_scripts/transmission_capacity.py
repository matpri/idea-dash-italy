import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc
from components import ids
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import geojson

from profiles.energy_model.visualization_scripts.utils import bar_over_regions
from profiles.energy_model import utils

def aggregate_lines(df):
    sum_values = df.groupby(['line', 'start', 'end'])["value"].sum().reset_index()

    # calculate the sum of the values for each connection
    connection_sum = df.groupby(['connection'])["value"].sum().reset_index()

    # separate connection_sum into two columns one for all connections with -> and one for all connections with <-
    larrow = connection_sum[connection_sum['connection'].str.contains('<-')]
    rarrow = connection_sum[connection_sum['connection'].str.contains('->')]

    # replace the -> and <- in larrow and rarrow connection with <-> so that the connection names match the names in the sum_values dataframe
    larrow['connection'] = larrow['connection'].str.replace('<-', '<->')
    rarrow['connection'] = rarrow['connection'].str.replace('->', '<->')

    # rename connection column to line so that it matches the column name in sum_values
    larrow = larrow.rename(columns={'connection': 'line', 'value': 'larrow'})
    rarrow = rarrow.rename(columns={'connection': 'line', 'value': 'rarrow'})

    # add larrow and rarrow together to sum_values as two new columns with titles larrow and rarrow match by
    sum_values = pd.merge(sum_values, larrow, on=['line'], how='left')
    sum_values = pd.merge(sum_values, rarrow, on=['line'], how='left')

    avg_lon_lat = df.groupby(['region', 'variable', 'line'])[[
        'from_lon', 'from_lat', 'to_lon', 'to_lat']].mean().reset_index()

    df = pd.merge(sum_values, avg_lon_lat, on=['line'], how='left')

    # fill nan in larrow and rarrow with 0
    df['larrow'] = df['larrow'].fillna(0)
    df['rarrow'] = df['rarrow'].fillna(0)

    df['bidirectional'] = df['value'] - (df['larrow'] + df['rarrow'])

    return df


def year_subset(Line_Flow, Year, Scenario):
    Line_Flow['from_lon'] = pd.to_numeric(Line_Flow['from_lon'])
    Line_Flow['from_lat'] = pd.to_numeric(Line_Flow['from_lat'])
    Line_Flow['to_lon'] = pd.to_numeric(Line_Flow['to_lon'])
    Line_Flow['to_lat'] = pd.to_numeric(Line_Flow['to_lat'])
    Line_Flow = Line_Flow[Line_Flow['scenario'] == Scenario]
    Line_Flow = Line_Flow[Line_Flow['period'] == Year]

    # Line_Flow = aggregate_lines(Line_Flow)
    Line_Flow = Line_Flow[Line_Flow['value'] != 0]
    return Line_Flow


def add_arrow(fig, df: pd.DataFrame, cfunc, group=None, year=None, scenario=None):
    """
    function that adds an arrow to the map figure
    the arrow is placed at the midpoint of the line between from_lon, from_lat and to_lon, to_lat
    the arrow is length long and color color
    We first normalize the vector between the two points and then multiply by length to get the arrow vector
    Then we add the arrow vector to the midpoint to get the arrow head

    """
    for i in range(len(df)):
        from_lon = df['from_lon'].iloc[i]
        from_lat = df['from_lat'].iloc[i]
        to_lon = df['to_lon'].iloc[i]
        to_lat = df['to_lat'].iloc[i]
        value = df['value'].iloc[i]
        norm_value = df['norm_value'].iloc[i]
        color = cfunc(norm_value)
        length = norm_value + 0.5 #np.exp(norm_value)/np.exp(df['norm_value'].max())

        #print(group, color, norm_value, length)

        # normalize the vector between the two points
        x = (to_lon - from_lon) / np.sqrt((to_lon - from_lon) ** 2 + (to_lat - from_lat) ** 2)
        y = (to_lat - from_lat) / np.sqrt((to_lon - from_lon) ** 2 + (to_lat - from_lat) ** 2)

        # get the midpoint of the line

        # get the arrow vector
        x_arrow = x * length
        y_arrow = y * length


        width = length * 0.035  # 2*widh is the width of the arrow base as triangle

        w = (np.array([-y_arrow, x_arrow]) * 10) * width


        fig.add_trace(
            go.Scattergeo(
                lon=[
                    from_lon - x_arrow - w[0],
                    from_lon - x_arrow + w[0],
                    from_lon + w[0],
                    from_lon + (2 * w[0]),
                    from_lon + x_arrow,
                    from_lon - (2 * w[0]),
                    from_lon - w[0],
                    from_lon - x_arrow - w[0],
                ],
                lat=[
                    from_lat - y_arrow - w[1],
                    from_lat - y_arrow + w[1],
                    from_lat + w[1],
                    from_lat + (2 * w[1]),
                    from_lat + y_arrow,
                    from_lat - (2 * w[1]),
                    from_lat - w[1],
                    from_lat - y_arrow - w[1],
                ],
                mode='lines',
                fill='toself',
                fillcolor=color,
                line_color=color,
                legendgroup=group,
                name=f'{df["short_region"].iloc[i]} -> {df["short_variable"].iloc[i]}',
                showlegend=False,
                hovertemplate=f'Connection: {group} <br>Value: {round(value,4)} GW <br> Year {year} <br> Scenario {scenario}<br><br> Line {df["short_region"].iloc[i]} -> {df["short_variable"].iloc[i]}<br><br><extra></extra>',
                )
        )


def to_color_plotly(min_value):
    def func(value, cmap_name='Plasma'):
        if value == 0:
            value_log = 1 - 0
        else:
            value_log = 1 - (np.log(value) / np.log(min_value)) # transform value to logarithmic scale between 0 and 1
        # if value_log is nan set it to 0
        value_log = 0 if np.isnan(value_log) else value_log
        #print(value, value_log)
        cmap = px.colors.sequential.__dict__[cmap_name]  # get the colormap
        color_idx = int(value_log * (len(cmap) - 1))  # map value to an index in colormap
        return cmap[color_idx]
    return func

def transmission_plot(df, scenario, year, title):
    df['line'] = df['short_region'] + ' -> ' + df['short_variable']

    min_value = df['value'].min()
    max_value = df['value'].max()
    df = year_subset(df, year, scenario)

    # round value, total, cumsum to 2 decimal places
    df['value'] = df['value'].round(2)

    if df.empty:
        fig = go.Figure()
        fig.update_layout(
            title_text=title,
            template="simple_white",
        )
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="No data available, since the results are all zero.",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )
        fig.layout.autosize = True
        return fig


    with open('profiles/energy_model/visualization_scripts/utils/canada.geojson') as f:
        canada = geojson.load(f)
    with open('profiles/energy_model/visualization_scripts/utils/arrows.geojson') as f:
        arrow = geojson.load(f)

    regions = list(set(df['region'].unique().tolist() + df['variable'].unique().tolist()))

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
    for area in fig_base.data:
        area.showlegend = False  # turn off legend
        df_region = df[df['region'] == area.name]
        df_region = df_region[df_region['value'] != 0]
        template = f'{area.name}<extra></extra>'
        area.update(hovertemplate=template)
    fig_base.update_layout(margin=dict(l=0, r=0, t=0, b=0))

    fig = go.Figure(
        data=fig_base.data,
        layout=go.Layout(
        )
    )
    df['text'] = f'Year: {year} <br> Line: ' + df.line.astype(str) + '<br>' + 'Scenario: ' + df.scenario.astype(
        str) + '<br>' + 'Total Capacity: ' + df['value'].astype(str) + ' GW <br>' #+ \
        #          'New Capacity: ' + df['value'].astype(str) + ' GW <br>' + 'Total Capacity: ' + df['total'].astype(
        # str) + " GW"

    fig_overlay = go.Figure(
        data=go.Choropleth(
            locations=df['line'],
            z=df['value'],
            geojson=arrow,
            featureidkey="properties.name",
            colorscale='GnBu',
            zmin=min_value,
            zmax=max_value,
            text=df['text'],
        )
    )
    fig_overlay.update_traces(coloraxis="coloraxis2")
    fig_overlay.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.add_traces(fig_overlay.data)

    fig.update_layout(coloraxis2=dict(cmin=min_value, cmax=max_value, colorbar=dict(x=0.9),
                                      # set colorscale
                                      colorscale='GnBu', colorbar_title='Transmission Capacity (GW)'))
    fig.update_geos(showcountries=False, showcoastlines=False, showland=False, fitbounds="locations", showlakes=False,
                    showrivers=False,
                    subunitcolor='white')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_geos(projection_type="orthographic")
    # remove box around plot
    fig.update_layout(showlegend=False)
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.layout.autosize = True
    return fig

def render_plot(type, df, scenarios, year):
    from profiles.energy_model.utils import plot_settings
    name = plot_settings['Transmission Capacity']['name']
    unit = plot_settings['Transmission Capacity']['unit']
    print('scenarios', scenarios)
    if type == 'Map Plot':
        plot_info = plot_settings['Transmission Capacity']['Map Plot']
        return transmission_plot(df, scenarios, year, plot_info['title'])
    if type == 'Bar Plot':
        plot_info = plot_settings['Transmission Capacity']['Bar Plot']
        df = df.copy()
        df['region'] = df['short_region'] + '<br>-><br>' + df['short_variable']
        df['variable'] = 'Capacity'
        df = df.rename(columns={'period': 'time'})
        return bar_over_regions.plot(df, scenarios, False, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)



def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    base_scenarios = list(set([scenario.split('|')[1] for scenario in scenarios]))
    base_scenarios = ['ALL'] + base_scenarios
    # years where region is not CAN
    years = df['period'].unique().tolist()
    years.sort()


    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Map Plot', 'Bar Plot']],
            value='Map Plot',
            id={
                'type': 'energy_model-transmissioncapacity-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'energy_model-transmissioncapacity-scenario-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'energy_model-transmissioncapacity-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'none'},
        ),
        dmc.Select(
            label='Scenario Group',
            data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
            value=[base_scenarios[0]],
            id={
                'type': 'energy_model-transmissioncapacity-scenario-group-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'energy_model-transmissioncapacity-year-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'energy_model-transmissioncapacity-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-transmissioncapacity-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Map Plot', df, scenarios[0], years[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'transmission_capacity'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
