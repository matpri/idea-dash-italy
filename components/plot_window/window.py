import dash_lumino_components as dlc
from dash import html

from components import ids
from components.plot_window import tabs


def render():
    card_id = f'card-{len(ids.card_ids)}'
    ids.card_ids += [card_id]

    layout = dlc.Widget(
        html.Div(
        tabs.render(card_id),
        style={'height': '100%',
               'width': '100%',}

        ),
        id=card_id,
        title='',
        closable=False,
        icon='fa fa-chart-line'
    )

    return layout
