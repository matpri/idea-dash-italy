import dash_mantine_components as dmc
from dash import html, dcc
from profiles.cims_output.visualization_scripts.utils import bar_over_years, bar_over_regions, trend_over_years, \
    pie_chart, sankey


def render_plot(sector, df, p_type, r_type, by_rep, year, region, scenarios, scenario, variable, pattern_active=True,
                text_active=False, service='Agriculture', tech_sector=None, tech_service=None):
    from profiles.cims_output.utils import plot_settings
    df_plt = df[
        (df['plot'] == p_type)
        ]

    name = plot_settings[p_type]['name']
    unit = plot_settings[p_type]['unit']

    df_plt = process_represenation(p_type, by_rep, variable, df_plt, service, tech_sector, tech_service)

    if p_type == 'Energy Demand':
        variable = 'Energy Demand'

    if r_type == 'By Year':
        return bar_over_years.plot(df_plt, scenarios, region, f'{sector}: ' + variable, 'Year',
                                   variable,
                                   name, unit, pattern_active=pattern_active,
                                   text_active=text_active)
    elif r_type == 'Trend Over Years':
        return trend_over_years.plot(df_plt, scenario, region, f'{sector}: ' + variable, 'Year',
                                   variable,
                                     name, unit)
    elif r_type == 'Pie Chart':
        return pie_chart.plot(df_plt, scenario, region, year, f'{sector}: ' + variable, 'Year',
                                   variable)

    elif r_type == 'Sankey':
        return sankey.plot(df_plt, scenario, region, year, f'{sector}: ' + variable, variable)

    else:
        return bar_over_regions.plot(df_plt, scenarios, year, f'{sector}: ' + variable, 'Year',
                                   variable,
                                     name, unit, pattern_active=pattern_active,
                                     text_active=text_active)


def process_represenation(p_type, by_rep, variable, df, service, tech_sector=None, tech_service=None):
    if p_type == 'Emissions':
        if by_rep:
            filtered_df = df[
                (df.parameter == variable) & (df.short_path == service)
                ]

            filtered_df['variable'] = filtered_df['sub_context'] + '|' + filtered_df['context']
            filtered_df['variable'] += '- Negative' if 'negative' in filtered_df[
                'variable'] else '- Avoided' if 'avoided' in \
                                                filtered_df[
                                                    'variable'] else '- Emitted'
            filtered_df = filtered_df[['region', 'variable', 'year', 'value_num', 'scenario']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'year': 'time'})
        else:
            filtered_df = df[
                (df.parameter == variable)
                ]

            filtered_df['context'] = filtered_df['sub_context'] + '|' + filtered_df['context']
            filtered_df['context'] += '- Negative' if 'negative' in filtered_df[
                'context'] else '- Avoided' if 'avoided' in \
                                                filtered_df[
                                                    'context'] else '- Emitted'

            filtered_df = filtered_df[['region', 'short_path', 'year', 'value_num', 'scenario', 'context']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    elif p_type == 'Technology Stocks':
        # Modified to work like "By Service" in overview tab
        filtered_df = df[df['parameter'] == variable]
        
        # Filter by sector and service if provided (similar to overview tab logic)
        if tech_sector:
            filtered_df = filtered_df[filtered_df['sector'] == tech_sector]
        if tech_service:
            # Handle both single service and list of services
            if isinstance(tech_service, list):
                filtered_df = filtered_df[filtered_df['short_path'].apply(lambda x: any(x.startswith(s) for s in tech_service))]
            else:
                filtered_df = filtered_df[filtered_df['short_path'].str.startswith(tech_service)]
        
        # Group by technology (same as overview tab "By Service" behavior)
        filtered_df = filtered_df[['region', 'technology', 'year', 'value_num', 'scenario']]
        filtered_df = filtered_df.rename(columns={'value_num': 'value', 'technology': 'variable', 'year': 'time'})
    else:
        df = df[df['context'] != 'Total']
        if by_rep:
            filtered_df = df[
                (df['technology'].isna()) & ~df.sector.isna() & (df.short_path == service)
            ]
            filtered_df = filtered_df[['region', 'context', 'year', 'value_num', 'scenario']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'context': 'variable', 'year': 'time'})
        else:
            filtered_df = df[
                (df['technology'].isna())
            ]
            filtered_df = filtered_df[['region', 'short_path', 'year', 'value_num', 'scenario', 'context', 'service', 'parent_service']]
            filtered_df = filtered_df.rename(columns={'value_num': 'value', 'short_path': 'variable', 'year': 'time'})
    return filtered_df

