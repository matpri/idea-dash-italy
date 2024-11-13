import dash
import dash_mantine_components as dmc
from dash import Output, Input, html

from components import ids
from components.data_selection import database_connection, local_files, selected_files, selected_db


def render(app):
    layout = dmc.Modal(
        title='Load Data',
        id={'type': ids.MODAL, 'index': 'data'},
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

                    html.Div([local_files.render(app), database_connection.render()], id=ids.DATA_LOADING_CONTENT,
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
                        selected_files.render(),
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
                dmc.Button('Submit', id={'type': ids.MODAL_SUBMIT_BUTTON, 'index': 'data'}),
                dmc.Button('Cancel', color='red', variant='outline',
                           id={'type': ids.MODAL_CLOSE_BUTTON, 'index': 'data'}, ),
            ], position='right'),]
        ),
    )



    return layout


