import json

import dash_mantine_components as dmc
import geojson
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from dash import html, dcc
from matplotlib.dates import datestr2num

from components import ids
from profiles.copper_output import utils
from profiles.copper_output.visualization_scripts.utils import bar_over_regions, bar_over_years, trend_over_years, \
    pie_chart

def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'

def render_cost(data, _c_type, _c_scenario, _c_region):
    data = data[data['variable'].str.startswith(_c_type)]
    unit = data['unit'].iloc[0]

    data['variable'] = data['variable'].replace(_c_type + '|', '', regex=True)
    return trend_over_years.plot(data, _c_scenario, _c_region, False, _c_type, 'x', 'y', _c_type, unit)


def render_t_cost(data, _t_cost_scenario):
    data = data[data['scenario'].isin(_t_cost_scenario)]
    if not data.empty:
        # create a table
        data = data[['scenario', 'variable', 'value']]

        df_pivot = data.pivot(index='variable', columns='scenario', values='value')


        df_pivot = df_pivot.fillna('')
        # Create a Plotly Table
        header_values = [''] + list(df_pivot.columns)
        cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

        min_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
        max_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

        def normalize(value):
            if isinstance(value, (int, float)):
                return (value - min_value) / (max_value - min_value)
            return None

        colors = []

        for col in df_pivot.columns:
            normalized_data = [normalize(val) for val in df_pivot[col]]
            colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[
                                     0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in
                                 normalized_data])]

        colors_by_row = [['#ffffff', '#e5eeec'] * (
                    len(df_pivot.index) // 2)] + colors  # Determine font colors based on the background color
        font_colors = [['#000000'] * len(df_pivot.index)]
        for column in colors:
            font_colors.append([get_contrasting_font_color(color) for color in column])
        # Calculate the width for each column
        column_width = []
        column_width.append(max(df_pivot.index.str.len()) * 8)
        for col in df_pivot.columns:
            column_width.append(max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8)

        # Create Plotly table
        fig = go.Figure(data=[go.Table(
            columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
            columnwidth=column_width,
            header=dict(values=header_values,
                        fill_color=['#ffffff', '#248ce6', '#248ce6'],
                        font=dict(color='white'),
                        align='center'),
            cells=dict(values=cell_values,
                       fill_color=colors_by_row,
                       line_color=colors_by_row,
                       font=dict(color=font_colors),

                       align='left'))
        ])
    else:
        fig = go.Figure()
        # print("No data available, since the results are all zero.")
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


    return fig


def render_tech_params(data, _p_scenario):
    data = data[data['scenario'].isin(_p_scenario)]
    if not data.empty:
        # create a table
        data = data[['scenario', 'variable', 'value']]

        df_pivot = data.pivot(index='variable', columns='scenario', values='value')


        df_pivot = df_pivot.fillna('')
        # Create a Plotly Table
        header_values = [''] + list(df_pivot.columns)
        cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

        min_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
        max_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

        def normalize(value):
            if isinstance(value, (int, float)):
                return (value - min_value) / (max_value - min_value)
            return None

        colors = []

        for col in df_pivot.columns:
            normalized_data = [normalize(val) for val in df_pivot[col]]
            colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[
                                     0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in
                                 normalized_data])]

        colors_by_row = [['#ffffff', '#e5eeec'] * (
                    len(df_pivot.index) // 2)] + colors  # Determine font colors based on the background color
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
            columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
            columnwidth=column_width,
            header=dict(values=header_values,
                        fill_color=['#ffffff', '#248ce6', '#248ce6'],
                        font=dict(color='white'),
                        align='center'),
            cells=dict(values=cell_values,
                       fill_color=colors_by_row,
                       line_color=colors_by_row,
                       font=dict(color=font_colors),

                       align='left'))
        ])
    else:
        fig = go.Figure()
        # print("No data available, since the results are all zero.")
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


    return fig


