from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.coders_input import utils
from profiles.coders_input.callbacks import (
    generation_capacity as generation_capacity_callbacks,
    transmission as transmission_callbacks,
    demand as demand_callbacks,
    settings as settings_callbacks,
)
from profiles.coders_input.processing_scripts import (
    generation_capacity as generation_capacity_processing,
    transmission as transmission_processing,
    demand as demand_processing,
)
from profiles.coders_input.visualization_scripts import (
    generation_capacity as generation_capacity_viz,
    transmission as transmission_viz,
    demand as demand_viz,
)


class CopperOutput(BaseProfile):
    name = 'CODERS Input'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Capacity',
        'Transmission',
        'Demand',
        'US Demand',
        'Annual Growth',
        'Generation Type Data',
        'Tech Evolution'
    ]
    viz_options = {

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
        'Transmission':
            {
                'check': transmission_processing.check,
                'db_check': transmission_processing.check,
                'process': transmission_processing.process,
                'db_process': transmission_processing.process,
                'viz': transmission_viz.plot,
                'callback': transmission_callbacks.link,
                'description': 'Transmission capacity and distance.'
            },
        'Demand':
            {
                'check': demand_processing.check,
                'db_check': demand_processing.check,
                'process': demand_processing.process,
                'db_process': demand_processing.process,
                'viz': demand_viz.plot,
                'callback': demand_callbacks.link,
                'description': 'Electricity demand in each region.'
            },
    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/coders_input/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/coders_input/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        super().link(app)

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='coders_input-settings-upload-yaml',
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

                html.Div(id='coders_input-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='coders_input-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='coders_input_plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='coders_input-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='coders_input-plot-settings_panel', value='plot',
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
                    id='coders_input-technology-select',
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
                     id='coders_input-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='coders_input-plot-select',
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
                     id='coders_input-plot-settings-output'),
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
