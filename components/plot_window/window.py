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
    card_id = f'card-{len(ids.card_ids)}'
    ids.card_ids += [card_id]
    link(card_id)

    layout = dlc.Widget(
        [
            html.Div(dmc.Button(
                'Hide',
                id={'type': 'hide-button', 'index': card_id},
            )),
            *tabs.render(card_id),

        ],
        id=card_id,
        title='',
        closable=True,
        icon='fa fa-chart-line'
    )

    return layout


def link(id):
    from main import app
    @app.callback(
        Output(id, 'children'),
        Input({'type': 'hide-button', 'index': dash.dependencies.ALL}, 'n_clicks'),
    )
    def hide_card(n_clicks):
        print('hiding card')
        if n_clicks:
            return html.Div(html.H1('Hidden'))
