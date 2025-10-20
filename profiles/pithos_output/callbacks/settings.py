import base64

import dash
from dash import html
import yaml
from dash import Output, Input, State, ALL

from profiles.pithos_output import utils


def link(app):
    @app.callback(
    Output('pithos-settings-upload-yaml-output', 'children'),
    Input('pithos-settings-upload-yaml', 'contents'),
    State('pithos-settings-upload-yaml', 'filename'),
    )
    def update_settings(content, filename):
        #print('Updating Settings', content, filename)
        if content is None:
            return 'Using Base Profile'

        # check if the file is a yaml file
        if filename.split('.')[-1] != 'yaml':
            return 'Invalid File Type'

        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        # read yaml as dict
        settings = yaml.load(decoded, Loader=yaml.FullLoader)

        from utils.data_state import data_handler
        data_handler.profiles['PITHOS'].settings = settings
        return html.Div([
            html.Div('Settings Updated'),
            html.Div(f'Using {filename}'),
        ])

    @app.callback(
        Output('pithos-technology-settings-output', 'children'),
        Input('pithos-technology-select', 'value')
    )
    def update_tech_settings(tech):
        #print('updating tech settings', tech)
        return utils.tech_edit(tech)

    @app.callback(
        Output('pithos-plot-settings-output', 'children'),
        Input('pithos-plot-select', 'value')
    )
    def update_tech_settings(plot):
        #print('updating tech settings', plot)
        return utils.plot_edit(plot)

    @app.callback(
        Output({'type': 'pithos-tech-update', 'index': ALL}, 'disabled'),
        Input({'type': 'pithos-tech-update', 'index': ALL}, 'n_clicks'),
        Input({'type': 'pithos-tech-name', 'index': ALL}, 'value'),
        Input({'type': 'pithos-tech-group', 'index': ALL}, 'value'),
        Input({'type': 'pithos-tech-color', 'index': ALL}, 'value'),
        Input({'type': 'pithos-tech-group-color', 'index': ALL}, 'value'),
        State({'type': 'pithos-tech-update', 'index': ALL}, 'disabled'),
        prevent_initial_call=True
    )
    def tech_update(n_clicks, names, groups, colors, group_colors, disabled):
        #print('updating tech settings', n_clicks, names, groups, colors, group_colors, disabled)
        ctx = dash.callback_context

        if not ctx.triggered:
            return [False] * len(n_clicks)

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        trigger_id = ctx.triggered_id
        #print('trigger:', trigger, trigger_id)
        idx = 0
        for i, out in enumerate(ctx.outputs_list):
            if out['id']['index'] == trigger_id['index']:
                idx = i
                break

        if trigger_id['type'] == 'pithos-tech-update':
            disabled[idx] = True
            tech = trigger_id['index']
            utils.colors[tech] = colors[idx]['hex']
            utils.group_colors[groups[idx]] = group_colors[idx]['hex']
            utils.names[tech] = names[idx]
            utils.groups[tech] = groups[idx]

        else:
            disabled[idx] = False

        return disabled

    @app.callback(
        Output({'type': 'pithos-plot-update', 'index': ALL, 'subtype':ALL}, 'disabled'),
        Input({'type': 'pithos-plot-update', 'index': ALL, 'subtype':ALL}, 'n_clicks'),
        Input({'type': 'pithos-plot-title', 'index': ALL, 'subtype':ALL}, 'value'),
        Input({'type': 'pithos-plot-x-axis', 'index': ALL, 'subtype':ALL}, 'value'),
        Input({'type': 'pithos-plot-y-axis', 'index': ALL, 'subtype':ALL}, 'value'),
        State({'type': 'pithos-plot-update', 'index': ALL, 'subtype':ALL}, 'disabled'),
        prevent_initial_call=True
    )
    def plot_update(n_clicks, titles, x_axis, y_axis, disabled):
        #print('updating plot settings', n_clicks, titles, x_axis, y_axis, disabled)
        ctx = dash.callback_context

        if not ctx.triggered:
            return [False] * len(n_clicks)

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        trigger_id = ctx.triggered_id
        #print('trigger:', trigger, trigger_id)
        idx = 0
        for i, out in enumerate(ctx.outputs_list):
            if out['id']['index'] == trigger_id['index']:
                if trigger_id['type'] == 'pithos-plot-update':
                    disabled[idx] = True
                    plot = trigger_id['index']
                    sub_plots = trigger_id['subtype'].split('-')
                    for sub_plot in sub_plots:
                        utils.plot_settings[plot][sub_plot]['title'] = titles[idx]
                        utils.plot_settings[plot][sub_plot]['x_label'] = x_axis[idx]
                        utils.plot_settings[plot][sub_plot]['y_label'] = y_axis[idx]
        else:
            disabled[idx] = False

        return disabled








