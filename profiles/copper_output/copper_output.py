from random import randint

import dash_mantine_components as dmc
import yaml
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
                                              settings as settings_callbacks
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
)


class CopperOutput(BaseProfile):
    name = 'COPPER Output'
    db_name = 'copper'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Emissions',
        'Capacity',
        'Net New Capacity',
        'New Capacity',
        'Qualifying Capacity',
        'Supply',
        'Transmission Capacity',
        'Transmission Flow'
    ]
    viz_options = {
        'Emissions':
            {
                'check': emissions_processing.check,
                'db_check': emissions_processing.check,
                'process': emissions_processing.process,
                'db_process': emissions_processing.process,
                'viz': emissions_viz.plot,
                'callback': emissions_callbacks.link
            },
        'Capacity':
            {
                'check': generation_capacity_processing.check,
                'db_check': generation_capacity_processing.check,
                'process': generation_capacity_processing.process,
                'db_process': generation_capacity_processing.process,
                'viz': generation_capacity_viz.plot,
                'callback': generation_capacity_callbacks.link
            },
        'Net New Capacity':
            {
                'check': net_new_capacity_processing.check,
                'db_check': net_new_capacity_processing.check,
                'process': net_new_capacity_processing.process,
                'db_process': net_new_capacity_processing.process,
                'viz': net_new_capacity_viz.plot,
                'callback': net_new_capacity_callbacks.link
            },
        'New Capacity':
            {
                'check': new_capacity_processing.check,
                'db_check': new_capacity_processing.check,
                'process': new_capacity_processing.process,
                'db_process': new_capacity_processing.process,
                'viz': new_capacity_viz.plot,
                'callback': new_capacity_callbacks.link
            },
        'Qualifying Capacity':
            {
                'check': qualifying_capacity_processing.check,
                'db_check': qualifying_capacity_processing.check,
                'process': qualifying_capacity_processing.process,
                'db_process': qualifying_capacity_processing.process,
                'viz': qualifying_capacity_viz.plot,
                'callback': qualifying_capacity_callbacks.link
            },
        'Supply':
            {
                'check': generation_supply_processing.check,
                'db_check': generation_supply_processing.check,
                'process': generation_supply_processing.process,
                'db_process': generation_supply_processing.process,
                'viz': generation_supply_viz.plot,
                'callback': generation_supply_callbacks.link
            },
        'Transmission Capacity':
            {
                'check': transmission_capacity_processing.check,
                'db_check': transmission_capacity_processing.check,
                'process': transmission_capacity_processing.process,
                'db_process': transmission_capacity_processing.process,
                'viz': transmission_capacity_viz.plot,
                'callback': transmission_capacity_callbacks.link
            },
        'Transmission Flow':
            {
                'check': transmission_flow_processing.check,
                'db_check': transmission_flow_processing.check,
                'process': transmission_flow_processing.process,
                'db_process': transmission_flow_processing.process,
                'viz': transmission_flow_viz.plot,
                'callback': transmission_flow_callbacks.link
            }

    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/copper_output/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/copper_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        for viz in self.viz_options:
            self.viz_options[viz]['callback'](app)

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
                        dmc.Tab('Plot Settings', id='plot-settings', value='plot'),
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
