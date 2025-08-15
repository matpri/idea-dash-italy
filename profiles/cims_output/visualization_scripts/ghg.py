import math

import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.cims_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart


def render_plot(representation, type, df, scenarios, region, year, scenario, pattern_active=True, text_active=False,
                sector=None, service=None, emissions_list=None, plot_name='Net Emissions'):
    print('rendering plot', type)
    from profiles.cims_output.utils import plot_settings
    # print('rendering plot', type)
    name = plot_settings[plot_name]['name']
    unit = plot_settings[plot_name]['unit']
    df = process_represenation(df, representation, sector, service, emissions_list)
    if type == 'By Year':
        plot_info = plot_settings[plot_name]['By Year']
        return bar_over_years.plot(df, scenarios, region, plot_info['title'], plot_info['x_label'],
                                   plot_info['y_label'],
                                   name, unit, pattern_active=pattern_active,
                                   text_active=text_active)
    elif type == 'Trend Over Years':
        plot_info = plot_settings[plot_name]['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'],
                                     name, unit)
    elif type == 'Pie Chart':
        plot_info = plot_settings[plot_name]['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, plot_info['title'], plot_info['x_label'],
                              plot_info['y_label'],
                              )
    else:
        plot_info = plot_settings[plot_name]['By Region']
        return bar_over_regions.plot(df, scenarios, year, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'],
                                     name, unit, pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(df, representation, sector, service, emissions_list):
    if representation == 'By Service':
        filtered_df = df[
            (df.parameter.isin(emissions_list)) &
            (df['sector'] == sector) &
            (df.short_path == service)
            ]

        filtered_df['variable'] = filtered_df['sub_context'] + '|' + filtered_df['context']
        filtered_df['variable'] += '- Negative' if 'negative' in filtered_df[
            'variable'] else '- Avoided' if 'avoided' in \
                                            filtered_df[
                                                'variable'] else '- Emitted'
        filtered_df = filtered_df[['region', 'variable', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'year': 'time'})

    elif representation == 'By Sector':
        filtered_df = df[
            (df.parameter.isin(emissions_list))
            ]

        filtered_df['variable'] = filtered_df['sector']
        # only keep where shortpath == sector
        filtered_df = filtered_df[filtered_df['short_path'] == filtered_df['sector']]
        filtered_df = filtered_df[['region', 'variable', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'year': 'time'})

    else:
        if sector == 'All':
            filtered_df = df[(df.parameter.isin(emissions_list))]
            filtered_df = filtered_df[filtered_df['short_path'] == filtered_df['sector']]
        else:
            filtered_df = df[(df.parameter.isin(emissions_list)) & (df['sector'] == sector) & (df['short_path'] == sector)]
        filtered_df['variable'] = filtered_df['sub_context'] + '|' + filtered_df['context']
        filtered_df['variable'] += '- Negative' if 'negative' in filtered_df[
            'variable'] else '- Avoided' if 'avoided' in \
                                            filtered_df[
                                                'variable'] else '- Emitted'
        filtered_df = filtered_df[['region', 'variable', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    return filtered_df


def widgets(df, window_id):
    """
    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    """
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['year'].unique().tolist()
    sectors = df['sector'].unique().tolist()
    sectors = [sector for sector in sectors if
               sector is not None and sector != '' and sector != math.nan and isinstance(sector, str)]
    services = df[(df['sector'] == sectors[0])]['short_path'].unique().tolist()
    emissions_list = df[df['parameter'].str.contains('emissions')]['parameter'].unique().tolist()

    plot_types = ['Net Emissions', 'Avoided Emissions', 'Negative Emissions', 'Emitted Emissions', 'Emissions Costs']

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'cims-ghg-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'cims-ghg-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    by_service_widgets = html.Div([
        dmc.Select(
            label='Sector',
            data=[{'label': sector, 'value': sector} for sector in sectors],
            value=sectors[0],
            id={
                'type': 'cims-ghg-service-sector-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Service',
            data=[{'label': service, 'value': service} for service in services],
            value=services[0] if len(services) > 0 else None,
            id={
                'type': 'cims-ghg-service-select',
                'index': window_id
            }
        ),
    ],
        style={'display': 'none'},
        id={
            'type': 'cims-ghg-service-widgets',
            'index': window_id
        })

    sectors = ['All'] + sectors
    by_sector_widgets = dmc.Select(
        label='Sector',
        data=[{'label': sector, 'value': sector} for sector in sectors],
        value=sectors[0],
        id={
            'type': 'cims-ghg-sector-select',
            'index': window_id
        },
        style={'display': 'block'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'cims-ghg-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'cims-ghg-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    widget_layout = [
        dmc.Select(
            label='Result Representation',
            data=[{'label': plot, 'value': plot} for plot in ['By Emission']],
            value='By Emission',
            id={
                'type': 'cims-ghg-representation-select',
                'index': window_id
            },
        ),
        by_sector_widgets,
        by_service_widgets,
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'cims-ghg-plot-select',
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
                'type': 'cims-ghg-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'cims-ghg-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Emissions',
            data=[{'label': emission, 'value': emission} for emission in plot_types],
            value=plot_types[0],
            id={
                'type': 'cims-ghg-emission-select',
                'index': window_id
            },
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'cims-ghg-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'cims-ghg-download', 'index': window_id}),
    ]

    return widget_layout, render_plot('By Emission', 'By Year', df, [scenarios[0]],
                                      'CAN' if 'CAN' in regions else regions[0],
                                      years[0], scenarios[0], sector=sectors[0], service=services[0],
                                      emissions_list=[e_type for e_type in emissions_list if not 'cost' in e_type],
                                      plot_name='Net Emissions')
