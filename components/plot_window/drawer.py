import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html

from assets.styles import glass_style

drawer_style = glass_style.copy()
drawer_style['height'] = '100%'


def render(card_id, viz_func):
    layout = html.Div([
        dmc.Burger(
            id={'type': 'burger', 'index': card_id},
            opened=False,
            size='sm'
        ),
        dbc.Popover(
            target={'type': 'burger', 'index': card_id},
            children=[dmc.Text("Widgets", align="left"),
             html.Div(viz_func,
                      style=drawer_style,
                      id={'type': 'drawer-content', 'index': card_id},
                      )]
            ,
            is_open=False,
            body=True,
            trigger="legacy",
            style={
                'background': 'rgba(47,146,231,0.2)',
                'border-radius': '10px',
                'backdrop-filter': 'blur(5px)',
                'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.2)',
                'border': '1px solid rgba(47,146,231, 0.3)',
                '-webkit-backdrop-filter': 'blur(5px)',
                'padding': '4px 2px 4px 4px',
            },
            id={'type': 'drawer', 'index': card_id},
        ),
    ])

    return layout
