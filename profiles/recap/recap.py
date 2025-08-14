from collections import defaultdict
from random import randint

import dash_mantine_components as dmc
import pandas as pd
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile

# Import COPPER processing scripts for Total Cost and Emissions
from profiles.recap.processing_scripts import (
    cost_total as copper_cost_total_processing,
    emissions as copper_emissions_processing
)
from profiles.recap import utils

# Import COPPER visualization scripts for Total Cost and Emissions
from profiles.recap.visualization_scripts import (
    cost_total as copper_cost_total_viz,
    emissions as copper_emissions_viz
)

# Import COPPER callback scripts for Total Cost and Emissions
from profiles.recap.callbacks import (
    cost_total as copper_cost_total_callbacks,
    emissions as copper_emissions_callbacks,
    settings as settings_callbacks
)
from profiles.recap.callbacks import (requested_quantities as requested_quantities_callbacks,
                                            stock_lcc as stock_lcc_callbacks,
                                            ghg as ghg_callbacks,
                                            overview as overview_callbacks,
                                            settings as settings_callbacks,
                                            sectored as sectored_callbacks,
                                            inputs as inputs_callbacks,

                                            )
from profiles.recap.processing_scripts import (
    overview as overview_processing,
    sectored as sectored_processing,
    inputs as inputs_processing,
)
from profiles.recap.processing_scripts.utils import ghg as ghg_processing, stock_lcc as stock_lcc_processing, \
    requested_quantities as requested_quantities_processing
from profiles.recap.visualization_scripts import (
    requested_quantities as emissions_viz,
    stock_lcc as stock_lcc_viz,
    ghg as ghg_viz,
    
    overview as overview_viz,
    sectored as sectored_viz,
    inputs as inputs_viz,
)

# Define which models this recap_2 profile will work with
recap = ['COPPER', 'CIMS']


