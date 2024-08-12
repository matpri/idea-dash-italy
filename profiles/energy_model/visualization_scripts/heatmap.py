import dash_mantine_components as dmc
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from plotly.subplots import make_subplots

from profiles.energy_model import utils


def render_plot(type, df, scenarios, year):
    from profiles.energy_model.utils import plot_settings
    # print('rendering plot', type)
    if len(scenarios) == 0:
        fig = go.Figure()
        fig.add_annotation(
            x=0.5,
            y=0.5,
            text="Please select at least one scenario",
            showarrow=False,
            font=dict(
                size=16,
                color="black"
            ),
            align="center",
            valign="middle",
        )
        return fig
    df = df[df.variable == type]
    df = df[df.region == 'CAN']
    df = df[df.scenario.isin(scenarios)]

    scen_diff_by_year = []
    for scenario in scenarios:
        for scenario2 in scenarios:
            if scenario != scenario2:
                df1 = df[df.scenario == scenario]
                df2 = df[df.scenario == scenario2]
                df1 = df1.drop(['variable', 'region'], axis=1)
                df2 = df2.drop(['variable', 'region'], axis=1)
                df1 = df1.pivot_table(values='value', columns='time')
                df2 = df2.pivot_table(values='value', columns='time')
                df1 = df1.to_numpy()
                df2 = df2.to_numpy()
                diff = df1 - df2
                scen_diff_by_year.append(diff)

    scen_diff = np.asarray(scen_diff_by_year).flatten()
    min_val = np.min(scen_diff)
    max_val = np.max(scen_diff)


    df = df[df.time == year]
    df_scenarios = df.scenario.unique().tolist()
    for scenario in scenarios:
        if scenario not in df_scenarios:
            df = pd.concat([df, pd.DataFrame({'scenario': [scenario], 'value': [None]})])

    df = df.drop(['time', 'variable', 'region'], axis=1)
    df = df.pivot_table(values='value', columns='scenario')
    heatmap = pd.DataFrame(columns=df.columns, index=df.columns[::-1], data=0)
    print(heatmap)
    for i in df.columns:
        masked = False
        for j in df.columns:

                heatmap.loc[i, j] = df[i].to_numpy() - df[j].to_numpy()
    fig = go.Figure(
        data=go.Heatmap(
            z=heatmap,
            x=heatmap.columns,
            y=heatmap.index,
            colorscale='RdBu',
            zmid=0,
            zmin=min_val,
            zmax=max_val,

            reversescale=True,
        ),
        # have x-axis labels on top
        layout=go.Layout(
            xaxis=dict(side='top'),
            yaxis=dict(title=''),
            title=f'{type} difference by scenario in {year}',
            margin=dict(l=100, r=100, t=50, b=50),
            template='simple_white',
        )

    )

    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting heatmap')
    classes = df['variable'].str.split('|', expand=True)[0].unique().tolist()
    years = df['time'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value=classes[0],
            id={
                'type': 'energy_model-heatmap-plot-select',
                'index': window_id
            },
        ),
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in df['scenario'].unique()],
            value=df['scenario'].unique(),
            id={
                'type': 'energy_model-heatmap-scenario-select',
                'index': window_id
            },
        ),

        dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': 'energy_model-heatmap-year-select',
                'index': window_id
            },
        ),
        dmc.Button('Download Data', id={'type': 'energy_model-heatmap-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'energy_model-heatmap-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(classes[0], df, df['scenario'].unique(), years[0]),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'energy_model',
            'viz': 'heatmap'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )
    return widget_layout, plot_layout
