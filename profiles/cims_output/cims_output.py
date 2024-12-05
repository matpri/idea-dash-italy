from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile, data_processing_task
from profiles.cims_output import utils
from profiles.cims_output.callbacks import (requested_quantities as requested_quantities_callbacks,
                                            stock_lcc as stock_lcc_callbacks,
                                            ghg as ghg_callbacks,
                                            agriculture as agriculture_callbacks,
                                            biodiesel as biodiesel_callbacks,
                                            overview as overview_callbacks,
                                            settings as settings_callbacks,
                                            chemical_products as chemical_products_callbacks,
                                            commercial as commercial_callbacks,
                                            electricity as electricity_callbacks,
                                            ethanol as ethanol_callbacks,
                                            hydrogen as hydrogen_callbacks,
                                            industrial_minerals as industrial_minerals_callbacks,
                                            iron_and_steel as iron_and_steel_callbacks,
                                            light_industrial as light_industrial_callbacks,
                                            metal_smelting as metal_smelting_callbacks,
                                            mining as mining_callbacks,
                                            natural_gas_extraction as natural_gas_extraction_callbacks,
                                            petroleum_crude as petroleum_crude_callbacks,
                                            petroleum_refining as petroleum_refining_callbacks,
                                            pulp_and_paper as pulp_and_paper_callbacks,
                                            residential as residential_callbacks,
                                            transportation_freight as transportation_freight_callbacks,
                                            transportation_personal as transportation_personal_callbacks,
                                            waste as waste_callbacks,
                                            inputs as inputs_callbacks,

                                            )
from profiles.cims_output.processing_scripts import (
    overview as overview_processing,
    agriculture as agriculture_processing,
    biodiesel as biodiesel_processing,
    chemical_products as chemical_products_processing,
    commercial as commercial_processing,
    electricity as electricity_processing,
    ethanol as ethanol_processing,
    hydrogen as hydrogen_processing,
    industrial_minerals as industrial_minerals_processing,
    iron_and_steel as iron_and_steel_processing,
    light_industrial as light_industrial_processing,
    metal_smelting as metal_smelting_processing,
    mining as mining_processing,
    natural_gas_extraction as natural_gas_extraction_processing,
    petroleum_crude as petroleum_crude_processing,
    petroleum_refining as petroleum_refining_processing,
    pulp_and_paper as pulp_and_paper_processing,
    residential as residential_processing,
    transportation_freight as transportation_freight_processing,
    transportation_personal as transportation_personal_processing,
    waste as waste_processing,
    inputs as inputs_processing,
)
from profiles.cims_output.processing_scripts.utils import ghg as ghg_processing, stock_lcc as stock_lcc_processing, \
    requested_quantities as requested_quantities_processing
from profiles.cims_output.visualization_scripts import (
    requested_quantities as emissions_viz,
    stock_lcc as stock_lcc_viz,
    ghg as ghg_viz,
    agriculture as agriculture_viz,
    biodiesel as biodiesel_viz,
    overview as overview_viz,
    chemical_products as chemical_products_viz,
    commercial as commercial_viz,
    electricity as electricity_viz,
    ethanol as ethanol_viz,
    hydrogen as hydrogen_viz,
    industrial_minerals as industrial_minerals_viz,
    iron_and_steel as iron_and_steel_viz,
    light_industrial as light_industrial_viz,
    metal_smelting as metal_smelting_viz,
    mining as mining_viz,
    natural_gas_extraction as natural_gas_extraction_viz,
    petroleum_crude as petroleum_crude_viz,
    petroleum_refining as petroleum_refining_viz,
    pulp_and_paper as pulp_and_paper_viz,
    residential as residential_viz,
    transportation_freight as transportation_freight_viz,
    transportation_personal as transportation_personal_viz,
    waste as waste_viz,
    inputs as inputs_viz,
)


