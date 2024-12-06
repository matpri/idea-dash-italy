import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

from components import ids
from profiles.macromodel.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart, trend_over_year


def render_plot(type, name, df, aggregate, scenarios, region, unit, year, scenario, pattern_active=True, text_active=False, sector='All'):
    print('rendering plot energy sectors', type)
    if sector == 'All':
        # only keep where sector is null
        df = df[df['sector'].isnull()]
    else:
        df = df[df['sector'] == sector]
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
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    units = df['unit'].unique().tolist()
    sectors = ['All'] + df['sector'].unique().tolist()
    if pd.api.types.is_numeric_dtype(df['time']):
        years = df['time'].unique().tolist()
        trend_one_year = False
    else:
        years = pd.to_datetime(df['time']).dt.strftime('%Y').unique().tolist()
        # set a boolean that shows that there are unique days in a single year
        dates = pd.to_datetime(df['time'])
        # find dates that are not in the same year
        unique_dates = dates.dt.year.unique()
        trend_one_year = False
        for year in unique_dates:
            if len(dates[dates.dt.year == year].dt.dayofyear.unique()) > 1:
                trend_one_year = True
                break


    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'sectored-region-select',
            'name': 'energy-sectors',
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
            'type': 'sectored-year-select',
            'name': 'energy-sectors',
            'profile': 'macromodel',
            'index': window_id
        },

        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'sectored-pattern-switch',
            'name': 'energy-sectors',
            'profile': 'macromodel',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'sectored-text-switch',
            'name': 'energy-sectors',
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
                'type': 'sectored-plot-select',
                'name': 'energy-sectors',
                'profile': 'macromodel',
                'index': window_id
            },
        ),
        dmc.Switch('Aggregate',
                   checked=True,
                   id={
                       'type': 'sectored-aggregate-switch',
                       'name': 'energy-sectors',
                       'profile': 'macromodel',
                       'index': window_id}),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'sectored-scenario-multi-select',
                'name': 'energy-sectors',
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
                'type': 'sectored-scenario-select',
                'name': 'energy-sectors',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'none'}
        ),

        dmc.Select(
            label='Sector',
            data=[{'label': sector, 'value': sector} for sector in sectors],
            value=sectors[0],
            id={
                'type': 'sectored-sector-select',
                'name': 'energy-sectors',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Unit',
            data=[{'label': unit, 'value': unit} for unit in units],
            value=units[0],
            id={
                'type': 'sectored-unit-select',
                'name': 'energy-sectors',
                'profile': 'macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'sectored-download-button',
                                        'name': 'energy-sectors',
                                        'profile': 'macromodel', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'sectored-download',
                         'name': 'energy-sectors',
                         'profile': 'macromodel', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Trend Over Years', 'Energy Sectors', df, True, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           units[0], years[0], scenarios[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'macromodel',
            'name': 'energy-sectors'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout

