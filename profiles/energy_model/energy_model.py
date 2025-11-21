from collections import defaultdict
from random import randint

import dash_mantine_components as dmc
import pandas as pd
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.energy_model import utils
from profiles.energy_model.callbacks import (
    overview as overview_callbacks,
    output_stats as output_stats_callbacks,
    matrix as matrix_callbacks,
    emissions as emissions_callbacks,
    generation_capacity as generation_capacity_callbacks,
    net_new_capacity as net_new_capacity_callbacks,
    new_capacity as new_capacity_callbacks,
    qualifying_capacity as qualifying_capacity_callbacks,
    generation_supply as generation_supply_callbacks,
    cost_vom as cost_vom_callbacks,
    cost_fom as cost_fom_callbacks,
    cost_gencap as cost_gencap_callbacks,
    cost_total as cost_total_callbacks,
    transmission_capacity as transmission_capacity_callbacks,
    transmission_flow as transmission_flow_callbacks,
    comparison as comparison_callbacks,
    settings as settings_callbacks

)
from profiles.energy_model.processing_scripts import (
    overview as overview_processing,
    output_stats as output_stats_processing,
    matrix as matrix_processing,
    emissions as emissions_processing,
    generation_capacity as generation_capacity_processing,
    net_new_capacity as net_new_capacity_processing,
    new_capacity as new_capacity_processing,
    qualifying_capacity as qualifying_capacity_processing,
    generation_supply as generation_supply_processing,
    cost_vom as cost_vom_processing,
    cost_fom as cost_fom_processing,
    cost_gencap as cost_gencap_processing,
    cost_total as cost_total_processing,
    transmission_capacity as transmission_capacity_processing,
    transmission_flow as transmission_flow_processing
)
from profiles.energy_model.visualization_scripts import (
    overview as overview_viz,
    output_stats as output_stats_viz,
    matrix as matrix_viz,
    emissions as emissions_viz,
    generation_capacity as generation_capacity_viz,
    net_new_capacity as net_new_capacity_viz,
    new_capacity as new_capacity_viz,
    qualifying_capacity as qualifying_capacity_viz,
    generation_supply as generation_supply_viz,
    cost_vom as cost_vom_viz,
    cost_fom as cost_fom_viz,
    cost_gencap as cost_gencap_viz,
    cost_total as cost_total_viz,
    transmission_capacity as transmission_capacity_viz,
    transmission_flow as transmission_flow_viz,
    comparison as comparison_viz,
)

power_system_models = ['COPPER', 'ECCC-NextGrid', 'NATEM Canada', 'PITHOS',
                       'NRCan-PyPsa', 'PyPSA_CAN', 'Sutubra-TEMOA', 'Canada Energy Futures', 'PaCES']

technologies_paths = [
    './profiles/copper_output/technologies.yaml'
    './profiles/natem_output/technologies.yaml'
    './profiles/nextgrid_output/technologies.yaml'
    './profiles/pypsa_can_output/technologies.yaml'
    './profiles/pypsa_output/technologies.yaml'
    './profiles/pithos_output/technologies.yaml'
    './profiles/temoa_output/technologies.yaml'
]


class energy_modelsOutput(BaseProfile):
    display_name = 'Power System Models'
    name = 'Power System Models'
    db_name = 'energy_models'
    color = 'yellow 8'
    description = (
        'In this tab you will find the collection of all models that can be considered Power System Models. '
        'It represents each models output as its own scenario which allows for easy inter model comparisons')

    plot_order = [
        'Overview',
        'Output Stats',
        'Comparison',
        'Comparison Matrix',
        'Emissions',
        'Capacity',
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
        'Dispatch'
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
                'description': 'Line plots for a variety of variables, overviewing main results across scenarios & models.'
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

        'Comparison':
            {
                'check': matrix_processing.check,
                'db_check': matrix_processing.check,
                'process': matrix_processing.process,
                'db_process': matrix_processing.process,
                'viz': comparison_viz.plot,
                'callback': comparison_callbacks.link
            },
        'Comparison Matrix':
            {
                'check': matrix_processing.check,
                'db_check': matrix_processing.check,
                'process': matrix_processing.process,
                'db_process': matrix_processing.process,
                'viz': matrix_viz.plot,
                'callback': matrix_callbacks.link
            },
        'Emissions':
            {
                'check': emissions_processing.check,
                'db_check': emissions_processing.check,
                'process': emissions_processing.process,
                'db_process': emissions_processing.process,
                'viz': emissions_viz.plot,
                'callback': emissions_callbacks.link,
                'description': 'Emissions that are produced by the generation mix in the models.'
            },
        'Capacity':
            {
                'check': generation_capacity_processing.check,
                'db_check': generation_capacity_processing.check,
                'process': generation_capacity_processing.process,
                'db_process': generation_capacity_processing.process,
                'viz': generation_capacity_viz.plot,
                'callback': generation_capacity_callbacks.link,
                'description': 'Total generation capacity of each technology in the models.'
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
                'description': 'New generation capacity that is built for each technology in the model (does not include retired technologies).'
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
        'Transmission Capacity':
            {
                'check': transmission_capacity_processing.check,
                'db_check': transmission_capacity_processing.check,
                'process': transmission_capacity_processing.process,
                'db_process': transmission_capacity_processing.process,
                'viz': transmission_capacity_viz.plot,
                'callback': transmission_capacity_callbacks.link,
                'description': 'Total transmission capacity between regions in the model.'
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
            }

    }

    def __init__(self):
        super().__init__()
        all_techs = {}

        for path in technologies_paths:
            techs = yaml.load(open(path, 'r'), Loader=yaml.FullLoader)
            all_techs.update(techs)

        self.technologies = all_techs
        self.plots = yaml.load(open('./profiles/energy_model/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        super().link(app)

    def process_data(self, data_collection):
        processed_data = defaultdict(list)

        for profile, viz_option, df in data_collection:
            print(profile, viz_option)
            if (profile in power_system_models and viz_option not in ['Comparison',
                                                                      'Comparison Matrix'] and viz_option in self.viz_options):

                data = df.copy()
                data['version'] = data['scenario'].apply(lambda x: x.split('|')[-1] if '|' in x else 'v0')
                data['scenario'] = profile + '|' + data['scenario']
                

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
            if model in power_system_models:
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

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='energy_models-settings-upload-yaml',
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

                html.Div(id='energy_models-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='energy_models-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='energy_models-plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='energy_models-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='energy_models-plot-settings-panel', value='plot',
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
                    id='energy_models-technology-select',
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
                     id='energy_models-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='energy_models-plot-select',
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
                     id='energy_models-plot-settings-output'),
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
