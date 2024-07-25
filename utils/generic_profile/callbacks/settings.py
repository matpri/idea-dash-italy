import dash
from dash import Output, Input, State, ALL, MATCH

from utils.generic_profile import utils


def link(app):
    @app.callback(
        Output({
            'type': 'general-technology-settings-output',
            'profile': MATCH,
        }, 'children'),
        Input({
            'type': 'general-technology-settings-dropdown',
            'profile': MATCH,
        }, 'value')
    )
    def update_tech_settings(tech):
        print('updating tech settings', tech)

        # get profile from the callback context
        ctx = dash.callback_context
        profile = ctx.triggered[0]['prop_id'].split('.')[0]['profile']

        return utils.tech_edit(tech, profile)

    @app.callback(
        Output({'type': 'generic-tech-update', 'index': ALL, 'profile': MATCH}, 'disabled'),
        Input({'type': 'generic-tech-update', 'index': ALL, 'profile': MATCH}, 'n_clicks'),
        Input({'type': 'generic-tech-name', 'index': ALL, 'profile': MATCH}, 'value'),
        Input({'type': 'generic-tech-group', 'index': ALL, 'profile': MATCH}, 'value'),
        Input({'type': 'generic-tech-color', 'index': ALL, 'profile': MATCH}, 'value'),
        Input({'type': 'generic-tech-group-color', 'index': ALL, 'profile': MATCH}, 'value'),
        State({'type': 'generic-tech-update', 'index': ALL, 'profile': MATCH}, 'disabled'),
        prevent_initial_call=True
    )
    def tech_update(n_clicks, names, groups, colors, group_colors, disabled):
        print('updating tech settings', n_clicks, names, groups, colors, group_colors, disabled)
        ctx = dash.callback_context

        if not ctx.triggered:
            return [False] * len(n_clicks)

        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        trigger_id = ctx.triggered_id
        print('trigger:', trigger, trigger_id)
        idx = 0
        for i, out in enumerate(ctx.outputs_list):
            if out['id']['index'] == trigger_id['index']:
                idx = i
                break

        if trigger_id['type'] == 'generic-tech-update':
            disabled[idx] = True
            tech = trigger_id['index']
            utils.colors[tech] = colors[idx]['hex']
            utils.group_colors[groups[idx]] = group_colors[idx]['hex']
            utils.names[tech] = names[idx]
            utils.groups[tech] = groups[idx]

        else:
            disabled[idx] = False

        return disabled