class RecapOutput(BaseProfile):
    display_name = 'recap'
    name = 'recap'
    db_name = 'recap'
    color = 'blue 8'
    description = (
        'recap profile combining key visualizations from COPPER and CIMS models. '
        'Provides essential cost and emissions analysis for quick overview and comparison.')

    plot_order = [
        'Total Cost',
        'Emissions',
        'Overview'
    ]
    
    viz_options = {
        'Total Cost':
            {
                'check': copper_cost_total_processing.check,
                'db_check': copper_cost_total_processing.check,
                'process': copper_cost_total_processing.process,
                'db_process': copper_cost_total_processing.process,
                'viz': copper_cost_total_viz.plot,
                'callback': copper_cost_total_callbacks.link,
                'description': 'Total costs of energy production and transmission from COPPER model.'
            },
        'Emissions':
            {
                'check': copper_emissions_processing.check,
                'db_check': copper_emissions_processing.check,
                'process': copper_emissions_processing.process,
                'db_process': copper_emissions_processing.process,
                'viz': copper_emissions_viz.plot,
                'callback': copper_emissions_callbacks.link,
                'description': 'Emissions analysis from COPPER model.'
            },
        'Overview':
            {
                'check': overview_processing.check,
                'db_check': overview_processing.check,
                'process': overview_processing.process,
                'db_process': overview_processing.process,
                'viz': overview_viz.plot,
                'callback': overview_callbacks.link,
                'description': 'Visualizations for a general overview of the data.'
            }
    }

    def __init__(self):
        super().__init__()
        # Load COPPER's technology and plot configurations
        try:
            self.technologies = yaml.load(
                open('./profiles/recap/technologies.yaml', 'r'), 
                Loader=yaml.FullLoader
            )
        except FileNotFoundError:
            # Fallback to basic technology configuration if file not found
            self.technologies = {}
            
        try:
            self.plots = yaml.load(
                open('./profiles/recap/plots.yaml', 'r'), 
                Loader=yaml.FullLoader
            )
        except FileNotFoundError:
            # Fallback to basic plot configuration if file not found
            self.plots = {}
            
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        # Link callbacks for the visualizations we're using
        # copper_cost_total_callbacks.link(app)
        # copper_emissions_callbacks.link(app)
        settings_callbacks.link(app)
        super().link(app)


    def process_data(self, data_collection):
        processed_data = defaultdict(list)

        for profile, viz_option, df in data_collection:
            print(profile, viz_option)
            if (profile in recap and viz_option in self.viz_options):
                data = df.copy()
                data['version'] = data['scenario'].apply(lambda x: x.split('|')[-1] if '|' in x else 'v0')
                data['scenario'] = profile + '|' + data['scenario']
                if not viz_option in ['Overview', 'Output Stats', 'Transmission Capacity', 'Transmission Flow']:
                    unique_regions = set(data['region'].unique())

                    # Check if both 'A' and 'B' are in the unique values
                    if {'AB', 'QC'}.issubset(unique_regions):
                        ab_qc = data[data.region.isin(['AB', 'QC'])]
                        # drop nan columns
                        ab_qc = ab_qc.dropna(axis=1, how='all')
                        columns = ab_qc.columns
                        columns = columns.drop('region')
                        columns = columns.drop('value').tolist()

                        # Perform groupby operation
                        ab_qc = ab_qc.groupby(columns).sum().reset_index()
                        ab_qc['region'] = 'AB+QC'
                        data = pd.concat([data, ab_qc])

                if 'time' in data.columns:
                    data = data[data['time'].isin(
                        [2021, 2025, 2030, 2035, 2040, 2045, 2050, '2021', '2025', '2030', '2035', '2040', '2045',
                         '2050'])]

                    # make time into int
                    data['time'] = pd.to_numeric(data['time'])



                elif 'period' in data.columns:
                    data = data[data['period'].isin([2021, 2025, 2030, 2035, 2040, 2045, 2050])]
                processed_data[viz_option].append(data)

        output_stats = []

        # if 'Overview' in processed_data:
        #     for p_data in processed_data['Overview']:
        #         for c in p_data.variable.unique():
        #             if c in self.viz_options:
        #                 data = p_data[p_data.variable == c]
        #                 # if net new capacity make cumsum of value based on time column
        #                 if 'Net New Capacity' in c or 'New Capacity' in c:
        #                     data['value'] = data.groupby(['region', 'scenario'])['value'].cumsum()
        #                 output_stats.append(data)

        results = [(self.display_name, viz_option, pd.concat(data)) for viz_option, data in processed_data.items()]

        dfs = []
        for _, viz_option, df in results:
            if viz_option != 'Overview':
                data = df.copy()
                data['variable'] = viz_option + '|' + data['variable']
                dfs.append(data)
        if len(dfs) > 0:
            full_df = pd.concat(dfs)

            results.extend([(self.display_name, 'Comparison', full_df), (self.display_name, 'Comparison Matrix', full_df)])

            return results

        return None
    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='recap-settings-upload-yaml',
                    children=html.Div([
                        'Drag and Drop or ',
                        html.A('Select YAML File')
                    ]),
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                    },
                    multiple=False
                ),

                html.Div(id='recap-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='recap-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='recap-plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='recap-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='recap-plot-settings-panel', value='plot',
                                  children=self.render_plot_settings()),
                ], value='tech')
            ]
        )

        return layout

    def render_technology_settings(self):
        techs = list(utils.groups.keys())
        
        # Safety check: if no technologies are available, provide a default empty state
        if not techs:
            layout = html.Div([
                dmc.Alert(
                    "No technology configurations found. Please load technology settings from a YAML file.",
                    title="No Technologies Available",
                    color="yellow",
                    style={'margin': '10px'}
                ),
                html.Div(
                    "Technology settings will appear here once configurations are loaded.",
                    style={'padding': '20px', 'textAlign': 'center', 'color': 'gray'}
                )
            ])
            return layout
        
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='recap-technology-select',
                    data=[{'label': tech, 'value': tech} for tech in techs],
                    value=techs[0],
                ),
                style={
                    'position': 'relative',
                    'zIndex': 999,
                    'background': 'rgba(255, 255, 255, 0.4)',
                    'backdropFilter': 'blur(20px)',
                    'borderRadius': '10px',
                    'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
                    'padding': '1rem',
                    'marginTop': '1rem',
                }
            ),
            html.Div(utils.tech_edit(techs[0]),
                    id='recap-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys()) if hasattr(utils, 'plot_settings') and utils.plot_settings else []
        
        # Safety check: if no plot settings are available, provide a default empty state
        if not plots:
            layout = html.Div([
                dmc.Alert(
                    "No plot configurations found. Please load plot settings from a YAML file.",
                    title="No Plot Settings Available", 
                    color="yellow",
                    style={'margin': '10px'}
                ),
                html.Div(
                    "Plot settings will appear here once configurations are loaded.",
                    style={'padding': '20px', 'textAlign': 'center', 'color': 'gray'}
                )
            ])
            return layout
            
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='recap-plot-select',
                    data=[{'label': plot, 'value': plot} for plot in plots],
                    value=plots[0]
                ),
                style={
                    'position': 'relative',
                    'zIndex': 999,
                    'background': 'rgba(255, 255, 255, 0.4)',
                    'backdropFilter': 'blur(20px)',
                    'borderRadius': '10px',
                    'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
                    'padding': '1rem',
                    'marginTop': '1rem',
                }
            ),
            html.Div(utils.plot_edit(plots[0]),
                    id='recap-plot-settings-output'),
        ])

        return layout

    def update_utils(self):
        """
        Update utility configurations based on loaded technology settings.
        Simplified version of the recap approach.
        """
        colors = {}
        group_colors = {}
        names = {}
        groups = {}
        
        # Process technology configurations if available
        for tech in self.technologies.keys() if self.technologies else []:
            colors[tech] = self.technologies[tech].get('color', f'#{randint(0, 0xFFFFFF):06X}')
            names[tech] = self.technologies[tech].get('name', tech)
            groups[tech] = self.technologies[tech].get('group', tech)
            group_colors[self.technologies[tech].get('group', tech)] = \
                self.technologies[tech].get('group_color', f'#{randint(0, 0xFFFFFF):06X}')

        # Store in utils module (ensure utils has these attributes)
        utils.colors = colors
        utils.group_colors = group_colors
        utils.names = names
        utils.groups = groups
        
        # Initialize plot_settings if not already present
        if not hasattr(utils, 'plot_settings'):
            utils.plot_settings = {}
        utils.plot_settings = self.plots if self.plots else {}

    def process_data_fixed(self, data_collection):
        """Fixed version of process_data method"""
        processed_data = defaultdict(list)

        for profile, viz_option, df in data_collection:
            print(profile, viz_option)
            if (profile in recap and viz_option not in ['Comparison',
                                                    'Comparison Matrix'] and viz_option in self.viz_options):

                data = df.copy()
                data['version'] = data['scenario'].apply(lambda x: x.split('|')[-1] if '|' in x else 'v0')
                data['scenario'] = profile + '|' + data['scenario']
                if not viz_option in ['Overview', 'Output Stats', 'Transmission Capacity', 'Transmission Flow']:
                    unique_regions = set(data['region'].unique())

                    # Check if both 'AB' and 'QC' are in the unique values
                    if {'AB', 'QC'}.issubset(unique_regions):
                        ab_qc = data[data.region.isin(['AB', 'QC'])]
                        # drop nan columns
                        ab_qc = ab_qc.dropna(axis=1, how='all')
                        columns = ab_qc.columns
                        columns = columns.drop('region')
                        columns = columns.drop('value').tolist()

                        # Perform groupby operation
                        ab_qc = ab_qc.groupby(columns).sum().reset_index()
                        ab_qc['region'] = 'AB+QC'
                        data = pd.concat([data, ab_qc])

                if 'time' in data.columns:
                    data = data[data['time'].isin(
                        [2021, 2025, 2030, 2035, 2040, 2045, 2050, '2021', '2025', '2030', '2035', '2040', '2045',
                        '2050'])]

                    # make time into int
                    data['time'] = pd.to_numeric(data['time'])

                elif 'period' in data.columns:
                    data = data[data['period'].isin([2021, 2025, 2030, 2035, 2040, 2045, 2050])]
                processed_data[viz_option].append(data)

        output_stats = []

        if 'Overview' in processed_data:
            for p_data in processed_data['Overview']:
                for c in p_data.variable.unique():
                    if c in self.viz_options:
                        data = p_data[p_data.variable == c]
                        # if net new capacity make cumsum of value based on time column
                        if 'Net New Capacity' in c or 'New Capacity' in c:
                            data['value'] = data.groupby(['region', 'scenario'])['value'].cumsum()
                        output_stats.append(data)

        min_days = []
        max_days = []
        for model, plot_type, df in data_collection:
            if model in recap:  # Fixed: changed from power_system_models to recap
                if plot_type == 'Dispatch':
                    dispatch_data = df[(df.region == 'CAN')].copy()
                    dispatch_data['time'] = pd.to_datetime(dispatch_data['time'])
                    dispatch_data['scenario'] = model + '|' + dispatch_data['scenario']
                    if 'version' in dispatch_data.columns:
                        dispatch_data['scenario'] = dispatch_data['scenario'] + '|' + dispatch_data['version']
                        dispatch_data = dispatch_data.drop(columns=['version'])

                    # make date day-month-year
                    dispatch_data['time'] = dispatch_data['time'].dt.strftime('%d-%m-%Y')
                    columns = ['scenario', 'time', 'variable', 'region', 'period']
                    dispatch_data = dispatch_data.groupby(columns).sum().reset_index()

                    for year in dispatch_data['period'].unique():
                        year_dispatch_data = dispatch_data[dispatch_data['period'] == year]
                        for scenario in year_dispatch_data['scenario'].unique():
                            scen_dispatch_data = year_dispatch_data[year_dispatch_data['scenario'] == scenario]
                            # find date where value is min and max
                            min_day = scen_dispatch_data[scen_dispatch_data['value'] == scen_dispatch_data['value'].min()]
                            min_day['variable'] = 'Min Dispatch'
                            min_day['date'] = min_day['time']
                            min_day['time'] = year

                            max_day = scen_dispatch_data[scen_dispatch_data['value'] == scen_dispatch_data['value'].max()]
                            max_day['variable'] = 'Max Dispatch'
                            max_day['date'] = max_day['time']
                            max_day['time'] = year

                            min_days.append(min_day)
                            max_days.append(max_day)

        output_stats += min_days + max_days

        if len(output_stats) > 0:
            processed_data['Output Stats'] = output_stats

        results = [(self.display_name, viz_option, pd.concat(data)) for viz_option, data in processed_data.items()]

        dfs = []
        for _, viz_option, df in results:
            if viz_option != 'Overview':
                data = df.copy()
                data['variable'] = viz_option + '|' + data['variable']
                dfs.append(data)
        if len(dfs) > 0:
            full_df = pd.concat(dfs)

            results.extend([(self.display_name, 'Comparison', full_df), (self.display_name, 'Comparison Matrix', full_df)])

            return results

        return None