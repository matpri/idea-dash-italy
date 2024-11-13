import dash
import dash_mantine_components as dmc
from dash import html, Output, Input, State
from dash_iconify import DashIconify
import base64

from components import ids
from components.data_selection import viz_edit_modal

def link(app):
    app.callback(
        Output(ids.DATA_SELECTED, 'children'),
        Output(ids.DB_SELECTED, 'children'),
        Output(ids.DATA_SELECTED_VIEW, 'value'),
        Output(ids.PROFILE_SELECT, 'data'),
        Output(ids.DATA_LOADING_NOTIFICATION, 'children'),
        Input(ids.DATA_UPLOAD, 'contents'),
        Input(ids.DB_LOAD_BUTTON, 'n_clicks'),
        Input(ids.UPDATE_CHIPS, 'n_clicks'),
        State(ids.DATA_UPLOAD, 'filename'),
        State( ids.DB_CHECKBOXES, 'value'),
        State(ids.DATA_SELECTED, 'children'),
        State(ids.DB_SELECTED, 'children'),
        prevent_initial_call=True,
    )(update_chips)


def update_chips(_contents, n_clicks, _update_chips,  filenames, selected_runs, views, db_views):
    from main import data_handler

    ctx = dash.callback_context

    if type(views) is str:
        views = []
    if type(db_views) is str:
        db_views = []
    if ctx.triggered_id == ids.UPDATE_CHIPS:
        views = []
        db_views = []
        return views, db_views, dash.no_update, dash.no_update, dash.no_update
    if ctx.triggered_id == ids.DB_LOAD_BUTTON:
        if n_clicks:
            for run in selected_runs:
                model, scenario, author, db = run.split('|')
                run = data_handler.select_run(model, scenario, author, db)
                db_views.append(dmc.Button(run, id={'type': ids.OPEN_MODAL, 'index': f'selected-{run}'},
                                           radius='xl', size='xs', compact=True,
                                           variant='light',
                                           leftIcon=DashIconify(icon='carbon:edit', width=10),
                                           style={'margin': '2px'}))
                db_views.append(viz_edit_modal.render(run))

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

    if filenames is not None:
        for i, filename in enumerate(filenames):
            file, extension = filename.split('.')
            if extension == 'pkl':
                data_handler.pkls[file] = base64.b64decode(_contents[i].split(',')[1])
                views.append(dmc.Button(file, id={'type': 'pkl', 'index': f'selected-{file}'},
                                        radius='xl', size='xs', compact=True,
                                        variant='light',
                                        style={'margin': '2px'}))

            elif extension == 'csv' or extension == 'xlsx':
                if file in selected_data.keys():
                    counter = 1
                    while f'{file}-{counter}' in selected_data.keys():
                        counter += 1
                    file = f'{file}-{counter}'

                checked, message, file = data_handler.check_content(file, _contents[i], extension)

                if not checked:
                    fail = True
                    messages.append(message)

                else:
                    profiles = list(data_handler.data[file]['visualizations'].keys())
                    colors = []
                    for p in profiles:
                        colors.append(data_handler.profiles[p].color)
                    # IDs are dictionaries now, to handle them use the MATCH and ALL special keywords
                    views.append(dmc.Button(file, id={'type': ids.OPEN_MODAL, 'index': f'selected-{file}'},
                                            radius='xl', size='xs', compact=True,
                                            variant='light',
                                            color=colors[0] if len(colors) == 1 else 'gray',
                                            leftIcon=DashIconify(icon='carbon:edit', width=10),
                                            style={'margin': '2px'}))
                    views.append(viz_edit_modal.render(file))
                    selected_data[file] = f'chip-{file}'
            else:
                fail = True
                messages.append(f'Only CSV or XLSX files are supported, {extension} is not supported')

        if fail:
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, [
                dmc.Alert(
                    message, color='red', title='Error',
                    withCloseButton=True
                ) for message in messages
            ]
        return views, dash.no_update, 'local', list(data_handler.data.keys()), dash.no_update