import dash_lumino_components as dlc
from dash import html

from components import ids


def render():
    layout = dlc.DockPanel([
        dlc.Widget(
            html.Img(
                src='assets/welcome.png',
                style={'width': '100%', 'height': '100%',
                       'object-fit': 'cover',
                       'object-position': 'center',

                       }
            ),
            id='welcome',
            title='Welcome',
            closable=True,
        )
    ], id=ids.PLOT_CANVAS)
    return layout
