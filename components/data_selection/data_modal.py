import dash
import dash_mantine_components as dmc
from dash import Output, Input, html

from components import ids
from components.data_selection import database_connection, local_files, selected_files, selected_db


def render(app):
    layout = dmc.Modal(
        title='Load Data',
        id={'type': 'modal', 'index': 'load_data'},
        zIndex=10000,
        size='75%',
        closeOnClickOutside=True,
        children=dmc.LoadingOverlay([
            dmc.Stack([
                html.Div([
                    dmc.Center([
                        dmc.ButtonGroup([
                            dmc.Button('Local File', id=ids.LOCAL_FILE_BUTTON, variant='gradient',
                                       gradient={'from': 'indigo', 'to': 'cyan'}, fullWidth=True),
                            dmc.Button('Database', id=ids.DATABASE_BUTTON, variant='outline', color='indigo',
                                       fullWidth=True),
                        ], style={'width': '80%', 'display': 'flex', 'justifyContent': 'space-between'}),
                    ]),

                    html.Div([local_files.render(app), database_connection.render(app)], id=ids.DATA_LOADING_CONTENT,
                             style={'display': 'flex', 'flexFlow': 'column', 'alignItems': 'center', 'width': '100%'}),
                ],
                    style={'width': '100%', 'display': 'flex', 'justifyContent': 'center',
                           # content in one column
                           'flexFlow': 'column',
                           'background': 'rgba(255, 255, 255, 0.4)',
                           'backdropFilter': 'blur(20px)',
                           'borderRadius': '10px',
                           'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
                           'padding': '1rem',
                           'marginTop': '1rem',
                           }

                ),
                dmc.Divider(),
                html.Div(
                    dmc.AccordionMultiple([
                        selected_files.render(app),
                        selected_db.render()],
                        style={'width': '100%', 'alignItems': 'center'},
                        id=ids.DATA_SELECTED_VIEW,
                        value='local',
                    ),
                    style={'width': '100%', 'display': 'flex', 'justifyContent': 'center',
                           # content in one column
                           'flexFlow': 'column',
                           'background': 'rgba(255, 255, 255, 0.4)',
                           'backdropFilter': 'blur(20px)',
                           'borderRadius': '10px',
                           'boxShadow': '10px 10px 15px rgba(0, 0, 0, 0.1)',
                           'padding': '1rem',
                           'marginTop': '1rem',
                           }),
            ],
            ),
            dmc.Space(h=20),
            dmc.Group([
                dmc.Button('Submit', id={'type': 'modal-submit-button', 'index': 'load_data'}),
                dmc.Button('Cancel', color='red', variant='outline',
                           id={'type': 'modal-close-button', 'index': 'load_data'}, ),
            ], position='right'),]
        ),
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
        return "gradient", "outline", {"width": "60%", 'display': 'block'}, {"width": "80%", 'display': 'none'}
    else:
        return "outline", "gradient", {"width": "60%", 'display': 'none'}, {"width": "80%", 'display': 'block'}
