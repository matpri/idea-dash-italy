import dash_lumino_components as dlc
from dash import html

from components import ids
from components.plot_window import window


def render(static=False, num_custom_frames=0):
    from utils.data_state import  data_handler

    hide_welcome = bool(data_handler.processed_data)
    print('HIDE WELCOME:', hide_welcome)

    if not hide_welcome:
        layout = dlc.DockPanel([
            dlc.Widget(
                html.Img(
                    src='assets/welcome_static.png' if static else 'assets/welcome.png',
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
    elif num_custom_frames == 0:
        layout = dlc.DockPanel([
            window.render()
        ], id=ids.PLOT_CANVAS)
        return layout
    else:
        frames = []
        for i in range(num_custom_frames):
            frames.append(window.render(i))
        return dlc.DockPanel(frames, id=ids.PLOT_CANVAS)
