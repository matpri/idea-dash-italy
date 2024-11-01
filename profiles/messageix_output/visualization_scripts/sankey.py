import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc

from profiles.messageix_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, pie_chart


def render_plot(df, scenario, region, year):
    l = pd.DataFrame(list(df['source'].append(df['target']).unique()))
    l.reset_index(level=0, inplace=True)
    l.set_index(0, inplace=True)

    # Assign integers to the strings in source column
    s = pd.DataFrame(df['source'])
    s.set_index('source', drop=True, inplace=True)
    s.index.names = [0]
    s['index'] = 'nan'
    s.update(l)

    # Assign integers to the strings in target column
    t = pd.DataFrame(df['target'])
    t.set_index('target', drop=True, inplace=True)
    t.index.names = [0]
    t['index'] = 'nan'
    t.update(l)

    # Create sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=10,
            line=dict(color="black", width=0.5),
            label=list(l.index),  # use the index of the labeled strings as integers
            hovertemplate='%{label}: %{value} TWh<extra></extra>',
            color="blue"
        ),
        link=dict(
            source=list(s['index']),  # each integer corresponds to the index of the labeled strings
            target=list(t['index']),  # each integer corresponds to the index of the labeled strings
            value=list(df['Value']),
            hovertemplate='"%{source.label}" to "%{target.label}": %{value} TWh<extra></extra>'
        ))])

    fig.update_layout(title_text="%s_%s" % (region, year), font_size=10)
    fig.show()

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
            'type': 'messageix-capacity-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'messageix-capacity-year-select',
            'index': window_id
        },

        style={'display': 'block'}
    )


    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'messageix-capacity-plot-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'messageix-capacity-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'messageix-capacity-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'messageix-capacity-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, scenarios[0], regions[0], years[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'messageix_output',
            'viz': 'capacity'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
