import dash
import dash_mantine_components as dmc
from dash import Output, Input, html

from components import ids
from components.data_selection import database_connection, local_files, selected_files, selected_db


def render(app):
    layout = dmc.Modal(
        title='Load Data',
        id={'type': 'modal', 'index': 'data'},
        zIndex=10000,
        size='75%',
        closeOnClickOutside=True,
        children=[
            dmc.Stack([
                dmc.Center([
                    dmc.ButtonGroup([
                        dmc.Button('Local File', id=ids.LOCAL_FILE_BUTTON, variant='gradient',
                                   gradient={'from': 'indigo', 'to': 'cyan'}, fullWidth=True),
                        dmc.Button('Database', id=ids.DATABASE_BUTTON, variant='outline', color='indigo',
                                   fullWidth=True),
                    ], style={'width': '80%', 'display': 'flex', 'justifyContent': 'space-between'}),
                ]),
                html.Div([local_files.render(app), database_connection.render(app)], id=ids.DATA_LOADING_CONTENT,
                         style={'display': 'flex', 'flexFlow': 'column', 'alignItems': 'center'}),
                dmc.Divider(),
                html.Div(
                    dmc.AccordionMultiple([
                        selected_files.render(app),
                        selected_db.render()],
                        style={'width': '100%', 'alignItems': 'center'},
                        id=ids.DATA_SELECTED_VIEW,
                        value='local',
                    ),
                    style={'display': 'flex', 'flexFlow': 'column', 'alignItems': 'center'}),
            ]),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button('Submit', id={'type': 'modal-submit-button', 'index': 'data'}),
                dmc.Button('Cancel', color='red', variant='outline',
                           id={'type': 'modal-close-button', 'index': 'data'}, ),
            ], position='right'),
        ],
    )

    app.callback(
        Output(ids.LOCAL_FILE_BUTTON, "variant"),
        Output(ids.DATABASE_BUTTON, "variant"),
        Output(ids.DATA_LOCAL_INPUT, "style"),
        Output(ids.DATABASE_VIEW, "style"),
        Input(ids.LOCAL_FILE_BUTTON, "n_clicks"),
        Input(ids.DATABASE_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )(toggle_button)

    return layout


def toggle_button(local, db):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == ids.LOCAL_FILE_BUTTON:
        return "gradient", "outline", {"width": "60%", 'display': 'block'}, {"width": "60%", 'display': 'none'}
    else:
        return "outline", "gradient", {"width": "60%", 'display': 'none'}, {"width": "60%", 'display': 'block'}
