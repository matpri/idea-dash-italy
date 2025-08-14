import math

import dash_mantine_components as dmc
from dash import html, dcc
from components import ids
import plotly.graph_objects as go

from profiles.recap.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart
import profiles.recap.utils as utils
from profiles.recap.utils import get_color


def render_plot(representation, type, df, scenarios, region, year, scenario, pattern_active=True, text_active=False,
                sector=None, service=None, fuel=None):
    from profiles.recap.utils import plot_settings
    plot_name = 'Energy Demand'
    name = plot_settings[plot_name]['name']
    unit = plot_settings[plot_name]['unit']
    print('rendering plot', type)
    if type == 'Sankey':
        df = df[(df['sector'] == sector)].copy()
    else:
        df = process_represenation(df, representation, sector, service, fuel)
    if type == 'By Year':
        plot_info = plot_settings[plot_name]['By Year']
        return bar_over_years.plot(df, scenarios, region, plot_info['title'], plot_info['x_label'],
                                   plot_info['y_label'],
                                   name, unit, pattern_active=pattern_active,
                                   text_active=text_active)
    elif type == 'Trend Over Years':
        plot_info = plot_settings[plot_name]['Trend Over Years']
        return trend_over_years.plot(df, scenario, region, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'],
                                     name, unit)
    elif type == 'Pie Chart':
        plot_info = plot_settings[plot_name]['Pie Chart']
        return pie_chart.plot(df, scenario, region, year, plot_info['title'], plot_info['x_label'],
                              plot_info['y_label'],
                              )
    elif type == 'Sankey':
        by_fuel = df[(df['year'] == year) & (df['region'] == region)].copy()
        # drop where context == Total
        by_fuel = by_fuel[by_fuel['context'] != 'Total']

        # drop where short_path is None
        by_fuel = by_fuel[by_fuel['short_path'].notna()]

        # Find rows where value_num, context, and service are the same
        duplicates = by_fuel[by_fuel.duplicated(subset=['value_num', 'context', 'service'], keep=False)]
        overlapping_propagating = by_fuel[by_fuel.service.isin(duplicates.parent_service.unique())]
        for i, row in overlapping_propagating.iterrows():
            by_fuel.loc[(by_fuel['parent_service'] == row['service']) & (
                    by_fuel['context'] == row['context']), 'value_num'] = row['value_num']
        # only keep one where parent_service, service, context, and value_num are the same
        by_fuel = by_fuel.drop_duplicates(subset=['parent_service', 'service', 'context', 'value_num'],
                                          keep='first')
        nodes = []
        for i, row in by_fuel.iterrows():
            if row['service'] not in nodes:
                nodes.append(row['service'])
            if row['parent_service'] not in nodes:
                nodes.append(row['parent_service'])
        by_fuel['source_int'] = by_fuel['service'].apply(lambda x: nodes.index(x))
        by_fuel['target_int'] = by_fuel['parent_service'].apply(lambda x: nodes.index(x))

        colors = [get_color(context) for context in by_fuel['context'].unique().tolist()]
        context_colors = dict(zip(by_fuel['context'].unique().tolist(), colors))
        contexts = by_fuel['context'].unique().tolist()

        fig = go.Figure(data=[go.Sankey(
            arrangement='perpendicular',
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=nodes

            ),
            link=dict(
                source=by_fuel['source_int'].tolist(),
                target=by_fuel['target_int'].tolist(),
                value=by_fuel['value_num'].tolist(),
                color=by_fuel['context'].apply(lambda x: context_colors[x]).tolist(),
            )
        )])

        for context in contexts:
            fig.add_scatter(x=[0], y=[0], mode='markers', marker=dict(color=context_colors[context], size=10),
                            showlegend=True, name=context)

        fig.update_layout(title_text="Sankey Diagram for Fuel Flow", font_size=10)
        return fig

    else:
        plot_info = plot_settings[plot_name]['By Region']
        return bar_over_regions.plot(df, scenarios, year, plot_info['title'], plot_info['x_label'],
                                     plot_info['y_label'],
                                     name, unit, pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(df, representation, sector, service, fuel):
    if representation == 'By Fuel':
        filtered_df = df[
            (df['technology'].isna()) &
            (df['sector'] == sector)
            ]
        filtered_df = filtered_df[(filtered_df.short_path == service) & (filtered_df['context'] != 'Total')]
        filtered_df = filtered_df[['region', 'context', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'context': 'variable', 'year': 'time'})

    elif representation == 'By Service':
        filtered_df = df[(df['technology'].isna()) & (df['context'] == fuel)].groupby(
            ['region', 'sector', 'year', 'short_path', 'scenario']).sum(numeric_only=True).reset_index()
        filtered_df = filtered_df[['region', 'short_path', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    else:
        if fuel != 'All':
            df = df[(df['context'] == fuel) & (df['sector'] != fuel)]
        filtered_df = df[(df['technology'].isna()) & ~df.sector.isna() & (
                (df.short_path == df.sector )& (df.parent_service==''))]
        filtered_df = filtered_df.groupby(
            ['region', 'sector', 'year', 'scenario']).sum(numeric_only=True).reset_index()

        filtered_df = filtered_df[['region', 'sector', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'sector': 'variable', 'year': 'time'})

    return filtered_df


def widgets(df, window_id):
    """
    :param df: pandas Dataframe containing the data to visualize
    :param window_id: window id to use when registering components to dash
    :return: html.Div([widgets]), dcc.Graph(plot)
    """
    scenarios = df['scenario'].unique().tolist()
    regions = df['region'].unique().tolist()
    years = df['year'].unique().tolist()
    sectors = df['sector'].unique().tolist()
    sectors = [sector for sector in sectors if
               sector is not None and sector != '' and sector != math.nan and isinstance(sector, str)]
    services = df[(df['technology'].isna()) & (df['sector'] == sectors[0])]['short_path'].unique().tolist()
    fuels = df[(df['technology'].isna())]['context'].unique().tolist()

    # get max depth which is the number of layers in the short_path
    max_depth = df['short_path'].apply(lambda x: len(x.split('.'))).max()

    by_year_widgets = dmc.Select(
        label='Region',
        data=[{'label': region, 'value': region} for region in regions],
        value='CAN' if 'CAN' in regions else regions[0],
        id={
            'type': 'recap-requested_quantities-region-select',
            'index': window_id
        },
        style={'display': 'block'}

    )

    by_region_widgets = dmc.Select(
        label='Year',
        data=[{'label': year, 'value': year} for year in years],
        value=years[0],
        id={
            'type': 'recap-requested_quantities-year-select',
            'index': window_id
        },

        style={'display': 'none'}
    )

    by_fuel_widgets = dmc.Select(
        label='Fuel',
        data=[{'label': fuel, 'value': fuel} for fuel in fuels],
        value=fuels[0],
        id={
            'type': 'recap-requested_quantities-fuel-select',
            'index': window_id
        },
        style={'display': 'block'}
    )

    by_service_widgets = []

    for i in range(max_depth):
        if i == 0:
            by_service_widgets.append(dmc.Select(
                label=f'Layer {i}',
                data=[{'label': service, 'value': service} for service in
                      df[df.sector == sectors[0]][f'layer_{i}'].unique().tolist()],
                value=df[df.sector == sectors[0]][f'layer_{i}'].unique().tolist()[0],
                id={
                    'type': f'recap-requested_quantities-service-select',
                    'index': window_id,
                    'layer': i
                },
                style={'display': 'none'}
            ))

        elif i == 1:
            by_service_widgets.append(dmc.Select(
                label=f'Layer {i}',
                data=[{'label': service, 'value': service} for service in df[(df.sector == sectors[0]) & (
                            df.layer_0 == df[df.sector == sectors[0]]['layer_0'].unique().tolist()[0])][
                    f'layer_{i}'].unique().tolist()],
                value='',
                id={
                    'type': f'recap-requested_quantities-service-select',
                    'index': window_id,
                    'layer': i
                },
                style={'display': 'none'}
            ))


        else:
            by_service_widgets.append(dmc.Select(
                label=f'Layer {i}',
                data=[],
                value='',
                id={
                    'type': 'recap-requested_quantities-service-select',
                    'index': window_id,
                    'layer': i
                },
                style={'display': 'none'}
            ))

    by_sector_widgets = dmc.Select(
        label='Sector',
        data=[{'label': sector, 'value': sector} for sector in sectors],
        value=sectors[0],
        id={
            'type': 'recap-requested_quantities-sector-select',
            'index': window_id
        },
        style={'display': 'none'}
    )

    pattern_toggle = dmc.Switch(
        label='Pattern',
        checked=True,
        id={
            'type': 'recap-requested_quantities-pattern-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    text_toggle = dmc.Switch(
        label='Text',
        checked=False,
        id={
            'type': 'recap-requested_quantities-text-switch',
            'index': window_id,
        },
        style={'display': 'block'}
    )

    widget_layout = [
        dmc.Select(
            label='Result Representation',
            data=[{'label': plot, 'value': plot} for plot in ['By Fuel', 'By Service', 'By Sector']],
            value='By Sector',
            id={
                'type': 'recap-requested_quantities-representation-select',
                'index': window_id
            },
            style={'display': 'block'}
        ),
        by_sector_widgets,
        *by_service_widgets,
        by_fuel_widgets,
        dmc.Select(
            label='Plot Options',
            data=[{'label': plot, 'value': plot} for plot in
                  ['Sankey', 'By Year', 'By Region', 'Trend Over Years', 'Pie Chart']],
            value='By Year',
            id={
                'type': 'recap-requested_quantities-plot-select',
                'index': window_id
            },
        ),
        pattern_toggle,
        text_toggle,
        dmc.MultiSelect(
            label='Scenarios',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=[scenarios[0]],
            id={
                'type': 'recap-requested_quantities-scenario-multi-select',
                'index': window_id,
            },
            style={'display': 'block'}
        ),
        dmc.Select(
            label='Scenario',
            data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
            value=scenarios[0],
            id={
                'type': 'recap-requested_quantities-scenario-select',
                'index': window_id,
            },
            style={'display': 'none'}
        ),
        by_year_widgets,
        by_region_widgets,
        dmc.Button('Download Data', id={'type': 'recap-requested_quantities-download-button', 'index': window_id},
                   variant='light',
                   # center the button
                   style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
        dcc.Download(id={'type': 'recap-requested_quantities-download', 'index': window_id}),
    ]

    return widget_layout, render_plot('By Sector', 'By Year', df, [scenarios[0]],
                                      'CAN' if 'CAN' in regions else regions[0],
                                      years[0], scenarios[0], fuel=fuels[0])
