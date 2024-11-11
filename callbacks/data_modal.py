import dash
from dash import Output, Input

from components import ids

def link(app):
    app.callback(
        Output(ids.LOCAL_FILE_BUTTON, "variant"),
        Output(ids.DATABASE_BUTTON, "variant"),
        Output(ids.DATA_LOCAL_INPUT, "style"),
        Output(ids.DATABASE_VIEW, "style"),
        Input(ids.LOCAL_FILE_BUTTON, "n_clicks"),
        Input(ids.DATABASE_BUTTON, "n_clicks"),
        prevent_initial_call=True,
    )(toggle_button)

def toggle_button(local, db):
    ctx = dash.callback_context
    triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_input == ids.LOCAL_FILE_BUTTON:
        return "gradient", "outline", {"width": "60%", 'display': 'block'}, {"width": "80%", 'display': 'none'}
    else:
        return "outline", "gradient", {"width": "60%", 'display': 'none'}, {"width": "80%", 'display': 'block'}
