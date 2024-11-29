from random import randint

import dash_mantine_components as dmc
import yaml
import pandas as pd
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.macromodel import utils
from profiles.macromodel.callbacks import (
                                              overview as overview_callbacks,
                                settings as settings_callbacks,
                                              non_sector as non_sector_callbacks,

                                              )
from profiles.macromodel.processing_scripts import (
    banks as banks_processing,
    central_Bank as central_Bank_processing,
    central_government as central_government_processing,
    credit_market as credit_market_processing,
    government_entities as government_entities_processing,
    overview as overview_processing,
)
from profiles.macromodel.visualization_scripts import (
    banks as banks_viz,
    central_Bank as central_Bank_viz,
    central_government as central_government_viz,
    credit_market as credit_market_viz,
    government_entities as government_entities_viz,
    overview as overview_viz,
)


def data_processing_task(profile_name, viz, data, processing_func):
    data_out = processing_func(data)
    return profile_name, viz, data_out


class Macromodel(BaseProfile):
    display_name = 'Macromodel'
    name = 'macromodel'
    db_name = 'macromodel'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Overview',
        'Banks',
        'Central Bank',
        'Central Government',
        'Credit Market',
        'Government Entities',
    ]
    viz_options = {
        'Overview':
            {
                'check': overview_processing.check,
                'db_check': overview_processing.check,
                'process': overview_processing.process,
                'db_process': overview_processing.process,
                'viz': overview_viz.plot,
                'callback': overview_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },
        'Banks':
            {
                'check': banks_processing.check,
                'db_check': banks_processing.check,
                'process': banks_processing.process,
                'db_process': banks_processing.process,
                'viz': banks_viz.plot,
                'callback': non_sector_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },
        'Central Bank':
            {
                'check': central_Bank_processing.check,
                'db_check': central_Bank_processing.check,
                'process': central_Bank_processing.process,
                'db_process': central_Bank_processing.process,
                'viz': central_Bank_viz.plot,
                'callback': non_sector_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },
        'Central Government':
            {
                'check': central_government_processing.check,
                'db_check': central_government_processing.check,
                'process': central_government_processing.process,
                'db_process': central_government_processing.process,
                'viz': central_government_viz.plot,
                'callback': non_sector_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },
        'Credit Market':
            {
                'check': credit_market_processing.check,
                'db_check': credit_market_processing.check,
                'process': credit_market_processing.process,
                'db_process': credit_market_processing.process,
                'viz': credit_market_viz.plot,
                'callback': non_sector_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },
        'Government Entities':
            {
                'check': government_entities_processing.check,
                'db_check': government_entities_processing.check,
                'process': government_entities_processing.process,
                'db_process': government_entities_processing.process,
                'viz': government_entities_viz.plot,
                'callback': non_sector_callbacks.link,
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
            },

    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/macromodel/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/macromodel/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def process_data(self, data_collection):
        """
        Process the data collection to generate overview and output statistics.

        Parameters:
            data_collection (dict): A dictionary containing visualization options and their corresponding data.

        Returns:
            list: A list of processed data tuples containing profile name, visualization option, and processed data.
        """
        # Flags to determine if overview or output statistics are requested
        wants_overview = 'Overview' in data_collection
        wants_output_stats = 'Output Stats' in data_collection

        # Prepare arguments for processing, excluding overview and output stats
        processing_args = [
            (self.display_name, viz_option, data, self.viz_options[viz_option]['process'])
            for viz_option, data in data_collection.items()
            if viz_option not in ['Overview', 'Output Stats']
        ]

        # Process the data using the defined processing function
        processed_data = [data_processing_task(*arg) for arg in processing_args]
        output_stats_data = []

        # Process overview and output statistics if requested
        if wants_overview or wants_output_stats:
            overview_scenarios = set(data_collection.get('Overview', {}).keys())
            output_stats_scenarios = set(data_collection.get('Output Stats', {}).keys())

            dfs = []
            for _, viz_option, data in processed_data:
                if viz_option in {'Dispatch', 'Transmission Flow', 'Transmission Capacity', 'Inputs'}:
                    if wants_output_stats and viz_option == 'Dispatch':
                        # Process dispatch data for output statistics
                        dispatch_data = self._prepare_dispatch_data(data)

                        # Collect min and max dispatch values for each year and scenario
                        output_stats_data.extend(self._collect_dispatch_min_max(dispatch_data))

                    continue

                # Filter out imports and exports from the data
                filtered_data = self._filter_import_export(data, viz_option)
                dfs.append(filtered_data)

            # Combine all dataframes into a single dataframe
            full_df = pd.concat(dfs, ignore_index=True)

            # only keep CAN
            full_df = full_df[full_df['region'] == 'CAN']

            # Append overview data to processed data
            overview_df = full_df[full_df['scenario'].isin(overview_scenarios)]
            processed_data.append(
                (self.display_name, 'Overview', overview_df[['scenario', 'variable', 'time', 'value', 'region', 'unit']]))

            # If output statistics are requested, append them as well
            if wants_output_stats:
                if output_stats_data:
                    stats_df = pd.concat(output_stats_data + [full_df], ignore_index=True)
                else:
                    stats_df = full_df
                stats_df['time'] = stats_df['time'].astype(int)
                output_stats_df = stats_df[stats_df['scenario'].isin(output_stats_scenarios)]
                processed_data.append((self.display_name, 'Output Stats', output_stats_df))

        return processed_data

    def _prepare_dispatch_data(self, data):
        """Prepare dispatch data for output statistics."""
        dispatch_data = data[data.region == 'CAN'].copy()
        dispatch_data['time'] = pd.to_datetime(dispatch_data['time']).dt.strftime('%d-%m-%Y')
        columns = ['scenario', 'time', 'variable', 'region', 'period', 'unit']
        return dispatch_data.groupby(columns).sum().reset_index()

    def _collect_dispatch_min_max(self, dispatch_data):
        """Collect min and max dispatch values for each year and scenario."""
        output_stats = []
        for year in dispatch_data['period'].unique():
            year_dispatch_data = dispatch_data[dispatch_data['period'] == year]
            for scenario in year_dispatch_data['scenario'].unique():
                scen_dispatch_data = year_dispatch_data[year_dispatch_data['scenario'] == scenario]
                min_day = scen_dispatch_data.loc[scen_dispatch_data['value'].idxmin()]
                max_day = scen_dispatch_data.loc[scen_dispatch_data['value'].idxmax()]

                # Append min and max dispatch data
                output_stats.append(self._create_dispatch_stat(min_day, 'Min Dispatch', year))
                output_stats.append(self._create_dispatch_stat(max_day, 'Max Dispatch', year))
        return output_stats

    def _filter_import_export(self, data, viz_option):
        """Filter out imports and exports from the data."""
        df = data[~data.variable.str.contains('Import|Export')]
        df['variable'] = viz_option
        return df

    def _aggregate_ab_qc(self, full_df):
        """Aggregate data for Alberta and Quebec."""
        ab_qc = full_df[full_df['region'].isin(['AB', 'QC'])].copy()
        ab_qc = ab_qc.groupby(['scenario', 'variable', 'time', 'unit']).sum(numeric_only=True).reset_index()
        ab_qc['region'] = 'AB+QC'

        # Concatenate the AB+QC data with the full dataframe
        full_df = pd.concat([full_df, ab_qc], ignore_index=True)
        full_df = full_df[full_df['region'].isin(['CAN', 'unit'])]
        return full_df.groupby(['scenario', 'variable', 'time', 'region', 'unit']).sum(numeric_only=True).reset_index()

    def _create_dispatch_stat(self, day_data, variable_name, year):
        """Helper function to create a dispatch statistic entry."""
        day_data['variable'] = variable_name
        day_data['date'] = day_data['time']
        day_data['time'] = year

        # Transpose the day_data Series and reset the index to convert the index into a column
        day_data = day_data.reset_index().T
        day_data.columns = day_data.iloc[0]
        day_data = day_data.iloc[1:]
        return day_data

    def link(self, app):
        settings_callbacks.link(app)
        non_sector_callbacks.link(app)
        overview_callbacks.link(app)

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='macromodel-settings-upload-yaml',
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

                html.Div(id='macromodel-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='macromodel-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='macromodel-plot-settings-tab', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='macromodel-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='macromodel-plot-settings', value='plot',
                                  children=self.render_plot_settings()),
                ], value='tech')
            ]
        )

        return layout

    def render_technology_settings(self):
        techs = list(utils.groups.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='macromodel-technology-select',
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
                     id='macromodel-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='macromodel-plot-select',
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
                     id='macromodel-plot-settings-output'),
        ])

        return layout

    def update_utils(self):
        colors = {}
        group_colors = {}
        names = {}
        groups = {}
        for tech in self.technologies.keys():
            colors[tech] = self.technologies[tech]['color'] if 'color' in self.technologies[
                tech] else '#%06X' % randint(0, 0xFFFFFF)
            names[tech] = self.technologies[tech]['name'] if 'name' in self.technologies[tech] else tech
            groups[tech] = self.technologies[tech]['group'] if 'group' in self.technologies[tech] else tech
            group_colors[self.technologies[tech].get('group', tech)] = self.technologies[tech][
                'group_color'] if 'group_color' in \
                                  self.technologies[
                                      tech] else '#%06X' % randint(0, 0xFFFFFF)

        utils.colors = colors
        utils.group_colors = group_colors
        utils.names = names
        utils.groups = groups

        utils.plot_settings = self.plots
