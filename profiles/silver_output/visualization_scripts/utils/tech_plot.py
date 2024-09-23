import pandas as pd
import plotly.graph_objects as go

from profiles.silver_output import utils
from profiles.silver_output.utils import custom_sort_key


def render(df, scenario, title, x_axis_label, y_axis_label, time_size='hourly'):
    # turn date range into a readable format

    fig = go.Figure()
    # add title
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template='simple_white',
    )
    df_scen = df.copy(deep=True)
    df_scen = df_scen[df_scen['scenario'] == scenario]

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
    cols.remove('region')
    df_scen = df_scen.groupby(cols).sum(numeric_only=True).reset_index()

    can_supply = df_scen.sort_values(by=['time', 'variable'], key=lambda x: x.map(custom_sort_key))
    can_emissions = can_supply[can_supply['value'] != 0]
    techs = can_emissions.variable.unique().tolist()

    # Determine the number of unique time entries
    unique_times = can_emissions['time'].nunique()

    if unique_times == 1:
        # Create a pie chart
        fig = go.Figure(data=[go.Pie(
            labels=can_emissions['variable'],
            values=can_emissions['value'],
            hole=.3,
            marker=dict(colors=[utils.get_color(tech) for tech in can_emissions['variable']])
        )])
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(
            title_text=title,
            annotations=[dict(text=f'Total: {can_emissions["value"].sum():.2f} {y_axis_label}', showarrow=False)]
        )
    elif unique_times < 12:
        # Create a bar plot
        for tech in techs:
            df_tech = can_emissions[can_emissions['variable'] == tech]
            df_tech = df_tech.sort_values(by=['time'])
            fig.add_trace(go.Bar(
                x=df_tech['time'],
                y=df_tech['value'],
                name=tech,
                marker_color=utils.get_color(tech),
                hovertemplate=f'<b>{tech}</b><br><br>' +
                              f'Scenario: {scenario} <br>' +
                              'Time: %{x}<br>' +
                              f'Value: %{{y:.2f}} {y_axis_label}<br>' +
                              '<extra></extra>'
            ))
        fig.update_layout(barmode='stack')
    else:
        # Create a stacked area chart (original behavior)
        for tech in techs:
            df_tech = can_emissions[can_emissions['variable'] == tech]
            df_tech = df_tech.sort_values(by=['time'])
            output = tech.split('|')[0]
            tech_type = tech.split('|')[1]
            fig.add_trace(go.Scatter(
                x=df_tech['time'],
                y=df_tech['value'],
                name=tech,
                mode='lines',
                line=dict(color=utils.get_color(tech)),
                stackgroup='one',
                hovertemplate=f'<b>{tech_type}</b><br><br>' +
                              f'Scenario: {scenario} <br>' +
                              'Time: %{x}<br>' +
                              f'{output}: %{{y:.2f}} {y_axis_label}<br>' +
                              '<extra></extra>'
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

    fig.layout.autosize = True
    return fig