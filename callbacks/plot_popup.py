import dash
from dash import html, Input, Output, State, MATCH, no_update, dcc
from components import ids

def link(app):
    @app.callback(
        Output( {'type': ids.PLOT_POPUP_GRAPH, 'index': MATCH}, 'figure'),
        Output( {'type': ids.PLOT_POPUP, 'index': MATCH}, 'opened'),
        Input({'type': 'open_popup', 'index': MATCH}, 'n_clicks'),
        State({
            'type': ids.PLOT,
            'index': MATCH
        }, 'figure'),

        prevent_initial_call=True,
    )
    def open_plot_popup(n_clicks, figure):

        if n_clicks is None:
            return no_update
        print('downloading graph', n_clicks)
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if 'open_popup' not in triggered_id:
            return no_update

        return figure, True

