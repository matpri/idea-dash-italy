import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from profiles.coders_input import utils


def plot(df, scenarios, region, aggregate, title, x_axis_label, y_axis_label, tooltip_name, unit, season=None):
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

            fig.add_bar(x=x, y=data["value"], name=tech,
                            customdata=np.stack([data['total'], data['exports'], data['imports']]).T, marker_color=color,
                        marker_pattern_shape=scen_patterns,
                        hovertemplate=f'<b>{tech}</b><br><br>' + 'Year: %{x[0]}<br>' + f'Region: {region}<br>' + 'Scenario: %{x[1]}<br>'+f'{tooltip_name}'+': %{y:.2f} '+f'{unit}'+'<br>Total: %{customdata:.2f}' + f'{unit}<br>' +
                                          'Exports: %{customdata[1]:.2f} ' + f'{unit}' + '<br>Imports: '
                                                                               '%{customdata[2]:.2f} ' + f'{unit}' + '<br>' + '<br><extra></extra>')
        fig.update_layout(barmode='relative')
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
        #print(title, 'plot:', e)

    fig.layout.autosize = True
    return fig

def aggregate_imports(df):
    imports = df[df['variable'].isin(['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL']) & (df['value'] > 0)]
    exports = df[df['variable'].isin(['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL']) & (df['value'] < 0)]

    imports['variable'] = 'Imports'
    exports['variable'] = 'Exports'

    df = df[~df['variable'].isin(['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL'])]
    return pd.concat([df, imports, exports])



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
        df_scen = aggregate_imports(df_scen)
    else:
        df_scen['variable'] = df_scen["variable"].map(utils.get_name).fillna(df_scen["variable"])

    df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()

    df_scen = df_scen[df_scen['scenario'].isin(scenarios)]

    df_scen = df_scen[df_scen['region'] == region]

    if region == 'CAN':
        df_scen = df_scen[~df_scen['variable'].isin(['Imports', 'Exports', 'BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL'])]

    # create new column for total in can_emissions df
    df_scen['total'] = df_scen.groupby(['time', 'scenario'])['value'].transform('sum').values

    if aggregate:
        df_scen.loc[df_scen['variable'] == 'Exports', 'exports'] = df_scen['value']
        df_scen.loc[df_scen['variable'] == 'Imports', 'imports'] = df_scen['value']
    else:
        df_scen.loc[df_scen['variable'].isin(['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL'])
                    & df_scen['value'] > 0, 'imports'] = df_scen[
            'value']
        df_scen.loc[df_scen['variable'].isin(['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'PE', 'NL']) & df_scen['value'] < 0, 'exports'] = df_scen[
            'value']

    df_scen['imports'].fillna(value=0, inplace=True)
    df_scen['exports'].fillna(value=0, inplace=True)

    df_scen = df_scen[df_scen['value'] != 0]
    df_scen = df_scen.fillna(0)

    def get_sum(row, col_name):
        return df_scen.loc[
            (df_scen['time'] == row['time']) & (df_scen['scenario'] == row['scenario']), col_name].sum()


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
    df_scen['imports'] = df_scen.apply(lambda row: get_sum(row, 'imports'), axis=1)
    df_scen['exports'] = df_scen.apply(lambda row: get_sum(row, 'exports'), axis=1)

    # subtract imports and exports from total
    df_scen['total'] = df_scen['total'] - df_scen['imports'] - df_scen['exports']
    df_scen = df_scen.sort_values(by=['time', 'variable'], key=lambda x: x.map(utils.custom_sort_key))
    return df_scen
