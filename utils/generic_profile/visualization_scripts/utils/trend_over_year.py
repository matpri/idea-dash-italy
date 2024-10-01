import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from profiles.copper_output import utils


def plot(df, scenario, region, year, aggregate, title, x_axis_label, y_axis_label, tooltip_name, unit, season=None):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template="simple_white",
    )

    try:
        df_scen = subset(df, region, year, scenario, aggregate, season)
        techs = df_scen.variable.unique().tolist()

        for i, tech in enumerate(techs):
            data = df_scen[df_scen["variable"] == tech]
            data = data.sort_values(by=['time'])

            if aggregate:
                color = utils.get_group_colors(tech)
            else:
                color = utils.get_color(tech)

            fig.add_scatter(x=data["time"], y=data["value"], name=tech, mode='lines+markers', marker_color=color,
                            hovertemplate=f'<b>{tech}</b><br><br>' + 'Year: %{x[0]}<br>' + f'Region: {region}<br>' + f'Scenario: {scenario}<br>'  + f'{tooltip_name}' + ': %{y:.2f} ' + f'{unit}' + '<br>Total: %{customdata:.2f} ' + f'{unit}' + '<br><extra></extra>')

        fig.update_yaxes(showgrid=True)
        if df_scen.empty:
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
        print(title, 'plot:', e)

    fig.layout.autosize = True
    return fig


def subset(df, region, year, scenario, aggregate, season=None):
    df_scen = df.copy(deep=True)
    df_scen['year'] = pd.to_datetime(df_scen['time'])
    df_scen['year'] = df_scen['year'].dt.strftime('%Y')

    df_scen = df_scen[df_scen['year'] == year]

    df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()

    df_scen = df_scen[df_scen['scenario'] == scenario]

    df_scen = df_scen[df_scen['region'] == region]

    # create new column for total in can_emissions df
    df_scen['total'] = df_scen.groupby(['time', 'scenario'])['value'].transform('sum').values

    df_scen = df_scen[df_scen['value'] != 0]

    df_scen = df_scen.fillna(0)
    df_scen = df_scen.sort_values(by=['time', 'variable'], key=lambda x: x.map(utils.custom_sort_key))
    return df_scen
