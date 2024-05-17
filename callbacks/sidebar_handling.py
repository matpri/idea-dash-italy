import dash
from dash import Output, Input, State, html
import dash_mantine_components as dmc

from components import ids
from components.plot_window import window, tabs


def link(app):
    app.callback(
        Output(ids.PLOT_CANVAS, 'children'),
        Output('window-clear', 'is_open'),
        Input('add-card', 'n_clicks'),
        Input('delete-card', 'n_clicks'),
        Input('trash-button', 'n_clicks'),
        Input('cancel-delete-card', 'n_clicks'),
        Input(ids.DATA_CHANGE, 'n_clicks'),
        Input(ids.SETTINGS_CHANGE, 'n_clicks'),
        Input(ids.AFTER_CHANGE, 'n_clicks'),
        State(ids.PLOT_CANVAS, 'children'),
        State('window-clear', 'is_open'),
        prevent_initial_call=True,
    )(edit_cards)

    app.callback(
        Output('settings-modal', 'opened'),
        Output('settings-modal', 'children'),
        Input('settings', 'n_clicks'),
        State('settings-modal', 'opened'),
        State('settings-modal', 'children'),
        prevent_initial_call=True,
    )(show_settings_modal)

    app.callback(
        Output(ids.SETTINGS_CHANGE, 'n_clicks'),
        Input('settings-modal', 'opened'),
        State(ids.SETTINGS_CHANGE, 'n_clicks'),
        prevent_initial_call=True,
    )(update_windows)


def update_windows(is_open, n_clicks):
    if is_open is None:
        return dash.no_update
    if not is_open:
        if n_clicks is None:
            return 1
        return n_clicks + 1
    return dash.no_update


def edit_cards(add_clicks, delete_click, trash_click, cancel_click, d_change, s_change, a_change,
               widgets, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        return widgets

    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger == 'add-card':
        widgets.append(window.render())
        return widgets, is_open
    if trigger == 'delete-card':
        ids.card_ids = []
        return [], False
    if trigger == 'trash-button':
        return widgets, True
    if trigger == 'cancel-delete-card':
        return widgets, False
    if trigger in [ids.DATA_CHANGE, ids.SETTINGS_CHANGE, ids.AFTER_CHANGE]:
        ids.card_ids = []
        updated_widgets = []
        for widget in widgets:
            updated_widgets.append(window.render())
        return updated_widgets, is_open


def show_settings_modal(n_clicks, is_open, _children):
    from main import data_handler
    tab_contents = []
    tabs = []
    for profile_name, profile in data_handler.profiles.items():
        tabs.append(
            dmc.Tab(
                value=profile_name,
                children=profile_name
            )
        )

        tab_contents.append(
            dmc.TabsPanel(
                value=profile_name,
                children=profile.settings
            )
        )

    _children = html.Div(
            [
                dmc.Tabs(
                    [
                        dmc.TabsList(children=tabs),
                        *tab_contents,
                    ],
                ),
            ]
        )
    if n_clicks:
        return not is_open, _children
    return is_open, _children
