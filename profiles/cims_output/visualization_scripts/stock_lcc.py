import math

import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.cims_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart


def render_plot(type, df, scenarios, region, year, scenario, pattern_active=True, text_active=False,
                sector=None, service=None, parameter='new_stock', plot_name='New Stock'):
    print('rendering plot', type)
    from profiles.cims_output.utils import plot_settings
    # print('rendering plot', type)
    name = plot_settings[plot_name]['name']
    unit = plot_settings[plot_name]['unit']
    print('rendering plot', type)
    df = process_represenation(df, sector, service, parameter)
    print('processed', df)
    if type == 'By Year':
        plot_info = plot_settings[plot_name]['By Year']
        return bar_over_years.plot(df, scenarios, region, plot_info['title'], plot_info['x_label'], plot_info['y_label'],
                                   name, unit, pattern_active=pattern_active,
                                   text_active=text_active)
    elif type == 'Trend Over Years':
        plot_info = plot_settings[plot_name]['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, plot_info['title'], plot_info['x_label'], plot_info['y_label'],
                                     name, unit)
    elif type == 'Pie Chart':
        plot_info = plot_settings[plot_name]['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'],
                              )
    else:
        plot_info = plot_settings[plot_name]['By Region']
        return bar_over_regions.plot(df, scenarios, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'],
                                     name, unit, pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(df, sector, service, parameter):
    df = df[df['parameter'] == parameter]
    filtered_df = df[
        (df['parameter'] == parameter) &
        (df['sector'] == sector) &
        (df.short_path.str.startswith(service))
        ]

    filtered_df = filtered_df[['region', 'technology', 'year', 'value_num', 'scenario']]
    filtered_df = filtered_df.rename(columns={'value_num': 'value', 'technology': 'variable', 'year': 'time'})

    return filtered_df


def plot(df, window_id):
    """
    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    """
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['year'].unique().tolist()
    years = [int(year) for year in years if not math.isnan(year)]
    sectors = df['sector'].unique().tolist()
    sectors = [sector for sector in sectors if
               sector is not None and sector != '' and sector != math.nan and isinstance(sector, str)]
    services = df[df['sector'] == sectors[0]]['short_path'].unique().tolist()
    stock_parameters = df['parameter'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'cims-stock_lcc-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'cims-stock_lcc-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    by_service_widgets = dmc.Select(
        label='Service',
        data=[{'label': service, 'value': service} for service in services],
        value=services[0] if len(services) > 0 else None,
        id={
            'type': 'cims-stock_lcc-service-select',
            'index': window_id
        },
        style={'display': 'block'}
    )

    by_sector_widgets = dmc.Select(
        label='Sector',
        data=[{'label': sector, 'value': sector} for sector in sectors],
        value=sectors[0],
        id={
            'type': 'cims-stock_lcc-sector-select',
            'index': window_id
        },
        style={'display': 'block'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'cims-stock_lcc-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'cims-stock_lcc-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'cims-stock_lcc-plot-select',
                'index': window_id
            },
        ),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'cims-stock_lcc-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'cims-stock_lcc-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_sector_widgets,
        by_service_widgets,
        dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in stock_parameters],
            value=stock_parameters[0],
            id={
                'type': 'cims-stock_lcc-variable-select',
                'index': window_id
            },
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'cims-stock_lcc-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'cims-stock_lcc-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           years[0], scenarios[0], sector=sectors[0], service=services[0],
                           parameter=stock_parameters[0], plot_name=stock_parameters[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'cims_output',
            'viz': 'stock_lcc'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
