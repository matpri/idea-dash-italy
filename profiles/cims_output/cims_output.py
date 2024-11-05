from random import randint

import dash_mantine_components as dmc
import pandas as pd
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile, data_processing_task
from profiles.cims_output import utils
from profiles.cims_output.callbacks import (requested_quantities as requested_quantities_callbacks,
                                            stock_lcc as stock_lcc_callbacks,
                                            ghg as ghg_callbacks,
                                            overview as overview_callbacks,
                                            settings as settings_callbacks,
                                            )
from profiles.cims_output.processing_scripts import (
    requested_quantities as requested_quantities_processing,
    stock_lcc as stock_lcc_processing,
    ghg as ghg_processing,
    overview as overview_processing
)
from profiles.cims_output.visualization_scripts import (
    requested_quantities as emissions_viz,
    stock_lcc as stock_lcc_viz,
    ghg as ghg_viz,
    overview as overview_viz,
)


class PypsaOutput(BaseProfile):
    display_name = 'CIMS'
    db_name = 'cims'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Overview',
        'Requested Quantities',
        'Stock LCC',
        'GHG'
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
        'Requested Quantities':
            {
                'check': requested_quantities_processing.check,
                'db_check': requested_quantities_processing.check,
                'process': requested_quantities_processing.process,
                'db_process': requested_quantities_processing.process,
                'viz': emissions_viz.plot,
                'callback': requested_quantities_callbacks.link,
                'description': 'Emissions that are produced by the generation mix in the model.'
            },
        'Stock LCC':
            {
                'check': stock_lcc_processing.check,
                'db_check': stock_lcc_processing.check,
                'process': stock_lcc_processing.process,
                'db_process': stock_lcc_processing.process,
                'viz': stock_lcc_viz.plot,
                'callback': stock_lcc_callbacks.link,
                'description': 'The stock of technologies in the model.'
            },
        'GHG':
            {
                'check': ghg_processing.check,
                'db_check': ghg_processing.check,
                'process': ghg_processing.process,
                'db_process': ghg_processing.process,
                'viz': ghg_viz.plot,
                'callback': ghg_callbacks.link,
                'description': 'The greenhouse gas emissions produced by the generation mix in the model.'
            }
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
