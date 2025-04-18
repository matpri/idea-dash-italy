import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

from components import ids
import plotly.express as px


def render_plot(type, df, scenarios, region, unit, year,variable, n_bins=20):
    print('rendering plot histogram', type)
    db = df.copy()
    print('scenarios', scenarios)
    df_scen = db[db['scenario'].isin(scenarios) & (db['region'] == region) & (db['time'] == year) & (db['variable'] == variable) & (db['unit'] == unit) & (db['type'] == type)]

    # make histogram where colour is scenario
    fig = px.histogram(df_scen, x='value', color='scenario', title=f'{variable} in {region} in {year}', labels={'value': f'{variable} ({unit})', 'scenario': 'Scenario'}, barmode='overlay', nbins=n_bins)
    fig.update_traces(opacity=max(0.3,1 / len(scenarios)) if len(scenarios) > 1 else 1)
    fig.update_layout(
        xaxis_title_text=f'{variable} ({unit})',
        yaxis_title_text='Count',
        template='simple_white'
    )
    return fig

def plot(df, window_id):
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    types = df['type'].unique().tolist()
    variables = df[df['type'] == types[0]]['variable'].unique().tolist()
    units = df[(df['type'] == types[0]) & (df['variable'] == variables[0])]['unit'].unique().tolist()
    years = df['time'].unique().tolist()


    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'region-select',
            'viz_type': 'Histograms',
            'profile': 'Macromodel',
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
            'viz_type': 'Histograms',
            'profile': 'Macromodel',
            'index': window_id
        },

        style={'display': 'block'}
    )

    plot_options = types
    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in plot_options
                  ],
            value=plot_options[0],
            id={
                'type': 'plot-select',
                'viz_type': 'Histograms',
                'profile': 'Macromodel',
                'index': window_id
            },
        ),dmc.Select(
            label='Variable',
            data=[{'label': plot, 'value': plot} for plot in variables
                  ],
            value=variables[0],
            id={
                'type': 'variable-select',
                'viz_type': 'Histograms',
                'profile': 'Macromodel',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'scenario-multi-select',
                'viz_type': 'Histograms',
                'profile': 'Macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Unit',
            data=[{'label': unit, 'value': unit} for unit in units],
            value=units[0],
            id={
                'type': 'unit-select',
                'viz_type': 'Histograms',
                'profile': 'Macromodel',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Text('Number of Bins'),
        dmc.Slider(
            value=20,
            min=1,
            max=100,
            step=1,
            id={
                'type': 'bins-slider',
                'viz_type': 'Histograms',
                'profile': 'Macromodel',
                'index': window_id
            },
        ),

        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'download-button',
                                        'viz_type': 'Histograms',
                                        'profile': 'Macromodel', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'download',
                         'viz_type': 'Histograms',
                         'profile': 'Macromodel', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(
            types[0], df, [scenarios[0]], regions[0], units[0], years[0],
            variables[0],
        ),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'Macromodel',
            'name': 'Histograms'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout

