import dash
from dash import html, Input, Output, State, MATCH, no_update, dcc
from components import ids


def link(app):
    @app.callback(
        Output({'type': ids.PLOT_POPUP_GRAPH, 'index': MATCH}, 'figure'),
        Output({'type': ids.PLOT_POPUP, 'index': MATCH}, 'opened'),
        Output({'type': ids.PLOT_POPUP_TITLE, 'index': MATCH}, 'value'),
        Output({'type': ids.PLOT_POPUP_X_LABEL, 'index': MATCH}, 'value'),
        Output({'type': ids.PLOT_POPUP_Y_LABEL, 'index': MATCH}, 'value'),
        Output({'type': ids.PLOT_POPUP_WIDTH, 'index': MATCH}, 'value'),
        Output({'type': ids.PLOT_POPUP_HEIGHT, 'index': MATCH}, 'value'),
        Input({'type': 'open_popup', 'index': MATCH}, 'n_clicks'),
        Input({'type': ids.PLOT_POPUP_FONT_SIZE, 'index': MATCH}, 'value'),
        Input({'type': ids.PLOT_POPUP_TITLE, 'index': MATCH}, 'value'),
        Input({'type': ids.PLOT_POPUP_X_LABEL, 'index': MATCH}, 'value'),
        Input({'type': ids.PLOT_POPUP_Y_LABEL, 'index': MATCH}, 'value'),
        Input({'type': ids.PLOT_POPUP_WIDTH, 'index': MATCH}, 'value'),
        Input({'type': ids.PLOT_POPUP_HEIGHT, 'index': MATCH}, 'value'),
        State({
            'type': ids.PLOT,
            'index': MATCH
        }, 'figure'),

        prevent_initial_call=True,
    )
    def open_plot_popup(n_clicks,
                        font_size,
                        title,
                        x_label,
                        y_label,
                        width,
                        height,
                        figure):
        if n_clicks is None:
            return no_update
        print('downloading graph', n_clicks)
        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if ids.PLOT_POPUP_WIDTH in triggered_id:
            # make sure the width is a a valid number and not a string
            try:
                width = int(width)
            except ValueError:
                width = 1920

        if ids.PLOT_POPUP_HEIGHT in triggered_id:
            # make sure the height is a a valid number and not a string
            try:
                height = int(height)
            except ValueError:
                height = 1080

        figure['layout']['template']['layout']['font']['size'] = font_size
        if 'open_popup' not in triggered_id:
            figure['layout']['title']['text'] = title
            figure['layout'].setdefault('xaxis', {}).setdefault('title', {})['text'] = x_label
            figure['layout'].setdefault('yaxis', {}).setdefault('title', {})['text'] = y_label
            return figure, no_update, no_update, no_update, no_update, no_update, no_update

        x_axis = figure['layout'].get('xaxis', {}).get('title', {}).get('text', '')
        y_axis = figure['layout'].get('yaxis', {}).get('title', {}).get('text', '')

        return figure, True, figure['layout']['title']['text'],x_axis, y_axis, width, height

    @app.callback(
        Output({'type': ids.PLOT_POPUP_COLLAPSE, 'index': MATCH}, 'is_open'),
        Output({'type': ids.PLOT_POPUP_BURGER, 'index': MATCH}, 'opened'),
        Input({'type': ids.PLOT_POPUP_COLLAPSE, 'index': MATCH}, 'is_open'),
        Input({'type': ids.PLOT_POPUP_BURGER, 'index': MATCH}, 'opened'),
        prevent_initial_call=True,
    )
    def toggle_burger(drawers_open, burgers_open):
        # Gather information about the triggering action
        ctx = dash.callback_context
        if not ctx.triggered:
            # No input has been triggered
            return drawers_open, burgers_open
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]  # using split as alternative to eval

        # Handle the scenario where drawer's state changes
        if ids.PLOT_POPUP_COLLAPSE in trigger_id:
            return drawers_open, drawers_open
        # Handle the scenario where burger's state changes
        elif ids.PLOT_POPUP_BURGER in trigger_id:
            return burgers_open, burgers_open
