from random import randint

import dash_mantine_components as dmc
import yaml
import pandas as pd
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.copper_output import utils
from profiles.copper_output.callbacks import (emissions as emissions_callbacks,
                                              generation_capacity as generation_capacity_callbacks,
                                              net_new_capacity as net_new_capacity_callbacks,
                                              new_capacity as new_capacity_callbacks,
                                              qualifying_capacity as qualifying_capacity_callbacks,
                                              generation_supply as generation_supply_callbacks,
                                              transmission_capacity as transmission_capacity_callbacks,
                                              transmission_flow as transmission_flow_callbacks,
                                              cost_total as cost_total_callbacks,
                                              cost_fom as cost_fom_callbacks,
                                              cost_vom as cost_vom_callbacks,
                                              cost_gencap as cost_gencap_callbacks,
                                              settings as settings_callbacks,
                                              dispatch as dispatch_callbacks,
                                              merra as merra_callbacks,
                                              overview as overview_callbacks,
                                              output_stats as output_stats_callbacks,
                                              inputs as inputs_callbacks
                                              )
from profiles.copper_output.processing_scripts import (
    emissions as emissions_processing,
    generation_capacity as generation_capacity_processing,
    net_new_capacity as net_new_capacity_processing,
    new_capacity as new_capacity_processing,
    qualifying_capacity as qualifying_capacity_processing,
    generation_supply as generation_supply_processing,
    transmission_capacity_plotly as transmission_capacity_processing,
    transmission_flow_plotly as transmission_flow_processing,
    cost_total as cost_total_processing,
    cost_fom as cost_fom_processing,
    cost_vom as cost_vom_processing,
    cost_gencap as cost_gencap_processing,
    dispatch as dispatch_processing,
    merra as merra_processing,
    overview as overview_processing,
    inputs as inputs_processing
)
from profiles.copper_output.visualization_scripts import (
    emissions as emissions_viz,
    generation_capacity as generation_capacity_viz,
    net_new_capacity as net_new_capacity_viz,
    new_capacity as new_capacity_viz,
    qualifying_capacity as qualifying_capacity_viz,
    generation_supply as generation_supply_viz,
    transmission_capacity as transmission_capacity_viz,
    transmission_flow as transmission_flow_viz,
    cost_total as cost_total_viz,
    cost_fom as cost_fom_viz,
    cost_vom as cost_vom_viz,
    cost_gencap as cost_gencap_viz,
    dispatch as dispatch_viz,
    merra as merra_viz,
    overview as overview_viz,
    output_stats as output_stats_viz,
    inputs as inputs_viz
)


def data_processing_task(profile_name, viz, data, processing_func):
    data_out = processing_func(data)
    return profile_name, viz, data_out


