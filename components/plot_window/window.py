import dash
import dash_lumino_components as dlc
from dash import html, Output, Input, State
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import dash_bootstrap_components as dbc

from assets.styles import hide_button_style, view_button_style
from components import ids
from components.plot_window import drawer, tabs, viz_container


def render():
    from main import app
    card_id = f'card-{len(ids.card_ids)}'
    ids.card_ids += [card_id]

    layout = dlc.Widget(
        [
            *tabs.render(card_id)
        ],
        id=card_id,
        title='',
        closable=True,
        icon='fa fa-chart-line'
    )

    @app.callback(
        Output(card_id, 'title'),
        Input(card_id, 'deleted')
    )
    def remove_card(closed):
        print('removing card')
        if closed:
            ids.card_ids.remove(card_id)


    return layout
