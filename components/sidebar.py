from functools import partial

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Output, Input, State, html, dcc
from dash_iconify import DashIconify
from assets.styles import button_style, hide_button_style

from components import data_viewer, settings, ids
from components.plot_window import window

HEIGHT = 48


def render(static):
    """
    :return: Rendering the sidebar containing the add window, clear windows, settings, and data viewer buttons.
    """
    icons = [
        dmc.Tooltip(
            label="Help",
            position="right",
            offset=3,
            children=[
                dmc.ActionIcon(
                    DashIconify(icon='carbon:help'),
                    size='lg',
                    radius='xl',
                    variant='outline',
                    id={'type': ids.OPEN_MODAL, 'index': 'help'},
                    className='my-button',
                    style=button_style
                )
            ]
        ),
        dmc.Tooltip(
            label="Add Card",
            position="right",
            offset=3,
            children=[
                dmc.ActionIcon(
                    DashIconify(icon='carbon:add'),
                    size='lg',
                    radius='xl',
                    variant='outline',
                    id='add-card',
                    className='my-button',
                    style=button_style
                )
            ]
        ),
        dmc.Tooltip(
            label="Clear Cards",
            position="right",
            offset=3,
            children=[
                dmc.ActionIcon(
                    DashIconify(icon='carbon:trash-can'),
                    size='lg',
                    radius='xl',
                    variant='outline',
                    id='trash-button',
                    className='my-button',
                    style=button_style
                )
            ]
        ),
    ]

    if not static:
        icons.extend([
            dmc.Tooltip(
                label="Plot Settings",
                position="right",
                offset=3,
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:settings'),
                        size='lg',
                        radius='xl',
                        variant='outline',
                        id='settings',
                        className='my-button',
                        style=button_style
                    )
                ]
            ),
            dmc.Tooltip(
                label="Scenario Settings",
                position="right",
                offset=3,
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:db2-database'),
                        size='lg',
                        radius='xl',
                        variant='outline',
                        className='my-button',
                        style=button_style,
                        id='data-viewer'
                    )
                ]
            ),
            dmc.Tooltip(
                label="Save Current State",
                position="right",
                offset=3,
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:save'),
                        size='lg',
                        radius='xl',
                        variant='outline',
                        className='my-button',
                        style=button_style,
                        id=ids.SAVE_BUTTON
                    )
                ]
            ),
            dcc.Download(id='download-datahandler'),
        ])

        icons = [
            dcc.Link(
                html.Img(src='/assets/logo.png', alt='IDEA', className=ids.LOGO, height=HEIGHT),
                href='/',
                style={'margin': '0 auto', 'padding-bottom': '0', 'margin-bottom': '0'}
            ),
            dmc.Tooltip(
                label="Upload Data",
                position="right",
                offset=3,
                children=[
                    dmc.ActionIcon(
                        DashIconify(icon='carbon:upload'),
                        size='lg',
                        radius='xl',
                        variant='outline',
                        className='my-button',
                        style=button_style,
                        id={'type': ids.OPEN_MODAL, 'index': 'data'}
                    )
                ]
            )
        ] + icons

    layout = html.Div([
        dbc.Collapse([
            dmc.Aside(
                id='sidebar',
                className='my-aside',
                children=[
                    dmc.Stack(icons)
                ],
                position={'top': '30%', 'left': 0} if not static else {'top': '50%', 'left': 0},
                width={"base": 48},
                height=440 if not static else 110,
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
                    'display': 'block'
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
        ], id='sidebar-collapse', is_open=True),
        # Separate Aside for the collapse button
        dmc.Aside(
            id='collapse-sidebar-container',
            className='my-aside',
            children=[
                dmc.Tooltip(
                    label="Collapse Sidebar",
                    position="right",
                    offset=3,
                    children=[
                        dmc.ActionIcon(
                            DashIconify(icon='carbon:chevron-left'),
                            size='lg',
                            radius='xl',
                            variant='outline',
                            id='collapse-sidebar',
                            className='my-button',
                            style=button_style
                        )
                    ]
                ),
                dmc.Tooltip(
                    label="Expand Sidebar",
                    position="right",
                    offset=3,
                    children=[
                        dmc.ActionIcon(
                            DashIconify(icon='carbon:chevron-right'),
                            size='lg',
                            radius='xl',
                            variant='outline',
                            id='view-sidebar',
                            className='my-button',
                            style=hide_button_style
                        )
                    ]
                ),
            ],
            position={'top': '50%', 'left': '48px'},  # Centered vertically
            width={"base": 48},
            height=36,
            fixed=True,
            zIndex=9998,
            style={
                'background': 'transparent',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
            }
        ),
    ])

    return layout
