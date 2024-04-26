import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

from profiles.natem_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart

regions_list = [
    'BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL', 'YT', 'NT', 'NU',
]

def render_plot(type, df, aggregate, scenarios, region, year, scenario, pattern_active=True, text_active=False):
    from profiles.natem_output.utils import plot_settings
    print('rendering plot', type)
    name = plot_settings['Supply']['name']
    unit = plot_settings['Supply']['unit']
    if type == 'By Year':
        plot_info = plot_settings['Supply']['By Year']
        if region == 'CAN':
            df = df[~df['variable'].isin(regions_list)]
        return bar_over_years.plot(df, scenarios, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active)
    elif type == 'Trend Over Years':
        plot_info = plot_settings['Supply']['Trend Over Years']
        if region == 'CAN':
            df = df[~df['variable'].isin(regions_list)]
        return trend_over_years.plot(df, scenario, region, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit)
    elif type == 'Pie Chart':
        if region == 'CAN':
            df = df[~df['variable'].isin(regions_list)]
        plot_info = plot_settings['Supply']['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, aggregate, plot_info['title'], plot_info['x_label'], plot_info['y_label'])
    else:
        plot_info = plot_settings['Supply']['By Region']
        return bar_over_regions.plot(df, scenarios, aggregate, year, plot_info['title'], plot_info['x_label'], plot_info['y_label'], name, unit, pattern_active=pattern_active, text_active=text_active)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['time'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value= 'CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'natem-supply-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'natem-supply-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'natem-supply-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'natem-supply-text-switch',
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
                'type': 'natem-supply-plot-select',
                'index': window_id
            },
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'natem-supply-aggregate-switch',
                       'index': window_id}),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'natem-supply-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'natem-supply-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'natem-supply-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'natem-supply-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('By Year', df, True, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           years[0],scenarios[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'natem_output',
            'viz': 'supply'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
