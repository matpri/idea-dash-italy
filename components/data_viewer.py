from functools import partial

import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL

from components import ids


def render(app):
    from main import data_handler

    layout = dmc.Modal(
        title='Data Selection',
        opened=False,
        id='uploaded-data-modal',
        children=[
            dmc.Text('Select Data:'),
            dmc.Select(
                id='profile-select',
                data=list(data_handler.data.keys()),
                value=None,
                style={'marginBottom': '10px'}
            ),
            html.Div(
                id='view-data-div',
                children=[],
            ),
            dmc.Divider(),
            html.Div(
                [
                    dmc.Button('Submit', id='submit-data', variant='gradient'),
                    dmc.Button('Cancel', id='cancel-data', variant='outline'),
                ],
                style={'display': 'flex', 'justifyContent': 'space-between'}
            )

        ],
    )

    app.callback(
        Output('view-data-div', 'children'),
        Input('profile-select', 'value'),
        prevent_initial_call=True,
    )(update_chips)

    app.callback(
        Output('uploaded-data-modal', 'opened'),
        Input('data-viewer', 'n_clicks'),
        Input('submit-data',  'n_clicks'),
        Input('cancel-data', 'n_clicks'),
        State('uploaded-data-modal', 'opened'),
        State({'type': 'data-chip-group', 'file': ALL, 'profile': ALL}, 'value'),
        State({'type': 'scenario-name', 'file': ALL, }, 'value'),
        prevent_initial_call=True,
    )(view_modal)

    return layout


def update_chips(file):
    from main import data_handler
    chip_groups = []
    for profile, viz_options in data_handler.data[file]['visualizations'].items():
        chips = []
        for viz in viz_options:
            chips.append(dmc.Chip(
                viz,
                value=viz,
                id={'type': 'data-chip', 'file': file, 'profile': profile, 'viz': viz},
                size='sm',
            ))
        chip_groups.append(dmc.ChipGroup(
            children=chips,
            id={'type': 'data-chip-group', 'file': file, 'profile': profile},
            value=data_handler.data[file]['selected'][profile],
            multiple=True,
            style={'padding': '4px'}
        ))

    layout = html.Div(
        [
            dmc.TextInput(
                id={'type': 'scenario-name', 'file': file},
                label='Scenario Name',
                value=data_handler.data[file]['scenario'],
                placeholder='Enter Scenario Name',
                style={'marginBottom': '10px'}
            ),
            *chip_groups,
        ],
    )

    return layout


def view_modal(n_click, n_submit, n_cancel, is_open, values, scenario_names):
    print('update_modal', n_click, n_submit, n_cancel, is_open, values, scenario_names)
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    if not any([n_click, n_submit, n_cancel]):
        return is_open

    if triggered_input == 'data-viewer':
        return not is_open

    if triggered_input == 'submit-data':
        from main import data_handler
        for i, ls in enumerate(ctx.states_list[1]):
            chip = ls['id']
            file = chip['file']
            profile = chip['profile']
            data_handler.data[file]['selected'][profile] = values[i]
            data_handler.data[file]['scenario'] = scenario_names[i]
        data_handler.process_data()

        return not is_open

    if triggered_input == 'cancel-data':
        return not is_open

    return is_open
