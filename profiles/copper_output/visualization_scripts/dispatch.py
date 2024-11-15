import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
from profiles.copper_output import utils
from profiles.copper_output.utils import custom_sort_key

date_mapper = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
               9: 'September',
               10: 'October', 11: 'November', 12: 'December', 'January': '01', 'February': '02', 'March': '03',
               'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09',
               'October': '10', 'November': '11', 'December': '12'}


def render_plot(type, df, aggregate, scenarios, region, year, day):
    from profiles.copper_output.utils import plot_settings
    if region == 'CAN':
        df = df[~(df['variable'].str.startswith('Export') | df['variable'].str.startswith('Import'))]
    if type == 'Dispatched Electricity':
        plot_info = plot_settings['Dispatch']['Dispatched Electricity']
        return plot_dispatch(df, scenarios, region, year, day, aggregate, plot_info['title'], plot_info['x_label'],
                             plot_info['y_label'])
    else:
        plot_info = plot_settings['Dispatch']['Exported Electricity']
        return plot_exports(df, scenarios, region, year, day, aggregate, plot_info['title'],
                            plot_info['x_label'], plot_info['y_label'])


def region_subset(df, scenario, region, year, day, aggregate):
    """
    Extract a subset of the DataFrame for a specific scenario, region, year, and day.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        scenario (str): Selected scenario.
        region (str): Selected region.
        year (int): Selected year.
        day (str): Selected day.

    Returns:
        pd.DataFrame: Subset of the DataFrame for the specified conditions.
    """
    df_scen = df.copy(deep=True)
    df_scen = df_scen[df_scen['scenario'] == scenario]
    day = f'{day.split("-")[1]}-{date_mapper[day.split("-")[0]]}'  # convert day to format in df

    # Filter by date range
    df_scen = df_scen[df_scen['period'] == year]
    # Filter by specific day
    df_scen = df_scen[df_scen['time'].dt.strftime('%d-%m') == day]

    if aggregate:
        df_scen['variable'] = df_scen["variable"].map(utils.get_group).fillna(df_scen["variable"])
        df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()
    else:
        df_scen['variable'] = df_scen["variable"].map(utils.get_name).fillna(df_scen["variable"])

    df_scen = df_scen.groupby(["variable", "region", "time", 'period', 'scenario']).sum(numeric_only=True).reset_index()
    times = df_scen['time'].unique().tolist()

    df_scen = df_scen.sort_values(by=['period', 'variable'], key=lambda x: x.map(custom_sort_key))

    df_scen = df_scen[df_scen['region'] == region]
    df_scen = df_scen[df_scen['value'] != 0]

    time_pad = []
    for var in df_scen['variable'].unique():
        for time in times:
            if not df_scen[(df_scen['variable'] == var) & (df_scen['time'] == time)].empty:
                continue
            else:
                time_pad.append(
                    {'time': time, 'variable': var, 'value': 0, 'region': region, 'scenario': scenario, 'period': year})
    time_pad = pd.DataFrame(time_pad)
    df_scen = pd.concat([df_scen, time_pad])

    # add a cumulative sum column where the sum is over the technologies before it in the df and is reset for each time point

    df_scen['total'] = df_scen.groupby(['time'])['value'].transform('sum').values
    # add the technology total into the variable column for every unique time point
    # subtract values for Exports from the total
    return df_scen


def plot_dispatch(df, scenario, region, year, day, aggregate, title='Dispatched Electricity', x_axis_label='Time',
                  y_axis_label='Dispatched Electricity (TWh)'):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )

    # try:
    df = df[~df['variable'].str.startswith('Export')]
    df = df[~df['variable'].str.startswith('Storage In|')]
    df['variable'] = df['variable'].str.replace('Storage Out|', '')
    can_emissions = region_subset(df, scenario, region, year, day, aggregate)
    techs = can_emissions.variable.unique().tolist()
    if aggregate:
        colors = {tech: utils.get_group_colors(tech) for tech in techs}
    else:
        colors = {tech: utils.get_color(tech) for tech in techs}

    # Create stacked bar chart
    for i, tech in enumerate(techs):
        df_tech = can_emissions[can_emissions['variable'] == tech]
        df_tech = df_tech.sort_values(by=['time'])
        fig.add_trace(go.Scatter(
            x=df_tech['time'],
            y=df_tech['value'],
            name=tech,
            mode='lines',
            line=dict(color=colors[tech]),
            stackgroup='one',
            customdata=df_tech['total'],
            hovertemplate=f'<b>{tech}</b><br><br> Region: {region}<br>' + 'Time: %{x}<br>Dispatch: %{y:.2f} TWh<br>Total: %{customdata:.2f} TWh<br><extra></extra>'
        ))
    fig.update_yaxes(showgrid=True)
    if can_emissions.empty:
        #print("No data available, since the results are all zero.")
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
    # except Exception as e:
    #     #print("Dispatch viz", e)
    #     pass

    fig.layout.autosize = True
    fig.add_hline(y=0, line_dash="dot", line_color="grey")
    fig.update_layout(legend=dict(
        font=dict(
            size=14,
        )
    ))
    # remove reset-axis button from toolbar
    fig.update_layout(modebar_remove=['autoScale', 'lasso2d'])
    return fig


