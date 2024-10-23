import dash_lumino_components as dlc
from dash import html

from components import ids
from components.plot_window import window


def render(hide_welcome=True):
    if not hide_welcome:
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
                closable=False,
            )
        ], id=ids.PLOT_CANVAS)
        return layout
    else:
        layout = dlc.DockPanel([
            window.render()
        ], id=ids.PLOT_CANVAS)
        return layout
