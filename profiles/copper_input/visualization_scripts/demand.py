import dash_mantine_components as dmc
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
date_mapper = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
               9: 'September',
               10: 'October', 11: 'November', 12: 'December', 'January': '01', 'February': '02', 'March': '03',
               'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09',
               'October': '10', 'November': '11', 'December': '12'}


def render_plot(df, type):
    from profiles.copper_input.utils import plot_settings
    if type == 'By Scenario':
        plot_info = plot_settings['Demand']['By Scenario']
        return plot_demand(df, plot_info['title'], plot_info['x_label'], plot_info['y_label'], type='By Scenario')
    else:
        plot_info = plot_settings['Demand']['By Region']
        return plot_demand(df, plot_info['title'], plot_info['x_label'], plot_info['y_label'], type='By Region')


def plot_demand(df, title='Dispatched Electricity', x_axis_label='Time',
                y_axis_label='Dispatched Electricity (TWh)', type='By Scenario'):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )

    if type == 'By Scenario':
        region = df['region'].iloc[0]
        scenarios = df['scenario'].unique().tolist()
        # try:
        for scenario in scenarios:
            df_scen = df[df['scenario'] == scenario]
            fig.add_trace(
                go.Scatter(
                    x=df_scen['time'],
                    y=df_scen['value'],
                    mode='lines',
                    showlegend=True,
                    name=scenario,
                    hovertemplate=f'Scenario: {scenario} <br> Region: {region}<br>' + 'Time: %{x}<br>Demand: %{y:.2f} TWh<br>'
                )
            )
    else:
        scenario = df['scenario'].iloc[0]
        regions = df['region'].unique().tolist()
        for region in regions:
            df_region = df[df['region'] == region]
            fig.add_trace(
                go.Scatter(
                    x=df_region['time'],
                    y=df_region['value'],
                    mode='lines',
                    showlegend=True,
                    name=region,
                    hovertemplate=f'Scenario: {scenario} <br> Region: {region}<br>' + 'Time: %{x}<br>Demand: %{y:.2f} TWh<br>'
                )
            )

    fig.update_yaxes(showgrid=True)
    if df.empty:
        #print("No data available, since the results are all zero.")
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
    # except Exception as e:
    #     #print("Dispatch viz", e)
    #     pass

    fig.layout.autosize = True
    fig.add_hline(y=0, line_dash="dot", line_color="grey")
    fig.update_layout(legend=dict(
        font=dict(
            size=14,
        )
    ))
    # remove reset-axis button from toolbar
    fig.update_layout(modebar_remove=['autoScale', 'lasso2d'])
    return fig


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in ['By Scenario', 'By Region']],
            value='By Scenario',
            id={
                'type': 'copper_input-demand-plot-select',
                'index': window_id
            },
        ),

        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'copper_input-demand-scenario-multi-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value='CAN' if 'CAN' in regions else regions[0],
            id={
                'type': 'copper_input-demand-region-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'copper_input-demand-scenario-select',
                'index': window_id
            },
            style={'display': 'none'}
        ),
    ])
    df_scen = df.copy()
    df_scen = df_scen[df_scen['scenario'].isin([scenarios[0]])]
    df_scen = df_scen[df_scen['region'] == regions[0]]

    plot_layout = dcc.Graph(
        figure=render_plot(df_scen, 'By Scenario'),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'COPPER Input',
            'viz': 'demand'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
