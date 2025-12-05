import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
from profiles.energy_model.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart


def render_plot(type, df, aggregate, scenarios, region, year, scenario, pattern_active=True, text_active=False, report_type='Total'):
    from profiles.energy_model.utils import plot_settings
    #print('rendering plot', type)
    name = plot_settings['Capacity Cost']['name']
    unit = plot_settings['Capacity Cost']['unit']
    if type == 'By Year':
        plot_info = plot_settings['Capacity Cost']['By Year']
        return bar_over_years.plot(df, scenarios, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active, report_type=report_type)
    elif type == 'Trend Over Years':
        plot_info = plot_settings['Capacity Cost']['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, report_type=report_type)
    elif type == 'Pie Chart':
        plot_info = plot_settings['Capacity Cost']['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'])
    else:
        plot_info = plot_settings['Capacity Cost']['By Region']
        return bar_over_regions.plot(df, scenarios, aggregate, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active, report_type=report_type)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()

    base_scenarios = list(set([scenario.split('|')[1] for scenario in scenarios]))
    base_scenarios = ['ALL'] + base_scenarios

    has_reference = 'Reference' in base_scenarios

    regions = df['region'].unique().tolist()
    years = df['time'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value= 'CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'energy_model-gencap_cost-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'energy_model-gencap_cost-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'energy_model-gencap_cost-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'energy_model-gencap_cost-text-switch',
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
                'type': 'energy_model-gencap_cost-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch(
            label='Compare to Reference',
            checked=False,
            id={
                'type': 'energy_model-gencap_cost-compare-reference',
                'index': window_id,
            },
            style={'display': 'block' if has_reference else 'none'}
        ),
        dmc.Select(
            label='Report Type',
            data=[{'label': report_type, 'value': report_type} for report_type in ['Total', 'Relative Change', 'Relative Makeup']],
            value='Total',
            id={
                'type': 'energy_model-gencap_cost-report-type-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'energy_model-gencap_cost-aggregate-switch',
                       'index': window_id}),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'energy_model-gencap_cost-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.MultiSelect(
            label='Scenario Group',
            data=[{'label': scenario, 'value': scenario} for scenario in base_scenarios],
            value=[],
            id={
                'type': 'energy_model-gencap_cost-scenario-group-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.MultiSelect(
            label='Version',
            data=[],
            value=[],
            id={
                'type': 'energy_model-gencap_cost-version-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'energy_model-gencap_cost-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'energy_model-gencap_cost-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-gencap_cost-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, True, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           years[0],scenarios[0], report_type='Total'),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'Power System Models',
            'viz': 'Capacity Cost'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
