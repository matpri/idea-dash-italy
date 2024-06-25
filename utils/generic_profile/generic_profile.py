from random import randint

import dash_mantine_components as dmc
from dash import html

from utils.generic_profile import utils
from utils.generic_profile.callbacks import generic_callback, settings
from utils.generic_profile.processing_scripts import generic_processing
from utils.generic_profile.visualization_scripts.generic_viz import create_generic_plots


def data_processing_task(profile_name, viz, data, processing_func):
    # try:
    data_out = processing_func(data)
    # except Exception as e:
    #     print(f"Error processing data for {profile_name} - {viz}: {e}")
    #     data_out = pd.DataFrame()

    return profile_name, viz, data_out


class GenericProfile:
    def __init__(self, name, classes, variables):
        self.name = name

        self.technologies = {}

        for variable in variables:
            self.technologies[variable] = {
                'color': '#000000',
                'group': variable,
                'group_color': '#000000',
                'name': variable,
            }
        self.update_utils()
        self.settings = self.render_settings()

        self.color = '#000000'
        self.description = 'Generic Profile'

        self.plot_order = classes
        self.plot_order.sort()

        self.viz_options = {}

        for class_name in classes:
            self.viz_options[class_name] = {
                'check': generic_processing.create_check(class_name, name),
                'db_check': generic_processing.create_check(class_name, name),
                'process': generic_processing.create_process(class_name),
                'db_process': generic_processing.create_process(class_name),
                'viz': create_generic_plots(name, class_name),
            }

    def link(self, app):
        generic_callback.link(app)
        settings.link(app)

    def process_data(self, data_collection):
        args = []
        for viz_option, data in data_collection.items():
            args.append((self.name, viz_option, data, self.viz_options[viz_option]['process']))

        processed_data = [data_processing_task(*arg) for arg in args]

        return processed_data

    def render_settings(self):
        techs = list(utils.groups.keys())
        layout = html.Div([
            html.Div(
                dmc.Select(
                    id={
                        'type': 'general-technology-settings-dropdown',
                        'profile': self.name,
                    },
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
            html.Div(utils.tech_edit(techs[0], self.name),
                     id={
                         'type': 'general-technology-settings-output',
                         'profile': self.name,
                     }),
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
