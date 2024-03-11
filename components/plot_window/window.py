import dash_lumino_components as dlc
import dash_mantine_components

from components import ids
from components.plot_window import tabs


def render():
    card_id = f'card-{len(ids.card_ids)}'
    ids.card_ids += [card_id]

    layout = dlc.Widget(
        dash_mantine_components.LoadingOverlay(
            tabs.render(card_id)
        ),
        id=card_id,
        title='',
        closable=True,
        icon='fa fa-chart-line'
    )

    return layout
