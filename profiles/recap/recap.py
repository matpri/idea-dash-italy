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

# Import COPPER visualization scripts for Total Cost and Emissions
from profiles.recap.visualization_scripts import (
    cost_total as copper_cost_total_viz,
    emissions as copper_emissions_viz
)

# Import COPPER callback scripts for Total Cost and Emissions
from profiles.recap.callbacks import (
    cost_total as copper_cost_total_callbacks,
    emissions as copper_emissions_callbacks
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
        'Emissions'
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
        copper_cost_total_callbacks.link(app)
        copper_emissions_callbacks.link(app)
        super().link(app)

    def process_data(self, data_collection):
        processed_data = defaultdict(list)

        for profile, viz_option, df in data_collection:
            print(f"Processing: {profile}, {viz_option}")
            
            # Only process data from our target models and for our specific visualizations
            if (profile in recap and viz_option in self.viz_options):
                data = df.copy()
                
                # Add version information if available
                data['version'] = data['scenario'].apply(
                    lambda x: x.split('|')[-1] if '|' in x else 'v0'
                )
                
                # Prefix scenario names with model name for identification
                data['scenario'] = profile + '|' + data['scenario']
                
                # Time filtering for relevant years
                if 'time' in data.columns:
                    data = data[data['time'].isin(
                        [2021, 2025, 2030, 2035, 2040, 2045, 2050, 
                         '2021', '2025', '2030', '2035', '2040', '2045', '2050']
                    )]
                    # Convert time to numeric
                    data['time'] = pd.to_numeric(data['time'])
                    
                elif 'period' in data.columns:
                    data = data[data['period'].isin([2021, 2025, 2030, 2035, 2040, 2045, 2050])]
                
                processed_data[viz_option].append(data)

        # Create results list
        results = []
        for viz_option, data_list in processed_data.items():
            if data_list:  # Only process if we have data
                combined_data = pd.concat(data_list, ignore_index=True)
                results.append((self.display_name, viz_option, combined_data))

        return results if results else None

    def render_settings(self):
        """
        Render settings panel for the recap profile.
        This is a simplified version compared to the recap profile.
        """
        layout = html.Div([
            dmc.Alert(
                "recap Profile Settings",
                title="Configuration",
                color="blue",
                style={'margin': '10px'}
            ),
            html.Div([
                dmc.Text("This profile combines visualizations from COPPER and CIMS models."),
                dmc.Text("Currently configured for:"),
                html.Ul([
                    html.Li("Total Cost analysis from COPPER"),
                    html.Li("Emissions analysis from COPPER"),
                ]),
                dmc.Text("Additional CIMS visualizations can be added as needed.", 
                        style={'fontStyle': 'italic', 'marginTop': '10px'})
            ], style={'padding': '20px'})
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

        # Store in a way that can be accessed by visualization scripts
        # Note: You may need to create a utils module for the recap profile
        # or modify this based on how COPPER's utils are structured
        self.colors = colors
        self.group_colors = group_colors
        self.names = names
        self.groups = groups
        self.plot_settings = self.plots