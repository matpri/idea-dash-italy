import dash
from dash import html, Input, Output, State
from assets.styles import hide_button_style, view_button_style
from components import ids

def link(app):
    @app.callback(
        [
            Output({'type': ids.DRAWER, 'index': dash.dependencies.ALL}, 'is_open'),
            Output({'type': ids.BURGER, 'index': dash.dependencies.ALL}, 'opened')
        ],
        [
            Input({'type': ids.BURGER, 'index': dash.dependencies.ALL}, 'opened'),
            Input({'type': ids.DRAWER, 'index': dash.dependencies.ALL}, 'is_open')
        ],
        prevent_initial_call=True,
    )
    def toggle_states(burgers_open, drawers_open):
        """
        This callback is used to toggle the state of the burger and drawer.
        It is triggered by the burger or drawer being clicked in a tab, to hide or show the drawer/ burger.
        """
        
        # Gather information about the triggering action
        ctx = dash.callback_context
        if not ctx.triggered:
            # No input has been triggered
            return drawers_open, burgers_open
        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]   # using split as alternative to eval

        # Handle the scenario where drawer's state changes
        if ids.DRAWER in trigger_id:
            return drawers_open, drawers_open
        # Handle the scenario where burger's state changes
        elif ids.BURGER in trigger_id:
            return burgers_open, burgers_open
