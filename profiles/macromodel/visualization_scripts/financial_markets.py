import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

from components import ids
from profiles.macromodel.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart, trend_over_year


def render_plot(type, name, df, aggregate, scenarios, region, unit, year, scenario, pattern_active=True, text_active=False):
    print('rendering plot financial_markets', type)
    if type == 'By Year':
        return bar_over_years.plot(df, scenarios, region, aggregate, name, "Year", name, name, unit,
                                   pattern_active=pattern_active,
                                   text_active=text_active)
    elif type == 'Trend Over Years':
        return trend_over_years.plot(df, scenario, region, aggregate, name, "Year", name, name, unit)
    elif type == 'Trend in one Year':
        return trend_over_year.plot(df, scenario, region, year, aggregate, name, "Year", name, name, unit)
    elif type == 'Pie Chart':
        return pie_chart.plot(df, scenario, region, year, aggregate, name, "Year", name, unit)
    else:
        return bar_over_regions.plot(df, scenarios, aggregate, year, name, "Region", name, name, unit,
                                     pattern_active=pattern_active,
                                     text_active=text_active)

def plot(df, window_id):
    df["variable"] = df["variable"].str.capitalize()
    df["variable"] = df["variable"].str.replace('_', ' ')
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    units = df['unit'].unique().tolist()

    trend_one_year = False
    years = df['time'].unique().tolist()


    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'region-select',
            'name': 'financial_markets',
            'profile': 'macromodel',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'year-select',
            'name': 'financial_markets',
            'profile': 'macromodel',
            'index': window_id
        },

        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'pattern-switch',
            'name': 'financial_markets',
            'profile': 'macromodel',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'text-switch',
            'name': 'financial_markets',
            'profile': 'macromodel',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    plot_options = ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']
    if trend_one_year:
        plot_options.append('Trend in one Year')
    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in plot_options
                  ],
            value='Trend Over Years',
            id={
                'type': 'plot-select',
                'name': 'financial_markets',
                'profile': 'macromodel',
                'index': window_id
            },
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'aggregate-switch',
                       'name': 'financial_markets',
                       'profile': 'macromodel',
                       'index': window_id}),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'scenario-multi-select',
                'name': 'financial_markets',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'scenario-select',
                'name': 'financial_markets',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        dmc.Select(
            label='Unit',
            data=[{'label': unit, 'value': unit} for unit in units],
            value=units[0],
            id={
                'type': 'unit-select',
                'name': 'financial_markets',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'download-button',
                                        'name': 'financial_markets',
                                        'profile': 'macromodel', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'download',
                         'name': 'financial_markets',
                         'profile': 'macromodel', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Trend Over Years', 'Financial Markets', df, True, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           units[0], years[0], scenarios[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'macromodel',
            'name': 'financial_markets'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout

