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
    icons = []
    if not static:
        icons = [dmc.Tooltip(
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
            html.Div(html.Hr(style={'margin': '4px 0'}), style={'width': '100%'})]
    icons = icons + [
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
            html.Div(html.Hr(style={'margin': '4px 0'}), style={'width': '100%'}),
            # Group 3: Plot and Scenario Settings
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
            # Separator
            # Group 4: Save Current State

        ])

        icons = ([dmc.Tooltip(
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
                 ]
                 + icons
                 )
    icons = [dmc.Tooltip(
        label="IDEA Repository",
        position="right",
        offset=3,
        children=[
            dcc.Link(
                html.Img(src='/assets/logo.png', alt='IDEA', className=ids.LOGO, height=HEIGHT,
                         width=HEIGHT),
                href='https://gitlab.com/sesit/idea-dash',
                target='_blank',
                style={'padding': '0', 'margin': '0 auto', 'display': 'block'}
            )
        ]
    ),
                html.Div(html.Hr(style={'margin': '4px 0'}), style={'width': '100%'})] + icons + [
                     html.Div(html.Hr(style={'margin': '4px 0'}), style={'width': '100%'}),
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
                     ), ]

    layout = html.Div([
        dbc.Collapse([
            dmc.Aside(
                id='sidebar',
                className='my-aside',
                children=[
                    html.Div(icons, style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center',
                                           'gap': '4px'}),
                ],
                position={'top': '27%', 'left': 0} if not static else {'top': '42%', 'left': 0},
                width={"base": 62},
                height=432 if not static else 212,
                fixed=True,
                zIndex=9999,
                style={
                    'background': 'rgba(47,146,231,0.2)',
                    'border-radius': '0 10px 10px 0',
                    'backdrop-filter': 'blur(5px)',
                    'box-shadow': '0 4 30px 0 rgba(0, 0, 0, 0.2)',
                    'border': '1px solid rgba(47,146,231, 0.3)',
                    '-webkit-backdrop-filter': 'blur(5px)',
                    'padding': '4px 2px 4px 4px',
                    'display': 'block',
                    'margin-left': '0',
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
            position={'top': '50%', 'left': '62px'},
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
