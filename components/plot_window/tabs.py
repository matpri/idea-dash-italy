import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import html, dcc
from dash_iconify import DashIconify

from assets.styles import hide_button_style, view_button_style
from components.plot_window import viz_container

from components import ids


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
    _b, _w, _f, _md, _hp = viz_container.render(card_id, profiles[0], plots[0], widgets, plot)
    layout = [dbc.Collapse(
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
    ), html.Div([
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
        # export button
        dmc.ActionIcon(
            html.Div(
                DashIconify(icon='carbon:intent-request-scale-out'),
                style={'text-align': 'center'}
            ),
            id={'type': 'open_popup', 'index': card_id},
            size='sm',
            radius='xl',
            variant='outline',
            style=view_button_style
        ),

    ],
        style={'display': 'flex',
               # all in one row,
               'justify-content': 'space-between', }
    ), html.Div(
        [
            _w,
            _f,
            _md
        ],
        style={'display': 'flex',
               'justify-content': 'space-between',
               'height': '90%',
               'width': '100%'}
    ), _hp, render_popup(card_id, _f)]

    return layout


def render_popup(window_id, graph):
    """
    :return: dmc.Modal that has a dcc.Graph object. And a hidable Aside with widgets for font size, y/x-axis label and title.
    """
    figure = graph.figure
    return dmc.Modal(
        id={'type': ids.PLOT_POPUP, 'index': window_id},
        fullScreen=True,
        children=[

            dcc.Download(id={'type': 'fig-download', 'index': window_id}),
            html.Div(
                [
                    dmc.Burger(id={'type': ids.PLOT_POPUP_BURGER, 'index': window_id},
                               opened=False),
                    dmc.ActionIcon(
                        html.Div(
                            DashIconify(icon='carbon:download'),
                            style={'text-align': 'center'}
                        ),
                        id={'type': 'export-tab', 'index': window_id},
                        size='sm',
                        radius='sm',
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
                        id={'type': ids.PLOT_POPUP_COLLAPSE, 'index': window_id},
                        children=[
                            dmc.Text("Widgets", align="left"),
                            html.Div(
                                [
                                    # widgets for font size, y/x-axis label and title
                                    dmc.Slider(
                                        id={'type': ids.PLOT_POPUP_FONT_SIZE, 'index': window_id},
                                        min=8,
                                        max=24,
                                        step=1,
                                        value=12,
                                        style={'width': '100%'}
                                    ),
                                    dmc.TextInput(
                                        label='Title',
                                        id={'type': ids.PLOT_POPUP_TITLE, 'index': window_id},
                                        placeholder='Title',
                                        value=figure['layout']['title']['text'] if 'layout' in figure else '',
                                        style={'width': '100%'}
                                    ),
                                    dmc.TextInput(
                                        label='X-axis Label',
                                        id={'type': ids.PLOT_POPUP_X_LABEL, 'index': window_id},
                                        placeholder='X-axis Label',
                                        value=figure['layout']['xaxis']['title']['text'] if 'layout' in figure else '',
                                        style={'width': '100%'}
                                    ),
                                    dmc.TextInput(
                                        label='Y-axis Label',
                                        id={'type': ids.PLOT_POPUP_Y_LABEL, 'index': window_id},
                                        placeholder='Y-axis Label',
                                        value=figure['layout']['yaxis']['title']['text'] if 'layout' in figure else '',
                                        style={'width': '100%'}
                                    ),
                                    html.Div(
                                        # width and height of the saved image
                                        [
                                            dmc.TextInput(
                                                label='Width',
                                                id={'type': ids.PLOT_POPUP_WIDTH, 'index': window_id},
                                                placeholder='Width',
                                                value='1920',
                                                style={'width': '100%'}
                                            ),
                                            dmc.TextInput(
                                                label='Height',
                                                id={'type': ids.PLOT_POPUP_HEIGHT, 'index': window_id},
                                                placeholder='Height',
                                                value='1080',
                                                style={'width': '100%'}
                                            ),
                                        ],
                                        style={'display': 'flex',
                                               'justify-content': 'space-between'}
                                    )

                                ],
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
                        style={
                            'width': '20%',
                            'height': '100%',
                        }
                    ),
                    dcc.Graph(
                        id={'type': ids.PLOT_POPUP_GRAPH, 'index': window_id},
                        responsive=True,
                        style={
                            'width': '95vw',
                            'height': '85vh'
                        }
                    ),
                ],
                style={'display': 'flex',
                       'justify-content': 'space-between',
                       'height': '100%',
                       'width': '100%'}
            ),

        ],

        style={
            'height': '100%',
            'width': '100%'
        }
    )
