import dash
from dash import Input, Output, State, ALL, callback_context, MATCH


def link(app):
    from main import data_handler
    app.callback(
        Output({'type': 'plot', 'index': MATCH}, 'figure'),
        Input({'type': 'figure', 'index': MATCH,
                'profile': ALL, 'viz': ALL}, 'figure'),
        State({'type': 'plot', 'index': MATCH}, 'figure'),
        prevent_initial_call=True,
    )(update_plot)


def update_plot(_figs, _plots):
    ctx = callback_context

    triggered_id = ctx.triggered_id
    triggered_value = ctx.triggered[0]['value']
    return triggered_value
