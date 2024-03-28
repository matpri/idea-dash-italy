import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

from assets.styles import glass_style

drawer_style = glass_style.copy()
drawer_style['height'] = '100%'


def render(card_id, viz_func):
    return dmc.Burger(
        id={'type': 'burger', 'index': card_id},
        opened=True,
        size='sm'
    ), dbc.Collapse(
        children=[dmc.Text("Widgets", align="left"),
                  html.Div(viz_func,
                           # style=drawer_style,
                           id={'type': 'drawer-content', 'index': card_id},
                           )]
        ,
        is_open=True,
        dimension="width",
        id={'type': 'drawer', 'index': card_id},
        style={
            'width': '20%',
            'height': '100%',
            'zIndex': 999,
            'background': 'linear-gradient(to right, rgba(255,255,255,0.4) 96%, rgba(0,0,0,0.1) 100%',
            'backdropFilter': 'blur(20px)',
            # 'borderRadius': '10px',
            'padding': '1rem',
            'marginTop': '1rem',
        }
    )
