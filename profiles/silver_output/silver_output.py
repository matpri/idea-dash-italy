from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc
import pandas as pd

from profiles.base_profile.base_profile import BaseProfile, data_processing_task
from profiles.silver_output import utils
from profiles.silver_output.callbacks import (
    settings as settings_callbacks,
    opf_costs as opf_costs_callbacks,
    opf_results as opf_results_callbacks,
    opf_emissions as opf_emissions_callbacks,
    uc_results as uc_results_callbacks,
    uc_emissions as uc_emissions_callbacks,
    price_opf as price_opf_callbacks,
opf_curtailment as opf_curtailment_callbacks,
uc_curtailment as uc_curtailment_callbacks,
map_plots as map_plots_callbacks,
opf_lineflow as opf_lineflow_callbacks,
uc_lineflow as uc_lineflow_callbacks,
overview as overview_callbacks
)
from profiles.silver_output.processing_scripts import (
    opf_costs as opf_costs_processing,
    opf_results as opf_results_processing,
    opf_emissions as opf_emissions_processing,
    uc_results as uc_results_processing,
    uc_emissions as uc_emissions_processing,
    price_opf as price_opf_processing,
opf_curtailment as opf_curtailment_processing,
uc_curtailment as uc_curtailment_processing,
map_plots as map_plots_processing,
opf_lineflow as opf_lineflow_processing,
uc_lineflow as uc_lineflow_processing,
overview as overview_processing
)
from profiles.silver_output.visualization_scripts import (
    opf_costs as opf_costs_viz,
    opf_results as opf_results_viz,
    uc_results as uc_results_viz,
    uc_emissions as uc_emissions_viz,
    opf_emissions as opf_emissions_viz,
    price_opf as price_opf_viz,
opf_curtailment as opf_curtailment_viz,
uc_curtailment as uc_curtailment_viz,
map_plots as map_plots_viz,
opf_lineflow as opf_lineflow_viz,
uc_lineflow as uc_lineflow_viz,
overview as overview_viz
)


class silverOutput(BaseProfile):
    display_name = 'SILVER'
    name = 'silver'
    db_name = 'silver'
    color = 'silver'
    description = (
        'The Strategic Integration of Large-capacity Variable Energy Resources (SILVER) tool is a generic electricity network optimization tool written in Python based on object-oriented programming. \n'
        'It has been designed to be adaptable in different dimensions: temporal, spatial, technology representation and market design.')

    plot_order = [
        'Overview',
        'OPF Costs',
        'OPF Results',
        'OPF Emissions',
        'OPF_VRE_Curtailment',
        'OPF Line Flow',
        'UC Results',
        'UC Emissions',
        'UC_VRE_Curtailment',
        'UC Line Flow',
        'Price OPF',
        'Map Plots'
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
        'OPF Costs': {
            'process': opf_costs_processing.process,
            'viz': opf_costs_viz.plot,
            'callback': opf_costs_callbacks.link,
            'check': opf_costs_processing.check,
        },
        'OPF Results': {
            'process': opf_results_processing.process,
            'viz': opf_results_viz.plot,
            'callback': opf_results_callbacks.link,
            'check': opf_results_processing.check,
        },
        'OPF Emissions': {
            'process': opf_emissions_processing.process,
            'viz': opf_emissions_viz.plot,
            'callback': opf_emissions_callbacks.link,
            'check': opf_emissions_processing.check,
        },
        'OPF_VRE_Curtailment': {
            'process': opf_curtailment_processing.process,
            'viz': opf_curtailment_viz.plot,
            'callback': opf_curtailment_callbacks.link,
            'check': opf_curtailment_processing.check,
        },
        'OPF Line Flow': {
            'process': opf_lineflow_processing.process,
            'viz': opf_lineflow_viz.plot,
            'callback': opf_lineflow_callbacks.link,
            'check': opf_lineflow_processing.check,
        },
        'UC Results': {
            'process': uc_results_processing.process,
            'viz': uc_results_viz.plot,
            'callback': uc_results_callbacks.link,
            'check': uc_results_processing.check,
        },
        'UC Emissions': {
            'process': uc_emissions_processing.process,
            'viz': uc_emissions_viz.plot,
            'callback': uc_emissions_callbacks.link,
            'check': uc_emissions_processing.check,
        },
        'UC_VRE_Curtailment': {
            'process': uc_curtailment_processing.process,
            'viz': uc_curtailment_viz.plot,
            'callback': uc_curtailment_callbacks.link,
            'check': uc_curtailment_processing.check,
        },
        'UC Line Flow': {
            'process': uc_lineflow_processing.process,
            'viz': uc_lineflow_viz.plot,
            'callback': uc_lineflow_callbacks.link,
            'check': uc_lineflow_processing.check,
        },
        'Price OPF': {
            'process': price_opf_processing.process,
            'viz': price_opf_viz.plot,
            'callback': price_opf_callbacks.link,
            'check': price_opf_processing.check,
        },
        'Map Plots': {
            'process': map_plots_processing.process,
            'viz': map_plots_viz.plot,
            'callback': map_plots_callbacks.link,
            'check': map_plots_processing.check,
        }
    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/silver_output/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/silver_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        for viz in self.viz_options:
            self.viz_options[viz]['callback'](app)

    #not sure if this function should be here
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
                    id='silver-settings-upload-yaml',
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

                html.Div(id='silver-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='silver-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='silver-plot-settings-tab', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='silver-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='silver-plot-settings', value='plot',
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
                    id='silver-technology-select',
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
                     id='silver-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='silver-plot-select',
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
                     id='silver-plot-settings-output'),
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