class PypsaOutput(BaseProfile):
    display_name = 'CIMS'
    db_name = 'cims'
    name='cims'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Overview',
        'Inputs',
        'Energy Demand',
        'Technology Stocks',
        'Emissions',
        'Agriculture',
        'Biodiesel',
        'Chemical Products',
        'Commercial',
        'Electricity',
        'Ethanol',
        'Hydrogen',
        'Industrial Minerals',
        'Iron and Steel',
        'Light Industrial',
        'Metal Smelting',
        'Mining',
        'Natural Gas Production',
        'Petroleum Crude',
        'Petroleum Refining',
        'Pulp and Paper',
        'Residential',
        'Transportation Freight',
        'Transportation Personal',
        'Waste'
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
        'Inputs':
            {
                'check': inputs_processing.check,
                'db_check': inputs_processing.check,
                'process': inputs_processing.process,
                'db_process': inputs_processing.process,
                'viz': inputs_viz.plot,
                'callback': inputs_callbacks.link,
                'description': 'Visualizations of the input data.'
            },
        'Energy Demand':
            {
                'check': requested_quantities_processing.check,
                'db_check': requested_quantities_processing.check,
                'process': requested_quantities_processing.process,
                'db_process': requested_quantities_processing.process,
                'viz': emissions_viz.plot,
                'callback': requested_quantities_callbacks.link,
                'description': 'Emissions that are produced by the generation mix in the model.'
            },
        'Technology Stocks':
            {
                'check': stock_lcc_processing.check,
                'db_check': stock_lcc_processing.check,
                'process': stock_lcc_processing.process,
                'db_process': stock_lcc_processing.process,
                'viz': stock_lcc_viz.plot,
                'callback': stock_lcc_callbacks.link,
                'description': 'The stock of technologies in the model.'
            },
        'Emissions':
            {
                'check': ghg_processing.check,
                'db_check': ghg_processing.check,
                'process': ghg_processing.process,
                'db_process': ghg_processing.process,
                'viz': ghg_viz.plot,
                'callback': ghg_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Agriculture':
            {
                'check': agriculture_processing.check,
                'db_check': agriculture_processing.check,
                'process': agriculture_processing.process,
                'db_process': agriculture_processing.process,
                'viz': agriculture_viz.plot,
                'callback': agriculture_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Biodiesel':
            {
                'check': biodiesel_processing.check,
                'db_check': biodiesel_processing.check,
                'process': biodiesel_processing.process,
                'db_process': biodiesel_processing.process,
                'viz': biodiesel_viz.plot,
                'callback': biodiesel_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Chemical Products':
            {
                'check': chemical_products_processing.check,
                'db_check': chemical_products_processing.check,
                'process': chemical_products_processing.process,
                'db_process': chemical_products_processing.process,
                'viz': chemical_products_viz.plot,
                'callback': chemical_products_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Commercial':
            {
                'check': commercial_processing.check,
                'db_check': commercial_processing.check,
                'process': commercial_processing.process,
                'db_process': commercial_processing.process,
                'viz': commercial_viz.plot,
                'callback': commercial_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Electricity':
            {
                'check': electricity_processing.check,
                'db_check': electricity_processing.check,
                'process': electricity_processing.process,
                'db_process': electricity_processing.process,
                'viz': electricity_viz.plot,
                'callback': electricity_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Ethanol':
            {
                'check': ethanol_processing.check,
                'db_check': ethanol_processing.check,
                'process': ethanol_processing.process,
                'db_process': ethanol_processing.process,
                'viz': ethanol_viz.plot,
                'callback': ethanol_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Hydrogen':
            {
                'check': hydrogen_processing.check,
                'db_check': hydrogen_processing.check,
                'process': hydrogen_processing.process,
                'db_process': hydrogen_processing.process,
                'viz': hydrogen_viz.plot,
                'callback': hydrogen_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Industrial Minerals':
            {
                'check': industrial_minerals_processing.check,
                'db_check': industrial_minerals_processing.check,
                'process': industrial_minerals_processing.process,
                'db_process': industrial_minerals_processing.process,
                'viz': industrial_minerals_viz.plot,
                'callback': industrial_minerals_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Iron and Steel':
            {
                'check': iron_and_steel_processing.check,
                'db_check': iron_and_steel_processing.check,
                'process': iron_and_steel_processing.process,
                'db_process': iron_and_steel_processing.process,
                'viz': iron_and_steel_viz.plot,
                'callback': iron_and_steel_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Light Industrial':
            {
                'check': light_industrial_processing.check,
                'db_check': light_industrial_processing.check,
                'process': light_industrial_processing.process,
                'db_process': light_industrial_processing.process,
                'viz': light_industrial_viz.plot,
                'callback': light_industrial_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Metal Smelting':
            {
                'check': metal_smelting_processing.check,
                'db_check': metal_smelting_processing.check,
                'process': metal_smelting_processing.process,
                'db_process': metal_smelting_processing.process,
                'viz': metal_smelting_viz.plot,
                'callback': metal_smelting_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Mining':
            {
                'check': mining_processing.check,
                'db_check': mining_processing.check,
                'process': mining_processing.process,
                'db_process': mining_processing.process,
                'viz': mining_viz.plot,
                'callback': mining_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Natural Gas Production':
            {
                'check': natural_gas_extraction_processing.check,
                'db_check': natural_gas_extraction_processing.check,
                'process': natural_gas_extraction_processing.process,
                'db_process': natural_gas_extraction_processing.process,
                'viz': natural_gas_extraction_viz.plot,
                'callback': natural_gas_extraction_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Petroleum Crude':
            {
                'check': petroleum_crude_processing.check,
                'db_check': petroleum_crude_processing.check,
                'process': petroleum_crude_processing.process,
                'db_process': petroleum_crude_processing.process,
                'viz': petroleum_crude_viz.plot,
                'callback': petroleum_crude_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Petroleum Refining':
            {
                'check': petroleum_refining_processing.check,
                'db_check': petroleum_refining_processing.check,
                'process': petroleum_refining_processing.process,
                'db_process': petroleum_refining_processing.process,
                'viz': petroleum_refining_viz.plot,
                'callback': petroleum_refining_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Pulp and Paper':
            {
                'check': pulp_and_paper_processing.check,
                'db_check': pulp_and_paper_processing.check,
                'process': pulp_and_paper_processing.process,
                'db_process': pulp_and_paper_processing.process,
                'viz': pulp_and_paper_viz.plot,
                'callback': pulp_and_paper_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Residential':
            {
                'check': residential_processing.check,
                'db_check': residential_processing.check,
                'process': residential_processing.process,
                'db_process': residential_processing.process,
                'viz': residential_viz.plot,
                'callback': residential_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Transportation Freight':
            {
                'check': transportation_freight_processing.check,
                'db_check': transportation_freight_processing.check,
                'process': transportation_freight_processing.process,
                'db_process': transportation_freight_processing.process,
                'viz': transportation_freight_viz.plot,
                'callback': transportation_freight_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Transportation Personal':
            {
                'check': transportation_personal_processing.check,
                'db_check': transportation_personal_processing.check,
                'process': transportation_personal_processing.process,
                'db_process': transportation_personal_processing.process,
                'viz': transportation_personal_viz.plot,
                'callback': transportation_personal_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Waste':
            {
                'check': waste_processing.check,
                'db_check': waste_processing.check,
                'process': waste_processing.process,
                'db_process': waste_processing.process,
                'viz': waste_viz.plot,
                'callback': waste_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },

    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/cims_output/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/cims_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        super().link(app)

    def process_data(self, data_collection):
        print('Base collective preprocess')
        args = []
        for viz_option, data in data_collection.items():
            args.append((self.display_name, viz_option, data, self.viz_options[viz_option]['process']))
        processed_data = [data_processing_task(*arg) for arg in args]

        return processed_data

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='cims-settings-upload-yaml',
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

                html.Div(id='cims-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='cims-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='cims-plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='cims-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='cims-plot-settings-panel', value='plot',
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
                    id='cims-technology-select',
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
                     id='cims-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='cims-plot-select',
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
                     id='cims-plot-settings-output'),
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
