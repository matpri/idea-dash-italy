import dash_lumino_components as dlc
from dash import html

from components import ids
from components.plot_window import tabs


def render(custom_frame_index=-1):
    """
    Render a new plot window with tabs.

    This function creates a new card for the plot window and initializes
    the layout with tabs for visualizations.

    Returns:
    - The layout of the plot window.
    """
    card_id = f'card-{len(ids.card_ids)}'
    ids.card_ids += [card_id]

    layout = dlc.Widget(
        html.Div(
            tabs.render(card_id, custom_frame_index),
            style={'height': '100%', 'width': '100%'}
        ),
        id=card_id,
        title='',
        closable=False,
        icon='fa fa-chart-line'
    )

    return layout
