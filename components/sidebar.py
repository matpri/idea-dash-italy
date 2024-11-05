from functools import partial

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Output, Input, State, html
from dash_iconify import DashIconify
from assets.styles import button_style

from components import data_viewer, settings,ids
from components.plot_window import window



def render(static):
    """
    :return: Rendering the sidebar containing the add window, clear windows, settings, and data viewer buttons.
    """
    icons = [
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:add'),
                        size='sm',
                        radius='xl',
                        variant='outline',
                        id='add-card',
                        className='my-button',
                        style=button_style
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:trash-can'),
                        size='sm',
                        radius='xl',
                        variant='outline',
                        id='trash-button',
                        className='my-button',
                        style=button_style
                    ),
                ]

    if not static:
        icons.extend([ dmc.ActionIcon(
                        DashIconify(icon='carbon:settings'),
                        size='sm',
                        radius='xl',
                        variant='outline',
                        id='settings',
                        className='my-button',
                        style=button_style
                    ),
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:db2-database'),
                        size='sm',
                        radius='xl',
                        variant='outline',
                        className='my-button',
                        style=button_style,
                        id='data-viewer'
                    ),])

    layout = html.Div([
        dmc.Aside(
            id='sidebar',
            className='my-aside',
            children=[
                dmc.Stack(icons)
            ],
            position={'top': '40%', 'left': 0} if not static else {'top': '50%', 'left': 0},
            width={"base": 32},
            height=144 if not static else 72,
            fixed=True,
            zIndex=9999,
            # round the corners
            style={
                'background': 'rgba(47,146,231,0.2)',
                'border-radius': '0 10px 10px 0',
                'backdrop-filter': 'blur(5px)',
                'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.2)',
                'border': '1px solid rgba(47,146,231, 0.3)',
                '-webkit-backdrop-filter': 'blur(5px)',
                'padding': '4px 2px 4px 4px',
            },

            withBorder=True,
        ),
        data_viewer.render(),
        settings.render(),
        dbc.Popover(
            target='trash-button',
            children=[
                dmc.Text("Clear all Windows?", align="center"),
                html.Div([
                    dmc.Button('Confirm', variant='light', color='red', id='delete-card'),
                    dmc.Button('Cancel', variant='light', id='cancel-delete-card')
                ], style={'display': 'flex', 'justify-content': 'center', 'gap': '10px'})
            ],
            body=True,
            is_open=False,
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
            hide_arrow=True,
            id='window-clear'
        )
    ]
    )

    return layout