def create_plot(sector):
    lower_sector = sector.lower()
    lower_sector = lower_sector.replace(' ', '_')
    def plot(df, window_id):
        plot_types = df['plot'].unique().tolist()
        plot_type = plot_types[0]
        df_plt = df[df['plot'] == plot_type]
        if plot_type == 'Energy Demand':
            df_plt = df_plt[df_plt['technology'].isna()]

        regions = df_plt.region.unique().tolist()
        years = df_plt.year.unique().tolist()
        scenarios = df_plt.scenario.unique().tolist()

        # get all columns with layer_ in the name
        max_depth = df_plt.columns.str.contains('layer_').sum()

        variables = [] if plot_type == 'Energy Demand' else df_plt[
            'parameter'].unique().tolist()

        # Get services for Technology Stocks (filtered by current sector)
        tech_services = []
        if plot_type == 'Technology Stocks':
            tech_df = df[df['plot'] == 'Technology Stocks']
            # Filter by the current sector (from the sector tab we're in)
            tech_df = tech_df[tech_df['sector'] == sector]
            tech_services = tech_df[tech_df['technology'].notna()]['short_path'].unique().tolist()
            tech_services = [s for s in tech_services if s is not None and str(s) != 'nan']

        by_service_widgets = []

        for i in range(max_depth):
            if i == 0:
                by_service_widgets.append(dmc.Select(
                    label=f'Layer {i}',
                    data=[{'label': service, 'value': service} for service in
                          df[f'layer_{i}'].unique().tolist()],
                    value=df[f'layer_{i}'].unique().tolist()[0],
                    id={
                        'type': f'cims-{lower_sector}-service-select',
                        'index': window_id,
                        'layer': i
                    },
                    style={'display': 'none'}
                ))

            elif i == 1:
                by_service_widgets.append(dmc.Select(
                    label=f'Layer {i}',
                    data=[{'label': service, 'value': service} for service in df[(
                            df.layer_0 == df['layer_0'].unique().tolist()[0])][
                        f'layer_{i}'].unique().tolist()],
                    value='',
                    id={
                        'type': f'cims-{lower_sector}-service-select',
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
                        'type': f'cims-{lower_sector}-service-select',
                        'index': window_id,
                        'layer': i
                    },
                    style={'display': 'none'}
                ))

        by_year_widgets = dmc.Select(
            label='Region',
            data=[{'label': region, 'value': region} for region in regions],
            value='CAN' if 'CAN' in regions else regions[0],
            id={
                'type': f'cims-{lower_sector}-region-select',
                'index': window_id
            },
            style={'display': 'block'}

        )

        by_region_widgets = dmc.Select(
            label='Year',
            data=[{'label': year, 'value': year} for year in years],
            value=years[0],
            id={
                'type': f'cims-{lower_sector}-year-select',
                'index': window_id
            },

            style={'display': 'block'}
        )

        pattern_toggle = dmc.Switch(
            label='Pattern',
            checked=True,
            id={
                'type': f'cims-{lower_sector}-pattern-switch',
                'index': window_id,
            },
            style={'display': 'block'}
        )

        text_toggle = dmc.Switch(
            label='Text',
            checked=False,
            id={
                'type': f'cims-{lower_sector}-text-switch',
                'index': window_id,
            },
            style={'display': 'block'} if plot_type in ('Energy Demand', 'Emissions') else {'display': 'none'}
        )

        variable_select = dmc.Select(
            label='Variable',
            data=[{'label': variable, 'value': variable} for variable in variables],
            value=variables[0] if variables else '',
            id={
                'type': f'cims-{lower_sector}-variable-select',
                'index': window_id
            },
            style={'display': 'block'} if len(variables) > 0 else {'display': 'none'}
        )

        widget_layout = html.Div([
            dmc.Select(
                label='Plot Options',
                data=[{'label': plot, 'value': plot} for plot in plot_types],
                value=plot_type,
                id={
                    'type': f'cims-{lower_sector}-plot-select',
                    'index': window_id
                },
            ),

            variable_select,

            # Keep the original switch hidden for Energy Demand, Emissions, and Technology Stocks
            dmc.Switch(
                label='By Service',
                checked=False,
                id={
                    'type': f'cims-{lower_sector}-rep_switch',
                    'index': window_id
                },
                style={'display': 'none'} if plot_type in ('Energy Demand', 'Emissions', 'Technology Stocks') else {'display': 'block'}
            ),

            # Add new dropdown for Energy Demand representation
            dmc.Select(
                label='Representation',
                data=[
                    {'label': 'By Service', 'value': 'By Service'},
                    {'label': 'By Fuel', 'value': 'By Fuel'}
                ],
                value='By Service',
                id={
                    'type': f'cims-{lower_sector}-energy-rep-select',
                    'index': window_id
                },
                style={'display': 'block'} if plot_type == 'Energy Demand' else {'display': 'none'}
            ),

            # Add new dropdown for Emissions representation
            dmc.Select(
                label='Representation',
                data=[
                    {'label': 'By Service', 'value': 'By Service'},
                    {'label': 'By Emission', 'value': 'By Emission'}
                ],
                value='By Service',
                id={
                    'type': f'cims-{lower_sector}-emissions-rep-select',
                    'index': window_id
                },
                style={'display': 'block'} if plot_type == 'Emissions' else {'display': 'none'}
            ),

            # Add new selector for Technology Stocks services (sector auto-determined from tab)
            dmc.MultiSelect(
                label='Services',
                data=[{'label': service, 'value': service} for service in tech_services],
                value=[tech_services[0]] if tech_services else [],
                id={
                    'type': f'cims-{lower_sector}-tech-service-select',
                    'index': window_id
                },
                style={'display': 'block'} if plot_type == 'Technology Stocks' else {'display': 'none'}
            ),

            dmc.Select(
                label='Representation Options',
                data=[{'label': plot, 'value': plot} for plot in ['Sankey', 'Trend Over Years']],
                value='Sankey',
                id={
                    'type': f'cims-{lower_sector}-rep-select',
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
                    'type': f'cims-{lower_sector}-scenario-multi-select',
                    'index': window_id,
                },
                style={'display': 'block'}
            ),
            dmc.Select(
                label='Scenario',
                data=[{'label': scenario, 'value': scenario} for scenario in scenarios],
                value=scenarios[0],
                id={
                    'type': f'cims-{lower_sector}-scenario-select',
                    'index': window_id,
                },
                style={'display': 'none'}
            ),
            *by_service_widgets,
            by_year_widgets,
            by_region_widgets,
            dmc.Button('Download Data', id={'type': f'cims-{lower_sector}-download-button', 'index': window_id},
                       variant='light',
                       # center the button
                       style={'display': 'flex', 'justify-content': 'center', 'margin-top': '4px'}),
            dcc.Download(id={'type': f'cims-{lower_sector}-download', 'index': window_id}),
        ])

        plot_layout = dcc.Graph(
            figure=render_plot(sector,
                df, plot_type, 'Sankey', False, years[0], regions[0], scenarios, scenarios[0], 
                variables[0] if variables else 'Energy Demand',
                pattern_active=True, text_active=False, service=df['layer_0'].unique().tolist()[0],
                tech_sector=sector,  # Use current sector tab name
                tech_service=[tech_services[0]] if tech_services else []
            ),
            id={
                'type': 'figure',
                'index': window_id,
                'profile': 'CIMS',
                'viz': sector
            },
            style={
                'width': '100%',
                'height': '100%'
            }
        )

        return widget_layout,plot_layout
    
    return plot