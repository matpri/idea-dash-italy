import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL
from components import ids
import pickle

def link(app):
    app.callback(
        Output(ids.SAVE_BUTTON, 'n_clicks'),
        Input(ids.SAVE_BUTTON, 'n_clicks'),
        prevent_initial_call=True,
    )(pickle_datahandler)

def pickle_datahandler(value):
    from main import data_handler
    print('PICKLING DATAHANDLER to datahandler.pkl')
    data_handler.save('datahandler.pkl')
    return dash.no_update