from functools import partial

import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL

from components import ids


def render():
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



    return layout



