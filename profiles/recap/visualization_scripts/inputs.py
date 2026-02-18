import json

import dash_mantine_components as dmc
import geojson
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import geopandas as gpd
from dash import html, dcc
from matplotlib.dates import datestr2num

from components import ids
from profiles.recap import utils
from profiles.recap.visualization_scripts.utils import bar_over_regions, bar_over_years, trend_over_years, \
    pie_chart


def get_contrasting_font_color(rgb_color):
    """Get a contrasting font color (black or white) based on the background color brightness."""
    print(rgb_color)
    r, g, b = [int(x) for x in rgb_color[4:-1].split(',')]
    brightness = (r * 299 + g * 587 + b * 114) / 1000  # Brightness formula for RGB
    return '#ffffff' if brightness < 128 else '#000000'


def render_cost(data, _c_type, _c_scenario, _c_region, _c_sector):
    data = data[data['variable'].str.startswith(_c_type)]
    unit = data['unit'].iloc[0]

    data['variable'] = data['variable'].str.replace(_c_type + '|', '')
    data = data[data['variable'].str.startswith(_c_sector)]
    data['variable'] = data['variable'].str.replace(_c_sector + '|', '')
    return trend_over_years.plot(data, _c_scenario, _c_region, _c_type, 'Year', 'Cost', _c_type, unit)


