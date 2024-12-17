import dash_mantine_components as dmc
import pandas as pd
import plotly.graph_objects as go
from dash import html, dcc
from components import ids
date_mapper = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
               9: 'September',
               10: 'October', 11: 'November', 12: 'December', 'January': '01', 'February': '02', 'March': '03',
               'April': '04', 'May': '05', 'June': '06', 'July': '07', 'August': '08', 'September': '09',
               'October': '10', 'November': '11', 'December': '12'}


def render_plot(df):
    from profiles.coders_input.utils import plot_settings
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
    df['local_time'] = pd.to_datetime(df['local_time'])
    df['demand_MWh'] = df['demand_MWh'].astype(float)
    
    regions = df['province'].unique().tolist()
    for region in regions:
        df_region = df[df['province'] == region]
        fig.add_trace(
            go.Scatter(
                x=df_region['local_time'],
                y=df_region['demand_MWh'],
                mode='lines',
                showlegend=True,
                name=region,
                hovertemplate=f'Region: {region}<br>' + 'Time: %{x}<br>Demand: %{y:.2f} TWh<br>'
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
    regions = df['province'].unique().tolist()

    widget_layout = html.Div([
        dmc.Button('Download Data', id={'type': 'coders_input-demand-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'coders_input-demand-download', 'index': window_id}),
    ], style={'textAlign': 'center'})

    plot_layout = dcc.Graph(
        figure=render_plot(df),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'coders_input',
            'viz': 'demand'
        },
        style={
            'width': '100%',
            'height': '100%'
        }
    )

    return widget_layout, plot_layout
