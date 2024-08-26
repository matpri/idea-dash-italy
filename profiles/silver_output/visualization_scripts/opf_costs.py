import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc

from profiles.silver_output import utils


def render_plot(df, scenarios, time_size='hourly'):
    from profiles.silver_output.utils import plot_settings
    print('rendering plot', type)
    name = plot_settings['OPF Costs']['name']
    unit = plot_settings['OPF Costs']['unit']
    title = plot_settings['OPF Costs']['Total']['title']
    x_axis_label = plot_settings['OPF Costs']['Total']['x_label']
    y_axis_label = plot_settings['OPF Costs']['Total']['y_label']


    fig = go.Figure()
    # add title
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )

    try:
        df_scen = df.copy(deep=True)
        df_scen = df_scen[df_scen['scenario'].isin(scenarios)]

        df_scen['time'] = pd.to_datetime(df_scen['time'])
        # groupby time based on time_size
        if time_size == 'daily':
            df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d')
        elif time_size == 'monthly':
            df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m')
        elif time_size == 'yearly':
            df_scen['time'] = df_scen['time'].dt.strftime('%Y')
        else:
            df_scen['time'] = df_scen['time'].dt.strftime('%Y-%m-%d %H:%M:%S')

        cols = df_scen.columns.tolist()
        # remove value column
        cols.remove('value')
        df_scen = df_scen.groupby(cols).sum(numeric_only=True).reset_index()

        can_supply = df_scen.sort_values(by=['time'])
        can_opf_costs = can_supply[can_supply['value'] != 0]
        total = can_opf_costs.groupby(['time', 'scenario']).sum().reset_index()

        # create stacked bar chart
        for i, scen in enumerate(scenarios):
            df_scen = total[total['scenario'].isin(scenarios)]
            df_scen = df_scen.sort_values(by=['time'])
            fig.add_trace(go.Scatter(
                x=df_scen['time'],
                y=df_scen['value'],
                name=scen,
                mode='lines' if len(df_scen['time']) > 1 else 'markers',
                # set line color to respective tech color
                line=dict(color=utils.get_color(scen)),
                marker=dict(color=utils.get_color(scen)),
                customdata=df_scen[['scenario']],  # Add any other columns as needed
                hovertemplate='<b>Scenario:</b> %{customdata[0]}<br>Time: %{x}<br>OPF Cost: %{y:.2f} ' + unit + '<br><extra></extra>'
            ))
        fig.update_yaxes(showgrid=True)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        if can_opf_costs.empty:
            print("No data available, since the results are all zero.")
            fig.add_annotation(
                x=0.5,
                y=0.5,
                text="No data available, since the results are all zero.",
                showarrow=False,
                font=dict(
                    size=16,
                    color="black"
                ),
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

    widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'silver-opf_costs-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Timestep',
            data=[{'label': t_step, 'value': t_step} for t_step in ['hourly', 'daily', 'monthly', 'yearly']],
            value='hourly',
            id={
                'type': 'silver-opf_costs-time_step-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),

        dmc.Button('Download Data', id={'type': 'silver-opf_costs-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'silver-opf_costs-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot(df, [scenarios[0]], 'hourly'),
        id={
            'type': 'figure',
            'index': window_id,
            'profile': 'silver_output',
            'viz': 'opf_costs'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
