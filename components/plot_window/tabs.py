import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html
from dash_iconify import DashIconify

from assets.styles import hide_button_style, view_button_style
from components.plot_window import viz_container


def render(card_id):
    from main import data_handler

    profile_options = data_handler.get_viz_options()
    profiles = list(profile_options.keys())

    # sort keys by data_handler.profile_order
    profiles.sort(key=lambda x: data_handler.profile_order.index(x) if x in data_handler.profile_order else 1000)


    if not profiles:
        return html.Div()

    profile_tab_list = []

    for profile in profiles:
        profile_tab_list.append(
            dmc.Tab(
                dmc.Tooltip(
                    multiline=True,
                    # width=220,
                    withArrow=True,
                    transition="fade",
                    transitionDuration=200,
                    label=data_handler.profiles[profile].description,
                    children=[profile],
                )
                ,
                id={'type': 'profile-tab', 'index': card_id, 'profile': profile},
                value=profile,
            )
        )

    profile_tab = dmc.Tabs([
        dmc.TabsList(
            [
                *profile_tab_list
            ]
        )
    ],
        value=profiles[0],
        id={'type': 'profile-tabs', 'index': card_id}
    )

    viz_options = profile_options[profiles[0]]
    plots = [plot_option for plot_option in data_handler.profiles[profiles[0]].plot_order if
             plot_option in viz_options]

    viz_tab_list = []
    for viz_type in plots:
        viz_tab_list.append(
            dmc.Tab(
                dmc.Tooltip(
                    multiline=True,
                    # width=220,
                    withArrow=True,
                    transition="fade",
                    transitionDuration=200,
                    label=data_handler.profiles[profiles[0]].viz_options[viz_type].get('description', ''),
                    children=[viz_type]
                ),
                id={'type': 'viz-tab', 'index': card_id, 'profile': profiles[0],
                    'viz': viz_type},
                value=viz_type,
            )
        )
    viz_tab = dmc.Tabs([
        dmc.TabsList(
            [
                *viz_tab_list
            ]
        )
    ],
        value=plots[0],
        id={'type': 'viz-tabs', 'index': card_id, 'profile': profiles[0]}
    )

    widgets, plot = data_handler.get_viz(profiles[0], plots[0], card_id)
    _b, _w, _f, _hp = viz_container.render(card_id, profiles[0], plots[0], widgets, plot)
    layout = [
        dbc.Collapse(
            [
                profile_tab,
                html.Div(
                    viz_tab,
                    id={
                        'type': 'viz-tab-container',
                        'index': card_id
                    })
            ], id={'type': 'collapse-tabs', 'index': card_id},
            is_open=True,
        ),
        html.Div([
            _b,
            html.Div(
                [
                    dmc.ActionIcon(
                        html.Div(
                            DashIconify(icon='carbon:chevron-down'),
                            style={'text-align': 'center'}
                        ),
                        id={'type': 'view-tab', 'index': card_id},
                        size='sm',
                        radius='xl',
                        variant='outline',
                        style=hide_button_style
                    ),
                    dmc.ActionIcon(
                        html.Div(
                            DashIconify(icon='carbon:chevron-up'),
                            style={'text-align': 'center'}
                        ),
                        id={'type': 'hide-tab', 'index': card_id},
                        size='sm',
                        radius='xl',
                        variant='outline',
                        style=view_button_style
                    ),
                ]
                # center align
                , style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
            ),

            html.Div(),
        ],
            style={'display': 'flex',
                   # all in one row,
                   'justify-content': 'space-between', }
        ),
        # flexgroup _w and _f
        html.Div(
            [
                _w,
                _f
            ],
            style={'display': 'flex',
                   'justify-content': 'space-between',
                   'height': '90%',
                   'width': '100%'}
        ),
        _hp
    ]

    return layout
