import json
import urllib.request as urllib

import dash
import dash_mantine_components as dmc
import pandas as pd
from dash import html, Input, Output, State

from components import ids
from components.data_selection import db_selector


def render():
    layout = html.Div([
        html.Div([
            dmc.TextInput(
                placeholder="Enter your API key",
                label="API Key",
                id=ids.API_KEY_INPUT,
                required=True,
                style={'marginBottom': '4px', 'width': '80%',
                       # center the input
                       'display': 'block',
                       'marginLeft': 'auto',
                       'marginRight': 'auto'}
            ),
            dmc.Button('Connect', id=ids.DATABASE_CONNECT_BUTTON, variant='gradient',
                       gradient={'from': 'indigo', 'to': 'cyan'}, fullWidth=True, disabled=True,
                       style={'width': '60%',
                              # center the button
                              'display': 'block',
                              'marginLeft': 'auto',
                              'marginRight': 'auto'
                              }),
        ], id=ids.DATABASE_INPUT, style={'width': '100%', 'display': 'block'}),
        html.Div([
            html.Div([
                dmc.Select(
                    id=ids.MODEL_SELECT,
                    label='Select Run',
                    data=[{'label': 'ALL', 'value': 'ALL'}],
                    value='ALL'
                ),
                dmc.Select(
                    id=ids.SCENARIO_SELECT,
                    label='Select Scenario',
                    data=[{'label': 'ALL', 'value': 'ALL'}],
                    value='ALL'
                ),
                dmc.Select(
                    id=ids.AUTHOR_SELECT,
                    label='Select Author',
                    data=[{'label': 'ALL', 'value': 'ALL'}],
                    value='ALL'
                ),
                dmc.Select(
                    id=ids.DB_SELECT,
                    label='Select DB',
                    data=[{'label': 'ALL', 'value': 'ALL'}],
                    value='ALL'
                ),
            ],
                style={'display': 'flex', 'flexFlow': 'row', 'justifyContent': 'space-between',
                       'width': '80%', 'marginLeft': 'auto', 'marginRight': 'auto'}),

            db_selector.render(),
            dmc.Button('Load', id=ids.DB_LOAD_BUTTON, variant='gradient',
                       gradient={'from': 'indigo', 'to': 'cyan'}, fullWidth=True,
                       style={'width': '80%',
                              # center the button
                              'display': 'block',
                              'marginLeft': 'auto',
                              'marginRight': 'auto'
                              }),
        ],
            id=ids.DB_CONNECTED,
            style={'display': 'none'}
        )

    ], id=ids.DATABASE_VIEW, style={"width": "100%", 'display': 'none'})



    return layout



