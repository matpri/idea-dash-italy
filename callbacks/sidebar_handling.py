import dash
from dash import Output, Input, State

from components import ids
from components.plot_window import window


def link(app):
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