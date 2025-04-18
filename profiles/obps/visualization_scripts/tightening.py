import dash_mantine_components as dmc
import numpy as np
from dash import html, dcc
from components import ids
from profiles.obps.visualization_scripts.utils import trend_over_years, table


def render_plot(type, df, scenarios, region, year, sector):
    from profiles.obps.utils import plot_settings
    #print('rendering plot', type)
    name = 'OBPS Tightening'
    data = df[df['sector'] == sector]
    if type == 'Table':
        return table.plot(data, scenarios, year, region)
    elif type == 'Trend Over Years':
        return trend_over_years.plot(data, scenarios, region, False, 'OBPS Tightening', 'Year', 'value', name)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['time'].unique().tolist()
    sectors = df['sector'].unique().tolist()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value= 'CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'obps-tightening-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'obps-tightening-year-select',
            'index': window_id
        },

        style={'display': 'block'}
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['Table', 'Trend Over Years']],
            value='Table',
            id={
                'type': 'obps-tightening-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Sector',
            data=[{'label': sector, 'value': sector} for sector in sectors],
            value=sectors[0],
            id={
                'type': 'obps-tightening-sector-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'obps-tightening-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'obps-tightening-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'obps-tightening-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'obps-tightening-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Table', df, [scenarios[0]], 'CAN' if 'CAN' in regions else regions[0],
                           years[0],sectors[0]),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'OBPS',
            'viz': 'tightening'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