class CopperOutput(BaseProfile):
    display_name = 'COPPER'
    name = 'copper'
    db_name = 'copper'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Inputs',
        'Output Stats',
        'Overview',
        'Emissions',
        'Capacity',
        'VRE Capacity',
        'Net New Capacity',
        'New Capacity',
        'Qualifying Capacity',
        'Supply',
        'Transmission Capacity',
        'Transmission Flow',
        'Total Cost',
        'Capacity Cost',
        'FOM Cost',
        'VOM Cost',
        'Dispatch',
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
        'Emissions':
            {
                'check': emissions_processing.check,
                'db_check': emissions_processing.check,
                'process': emissions_processing.process,
                'db_process': emissions_processing.process,
                'viz': emissions_viz.plot,
                'callback': emissions_callbacks.link,
                'description': 'Emissions that are produced by the generation mix in the model.'
            },
        'Capacity':
            {
                'check': generation_capacity_processing.check,
                'db_check': generation_capacity_processing.check,
                'process': generation_capacity_processing.process,
                'db_process': generation_capacity_processing.process,
                'viz': generation_capacity_viz.plot,
                'callback': generation_capacity_callbacks.link,
                'description': 'Capacity of each technology in the model.'
            },
        'VRE Capacity':
            {
                'check': merra_processing.check,
                'db_check': merra_processing.check,
                'process': merra_processing.process,
                'db_process': merra_processing.process,
                'viz': merra_viz.plot,
                'callback': merra_callbacks.link,
                'description': 'Capacity of each VRE technology grouped to their MERRA cell in the model.'
            },

        'Net New Capacity':
            {
                'check': net_new_capacity_processing.check,
                'db_check': net_new_capacity_processing.check,
                'process': net_new_capacity_processing.process,
                'db_process': net_new_capacity_processing.process,
                'viz': net_new_capacity_viz.plot,
                'callback': net_new_capacity_callbacks.link,
                'description': 'Net new capacity of each technology in the model.'
            },
        'New Capacity':
            {
                'check': new_capacity_processing.check,
                'db_check': new_capacity_processing.check,
                'process': new_capacity_processing.process,
                'db_process': new_capacity_processing.process,
                'viz': new_capacity_viz.plot,
                'callback': new_capacity_callbacks.link,
                'description': 'New capacity that is built of each technology in the model (does not include retired technologies).'
            },
        'Qualifying Capacity':
            {
                'check': qualifying_capacity_processing.check,
                'db_check': qualifying_capacity_processing.check,
                'process': qualifying_capacity_processing.process,
                'db_process': qualifying_capacity_processing.process,
                'viz': qualifying_capacity_viz.plot,
                'callback': qualifying_capacity_callbacks.link,
                'description': 'Capacity that qualifies for the capacity market.'
            },
        'Supply':
            {
                'check': generation_supply_processing.check,
                'db_check': generation_supply_processing.check,
                'process': generation_supply_processing.process,
                'db_process': generation_supply_processing.process,
                'viz': generation_supply_viz.plot,
                'callback': generation_supply_callbacks.link,
                'description': 'Generation supply of each technology in the model.'
            },
        'Transmission Capacity':
            {
                'check': transmission_capacity_processing.check,
                'db_check': transmission_capacity_processing.check,
                'process': transmission_capacity_processing.process,
                'db_process': transmission_capacity_processing.process,
                'viz': transmission_capacity_viz.plot,
                'callback': transmission_capacity_callbacks.link,
                'description': 'Transmission capacity between regions in the model.'
            },
        'Transmission Flow':
            {
                'check': transmission_flow_processing.check,
                'db_check': transmission_flow_processing.check,
                'process': transmission_flow_processing.process,
                'db_process': transmission_flow_processing.process,
                'viz': transmission_flow_viz.plot,
                'callback': transmission_flow_callbacks.link,
                'description': 'Transmission flow between regions in the model.'
            },
        'Total Cost':
            {
                'check': cost_total_processing.check,
                'db_check': cost_total_processing.check,
                'process': cost_total_processing.process,
                'db_process': cost_total_processing.process,
                'viz': cost_total_viz.plot,
                'callback': cost_total_callbacks.link,
                'description': 'Total costs of energy production and transmission in the model.'

            },
        'Capacity Cost':
            {
                'check': cost_gencap_processing.check,
                'db_check': cost_gencap_processing.check,
                'process': cost_gencap_processing.process,
                'db_process': cost_gencap_processing.process,
                'viz': cost_gencap_viz.plot,
                'callback': cost_gencap_callbacks.link,
                'description': 'Capital costs of energy production and transmission in the model.'
            },
        'FOM Cost':
            {
                'check': cost_fom_processing.check,
                'db_check': cost_fom_processing.check,
                'process': cost_fom_processing.process,
                'db_process': cost_fom_processing.process,
                'viz': cost_fom_viz.plot,
                'callback': cost_fom_callbacks.link,
                'description': 'Fixed operating and maintenance costs of energy production and transmission in the model.'
            },
        'VOM Cost':
            {
                'check': cost_vom_processing.check,
                'db_check': cost_vom_processing.check,
                'process': cost_vom_processing.process,
                'db_process': cost_vom_processing.process,
                'viz': cost_vom_viz.plot,
                'callback': cost_vom_callbacks.link,
                'description': 'Variable operating and maintenance costs of energy production and transmission in the model.'

            },
        'Dispatch':
            {
                'check': dispatch_processing.check,
                'db_check': dispatch_processing.check,
                'process': dispatch_processing.process,
                'db_process': dispatch_processing.process,
                'viz': dispatch_viz.plot,
                'callback': dispatch_callbacks.link,
                'description': 'Dispatch of each technology in the model.'
            },
        'Output Stats':
            {
                'check': overview_processing.check,
                'db_check': overview_processing.check,
                'process': overview_processing.process,
                'db_process': overview_processing.process,
                'viz': output_stats_viz.plot,
                'callback': output_stats_callbacks.link,
                'description': 'Output statistics of the model.'
            },
        'Inputs':
            {
                'check': inputs_processing.check,
                'db_check': inputs_processing.check,
                'process': inputs_processing.process,
                'db_process': inputs_processing.process,
                'viz': inputs_viz.plot,
                'callback': inputs_callbacks.link,
                'description': 'Input data for the model.'
            }
    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/copper_output/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/copper_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
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

            # Aggregate data for Alberta and Quebec
            full_df = self._aggregate_ab_qc(full_df)

            # Append overview data to processed data
            overview_df = full_df[full_df['scenario'].isin(overview_scenarios)]
            processed_data.append(
                (self.display_name, 'Overview', overview_df[['scenario', 'variable', 'time', 'value', 'region']]))

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
        columns = ['scenario', 'time', 'variable', 'region', 'period']
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
        ab_qc = ab_qc.groupby(['scenario', 'variable', 'time']).sum(numeric_only=True).reset_index()
        ab_qc['region'] = 'AB+QC'

        # Concatenate the AB+QC data with the full dataframe
        full_df = pd.concat([full_df, ab_qc], ignore_index=True)
        full_df = full_df[full_df['region'].isin(['CAN', 'AB+QC'])]
        return full_df.groupby(['scenario', 'variable', 'time', 'region']).sum(numeric_only=True).reset_index()

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
        super().link(app)

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='copper-settings-upload-yaml',
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

                html.Div(id='copper-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='copper-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='copper-plot-settings-tab', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='copper-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='copper-plot-settings', value='plot',
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
                    id='copper-technology-select',
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
                     id='copper-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='copper-plot-select',
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
                     id='copper-plot-settings-output'),
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
