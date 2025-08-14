import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from profiles.recap import utils


def plot(df, scenarios, region, aggregate, title, x_axis_label, y_axis_label, tooltip_name, unit, season=None, pattern_active=True, text_active=False):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template="simple_white",
    )

    try:
        df_scen = subset(df, region, scenarios, aggregate, season)
        scenarios.sort()
        techs = df_scen.variable.unique().tolist()
        num_years = df_scen.time.nunique()
        scen_patterns = [utils.pattern_from_key(scen) for scen in scenarios] * num_years

        for i, tech in enumerate(techs):
            data = df_scen[df_scen["variable"] == tech]
            data = data.sort_values(by=['time', 'scenario'])

            x = []
            x.append(data["time"].values)
            x.append(data['scenario'].values)
            if aggregate:
                color = utils.get_group_colors(tech)
            else:
                color = utils.get_color(tech)

            fig.add_bar(x=x, y=data["value"], name=tech, customdata=data['total'], marker_color=color,
                        marker_pattern_shape=scen_patterns if pattern_active else None,
                        textposition='auto' if text_active else None, text=tech if text_active else None,
                        hovertemplate=f'<b>{tech}</b><br><br>' + 'Year: %{x[0]}<br>' + f'Region: {region}<br>' + 'Scenario: %{x[1]}<br>'+f'{tooltip_name}'+': %{y:.2f} '+f'{unit}'+'<br>Total: %{customdata:.2f} '+f'{unit}'+'<br><extra></extra>')
        
        total_data = df_scen.groupby(['time', 'scenario'])['value'].sum().reset_index()
        x = []
        x.append(total_data['time'].values)
        x.append(total_data['scenario'].values)
        fig.add_trace(go.Scatter(x=x, y=total_data["value"], name='Total', mode='markers', 
                                 marker=dict(size=3, color='rgba(0, 0, 255, 0.6)'),  # Smaller size and softer blue color
                                 hovertemplate='Total: %{y:.2f} '+f'{unit}'+'<br>Year: %{x[0]}<br>' + f'Region: {region}<br>' + 'Scenario: %{x[1]}<br><extra></extra>'))
        fig.update_layout(barmode='relative', legend_traceorder="reversed")
        fig.update_yaxes(showgrid=True)
        if df_scen.empty:
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

    except Exception as e:
        print(title, 'plot:', e)

    fig.layout.autosize = True
    fig.update_xaxes(tickangle=90)  # Rotate x-axis tick labels by 90 degrees for better readability
    return fig


def subset(df, region, scenarios, aggregate, season=None):
    df_scen = df.copy(deep=True)


    # Remove the years where all entries in the value column are 0
    value_sum_per_year = df_scen.groupby('time')['value'].sum()
    years_with_non_zero_values = value_sum_per_year[value_sum_per_year != 0].index
    df_scen = df_scen[df_scen['time'].isin(years_with_non_zero_values)]
    years = df_scen['time'].unique().tolist()

    if season is not None:
        df_scen = df_scen[df_scen['season'] == season]
    if aggregate:
        df_scen['variable'] = df_scen["variable"].map(utils.get_group).fillna(df_scen["variable"])
        df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()
    else:
        df_scen['variable'] = df_scen["variable"].map(utils.get_name).fillna(df_scen["variable"])

    df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()

    df_scen = df_scen[df_scen['scenario'].isin(scenarios)]

    df_scen = df_scen[df_scen['region'] == region]

    # create new column for total in can_emissions df
    df_scen['total'] = df_scen.groupby(['time', 'scenario'])['value'].transform('sum').values

    df_scen = df_scen[df_scen['value'] != 0]


    df_scen = df_scen.fillna(0)
    year_pad = []
    for var in df_scen.variable.unique():
        for scen in df_scen.scenario.unique():
            for year in years:
                if not df_scen[
                    (df_scen['variable'] == var) & (df_scen['scenario'] == scen) & (
                            df_scen['time'] == year)].empty:
                    continue
                else:
                    year_pad.append(
                        {'variable': var, 'region': region, 'time': year, 'scenario': scen, 'value': 0, 'total': 0},
                    )
    year_pad_df = pd.DataFrame(year_pad)
    df_scen = pd.concat([df_scen, year_pad_df])
    df_scen = df_scen.sort_values(by=['time', 'variable'], key=lambda x: x.map(utils.custom_sort_key))
    return df_scen
