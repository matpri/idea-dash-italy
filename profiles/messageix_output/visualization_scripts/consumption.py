import dash_mantine_components as dmc
from dash import html, dcc

from profiles.messageix_output import utils
from components import ids
from profiles.messageix_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart, map_plot


# sources = ['Electricity', 'Gases', 'Geothermal', 'Heat', 'Liquids', 'Solids', 'Hydrogen']
# sectors = ['Electricity', 'Gases', 'Geothermal', 'Heat', 'Liquids', 'Solids', 'Hydrogen']


def render_plot(type, df, aggregate, scenarios, region, year, scenario, pattern_active=True, text_active=False,
                variables=[]):
    from profiles.messageix_output.utils import plot_settings
    print('rendering plot', type)
    name = plot_settings['Consumption']['name']
    unit = plot_settings['Consumption']['unit']

    if type == 'By Year':
        plot_info = plot_settings['Consumption']['By Year']
        return bar_over_years.plot(df, scenarios, region, aggregate, plot_info['title'], plot_info['x_label'],
                                   plot_info['y_label'], name, unit, pattern_active=pattern_active,
                                   text_active=text_active, variables=variables)
    elif type == 'Trend Over Years':
        plot_info = plot_settings['Consumption']['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, aggregate, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'], name, unit, variables=variables)
    elif type == 'Pie Chart':
        plot_info = plot_settings['Consumption']['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, aggregate, plot_info['title'], plot_info['x_label'],
                              plot_info['y_label'], variables=variables)
    elif type == 'Map Plot':
        title = plot_settings['Consumption']['Map']['title']
        return map_plot.plot_map(df, scenario, year, title, name, unit, variables)
    else:
        plot_info = plot_settings['Consumption']['By Region']
        return bar_over_regions.plot(df, scenarios, aggregate, year, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'], name, unit, pattern_active=pattern_active,
                                     text_active=text_active, variables=variables)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['time'].unique().tolist()

    df_scen = df.copy(deep=True)
    df_scen['variable'] = df_scen["variable"].map(utils.groups).fillna(df_scen["variable"])
    df_scen = df_scen[
        (df_scen['region'] == 'Canada' if 'Canada' in regions else regions[0]) & (df_scen['time'] == years[0]) & (
                df_scen['scenario'] == scenarios[0])]
    # df_scen = df_scen[df_scen['type'].isin(sectors)]
    types = ['All'] + sorted(df_scen['type'].unique().tolist())

    max_depth = df_scen.levels.max()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='Canada' if 'Canada' in regions else regions[0],
        id={
            'type': 'messageix-consumption-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'messageix-consumption-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    map_plot_widgets = [
        dmc.Select(
            label='Production Type',
            data=[{'label': variable, 'value': variable} for variable in types],
            value='All',
            id={
                'type': 'messageix-consumption-type-select',
                'index': window_id
            },
        ),
           ]
    parents = df_scen.type.unique().tolist()
    parents = ['Consumption|' + parent for parent in parents]
    for i in range(max_depth):
        if i == 0:
            variables = parents
        else:
            variables = df_scen[df_scen.parent.isin(parents)].variable.unique().tolist()
        map_plot_widgets.append(
            dmc.MultiSelect(
                label=f'Level {i + 1}',
                data=[{'label': variable, 'value': variable} for variable in variables],
                value=[],
                id={
                    'type': 'messageix-consumption-level-select',
                    'index': window_id,
                    'level': i
                },
                style={'display': 'block'} if i == 0 else {'display': 'none'}
            )
        )
        parents = []

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'messageix-consumption-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'messageix-consumption-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in
                  ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart', 'Map Plot']],
            value='By Year',
            id={
                'type': 'messageix-consumption-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch('Show Sector',
                   checked=True,
                   id={
                       'type': 'messageix-consumption-show_sector-switch',
                       'index': window_id},

                   style={'display': 'none'}),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'messageix-consumption-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'messageix-consumption-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        *map_plot_widgets,
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'messageix-consumption-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'messageix-consumption-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, True, [scenarios[0]], 'Canada' if 'Canada' in regions else regions[0],
                           years[0], scenarios[0], variables=[]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'messageix_output',
            'viz': 'Consumption'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
