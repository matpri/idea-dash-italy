import dash_mantine_components as dmc
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash_iconify import DashIconify

from assets.styles import view_button_style
from components import ids


def render():
    """
    :return: dmc.Modal that has a dcc.Graph object. And a hidable Aside with widgets for font size, y/x-axis label and title.
    """

    return dmc.Modal(
        id=ids.PLOT_POPUP,
        title='Plot',
        children=[

            dcc.Download(id='fig-download'),
            html.Div(
                [
                    dmc.Burger(id=ids.PLOT_POPUP_BURGER, opened=False),
                    dmc.ActionIcon(
                        html.Div(
                            DashIconify(icon='carbon:download'),
                            style={'text-align': 'center'}
                        ),
                        id='export-tab',
                        size='sm',
                        radius='xl',
                        variant='outline',
                        style=view_button_style
                    ),
                ],
                style={'display': 'flex',
                       # all in one row,
                       'justify-content': 'space-between', }
            ),
            html.Div(
                [
                    dbc.Collapse(
                        children=[
                            dmc.Text("Widgets", align="left"),
                            html.Div(
                                id=ids.PLOT_POPUP_WIDGETS,
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
                            )
                        ],
                        is_open=False,
                        dimension="width",
                        id=ids.PLOT_POPUP_DRAWER,
                        style={
                            'width': '20%',
                            'height': '100%',
                        }
                    ),

                    dcc.Graph(
                        id=ids.PLOT_POPUP_GRAPH,
                        style={
                            'width': '100%',
                            'height': '100%'
                        }
                    )
                ]
            )

        ]
    )
