import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

from profiles.labourabm_output import utils


def render_plot(df, scenarios, occupations):
    print('rendering plot', type)
    fig = go.Figure()
    fig.update_layout(
        template='simple_white',
    )

    try:
        df_scen = df.copy(deep=True)
        df_scen = df_scen[df_scen['scenario'].isin(scenarios) & df_scen['variable'].isin(occupations)]

        # Line plot for more than 10 time entries
        for scen in scenarios:
            pattern = utils.dash_from_key(scen)
            for occ in occupations:
                color = utils.get_color(occ)

                df_scen_temp = df_scen[(df_scen['scenario'] == scen) & (df_scen['variable'] == occ)]
                fig.add_trace(
                    go.Scatter(
                        x=df_scen_temp['time'],
                        y=df_scen_temp['value'],
                        mode='lines',
                        name=f'{scen} - {occ}',
                        line=dict(color=color, dash=pattern),
                    )
                )

        if df_scen.empty:
            print("No data available, since the results are all zero.")
            fig.add_annotation(
                x=0.5,
                y=0.5,
                text="No data available, since the results are all zero.",
                showarrow=False,
                font=dict(size=16, color="black"),
                align="center",
                valign="middle",
            )

    except Exception as e:
        print("Dispatch viz", e)
        pass

    fig.layout.autosize = True
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    occupations = df['variable'].unique().tolist()

    widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'labourabm-total_employment-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.MultiSelect(
            label='Occupation',
            data=[{'label': occupation, 'value': occupation} for occupation in occupations],
            value=['Total'],
            id={
                'type': 'labourabm-total_employment-occupation-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Button('Download Data', id={'type': 'labourabm-total_employment-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'labourabm-total_employment-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, [scenarios[0]], ['Total']),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'labourabm_output',
            'viz': 'total_employment'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
