import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

import plotly.graph_objects as go
import plotly.express as px
import panel as pn
import numpy as np
import geojson

from profiles.copper_output import utils

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

    Line_Flow = Line_Flow[Line_Flow['period'] == Year]
    Line_Flow = Line_Flow[Line_Flow['scenario'] == Scenario]

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

        print(group, color, norm_value, length)

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
        print(value, value_log)
        cmap = px.colors.sequential.__dict__[cmap_name]  # get the colormap
        color_idx = int(value_log * (len(cmap) - 1))  # map value to an index in colormap
        return cmap[color_idx]
    return func

def transmission_plot(df, scenario, year, title):
    # normalize the values where max value is 1
    max_value = df['value'].max()
    df['norm_value'] = df['value'] / max_value
    df['norm_value'] = df['norm_value'].fillna(0)

    colorfunc = to_color_plotly(df['norm_value'].min())

    min_value = df['value'].min()
    max_value = df['value'].max()
    df = year_subset(df, year, scenario)



    with open('profiles/copper_output/canada.geojson') as f:
        canada = geojson.load(f)

    regions = ['British Columbia', 'Alberta', 'Saskatchewan', 'Manitoba', 'Ontario', 'Quebec', 'New Brunswick',
               'Nova Scotia', 'Prince Edward Island',
               'Newfoundland and Labrador', 'Yukon', 'Northwest Territories', 'Nunavut']
    colors = ['#a098ce', '#94cecc', '#c2be99', '#b8a891', '#afd6b8', '#bdafac', '#c89195', '#d2beaa', '#d7aabe',
              '#99c1c7', '#cdb9bd', '#aba8c1', '#d3cfae']

    id = np.arange(0, len(regions))

    region_colors = pd.DataFrame({'Region': regions, 'Color': colors, 'id': id})



    fig = px.choropleth(region_colors, geojson=canada, locations='Region', featureidkey="properties.name",
                        color='Region',
                        color_discrete_map=dict(zip(regions, colors)),
                        scope='north america',
                        locationmode='geojson-id',
                        hover_name='Region',
                        title=title,
                        template="simple_white",
                        height=500,
                        )



    for trace in fig.data:
        trace.update(legendgroup=trace.name)

        df_region = df[df['region'] == trace.name]
        df_region = df_region[df_region['value'] != 0]
        template = f'{trace.name} <br><br> Lines: <br>'
        for index, row in df_region.iterrows():
            template += f'{row["short_region"]} -> {row["short_variable"]}: {row["value"]} GW <br>'
        template += '<extra></extra>'
        trace.update(hovertemplate=template)

        # for every entry in df_region add an arrow to the map figure
        add_arrow(fig, df_region, colorfunc, group=trace.name,
                  year=year, scenario=scenario)

    # Create a scatter plot trace to generate the colorbar
    colorbar_trace = go.Scatter(
        x=[None],
        y=[None],

        mode="markers",
        marker=dict(
            cmin=min_value,
            cmax=max_value,
            color=[min_value, max_value] if min_value != max_value else [min_value],
            colorscale='Plasma',
            colorbar=dict(
                          title="Transmission Flow (GW)",
                          titleside="top", x=0,tickmode="array",tickvals=[min_value, max_value] if min_value != max_value else [min_value],ticktext=[min_value, max_value] if min_value != max_value else [min_value],

                            len=0.5,
                          ),
        ),
        showlegend=False,
        # hide y_axis from the
    )

    # add the dummy trace to the figure
    fig.add_trace(colorbar_trace)


    fig.update_geos(showcountries=False, showcoastlines=False,
                    showland=False, fitbounds="locations",
                    subunitcolor='white')

    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                      xaxis_visible=False,
                      yaxis_visible=False,
                      )
    fig.update_xaxes(showticklabels=False, zeroline=False, showgrid=False)
    fig.update_yaxes(showticklabels=False, zeroline=False, showgrid=False)
    fig.layout.autosize = True
    return fig

def render_plot(df, scenarios, year, title):
    return transmission_plot(df, scenarios, year, title)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''

    scenarios = df['scenario'].unique().tolist()
    # years where region is not CAN
    years = df['period'].unique().tolist()
    # make all years int
    years.sort()


    widget_layout = html.Div([
        dmc.Select(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'copper-transmissioncapacity-scenario-multi-select',
                'index': window_id,
            }
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'copper-transmissioncapacity-year-select',
                'index': window_id
            },
        )
    ])

    plot_layout = dcc.Graph(
        figure=render_plot( df, scenarios[0], years[0],
                           title='Transmission Capacity by Year',
                           ),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'copper_output',
            'viz': 'transmission_capacity'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
