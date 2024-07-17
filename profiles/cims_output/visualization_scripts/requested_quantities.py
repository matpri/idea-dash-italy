import dash_mantine_components as dmc
from dash import html, dcc

from profiles.cims_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart


def render_plot(representation, type, df, scenarios, region, year, scenario, pattern_active=True, text_active=False,
                sector=None, service=None, fuel=None):
    print('rendering plot', type)
    df = process_represenation(df, representation, sector, service, fuel)
    if type == 'By Year':
        return bar_over_years.plot(df, scenarios, region, representation, 'x',
                                   'y', 'name', 'unit', pattern_active=pattern_active,
                                   text_active=text_active)
    elif type == 'Trend Over Years':
        return trend_over_years.plot(df, scenario, region, representation, 'x',
                                     'y', 'name', 'unit')
    elif type == 'Pie Chart':
        return pie_chart.plot(df, scenario, region, year, representation, 'x',
                              'y')
    else:
        return bar_over_regions.plot(df, scenarios, year, representation, 'x',
                                     'y', 'name', 'unit', pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(df, representation, sector, service, fuel):
    if representation == 'By Fuel':
        filtered_df = df[
            (df['technology'].isna()) &
            (df['sector'] == sector)
            ]
        filtered_df = filtered_df[filtered_df.short_path == service]
        filtered_df = filtered_df[['region', 'context', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'context': 'variable', 'year': 'time'})

    elif representation == 'By Service':
        filtered_df = df[(df['technology'].isna()) & (df['context'] == fuel)].groupby(
            ['region', 'sector', 'year', 'short_path', 'scenario']).sum(numeric_only=True).reset_index()
        filtered_df = filtered_df[['region', 'short_path', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    else:
        filtered_df = df[(df['technology'].isna()) & (df['context'] == fuel)].groupby(
            ['region', 'sector', 'year', 'scenario']).sum(numeric_only=True).reset_index()

        filtered_df = filtered_df[['region', 'sector', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'sector': 'variable', 'year': 'time'})

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
    sectors = df['sector'].unique().tolist()
    sectors = [sector for sector in sectors if sector is not None or sector != '' or sector != 'nan']
    services = df[(df['technology'].isna()) & (df['sector'] == sectors[0])]['short_path'].unique().tolist()
    fuels = df[(df['technology'].isna())]['context'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'cims-requested_quantities-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'cims-requested_quantities-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    by_fuel_widgets = dmc.Select(
        label='Fuel',
        data=[{'label': fuel, 'value': fuel} for fuel in fuels],
        value=fuels[0],
        id={
            'type': 'cims-requested_quantities-fuel-select',
            'index': window_id
        },
        style={'display': 'block'}
    )

    by_service_widgets = dmc.Select(
        label='Service',
        data=[{'label': service, 'value': service} for service in services],
        value=services[0] if len(services) > 0 else None,
        id={
            'type': 'cims-requested_quantities-service-select',
            'index': window_id
        },
        style={'display': 'none'}
    )

    by_sector_widgets = dmc.Select(
        label='Sector',
        data=[{'label': sector, 'value': sector} for sector in sectors],
        value=sectors[0],
        id={
            'type': 'cims-requested_quantities-sector-select',
            'index': window_id
        },
        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'cims-requested_quantities-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'cims-requested_quantities-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Result Representation',
            data=[{'label': plot, 'value': plot} for plot in ['By Fuel', 'By Service', 'By Sector']],
            value='By Sector',
            id={
                'type': 'cims-requested_quantities-representation-select',
                'index': window_id
            },
        ),
        by_sector_widgets,
        by_service_widgets,
        by_fuel_widgets,
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'cims-requested_quantities-plot-select',
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
                'type': 'cims-requested_quantities-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'cims-requested_quantities-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'cims-requested_quantities-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'cims-requested_quantities-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Sector', 'By Year', df, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           years[0], scenarios[0], fuel=fuels[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'cims_output',
            'viz': 'requested_quantities'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
