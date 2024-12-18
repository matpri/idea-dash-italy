from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile, data_processing_task
from profiles.cims_output import utils
from profiles.cims_output.callbacks import (requested_quantities as requested_quantities_callbacks,
                                            stock_lcc as stock_lcc_callbacks,
                                            ghg as ghg_callbacks,
                                            overview as overview_callbacks,
                                            settings as settings_callbacks,
                                            sectored as sectored_callbacks,
                                            inputs as inputs_callbacks,

                                            )
from profiles.cims_output.processing_scripts import (
    overview as overview_processing,
    sectored as sectored_processing,
    inputs as inputs_processing,
)
from profiles.cims_output.processing_scripts.utils import ghg as ghg_processing, stock_lcc as stock_lcc_processing, \
    requested_quantities as requested_quantities_processing
from profiles.cims_output.visualization_scripts import (
    requested_quantities as emissions_viz,
    stock_lcc as stock_lcc_viz,
    ghg as ghg_viz,
    
    overview as overview_viz,
    sectored as sectored_viz,
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
                'description': 'Visualizations for a general overview of the data.'
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
        'Agriculture':
            {
                'check': sectored_processing.create_check('Agriculture'),
                'db_check': sectored_processing.create_check('Agriculture'),
                'process': sectored_processing.create_process('Agriculture'),
                'db_process': sectored_processing.create_process('Agriculture'),
                'viz': sectored_viz.create_plot('Agriculture'),
                'callback': sectored_callbacks.create_link('Agriculture'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Biodiesel':
            {
                'check': sectored_processing.create_check('Biodiesel'),
                'db_check': sectored_processing.create_check('Biodiesel'),
                'process': sectored_processing.create_process('Biodiesel'),
                'db_process': sectored_processing.create_process('Biodiesel'),
                'viz': sectored_viz.create_plot('Biodiesel'),
                'callback': sectored_callbacks.create_link('Biodiesel'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Chemical Products':
            {
                'check': sectored_processing.create_check('Chemical Products'),
                'db_check': sectored_processing.create_check('Chemical Products'),
                'process': sectored_processing.create_process('Chemical Products'),
                'db_process': sectored_processing.create_process('Chemical Products'),
                'viz': sectored_viz.create_plot('Chemical Products'),
                'callback': sectored_callbacks.create_link('Chemical Products'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Commercial':
            {
                'check': sectored_processing.create_check('Commercial'),
                'db_check': sectored_processing.create_check('Commercial'),
                'process': sectored_processing.create_process('Commercial'),
                'db_process': sectored_processing.create_process('Commercial'),
                'viz': sectored_viz.create_plot('Commercial'),
                'callback': sectored_callbacks.create_link('Commercial'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Electricity':
            {
                'check': sectored_processing.create_check('Electricity'),
                'db_check': sectored_processing.create_check('Electricity'),
                'process': sectored_processing.create_process('Electricity'),
                'db_process': sectored_processing.create_process('Electricity'),
                'viz': sectored_viz.create_plot('Electricity'),
                'callback': sectored_callbacks.create_link('Electricity'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Ethanol':
            {
                'check': sectored_processing.create_check('Ethanol'),
                'db_check': sectored_processing.create_check('Ethanol'),
                'process': sectored_processing.create_process('Ethanol'),
                'db_process': sectored_processing.create_process('Ethanol'),
                'viz': sectored_viz.create_plot('Ethanol'),
                'callback': sectored_callbacks.create_link('Ethanol'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Hydrogen':
            {
                'check': sectored_processing.create_check('Hydrogen'),
                'db_check': sectored_processing.create_check('Hydrogen'),
                'process': sectored_processing.create_process('Hydrogen'),
                'db_process': sectored_processing.create_process('Hydrogen'),
                'viz': sectored_viz.create_plot('Hydrogen'),
                'callback': sectored_callbacks.create_link('Hydrogen'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Industrial Minerals':
            {
                'check': sectored_processing.create_check('Industrial Minerals'),
                'db_check': sectored_processing.create_check('Industrial Minerals'),
                'process': sectored_processing.create_process('Industrial Minerals'),
                'db_process': sectored_processing.create_process('Industrial Minerals'),
                'viz': sectored_viz.create_plot('Industrial Minerals'),
                'callback': sectored_callbacks.create_link('Industrial Minerals'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Iron and Steel':
            {
                'check': sectored_processing.create_check('Iron and Steel'),
                'db_check': sectored_processing.create_check('Iron and Steel'),
                'process': sectored_processing.create_process('Iron and Steel'),
                'db_process': sectored_processing.create_process('Iron and Steel'),
                'viz': sectored_viz.create_plot('Iron and Steel'),
                'callback': sectored_callbacks.create_link('Iron and Steel'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Light Industrial':
            {
                'check': sectored_processing.create_check('Light Industrial'),
                'db_check': sectored_processing.create_check('Light Industrial'),
                'process': sectored_processing.create_process('Light Industrial'),
                'db_process': sectored_processing.create_process('Light Industrial'),
                'viz': sectored_viz.create_plot('Light Industrial'),
                'callback': sectored_callbacks.create_link('Light Industrial'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Metal Smelting':
            {
                'check': sectored_processing.create_check('Metal Smelting'),
                'db_check': sectored_processing.create_check('Metal Smelting'),
                'process': sectored_processing.create_process('Metal Smelting'),
                'db_process': sectored_processing.create_process('Metal Smelting'),
                'viz': sectored_viz.create_plot('Metal Smelting'),
                'callback': sectored_callbacks.create_link('Metal Smelting'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Mining':
            {
                'check': sectored_processing.create_check('Mining'),
                'db_check': sectored_processing.create_check('Mining'),
                'process': sectored_processing.create_process('Mining'),
                'db_process': sectored_processing.create_process('Mining'),
                'viz': sectored_viz.create_plot('Mining'),
                'callback': sectored_callbacks.create_link('Mining'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Natural Gas Production':
            {
                'check': sectored_processing.create_check('Natural Gas Production'),
                'db_check': sectored_processing.create_check('Natural Gas Production'),
                'process': sectored_processing.create_process('Natural Gas Production'),
                'db_process': sectored_processing.create_process('Natural Gas Production'),
                'viz': sectored_viz.create_plot('Natural Gas Production'),
                'callback': sectored_callbacks.create_link('Natural Gas Production'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Petroleum Crude':
            {
                'check': sectored_processing.create_check('Petroleum Crude'),
                'db_check': sectored_processing.create_check('Petroleum Crude'),
                'process': sectored_processing.create_process('Petroleum Crude'),
                'db_process': sectored_processing.create_process('Petroleum Crude'),
                'viz': sectored_viz.create_plot('Petroleum Crude'),
                'callback': sectored_callbacks.create_link('Petroleum Crude'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Petroleum Refining':
            {
                'check': sectored_processing.create_check('Petroleum Refining'),
                'db_check': sectored_processing.create_check('Petroleum Refining'),
                'process': sectored_processing.create_process('Petroleum Refining'),
                'db_process': sectored_processing.create_process('Petroleum Refining'),
                'viz': sectored_viz.create_plot('Petroleum Refining'),
                'callback': sectored_callbacks.create_link('Petroleum Refining'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Pulp and Paper':
            {
                'check': sectored_processing.create_check('Pulp and Paper'),
                'db_check': sectored_processing.create_check('Pulp and Paper'),
                'process': sectored_processing.create_process('Pulp and Paper'),
                'db_process': sectored_processing.create_process('Pulp and Paper'),
                'viz': sectored_viz.create_plot('Pulp and Paper'),
                'callback': sectored_callbacks.create_link('Pulp and Paper'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Residential':
            {
                'check': sectored_processing.create_check('Residential'),
                'db_check': sectored_processing.create_check('Residential'),
                'process': sectored_processing.create_process('Residential'),
                'db_process': sectored_processing.create_process('Residential'),
                'viz': sectored_viz.create_plot('Residential'),
                'callback': sectored_callbacks.create_link('Residential'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Transportation Freight':
            {
                'check': sectored_processing.create_check('Transportation Freight'),
                'db_check': sectored_processing.create_check('Transportation Freight'),
                'process': sectored_processing.create_process('Transportation Freight'),
                'db_process': sectored_processing.create_process('Transportation Freight'),
                'viz': sectored_viz.create_plot('Transportation Freight'),
                'callback': sectored_callbacks.create_link('Transportation Freight'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Transportation Personal':
            {
                'check': sectored_processing.create_check('Transportation Personal'),
                'db_check': sectored_processing.create_check('Transportation Personal'),
                'process': sectored_processing.create_process('Transportation Personal'),
                'db_process': sectored_processing.create_process('Transportation Personal'),
                'viz': sectored_viz.create_plot('Transportation Personal'),
                'callback': sectored_callbacks.create_link('Transportation Personal'),
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            },
        'Waste':
            {
                'check': sectored_processing.create_check('Waste'),
                'db_check': sectored_processing.create_check('Waste'),
                'process': sectored_processing.create_process('Waste'),
                'db_process': sectored_processing.create_process('Waste'),
                'viz': sectored_viz.create_plot('Waste'),
                'callback': sectored_callbacks.create_link('Waste'),
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
