import base64
import io
from functools import partial
from typing import List, Dict

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, Output, Input, State
from dash_iconify import DashIconify

from components import ids
from components.data_selection import viz_edit_modal


def render(app):
    layout = dmc.AccordionItem([
        dmc.AccordionControl('Local Files:'),
        dmc.AccordionPanel('Upload Local Results file', id=ids.DATA_SELECTED)
    ],
        value='local',
        style={'width': '100%'})

    app.callback(
        Output(ids.DATA_SELECTED, 'children'),
        Output(ids.DB_SELECTED, 'children'),
        Output(ids.DATA_SELECTED_VIEW, 'value'),
        Output('profile-select', 'data'),
        Output('data-loading-notification', 'children'),
        Input(ids.DATA_UPLOAD, 'contents'),
        Input(ids.DB_LOAD_BUTTON, 'n_clicks'),
        Input(ids.UPDATE_CHIPS, 'n_clicks'),
        State(ids.DATA_UPLOAD, 'filename'),
        State('db-checkboxes', 'value'),
        State(ids.DATA_SELECTED, 'children'),
        prevent_initial_call=True,
    )(partial(update_chips, app=app))
    return layout


def check_content(content, found_profiles) -> Dict[str, List[str]]:
    if content is None:
        return {}

    # decode the content string
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)

    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    visualizations = {}
    for profile_name, profile in found_profiles.items():
        for viz_name, viz_dict in profile.viz_options.items():
            if viz_name not in visualizations:
                check_func = viz_dict.get('check')
                if check_func(df):
                    if visualizations.get(profile.name) is None:
                        visualizations[profile.name] = []
                    visualizations[profile.name].append(viz_name)
    return visualizations


def update_chips(_contents, n_clicks, _update_chips,  filenames, selected_runs, views, app):
    from main import data_handler

    ctx = dash.callback_context
    db_views = []
    if ctx.triggered_id == ids.DB_LOAD_BUTTON:
        if n_clicks:
            for run in selected_runs:
                model, scenario, author, db = run.split('|')
                data_handler.select_run(model, scenario, author, db)
                db_views.append(dmc.Button(run, id={'type': 'open-modal', 'index': f'selected-{run}'},
                                           radius='xl', size='xs', compact=True,
                                           variant='light',
                                           leftIcon=DashIconify(icon='carbon:edit', width=10),
                                           style={'margin': '2px'}))
                db_views.append(viz_edit_modal.render(app, run))

            db_layout = html.Div(
                [
                    dmc.Text('Database:'),
                    *db_views
                ]
            )

            return dash.no_update, db_layout, 'db', list(data_handler.data.keys()), dash.no_update

    selected_data = {}
    fail = False
    messages = []
    if type(views) is str:
        views = []
    if ctx.triggered_id == ids.UPDATE_CHIPS:
        views = []

    if filenames is not None:
        for i, filename in enumerate(filenames):
            file, extension = filename.split('.')

            if extension == 'csv' or extension == 'xlsx':
                if file in selected_data.keys():
                    counter = 1
                    while f'{file}-{counter}' in selected_data.keys():
                        counter += 1
                    file = f'{file}-{counter}'

                checked, message = data_handler.check_content(file, _contents[i], extension)

                if not checked:
                    fail = True
                    messages.append(message)

                else:
                    profiles = list(data_handler.data[file]['visualizations'].keys())
                    colors = []
                    for p in profiles:
                        colors.append(data_handler.profiles[p].color)
                    # IDs are dictionaries now, to handle them use the MATCH and ALL special keywords
                    views.append(dmc.Button(file, id={'type': 'open-modal', 'index': f'selected-{file}'},
                                            radius='xl', size='xs', compact=True,
                                            variant='light',
                                            color=colors[0] if len(colors) == 1 else 'gray',
                                            leftIcon=DashIconify(icon='carbon:edit', width=10),
                                            style={'margin': '2px'}))
                    views.append(viz_edit_modal.render(app, file))
                    selected_data[file] = f'chip-{file}'
            else:
                fail = True
                messages.append(f'Only CSV or XLSX files are supported, {extension} is not supported')

        if fail:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, [
                dmc.Alert(
                    f'Message', color='red', title='Error',
                    withCloseButton=True
                ) for message in messages
            ]
        return views, dash.no_update, 'local', list(data_handler.data.keys()), dash.no_update
