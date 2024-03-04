import dash
from dash import html, Input, Output, State
from assets.styles import hide_button_style, view_button_style
from components import ids

def link(app):
    @app.callback(
        [
            Output({'type': 'drawer', 'index': dash.dependencies.ALL}, 'is_open'),
            Output({'type': 'burger', 'index': dash.dependencies.ALL}, 'opened')
        ],
        [
            Input({'type': 'burger', 'index': dash.dependencies.ALL}, 'opened'),
            Input({'type': 'drawer', 'index': dash.dependencies.ALL}, 'is_open')
        ],
        prevent_initial_call=True,
    )
    def toggle_states(burgers_open, drawers_open):
        # Gather information about the triggering action
        ctx = dash.callback_context
        if not ctx.triggered:
            # No input has been triggered
            return drawers_open, burgers_open
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]   # using split as alternative to eval

        # Handle the scenario where drawer's state changes
        if 'drawer' in trigger_id:
            return drawers_open, drawers_open
        # Handle the scenario where burger's state changes
        elif 'burger' in trigger_id:
            return burgers_open, burgers_open
