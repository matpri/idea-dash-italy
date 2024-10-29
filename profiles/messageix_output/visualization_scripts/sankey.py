import dash_mantine_components as dmc
import pandas as pd
from dash import html, dcc
import plotly.graph_objects as go


def render_plot(df, scenario, region, year):
    csv = df[(df['scenario'] == scenario) & (df['region'] == region) & (df['time'] == year)].copy()
    csv = csv.groupby(['source', 'target']).sum().reset_index()

    # map source and target to integers adding a new column for label that is the source and target separated by a comma
    nodes = []
    for i, row in csv.iterrows():
        if row['source'] not in nodes:
            nodes.append(row['source'])
        if row['target'] not in nodes:
            nodes.append(row['target'])
    csv['source_int'] = csv['source'].apply(lambda x: nodes.index(x))
    csv['target_int'] = csv['target'].apply(lambda x: nodes.index(x))
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color="blue"

        ),
        link=dict(
            source=csv['source_int'].tolist(),
            target=csv['target_int'].tolist(),
            value=csv['value'].tolist(),
        )
    )])

    fig.update_layout(title_text="Sankey Diagram for Fuel Flow", font_size=10)
    return fig

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
            'type': 'messageix-sankey-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'messageix-sankey-year-select',
            'index': window_id
        },

        style={'display': 'block'}
    )


    widget_layout = html.Div([
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'messageix-sankey-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'messageix-sankey-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                     style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'messageix-sankey-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, scenarios[0], regions[0], years[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'messageix_output',
            'viz': 'sankey'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
