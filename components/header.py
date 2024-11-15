import dash_mantine_components as dmc
from dash import html, dcc, Input, Output

from components import ids

HEIGHT = 40


def render(app):
    buttons = [
        # logo from ./assets/logo.png
        dcc.Link(
            html.Img(src='/assets/logo.png', alt='IDEA', className=ids.LOGO, height=HEIGHT),
            href='/',
        ),
        # buttons
        dmc.Button(
            'Load Data',
            variant='subtle',
            id={'type': ids.OPEN_MODAL, 'index': 'data'}
        ),
        dmc.Button(
            'Help',
            variant='subtle',
            id={'type': ids.OPEN_MODAL, 'index': 'help'}
        ),
    ]
    layout = html.Div(
        children=[
            dmc.Header(
                [
                    dmc.Group(buttons, spacing=1)
                ], height=HEIGHT, id=ids.HEADER
            ),
        ],
    )

    return layout