def plot_exports(df, scenario, region, year, day, aggregate, title='Exported Electricity', x_axis_label='Time',
                 y_axis_label='Exported Electricity (TWh)'):
    """
    Create a Plotly plot for dispatch in Canada.

    Parameters:
        df (pd.DataFrame): DataFrame containing the data.
        scenario (str): Selected scenario.
        region (str): Selected region.
        year (int): Selected year.
        colors (dict): Dictionary mapping technologies to colors.
        title (str): Plot title.
        x_axis_label (str): X-axis label.
        y_axis_label (str): Y-axis label.
        day (str): Selected day.

    Returns:
        pn.pane.Plotly: Plotly plot as a Panel component.
    """
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )

    # try:
    exports = df[df['variable'].str.startswith('Export')]
    outs = df[df['variable'].str.startswith('Storage In|')]
    outs['variable'] = outs['variable'].str.replace('Storage In|', '')
    df = pd.concat([exports, outs])
    can_emissions = region_subset(df, scenario, region, year, day, aggregate)
    techs = can_emissions.variable.unique().tolist()
    if aggregate:
        colors = {tech: utils.get_group_colors(tech) for tech in techs}
    else:
        colors = {tech: utils.get_color(tech) for tech in techs}

    # Create stacked bar chart
    for i, tech in enumerate(techs):
        df_tech = can_emissions[can_emissions['variable'] == tech]
        df_tech = df_tech.sort_values(by=['time'])
        fig.add_trace(go.Scatter(
            x=df_tech['time'],
            y=df_tech['value'],
            name=tech,
            mode='lines',
            line=dict(color=colors[tech]),
            stackgroup='one',
            customdata=df_tech['total'],
            hovertemplate=f'<b>{tech}</b><br><br> Region: {region}<br>' + 'Time: %{x}<br>Export: %{y:.2f} TWh<br>Total: %{customdata:.2f} TWh<br><extra></extra>'
        ))
    fig.update_yaxes(showgrid=True)
    if can_emissions.empty:
        #print("No data available, since the results are all zero.")
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
    # except Exception as e:
    #     #print("Dispatch viz", e)
    #     pass

    fig.layout.autosize = True
    fig.add_hline(y=0, line_dash="dot", line_color="grey")
    fig.update_layout(legend=dict(
        font=dict(
            size=14,
        )
    ))
    # remove reset-axis button from toolbar
    fig.update_layout(modebar_remove=['autoScale', 'lasso2d'])
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['period'].unique().tolist()

    df_scen = df.copy(deep=True)
    df_scen = df_scen[df_scen['scenario'] == scenarios[0]]
    df_scen = df_scen[df_scen['period'] == years[0]]
    days = df_scen['time'].dt.strftime('%d-%m').unique().tolist()
    # sort days by month and day
    days = sorted(days, key=lambda x: (int(x.split('-')[1]), int(x.split('-')[0])))
    days = [date_mapper[int(x.split('-')[1])] + '-' + x.split('-')[0] for x in days]

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Dispatched Electricity', 'Exported Electricity']],
            value='Dispatched Electricity',
            id={
                'type': 'copper-dispatch-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'copper-dispatch-aggregate-switch',
                       'index': window_id}),
        dmc.Select(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'copper-dispatch-scenario-multi-select',
                'index': window_id,
            }
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value= 'CAN' if 'CAN' in regions else regions[0],
            id={
                'type': 'copper-dispatch-region-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'copper-dispatch-year-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Day',
            data=[{'label': day, 'value': day} for day in days],
            value=days[0],
            id={
                'type': 'copper-dispatch-day-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'copper-dispatch-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'copper-dispatch-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Dispatched Electricity', df, True, scenarios[0], 'CAN' if 'CAN' in regions else regions[0], years[0], days[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'copper_output',
            'viz': 'dispatch'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
