from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.copper_input import utils
from profiles.copper_input.callbacks import (
    generation_capacity as generation_capacity_callbacks,
    transmission as transmission_callbacks,
    demand as demand_callbacks,
    generation_type_data as generation_type_data_callbacks,
    annual_growth as annual_growth_callbacks,
    tech_evolution as tech_evolution_callbacks,
    settings as settings_callbacks,
)
from profiles.copper_input.processing_scripts import (
    generation_capacity as generation_capacity_processing,
    transmission as transmission_processing,
    generation_type_data as generation_type_data_processing,
    annual_growth as annual_growth_processing,
    demand as demand_processing,
    tech_evolution as tech_evolution_processing,
)
from profiles.copper_input.visualization_scripts import (
    generation_capacity as generation_capacity_viz,
    transmission as transmission_viz,
    generation_type_data as generation_type_data_viz,
    annual_growth as annual_growth_viz,
    demand as demand_viz,
    tech_evolution as tech_evolution_viz,
)


class CopperOutput(BaseProfile):
    name = 'COPPER Input'
    color = 'yellow 8'
    description = (
        'The Canadian Opportunities for Planning and Production of Electricity Resources (COPPER) framework is an electricity system planning model. \n'
        'It minimizes total system costs (including investment, operation and maintenance costs) over an extended planning period.')

    plot_order = [
        'Capacity',
        'Transmission',
        'Demand',
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
        'Annual Growth':
            {
                'check': annual_growth_processing.check,
                'db_check': annual_growth_processing.check,
                'process': annual_growth_processing.process,
                'db_process': annual_growth_processing.process,
                'viz': annual_growth_viz.plot,
                'callback': annual_growth_callbacks.link,
                'description': 'Annual growth factor of demand in each region.'
            },
        'Generation Type Data':
            {
                'check': generation_type_data_processing.check,
                'db_check': generation_type_data_processing.check,
                'process': generation_type_data_processing.process,
                'db_process': generation_type_data_processing.process,
                'viz': generation_type_data_viz.plot,
                'callback': generation_type_data_callbacks.link,
                'description': 'Definitions of input variables by technology.'
            },
        'Tech Evolution':
            {
                'check': tech_evolution_processing.check,
                'db_check': tech_evolution_processing.check,
                'process': tech_evolution_processing.process,
                'db_process': tech_evolution_processing.process,
                'viz': tech_evolution_viz.plot,
                'callback': tech_evolution_callbacks.link,
                'description': 'Projected evolution of technology capacities/ price.'
            }

    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/copper_input/technologies.yaml', 'r'), Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/copper_input/plots.yaml', 'r'), Loader=yaml.FullLoader)
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
                    id='copper_input-settings-upload-yaml',
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

                html.Div(id='copper_input-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='copper_input-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='copper_input_plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='copper_input-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='copper_input-plot-settings_panel', value='plot',
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
                    id='copper_input-technology-select',
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
                     id='copper_input-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='copper_input-plot-select',
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
                     id='copper_input-plot-settings-output'),
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
