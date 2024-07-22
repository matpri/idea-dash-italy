import dash_mantine_components as dmc
from dash import html, dcc
from profiles.cims_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart


def render_plot(df, p_type, r_type, by_rep, year, region, scenarios, scenario, variable, pattern_active=True,
                text_active=False):
    from profiles.cims_output.utils import plot_settings
    df_plt = df[
        (df['plot'] == p_type)
        ]

    name = plot_settings[p_type]['name']
    unit = plot_settings[p_type]['unit']

    df_plt = process_represenation(p_type, by_rep, variable, df_plt)\

    if p_type == 'Requested Quantities':
        variable = 'Requested Quantities'

    if r_type == 'By Year':
        return bar_over_years.plot(df_plt, scenarios, region, 'Electricity:' + variable, 'Year',
                                   variable,
                                   name, unit, pattern_active=pattern_active,
                                   text_active=text_active)
    elif r_type == 'Trend Over Years':
        return trend_over_years.plot(df_plt, scenario, region, 'Electricity:' + variable, 'Year',
                                   variable,
                                     name, unit)
    elif r_type == 'Pie Chart':
        return pie_chart.plot(df_plt, scenario, region, year, 'Electricity:' + variable, 'Year',
                                   variable)

    else:
        return bar_over_regions.plot(df_plt, scenarios, year, 'Electricity:' + 'Electricity:' + variable, 'Year',
                                   variable,
                                     name, unit, pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(p_type, by_rep, variable, df):
    if p_type == 'GHG':
        filtered_df = df[
            (df.parameter == variable)
        ]
        filtered_df['variable'] = filtered_df['sub_context'] + '|' + filtered_df['context']
        filtered_df['variable'] += '- Negative' if 'negative' in filtered_df[
            'variable'] else '- Avoided' if 'avoided' in \
                                            filtered_df[
                                                'variable'] else '- Emitted'
        filtered_df = filtered_df[['region', 'variable', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    elif p_type == 'Stock':
        filtered_df = df[df['parameter'] == variable]
        filtered_df = filtered_df[['region', 'technology', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'technology': 'variable', 'year': 'time'})
    else:
        df = df[df['context'] == 'Total']
        if by_rep:
            filtered_df = df[
                (df['technology'].isna())
            ]
            filtered_df = filtered_df[['region', 'context', 'year', 'value_num', 'scenario']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'context': 'variable', 'year': 'time'})
        else:
            filtered_df = df[
                (df['technology'].isna())
            ]
            filtered_df = filtered_df[['region', 'short_path', 'year', 'value_num', 'scenario']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    return filtered_df


def plot(df, window_id):
    plot_types = df['plot'].unique().tolist()
    plot_type = plot_types[0]
    df_plt = df[df['plot'] == plot_type]
    if plot_type == 'Requested Quantities':
        df_plt = df_plt[df_plt['technology'].isna()]

    regions = df_plt.region.unique().tolist()
    years = df_plt.year.unique().tolist()
    scenarios = df_plt.scenario.unique().tolist()

    variables = df_plt[df_plt['parameter'].str.contains('emissions')][
        'parameter'].unique().tolist() if plot_type == 'GHG' else \
        df_plt[df_plt['parameter'].str.contains('stock')][
            'parameter'].unique().tolist() if plot_type == 'Stock' else []

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'cims-electricity-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'cims-electricity-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'cims-electricity-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'cims-electricity-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    variable_select = dmc.Select(
        label='Variable',
        data=[{'label': variable, 'value': variable} for variable in variables],
        value=variables[0],
        id={
            'type': 'cims-electricity-variable-select',
            'index': window_id
        },
        style={'display': 'block'} if len(variables) > 0 else {'display': 'none'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in plot_types],
            value=plot_type,
            id={
                'type': 'cims-electricity-plot-select',
                'index': window_id
            },
        ),

        variable_select,

        dmc.Switch(
            label='By Sector',
            checked=False,
            id={
                'type': 'cims-electricity-rep_switch',
                'index': window_id
            },
            style={'display': 'block'} if plot_type == 'Requested Quantities' else {'display': 'none'}
        ),

        dmc.Select(
            label='Representation Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'cims-electricity-rep-select',
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
                'type': 'cims-electricity-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'cims-electricity-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'cims-electricity-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'cims-electricity-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(
            df, plot_type, 'By Year', False, years[0], regions[0], scenarios, scenarios[0], variables[0]
        ),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'cims_output',
            'viz': 'electricity'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout,plot_layout