def render_t_cost(data, _t_cost_scenario, bl=False, region=None):
    data = data[data['scenario'].isin(_t_cost_scenario)]
    if region is not None:
        data = data[data['region'] == region]
    if not data.empty:
        # create a table
        data = data[['scenario', 'variable', 'value']]

        df_pivot = data.pivot(index='variable', columns='scenario', values='value')

        df_pivot = df_pivot.fillna('')
        # Create a Plotly Table
        header_values = [''] + list(df_pivot.columns)
        if bl:
            df_pivot = df_pivot.applymap(lambda x: 'Yes' if x else 'No')
        cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

        colors_by_row = []
        font_colors = [['#000000'] * len(df_pivot.index)]

        if bl:
            colors = []
            for col in df_pivot.columns:
                colors.append(['rgb(255,153,153)' if val == "No" else 'rgb(153,255,153)' for val in df_pivot[col]])
            colors_by_row = [['#ffffff', '#e5eeec'] * (len(df_pivot.index) // 2)] + colors
            for column in colors:
                font_colors.append([get_contrasting_font_color(color) for color in column])
        else:
            # Normal processing for numeric values
            min_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
            max_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

            def normalize(value):
                if isinstance(value, (int, float)):
                    return (value - min_value) / (max_value - min_value)
                return None

            colors = []
            for col in df_pivot.columns:
                normalized_data = [normalize(val) for val in df_pivot[col]]
                colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[
                                         0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value
                                     in
                                     normalized_data])]
            colors_by_row = [['#ffffff', '#e5eeec'] * (
                    len(df_pivot.index) // 2)] + colors  # Determine font colors based on the background color
            for column in colors:
                font_colors.append([get_contrasting_font_color(color) for color in column])

        # Calculate the width for each column
        column_width = []
        column_width.append(max(df_pivot.index.str.len()) * 8)
        for col in df_pivot.columns:
            column_width.append(max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8)

        # Create Plotly table
        fig = go.Figure(data=[go.Table(
            columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
            columnwidth=column_width,
            header=dict(values=header_values,
                        fill_color=['#ffffff', '#248ce6', '#248ce6'],
                        font=dict(color='white'),
                        align='center'),
            cells=dict(values=cell_values,
                       fill_color=colors_by_row,
                       line_color=colors_by_row,
                       font=dict(color=font_colors),
                       align='left'))
        ])
    else:
        fig = go.Figure()
        # print("No data available, since the results are all zero.")
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

    return fig


def render_tech_params(data, _p_scenario):
    data = data[data['scenario'].isin(_p_scenario)]
    if not data.empty:
        # create a table
        data = data[['scenario', 'variable', 'value']]

        df_pivot = data.pivot(index='variable', columns='scenario', values='value')

        df_pivot = df_pivot.fillna('')
        # Create a Plotly Table
        header_values = [''] + list(df_pivot.columns)
        cell_values = [df_pivot.index] + [df_pivot[col] for col in df_pivot.columns]

        min_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('inf')).min()
        max_value = data['value'].apply(lambda x: x if isinstance(x, (int, float)) else float('-inf')).max()

        def normalize(value):
            if isinstance(value, (int, float)):
                return (value - min_value) / (max_value - min_value)
            return None

        colors = []

        for col in df_pivot.columns:
            normalized_data = [normalize(val) for val in df_pivot[col]]
            colors += [np.array([px.colors.sample_colorscale('Blues', normalized_value)[
                                     0] if normalized_value is not None else 'rgb(255,255,255)' for normalized_value in
                                 normalized_data])]

        colors_by_row = [['#ffffff', '#e5eeec'] * (
                len(df_pivot.index) // 2)] + colors  # Determine font colors based on the background color
        font_colors = [['#000000'] * len(df_pivot.index)]
        for column in colors:
            font_colors.append([get_contrasting_font_color(color) for color in column])
        # Calculate the width for each column
        column_width = []
        column_width.append(max(df_pivot.index.str.len()) * 8)
        for col in df_pivot.columns:
            column_width.append(max([len(str(col))] + [len(str(val)) for val in df_pivot[col]]) * 8)

        print(column_width)

        # Create Plotly table
        fig = go.Figure(data=[go.Table(
            columnorder=[i + 1 for i in range(len(df_pivot.columns) + 1)],
            columnwidth=column_width,
            header=dict(values=header_values,
                        fill_color=['#ffffff', '#248ce6', '#248ce6'],
                        font=dict(color='white'),
                        align='center'),
            cells=dict(values=cell_values,
                       fill_color=colors_by_row,
                       line_color=colors_by_row,
                       font=dict(color=font_colors),

                       align='left'))
        ])
    else:
        fig = go.Figure()
        # print("No data available, since the results are all zero.")
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

    return fig


def render_generic(df_scen, p_type, _scenario, _region, _multi_scenario=None, _multi_region=None, _gen_type='By Scenario'):
    if _gen_type == 'By Scenario':
        scenarios = _multi_scenario
        regions = [_region]
    else:
        scenarios = [_scenario]
        regions = _multi_region
    fig = go.Figure()
    y_axis_label = p_type
    fig.update_layout(
        title_text=p_type,
        xaxis_title='Time',
        yaxis_title=y_axis_label,
        template="simple_white",
    )
    try:
        if 'Average' in regions:
            df_scen_total = df_scen.groupby(['class', 'time', 'scenario', 'unit']).mean(numeric_only=True).reset_index()
            df_scen_total['region'] = 'Average'
            df_scen = pd.concat([df_scen, df_scen_total], ignore_index=True)

        df_scen = df_scen[df_scen['scenario'].isin(scenarios)]
        df_scen = df_scen[df_scen['region'].isin(regions)]



        unit = df_scen['unit'].iloc[0] if not df_scen.empty else None
        vars = scenarios if _gen_type == 'By Scenario' else regions
        for i, _var in enumerate(vars):
            data = df_scen[df_scen["scenario"] == _var] if _gen_type == 'By Scenario' else df_scen[df_scen["region"] == _var]
            data = data.sort_values(by=['time'])

            # color = utils.get_color(_var)

            fig.add_scatter(x=data["time"], y=data["value"], name=_var, mode='lines+markers',# marker_color=color,
                            hovertemplate=f'<b>{_var}</b><br><br>' + 'Year: %{x}<br>' + f'Region: {_region}<br>' + f'{p_type}' + ': %{y:.2f} ' + f'{unit}' + '<br><extra></extra>')

        fig.update_yaxes(showgrid=True)
        if df_scen.empty:
            # print("No data available, since the results are all zero.")
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
        print(p_type, 'plot:', e)

    fig.layout.autosize = True
    return fig


def render_plot(p_type, df,
                _scenario=None, _region=None, _multi_scenario=None, _multi_region=None, _gen_type=None,
                _c_type=None, _c_scenario=None, _c_region=None, _c_sector=None,
                _policy_scenarios=None, _policy_region=None):
    data = df.copy()
    data['class'], data['variable'] = data['variable'].apply(lambda x: x.split('|')[0]), data['variable'].apply(
        lambda x: '|'.join(x.split('|')[1:]))
    data = data[data['class'] == p_type]
    if p_type == 'Cost':
        return render_cost(data, _c_type, _c_scenario, _c_region, _c_sector)
    elif p_type == 'Policy':
        return render_t_cost(data, _policy_scenarios, True, _policy_region)
    else:
        return render_generic(data, p_type, _scenario, _region,
                              _multi_scenario, _multi_region, _gen_type)


def plot(df, window_id):
    '''

    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    '''
    # print('plotting inputs')
    classes = df['variable'].apply(lambda x: x.split('|')[0]).unique()

    scenarios = df['scenario'].unique().tolist()
    regions = ['Average'] + df['region'].unique().tolist()

    generic_widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': _p, 'value': _p} for _p in ['By Scenario', 'By Region']],
            value='By Scenario',
            id={
                'type': 'recap-inputs-generic-plot-select',
                'index': window_id
            },
        ),
        html.Div([
            dmc.MultiSelect(
                label='Scenarios',
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                value=[scenarios[0]] if len(scenarios) else '',
                id={
                    'type': 'recap-inputs-scenario-multi-select',
                    'index': window_id
                },
            ),
            dmc.Select(
                label='Region',
                data=[{'label': region, 'value': region} for region in regions],
                value=regions[0] if len(regions) else '',
                id={
                    'type': 'recap-inputs-region-select',
                    'index': window_id
                },
            ),
        ],
            style={'display': 'block'},
            id={
                'type': 'recap-inputs-generic-byscenario-widget',
                'index': window_id
            }
        ),
        html.Div([
            dmc.Select(
                label='Scenarios',
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                value=scenarios[0] if len(scenarios) else '',
                id={
                    'type': 'recap-inputs-scenario-select',
                    'index': window_id
                },
            ),
            dmc.MultiSelect(
                label='Region',
                data=[{'label': region, 'value': region} for region in regions],
                value=[regions[0]] if len(regions) else '',
                id={
                    'type': 'recap-inputs-region-multi-select',
                    'index': window_id
                },
            ),
        ],
            style={'display': 'none'},
            id={
                'type': 'recap-inputs-generic-byregion-widget',
                'index': window_id
            }
        ),

    ],
        style={'display': 'block'} if 'Policy' not in classes and classes[0] != 'Cost' else {'display': 'none'},
        id={
            'type': 'recap-inputs-generic-widget',
            'index': window_id
        }
    )

    policy_scenarios = []
    policy_regions = []
    if 'Policy' in classes:
        policy_scenarios = df[df['variable'].str.startswith('Policy')]['scenario'].unique()
        policy_regions = df[df['variable'].str.startswith('Policy')]['region'].unique()
        if "AB" in policy_regions:
            policy_regions = ["AB"]

    policy_widget_layout = html.Div([
        dmc.MultiSelect(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in policy_scenarios],
            value=policy_scenarios if len(policy_scenarios) else [],
            id={
                'type': 'recap-inputs-policy-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in policy_regions],
            value=policy_regions[0] if len(policy_regions) else '',
            id={
                'type': 'recap-inputs-policy-region-select',
                'index': window_id
            },
        )
    ],
        style={'display': 'block'} if 'Policy' in classes else {'display': 'none'},
        id={
            'type': 'recap-inputs-policy-widget',
            'index': window_id
        }
    )

    costs = []
    c_regions = []
    c_scenarios = []
    c_sector = []
    if 'Cost' in classes:
        costs = df[df['variable'].str.startswith('Cost')]['variable'].apply(lambda x: x.split('|')[1]).unique()
        c_sector = df[df['variable'].str.startswith('Cost')]['variable'].apply(lambda x: x.split('|')[2]).unique()
        c_regions = df[df['variable'].str.startswith('Cost')]['region'].unique()
        if "AB" in c_regions:
            c_regions = ["AB"]
        c_scenarios = df[df['variable'].str.startswith('Cost')]['scenario'].unique()

    cost_widget_layout = html.Div([
        dmc.Select(
            label='Cost Type',
            data=[{'label': cost, 'value': cost} for cost in costs],
            value=costs[0] if len(costs) else '',
            id={
                'type': 'recap-inputs-cost-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Sector',
            data=[{'label': sector, 'value': sector} for sector in c_sector],
            value=c_sector[0] if len(c_sector) else '',
            id={
                'type': 'recap-inputs-cost-sector-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in c_scenarios],
            value=c_scenarios[0] if len(c_scenarios) else '',
            id={
                'type': 'recap-inputs-cost-scenario-select',
                'index': window_id
            },
        ),
        dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in c_regions],
            value=c_regions[0] if len(c_regions) else '',
            id={
                'type': 'recap-inputs-cost-region-select',
                'index': window_id
            },
        ),
    ],
        style={'display': 'none'} if 'Policy' in classes or classes[0] != 'Cost' else {'display': 'block'},
        id={
            'type': 'recap-inputs-cost-widget',
            'index': window_id
        }
    )

    widget_layout = html.Div([
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in classes],
            value='Policy' if 'Policy' in classes else classes[0],
            id={
                'type': 'recap-inputs-plot-select',
                'index': window_id
            },
        ),
        generic_widget_layout,
        cost_widget_layout,
        policy_widget_layout,
        dmc.Button('Download Data', id={'type': 'recap-inputs-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'recap-inputs-download', 'index': window_id}),
    ])

    plot_layout = dcc.Graph(
        figure=render_plot('Policy' if 'Policy' in classes else classes[0], df,
                           _scenario=[scenarios[0]] if len(scenarios) else None,
                           _region=regions[0] if len(regions) else None,
                            _multi_scenario=scenarios if len(scenarios) else None,
                            _multi_region=regions if len(regions) else None,
                            _gen_type='By Scenario',
                           _policy_scenarios=policy_scenarios if len(policy_scenarios) else None,
                           _policy_region=policy_regions[0] if len(policy_regions) else None,
                           _c_type=costs[0] if len(costs) else None,
                           _c_scenario=c_scenarios[0] if len(c_scenarios) else None,
                           _c_region=c_regions[0] if len(c_regions) else None,
                           _c_sector=c_sector[0] if len(c_sector) else None
                           ),
        id={
            'type': ids.FIGURE,
            'index': window_id,
            'profile': 'Summary',
            'viz': 'Electricity Prices'
        },
        style={
            'width': '100%',
            'height': '100%'
        }

    )
    return widget_layout, plot_layout
