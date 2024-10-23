from random import randint

import dash_mantine_components as dmc
import yaml
from dash import html, dcc
import pandas as pd

from profiles.base_profile.base_profile import BaseProfile, data_processing_task
from profiles.labourabm_output import utils
from profiles.labourabm_output.callbacks import (
    settings as settings_callbacks,
    total_unemployment as total_unemployment_callbacks,
    total_vacancies as total_vacancies_callbacks,
    total_employment as total_employment_callbacks,
    total_demand as total_demand_callbacks,
    overview as overview_callbacks
)

from profiles.labourabm_output.processing_scripts import (
    total_unemployment as total_unemployment_process,
    total_vacancies as total_vacancies_process,
    total_employment as total_employment_process,
    total_demand as total_demand_process,
)
from profiles.labourabm_output.visualization_scripts import (
    total_unemployment as total_unemployment_viz,
    total_vacancies as total_vacancies_viz,
    total_employment as total_employment_viz,
    total_demand as total_demand_viz,
    overview as overview_viz
)


class labourabmOutput(BaseProfile):
    display_name = 'LabourABM Output'
    name = 'LabourABM'

    db_name = 'LabourABM'

    color = 'red'
    description = (
        'The Strategic Integration of Large-capacity Variable Energy Resources (SILVER) tool is a generic electricity network optimization tool written in Python based on object-oriented programming. \n'
        'It has been designed to be adaptable in different dimensions: temporal, spatial, technology representation and market design.')

    plot_order = [
        'Overview',
        'Total Unemployment',
        'Total Vacancies',
        'Total Employment',
        'Total Demand'
    ]

    viz_options = {'Overview':
        {
            'check': lambda x: False,
            'db_check': lambda x: False,
            'process': lambda x: x,
            'db_process': lambda x: x,
            'viz': overview_viz.plot,
            'callback': overview_callbacks.link,
            'description': 'Line plots for a variety of variables, overviewing main results across scenarios.'
        },
        'Total Unemployment': {
            'process': total_unemployment_process.process,
            'viz': total_unemployment_viz.plot,
            'callback': total_unemployment_callbacks.link,
            'check': total_unemployment_process.check,
        },
        'Total Vacancies': {
            'process': total_vacancies_process.process,
            'viz': total_vacancies_viz.plot,
            'callback': total_vacancies_callbacks.link,
            'check': total_vacancies_process.check,
        },
        'Total Employment': {
            'process': total_employment_process.process,
            'viz': total_employment_viz.plot,
            'callback': total_employment_callbacks.link,
            'check': total_employment_process.check,
        },
        'Total Demand': {
            'process': total_demand_process.process,
            'viz': total_demand_viz.plot,
            'callback': total_demand_callbacks.link,
            'check': total_demand_process.check,
        }
    }

    def __init__(self):
        super().__init__()
        self.technologies = yaml.load(open('./profiles/labourabm_output/technologies.yaml', 'r'),
                                      Loader=yaml.FullLoader)
        self.plots = yaml.load(open('./profiles/labourabm_output/plots.yaml', 'r'), Loader=yaml.FullLoader)
        self.update_utils()
        self.settings = self.render_settings()

    def link(self, app):
        settings_callbacks.link(app)
        for viz in self.viz_options:
            self.viz_options[viz]['callback'](app)

    # not sure if this function should be here
    def process_data(self, data_collection):
        print('Base collective preprocess')
        wants_overview = False
        args = []
        for viz_option, data in data_collection.items():
            if viz_option == 'Overview':
                wants_overview = True
                continue
            args.append((self.display_name, viz_option, data, self.viz_options[viz_option]['process']))
        processed_data = [data_processing_task(*arg) for arg in args]
        if wants_overview:
            dfs = []
            for _, viz_option, data in processed_data:
                df = data.copy()
                df['variable'] = viz_option
                df = df.groupby(['scenario', 'time', 'region', 'variable']).sum().reset_index()
                dfs.append(df)
            full_df = pd.concat(dfs)
            full_df['scenario'] = full_df['scenario'] + ' - ' + full_df['region']
            processed_data.append(
                (self.display_name, 'Overview', full_df[['scenario', 'variable', 'time', 'value', 'region']]))

        return processed_data

    def render_settings(self):
        layout = html.Div(
            [
                # upload for yaml
                dcc.Upload(
                    id='labourabm-settings-upload-yaml',
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

                html.Div(id='labourabm-settings-upload-yaml-output'),
                dmc.Tabs([
                    dmc.TabsList([
                        dmc.Tab('Technology Settings', id='labourabm-technologies', value='tech'),
                        dmc.Tab('Plot Settings', id='labourabm-plot-settings-tab', value='plot'),
                    ]
                    ),
                    dmc.TabsPanel(id='labourabm-technologies-settings', value='tech',
                                  children=self.render_technology_settings()),
                    dmc.TabsPanel(id='labourabm-plot-settings', value='plot',
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
                    id='labourabm-technology-select',
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
                     id='labourabm-technology-settings-output'),
        ])

        return layout

    def render_plot_settings(self):
        plots = list(utils.plot_settings.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id='labourabm-plot-select',
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
                     id='labourabm-plot-settings-output'),
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