def render_plot(p_type, df, vre_variable=None, season=None, t_p_type=None, t_year=None, t_scenarios=None,
                e_p_type=None, e_year=None, e_region=None, e_scenarios=None,
                _demand_scenario=None, _demand_time_step=None, _demand_year=None, _demand_month=None, _demand_date=None,
                _c_type=None, _c_scenario=None, _c_region=None,
                _t_cost_scenarios=None, _p_scenario=None, _p_variable=None,
                _policy_scenarios=None):
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
    elif p_type == 'Extant Transmission':
        return render_extant_transmission(t_p_type, data, t_scenarios, t_year)
    elif p_type == 'Extant Capacity':
        return plot_capacity(e_p_type, data, False, e_scenarios, e_region, e_year, e_scenarios[0])
    elif p_type == 'Demand':
        return render_demand(data, _demand_scenario, _demand_year, _demand_month, _demand_date, 'Demand', 'Time', 'Demand (MW)', time_size=_demand_time_step)
    elif p_type == 'Cost':
        return render_cost(data, _c_type, _c_scenario, _c_region)
    elif p_type == 'Transmission Costs':
        return render_t_cost(data, _t_cost_scenarios)
    elif p_type == 'Technology Parameter':
        data = data[data['variable'].str.startswith(_p_variable)]
        return render_tech_params(data, _p_scenario)
    elif p_type == 'Policy':
        return render_t_cost(data, _policy_scenarios)
    else:
        return go.Figure()

def plot_capacity(type, df, aggregate, scenarios, region, year, scenario, pattern_active=True, text_active=False):
    from profiles.copper_output.utils import plot_settings
    #print('rendering plot', type)
    name = plot_settings['Capacity']['name']
    unit = plot_settings['Capacity']['unit']
    if type == 'By Year':
        plot_info = plot_settings['Capacity']['By Year']
        return bar_over_years.plot(df, scenarios, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active)
    elif type == 'Trend Over Years':
        plot_info = plot_settings['Capacity']['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)
    elif type == 'Pie Chart':
        plot_info = plot_settings['Capacity']['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'])
    else:
        plot_info = plot_settings['Capacity']['By Region']
        return bar_over_regions.plot(df, scenarios, aggregate, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active)



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
        mapbox_zoom=2.5, mapbox_center={"lat": 54.0902, "lon": -95.7129},
        geo=dict(
            showframe=False,
            bgcolor='rgba(0,0,0,0)'),

    )


    fig.update_layout(title=title, xaxis_title=x_label, yaxis_title=y_label)

    fig.update_geos(projection_type="orthographic")
    fig.layout.template = None
    return fig

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
    Line_Flow = Line_Flow[Line_Flow['time'] == Year]

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


    with open('profiles/copper_output/visualization_scripts/utils/canada.geojson') as f:
        canada = geojson.load(f)
    with open('profiles/copper_output/visualization_scripts/utils/arrows.geojson') as f:
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

def render_extant_transmission(p_type, df, scenarios, year):
    from profiles.copper_output.utils import plot_settings
    name = plot_settings['Transmission Capacity']['name']
    unit = plot_settings['Transmission Capacity']['unit']
    if p_type == 'Map Plot':
        plot_info = plot_settings['Transmission Capacity']['Map Plot']
        return transmission_plot(df, scenarios, year, plot_info['title'])
    if p_type == 'Bar Plot':
        plot_info = plot_settings['Transmission Capacity']['Bar Plot']
        df = df.copy()
        df['region'] = df['short_region'] + '<br>-><br>' + df['short_variable']
        df['variable'] = 'Capacity'
        return bar_over_regions.plot(df, scenarios, False, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)

def render_demand(df, scenario, year, month, date, title, x_axis_label, y_axis_label, time_size='hourly'):
    # turn date range into a readable format

    fig = go.Figure()
    # add title
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )
    df_scen = df.copy(deep=True)
    df_scen = df_scen[df_scen['scenario'] == scenario]

    df_scen['time'] = pd.to_datetime(df_scen['time'])
    # groupby time based on time_size
    if time_size == 'daily':
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen = df_scen[df_scen['time'].dt.strftime('%B') == month]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d')
    elif time_size == 'monthly':
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m')
    elif time_size == 'yearly':
        df_scen['time'] = df_scen['time'].dt.strftime('%Y')
    else:
        df_scen = df_scen[df_scen['time'].dt.year == year]
        df_scen = df_scen[df_scen['time'].dt.strftime('%B') == month]
        df_scen = df_scen[df_scen['time'].dt.strftime('%d') == date]
        df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

    cols = df_scen.columns.tolist()
    # remove value column
    cols.remove('value')
    df_scen = df_scen.groupby(['time', 'region']).sum(numeric_only=True).reset_index()

    regions = df_scen.region.unique().tolist()


    # Create a stacked area chart (original behavior)
    for region in regions:
        df_tech = df_scen[df_scen['region'] == region]
        df_tech = df_tech.sort_values(by=['time'])
        fig.add_trace(go.Scatter(
            x=df_tech['time'],
            y=df_tech['value'],
            name=region,
            mode='lines',
            line=dict(color=utils.get_color(region)),
            stackgroup='one',
            hovertemplate=f'<b>{region}</b><br><br>' +
                          f'Scenario: {scenario} <br>' +
                          'Time: %{x}<br>' +
                          f'Demand: %{{y:.2f}} {y_axis_label}<br>' +
                          '<extra></extra>'
        ))
    fig.update_yaxes(showgrid=True)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1d", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.layout.autosize = True
    return fig

