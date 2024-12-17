import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from profiles.copper_output import utils


def plot(df, scenario, region, year, aggregate, title, x_axis_label, y_axis_label, unit, season=None):
    fig = go.Figure()
    fig.update_layout(
        title_text=title + f' ({scenario})',
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label + f' ({unit})' if unit != 'NA' else y_axis_label,
        template="simple_white",
    )
    try:
        df_scen = subset(df, region, year, scenario, unit, aggregate, season)
        techs = df_scen.variable.unique().tolist()
        if aggregate:
            colors = [utils.get_group_colors(tech) for tech in techs]
        else:
            colors = [utils.get_color(tech) for tech in techs]

        fig.add_trace(go.Pie(labels=techs, values=df_scen['value'], marker=dict(colors=colors)),)
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


def subset(df, region, year, scenario, unit, aggregate, season=None):
    df_scen = df.copy(deep=True)


    if not pd.api.types.is_numeric_dtype(df['time']):
        df_scen['time'] = pd.to_datetime(df_scen['time'])
        df_scen['time'] = df_scen['time'].dt.strftime('%Y')

    if season is not None:
        df_scen = df_scen[df_scen['season'] == season]
    if aggregate:
        df_scen['variable'] = df_scen["variable"].map(utils.get_group).fillna(df_scen["variable"])
        df_scen = df_scen.groupby(["variable", "region", "time", 'scenario', 'unit']).sum(numeric_only=True).reset_index()
    else:
        df_scen['variable'] = df_scen["variable"].map(utils.get_name).fillna(df_scen["variable"])

    df_scen = df_scen.groupby(["variable", "region", "time", 'scenario', 'unit']).sum(numeric_only=True).reset_index()

    df_scen = df_scen[df_scen['scenario'] == scenario]
    df_scen = df_scen[df_scen['unit'] == unit]  
    df_scen = df_scen[df_scen['region'] == region]
    df_scen = df_scen[df_scen['time'] == year]

    # create new column for total in can_emissions df
    df_scen['total'] = df_scen.groupby(['time', 'scenario'])['value'].transform('sum').values
    df_scen = df_scen[df_scen['value'] != 0]

    return df_scen
