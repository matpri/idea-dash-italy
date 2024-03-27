import plotly.graph_objects as go

from profiles.silver_output import utils

def render(df, scenario, title, y_axis_label, x_axis_label):
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
        df_scen = df_scen[df_scen['scenario'] == scenario]

        can_supply = df_scen.sort_values(by=['time', 'variable'], key=lambda x: x.map(custom_sort_key))
        can_emissions = can_supply[can_supply['value'] != 0]
        techs = can_emissions.variable.unique().tolist()

        # create stacked bar chart
        for i, tech in enumerate(techs):
            df_tech = can_emissions[can_emissions['variable'] == tech]
            df_tech = df_tech.sort_values(by=['time'])
            fig.add_trace(go.Scatter(
                x=df_tech['time'],
                y=df_tech['value'],
                name=tech,
                mode='lines',
                # set line color to respective tech color
                line=dict(color=utils.get_color(techs)),
                stackgroup='one'
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

    except Exception as e:
        print("Dispatch viz", e)
        pass