def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting inputs')
    classes = df['variable'].apply(lambda x: x.split('|')[0]).unique()

    policy_scenarios = []
    if 'Policy' in classes:
        policy_scenarios = df[df['variable'].str.startswith('Policy')]['scenario'].unique()

    policy_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in policy_scenarios],
            value=[policy_scenarios[0]] if len(policy_scenarios) else [],
            id={
                'type': 'copper-inputs-policy-scenario-select',
                'index': window_id
            },
        ),
        ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-policy-widget',
            'index': window_id
        }
    )


    transmission_cost_scenario = []
    if 'Transmission Costs' in classes:
        transmission_cost_scenario = df[df['variable'].str.startswith('Transmission Costs')]['scenario'].unique()

    transmission_cost_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in transmission_cost_scenario],
            value=[transmission_cost_scenario[0]] if len(transmission_cost_scenario) else [],
            id={
                'type': 'copper-inputs-transmission-cost-scenario-select',
                'index': window_id
            },
        ),
        ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-transmission-cost-widget',
            'index': window_id
        }
    )

    params_scenario = []
    params_variables = []
    if 'Technology Parameter' in classes:
        params_scenario = df[df['variable'].str.startswith('Technology Parameter')]['scenario'].unique()
        params_variables = df[df['variable'].str.startswith('Technology Parameter')]['variable'].apply(lambda x: x.split('|')[1]).unique()

    params_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in params_scenario],
            value=[params_scenario[0]] if len(params_scenario) else [],
            id={
                'type': 'copper-inputs-params-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in params_variables],
            value=params_variables[0] if len(params_variables) else '',
            id={
                'type': 'copper-inputs-params-variable-select',
                'index': window_id
            },
        ),
        ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-params-widget',
            'index': window_id
        }
    )


    demand_scenarios = []
    demand_years = []
    demand_months = []
    demand_dates = []
    if 'Demand' in classes:
        demand = df[df['variable'].str.startswith('Demand')].copy()
        demand['time'] = pd.to_datetime(demand['time'])
        demand_scenarios = demand['scenario'].unique()
        demand_years = demand['time'].dt.year.unique()
        demand_months = demand['time'].dt.strftime('%B').unique()
        demand_dates = demand['time'].dt.strftime('%d').unique()

    demand_widget_layout = html.Div([
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in demand_scenarios],
            value=demand_scenarios[0] if demand_scenarios else '',
            id={
                'type': 'copper-inputs-demand-scenario-select',
                'index': window_id,
            },
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='yearly',
            id={
                'type': 'copper-inputs-demand-time_step-select',
                'index': window_id,
            },
        ),
        dmc.Select(
          label='Year',
            data=[{'label': year, 'value': year} for year in demand_years],
            value=demand_years[0] if len(demand_years) else '',
            id={
                'type': 'copper-inputs-demand-year-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Month',
            data=[{'label': month, 'value': month} for month in demand_months],
            value=demand_months[0] if len(demand_months) else '',
            id={
                'type': 'copper-inputs-demand-month-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Date',
            data=[{'label': date, 'value': date} for date in demand_dates],
            value=demand_dates[0] if len(demand_dates) else '',
            id={
                'type': 'copper-inputs-demand-date-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        ],
        id={
            'type': 'copper-inputs-demand-widget',
            'index': window_id
        },
        style={'display': 'block'},)

    print(classes)
    seasons = []
    vre_variables = []
    if 'Vre Capacity Factors' in classes:
        seasons = ['Winter', 'Summer']
        vre_variables = ['Wind', 'Solar']

    costs = []
    c_regions = []
    c_scenarios = []
    if 'Cost' in classes:
        costs = df[df['variable'].str.startswith('Cost')]['variable'].apply(lambda x: x.split('|')[1]).unique()
        c_regions = df[df['variable'].str.startswith('Cost')]['region'].unique()
        c_scenarios = df[df['variable'].str.startswith('Cost')]['scenario'].unique()

    cost_widget_layout = html.Div([
        dmc.Select(
            label='Cost Type',
            data=[{'label': cost, 'value': cost} for cost in costs],
            value=costs[0] if len(costs) else '',
            id={
                'type': 'copper-inputs-cost-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in c_scenarios],
            value=c_scenarios[0] if len(c_scenarios) else '',
            id={
                'type': 'copper-inputs-cost-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in c_regions],
            value=c_regions[0] if len(c_regions) else '',
            id={
                'type': 'copper-inputs-cost-region-select',
                'index': window_id
            },
        ),
        ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-cost-widget',
            'index': window_id
        }
    )

    e_years = []
    e_regions = []
    e_scenarios = []
    e_p_type = []
    if 'Extant Capacity' in classes:
        e_p_type = ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']
        e_years = df[df['variable'].str.startswith('Extant Capacity')]['time'].unique()
        e_scenarios = df[df['variable'].str.startswith('Extant Capacity')]['scenario'].unique()
        e_regions = df[df['variable'].str.startswith('Extant Capacity')]['region'].unique()

    t_p_type = []
    t_years = []
    t_scenarios = []
    if 'Extant Transmission' in classes:
        t_p_type = ['Map Plot', 'Bar Plot']
        t_years = df[df['variable'].str.startswith('Extant Transmission')]['time'].unique()
        t_scenarios = df[df['variable'].str.startswith('Extant Transmission')]['scenario'].unique()

    vre_widget_layout = html.Div([
        dmc.Select(
            label='Season',
            data=[{'label': season, 'value': season} for season in seasons],
            value=seasons[0] if seasons else '',
            id={
                'type': 'copper-inputs-season-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='VRE Variable',
            data=[{'label': vre_variable, 'value': vre_variable} for vre_variable in vre_variables],
            value=vre_variables[0] if vre_variables else '',
            id={
                'type': 'copper-inputs-vre-variable-select',
                'index': window_id
            },
        )
    ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-vre-widget',
            'index': window_id
        }
    )

    transmission_widget_layout = html.Div([
        dmc.Select(
            label='Representation Options',
            data=[{'label': plot, 'value': plot} for plot in t_p_type],
            value=t_p_type[0],
            id={
                'type': 'copper-inputs-transmission-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in t_years],
            value=t_years[0],
            id={
                'type': 'copper-inputs-year-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in t_scenarios],
            value=t_scenarios[0] if t_scenarios else '',
            id={
                'type': 'copper-inputs-scenario-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.MultiSelect(
            label='Select Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in t_scenarios],
            value=t_scenarios if t_scenarios else [],
            id={
                'type': 'copper-inputs-scenario-multi-select',
                'index': window_id
            },
            style={'display': 'none'}
        )

        ],
        style={'display': 'none'},
        id={
            'type': 'copper-inputs-transmission-widget',
            'index': window_id
        })


    extant_capacity_widget_layout = html.Div([
        dmc.Select(
            label='Representation Options',
            data=[{'label': plot, 'value': plot} for plot in e_p_type],
            value=e_p_type[0],
            id={
                'type': 'copper-inputs-extant-capacity-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in e_years],
            value=e_years[0],
            id={
                'type': 'copper-inputs-extant-capacity-year-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in e_regions],
            value=e_regions[0],
            id={
                'type': 'copper-inputs-extant-capacity-region-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in e_scenarios],
            value=e_scenarios[0],
            id={
                'type': 'copper-inputs-extant-capacity-scenario-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Select Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in e_scenarios],
            value=e_scenarios,
            id={
                'type': 'copper-inputs-extant-capacity-scenario-multi-select',
                'index': window_id
            },
            style={'display': 'none'}
        )
        ],
        id={
            'type': 'copper-inputs-extant-capacity-widget',
            'index': window_id
        },
        style={'display': 'none'}
    )


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
        vre_widget_layout,
        transmission_widget_layout,
        extant_capacity_widget_layout,
        demand_widget_layout,
        cost_widget_layout,
        transmission_cost_widget_layout,
        params_widget_layout,
        policy_widget_layout,
        dmc.Button('Download Data', id={'type': 'copper-inputs-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'copper-inputs-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df,
                            vre_variable=vre_variables[0] if len(vre_variables) else None,
                            season=seasons[0] if len(seasons) else None,
                            t_p_type=t_p_type[0] if len(t_p_type) else None,
                            t_year=t_years[0] if len(t_years) else None,
                            t_scenarios=t_scenarios if len(t_scenarios) else None,
                            e_p_type=e_p_type[0] if len(e_p_type) else None,
                            e_year=e_years[0] if len(e_years) else None,
                            e_region=e_regions[0] if len(e_regions) else None,
                            e_scenarios=e_scenarios if len(e_scenarios) else None,
                            _demand_scenario=demand_scenarios[0] if len(demand_scenarios) else None,
                            _demand_time_step='yearly',
                            _c_type=costs[0] if len(costs) else None,
                           ),
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
