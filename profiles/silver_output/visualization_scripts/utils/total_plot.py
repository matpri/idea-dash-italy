import pandas as pd
import plotly.graph_objects as go

from profiles.silver_output import utils

def render(df, scenarios, title, x_axis_label, y_axis_label, time_size='hourly'):
    # turn date range into a readable format

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
        cols.remove('region')
        df_scen = df_scen.groupby(cols).sum(numeric_only=True).reset_index()

        can_supply = df_scen.sort_values(by=['time'])
        can_opf_costs = can_supply[can_supply['value'] != 0]
        total = can_opf_costs.groupby(['time', 'scenario']).sum().reset_index()
        unit = y_axis_label

        # Determine the number of unique time entries
        unique_times = total['time'].nunique()

        if unique_times == 1:
            # Create a pie chart
            fig = go.Figure(data=[go.Pie(
                labels=total['scenario'],
                values=total['value'],
                hole=.3,
                marker=dict(colors=[utils.get_color(scen) for scen in total['scenario']])
            )])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                title_text=title,
                annotations=[dict(text=f'Total: {total["value"].sum():.2f} {unit}', showarrow=False)]
            )
        elif unique_times < 12:
            # Create a bar plot
            for i, scen in enumerate(scenarios):
                df_scen = total[total['scenario'] == scen]
                df_scen = df_scen.sort_values(by=['time'])
                fig.add_trace(go.Bar(
                    x=df_scen['time'],
                    y=df_scen['value'],
                    name=scen,
                    marker_color=utils.get_color(scen),
                    hovertemplate=f'<b>{scen}</b><br><br>' +
                                  'Time: %{x}<br>' +
                                  'Total: %{y:.2f} ' + f'{unit}<br>' +
                                  '<extra></extra>'
                ))
            fig.update_layout(barmode='group')
        else:
            # Create a line plot (original behavior)
            for i, scen in enumerate(scenarios):
                df_scen = total[total['scenario'] == scen]
                df_scen = df_scen.sort_values(by=['time'])
                fig.add_trace(go.Scatter(
                    x=df_scen['time'],
                    y=df_scen['value'],
                    name=scen,
                    mode='lines' if len(df_scen['time']) > 1 else 'markers',
                    line=dict(color=utils.get_color(scen)),
                    marker=dict(color=utils.get_color(scen)),
                    hovertemplate=f'<b>{scen}</b><br><br>' +
                                  'Time: %{x}<br>' +
                                  'Total: %{y:.2f} ' + f'{unit}<br>' +
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