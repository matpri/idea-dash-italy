from functools import partial

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import Output, Input, State, html
from dash_iconify import DashIconify
from assets.styles import button_style

from components import data_viewer, settings,ids
from components.plot_window import window



def render(app):
    layout = html.Div([
        dmc.Aside(
            id='sidebar',
            className='my-aside',
            children=[
                dmc.Stack([
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
                    dmc.ActionIcon(
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
                    ),
                ])
            ],
            position={'top': '40%', 'left': 0},
            width={"base": 32},
            height=144,
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
        data_viewer.render(app),
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

    app.callback(
        Output(ids.PLOT_CANVAS, 'children'),
        Output('window-clear', 'is_open'),
        Input('add-card', 'n_clicks'),
        Input('delete-card', 'n_clicks'),

        Input('trash-button', 'n_clicks'),
        Input('cancel-delete-card', 'n_clicks'),
        State(ids.PLOT_CANVAS, 'children'),
        State('window-clear', 'is_open'),
        prevent_initial_call=True,
    )(edit_cards)

    app.callback(
        Output('settings-modal', 'opened'),
        Input('settings', 'n_clicks'),
        State('settings-modal', 'opened'),
        prevent_initial_call=True,
    )(show_settings_modal)

    return layout


def edit_cards(add_clicks, delete_click, trash_click, cancel_click, widgets, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return widgets

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'add-card':
        widgets.append(window.render())
        return widgets, is_open
    elif trigger == 'delete-card':
        ids.card_ids = []
        return [], False
    elif trigger == 'trash-button':
        return widgets, True
    elif trigger == 'cancel-delete-card':
        return widgets, False


def show_settings_modal(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open