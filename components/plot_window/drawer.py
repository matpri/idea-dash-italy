import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

from assets.styles import glass_style
from components import ids

drawer_style = glass_style.copy()
drawer_style['height'] = '100%'

def render(card_id, viz_func):
    """
    Render the drawer component for the visualization.

    Parameters:
    - card_id: Unique identifier for the drawer.
    - viz_func: Function to render the visualization widgets.

    Returns:
    - A tuple containing the burger button and the collapse component.
    """
    return dmc.Burger(
        id={'type': ids.BURGER, 'index': card_id},
        opened=True,
        size='sm'
    ), dbc.Collapse(
        children=[dmc.Text("Widgets", align="left"),
                  html.Div(viz_func,
                           id={'type': 'drawer-content', 'index': card_id},
                           style={
                               'height': 'calc(100% - 1rem)',
                               'background': 'rgba(255,255,255,0.4)',
                               'backdropFilter': 'blur(20px)',
                               'zIndex': 999,
                               'position': 'relative',
                               'boxShadow': '0 0 10px 0 rgba(0,0,0,0.1)',
                               'border': '1px solid rgba(0,0,0,0.1)',
                               'borderRadius': '10px',
                               'padding': '1rem',
                               'marginTop': '1rem',
                           }
                           )]
        ,
        is_open=True,
        dimension="width",
        id={'type': ids.DRAWER, 'index': card_id},
        style={
            'width': '20%',
            'height': '100%',
        }
    )
