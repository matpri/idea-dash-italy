import plotly.graph_objects as go
import pandas as pd

from profiles.energy_model import utils
from dash import dcc


def plot(df, scenarios, aggregate, year, title, x_axis_label, y_axis_label, tooltip_name, unit, season=None, pattern_active=True, text_active=False, report_type='Total'):
    fig = go.Figure()
    fig.update_layout(
        title_text=title,
        xaxis_title=x_axis_label,
        yaxis_title=y_axis_label,
        template="simple_white",
    )

    try:
        df_scen = subset(df, year, scenarios, aggregate, season)
        scenarios.sort()


        df_scen_time = df_scen[df_scen['time'] == year]


        # remove territories if they exist
        regions_to_keep = [reg for reg in df_scen_time['region'].unique().tolist() if reg not in ['YT', 'NT', 'NU']]
        df_scen = df_scen[df_scen['region'].isin(regions_to_keep)]

        techs = df_scen_time.variable.unique().tolist()

        if report_type == 'Relative Change':
            for tech in techs:
                tech_data = df_scen[df_scen["variable"] == tech]
                for scen in scenarios:
                    tech_data_scen = tech_data[tech_data['scenario'] == scen].sort_values(by=['time'])
                    regions = tech_data_scen['region'].unique().tolist()
                    for reg in regions:
                        tech_data_scen_reg = tech_data_scen[tech_data_scen['region'] == reg]
                        if not tech_data_scen_reg.empty:
                            base_value = tech_data_scen_reg.iloc[0]['value']
                            idx = 0
                            while idx < len(tech_data_scen_reg) and base_value == 0:
                                base_value = tech_data_scen_reg.iloc[idx]['value']
                                idx += 1
                            if base_value != 0:
                                df_scen.loc[(df_scen["variable"] == tech) & (df_scen['scenario'] == scen) & (df_scen['region'] == reg), 'value'] = (tech_data_scen_reg['value'] / base_value)
                            else:
                                df_scen.loc[(df_scen["variable"] == tech) & (df_scen['scenario'] == scen) & (df_scen['region'] == reg), 'value'] = 0
            y_axis_label += ' (%)'
        elif report_type == 'Relative Makeup':
            df_scen = df_scen[df_scen['time'] == year]
            for scen in scenarios:
                scen_data = df_scen[df_scen['scenario'] == scen]
                regions = scen_data['region'].unique().tolist()
                for reg in regions:
                    scen_data_reg = scen_data[scen_data['region'] == reg]
                    total_per_region = scen_data_reg['value'].sum()
                    if total_per_region != 0:
                        df_scen.loc[(df_scen['scenario'] == scen) & (df_scen['region'] == reg), 'value'] = (scen_data_reg['value'] / total_per_region)
                    else:
                        df_scen.loc[(df_scen['scenario'] == scen) & (df_scen['region'] == reg), 'value'] = 0
            y_axis_label += ' (%)'

        df_scen = df_scen[df_scen['time'] == year]
        df_scen['total'] = df_scen.groupby(['region', 'scenario'])['value'].transform('sum')

        for i, tech in enumerate(techs):
            data = df_scen[df_scen["variable"] == tech]
            data = data.sort_values(by=['region', 'scenario'], key=lambda x: x.map(utils.custom_sort_key))

            x = []
            x.append(data["region"].values)
            x.append(data['scenario'].values)
            scen_patterns = [utils.pattern_from_key(scen) for scen in data['scenario'].values]

            if aggregate:
                color = utils.get_group_colors(tech)
            else:
                color = utils.get_color(tech)

            fig.add_bar(x=x, y=data["value"], name=tech, customdata=data['total'],
                        marker_color=color, marker_pattern_shape=scen_patterns if pattern_active else None,
                        textposition='auto' if text_active else None, text=tech if text_active else None,
                        hovertemplate=f'<b>{tech}</b><br><br>' + 'Region: %{x[0]}<br>' + f'Year: {year}<br>' + 'Scenario: %{x[1]}<br>'+f'{tooltip_name}'+': %{y:.2f} '+f'{unit}'+'<br>Total: %{customdata:.2f} '+f'{unit}'+'<br><extra></extra>')
        total_data = df_scen.groupby(['region', 'scenario'])['value'].sum().reset_index()
        x = []
        x.append(total_data['region'].values)
        x.append(total_data['scenario'].values)
        fig.add_trace(go.Scatter(x=x, y=total_data["value"], name='Total', mode='markers', 
                                 marker=dict(size=3, color='rgba(0, 0, 255, 0.6)'),  # Smaller size and softer blue color
                                 hovertemplate='Total: %{y:.2f} '+f'{unit}'+'<br>Region: %{x[0]}<br>' + f'Year: {year}<br>' + 'Scenario: %{x[1]}<br><extra></extra>'))
        
        
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
    return fig


def subset(df, year, scenarios, aggregate, season=None):
    df_scen = df.copy(deep=True)
    df_scen = df_scen[df_scen['region'] != 'CAN']
    regions = df_scen['region'].unique().tolist()
    if season is not None:
        df_scen = df_scen[df_scen['season'] == season]
    if aggregate:
        df_scen['variable'] = df_scen["variable"].map(utils.get_group).fillna(df_scen["variable"])
        df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()
    else:
        df_scen['variable'] = df_scen["variable"].map(utils.get_name).fillna(df_scen["variable"])

    df_scen = df_scen.groupby(["variable", "region", "time", 'scenario']).sum(numeric_only=True).reset_index()

    df_scen = df_scen[df_scen['scenario'].isin(scenarios)]
    df_scen = df_scen[df_scen['region'] != 'CAN']
    df_scen = df_scen[df_scen['value'] != 0]
    # for every variable type in the df, make sure all regions are present if necessary fill with 0
    region_pad = []
    for var in df_scen.variable.unique():
        for scen in df_scen.scenario.unique():
            for reg in regions:
                if not df_scen[
                    (df_scen['variable'] == var) & (df_scen['scenario'] == scen) & (df_scen['region'] == reg)].empty:
                    continue
                else:
                    region_pad.append(
                        {'variable': var, 'region': reg, 'time': year, 'scenario': scen, 'value': 0, 'total': 0},
                    )
    region_pad_df = pd.DataFrame(region_pad)
    df_scen = pd.concat([df_scen, region_pad_df])
    df_scen = df_scen.sort_values(by=['region', 'variable'], key=lambda x: x.map(utils.custom_sort_key))
    return df_scen

