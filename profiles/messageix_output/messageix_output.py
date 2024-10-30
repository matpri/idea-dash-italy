from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc

from profiles.base_profile.base_profile import BaseProfile
from profiles.messageix_output import utils
from profiles.messageix_output.callbacks import (emissions as emissions_callbacks,
                                                 capital_cost as capital_cost_callbacks,
                                                 total_cost as total_cost_callbacks,
                                                 capacity_additions as capacity_additions_callbacks,
                                                 capacity as capacity_callbacks,
                                                 primary_energy as primary_energy_callbacks,
                                                 secondary_energy as secondary_energy_callbacks,
                                                 final_energy as final_energy_callbacks,
                                                 useful_energy as useful_energy_callbacks,
                                                 settings as settings_callbacks,
                                                 overview as overview_callbacks,
                                                 sankey as sankey_callbacks

                                                 )
from profiles.messageix_output.processing_scripts import (
    emissions as emissions_processing,
    total_cost as total_cost_processing,
    capital_cost as capital_cost_processing,
    capacity_additions as capacity_additions_processing,
    capacity as capacity_processing,
    primary_energy as primary_energy_processing,
    secondary_energy as secondary_energy_processing,
    final_energy as final_energy_processing,
    useful_energy as useful_energy_processing,
    overview as overview_processing,
    sankey as sankey_processing
)
from profiles.messageix_output.visualization_scripts import (
    emissions as emissions_viz,
    total_cost as total_cost_viz,
    capital_cost as capital_cost_viz,
    capacity_additions as capacity_additions_viz,
    capacity as capacity_viz,
    primary_energy as primary_energy_viz,
    secondary_energy as secondary_energy_viz,
    final_energy as final_energy_viz,
    useful_energy as useful_energy_viz,
    overview as overview_viz,
    sankey as sankey_viz
)


class messageixOutput(BaseProfile):
    name = 'MESSAGEix-Canada'
    display_name = 'MESSAGEix-Canada'
    db_name = 'messageix'
    color = 'yellow 8'
    description = (
        'MESSAGEix is a versatile, dynamic, model framework for energy-engineering-economy-environment (E4) systems research.')

    plot_order = [
        'Overview',
        'Emissions',
        'Capacity',
        'Capacity Additions',
        'Capital Cost',
        'Total Cost',
        'Primary Energy',
        'Secondary Energy',
        'Final Energy',
        'Useful Energy',
        # 'Sankey'
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
        'Total Cost':
            {
                'check': total_cost_processing.check,
                'db_check': total_cost_processing.check,
                'process': total_cost_processing.process,
                'db_process': total_cost_processing.process,
                'viz': total_cost_viz.plot,
                'callback': total_cost_callbacks.link,
                'description': 'Total cost of the energy system.'
            },
        'Capital Cost':
            {
                'check': capital_cost_processing.check,
                'db_check': capital_cost_processing.check,
                'process': capital_cost_processing.process,
                'db_process': capital_cost_processing.process,
                'viz': capital_cost_viz.plot,
                'callback': capital_cost_callbacks.link,
                'description': 'Capital cost of the energy system.'
            },
        'Capacity Additions':
            {
                'check': capacity_additions_processing.check,
                'db_check': capacity_additions_processing.check,
                'process': capacity_additions_processing.process,
                'db_process': capacity_additions_processing.process,
                'viz': capacity_additions_viz.plot,
                'callback': capacity_additions_callbacks.link,
                'description': 'Capacity additions in the energy system.'
            },
        'Capacity':
            {
                'check': capacity_processing.check,
                'db_check': capacity_processing.check,
                'process': capacity_processing.process,
                'db_process': capacity_processing.process,
                'viz': capacity_viz.plot,
                'callback': capacity_callbacks.link,
                'description': 'Capacity of the energy system.'
            },
        'Primary Energy':
            {
                'check': primary_energy_processing.check,
                'db_check': primary_energy_processing.check,
                'process': primary_energy_processing.process,
                'db_process': primary_energy_processing.process,
                'viz': primary_energy_viz.plot,
                'callback': primary_energy_callbacks.link,
                'description': 'Primary energy in the energy system.'
            },
        'Secondary Energy':
            {
                'check': secondary_energy_processing.check,
                'db_check': secondary_energy_processing.check,
                'process': secondary_energy_processing.process,
                'db_process': secondary_energy_processing.process,
                'viz': secondary_energy_viz.plot,
                'callback': secondary_energy_callbacks.link,
                'description': 'Secondary energy in the energy system.'
            },
        'Final Energy':
            {
                'check': final_energy_processing.check,
                'db_check': final_energy_processing.check,
                'process': final_energy_processing.process,
                'db_process': final_energy_processing.process,
                'viz': final_energy_viz.plot,
                'callback': final_energy_callbacks.link,
                'description': 'Final energy in the energy system.'
            },
        'Useful Energy':
            {
                'check': useful_energy_processing.check,
                'db_check': useful_energy_processing.check,
                'process': useful_energy_processing.process,
                'db_process': useful_energy_processing.process,
                'viz': useful_energy_viz.plot,
                'callback': useful_energy_callbacks.link,
                'description': 'Useful energy in the energy system.'
            },
        'Sankey':
            {
                'check': sankey_processing.check,
                'db_check': sankey_processing.check,
                'process': sankey_processing.process,
                'db_process': sankey_processing.process,
                'viz': sankey_viz.plot,
                'callback': sankey_callbacks.link,
                'description': 'Sankey diagram showing the flow of energy in the energy system.'
            },
    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/messageix_output/technologies.yaml', 'r'),
                                      Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/messageix_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
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
                    id='messageix-settings-upload-yaml',
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

                html.Div(id='messageix-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='messageix-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='messageix-plot-settings', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='messageix-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='messageix-plot-settings-panel', value='plot',
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
                    id='messageix-technology-select',
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
                     id='messageix-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='messageix-plot-select',
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
                     id='messageix-plot-settings-output'),
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
