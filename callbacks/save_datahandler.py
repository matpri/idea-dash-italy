import dash
import dash_mantine_components as dmc
from dash import html, Input, Output, State, ALL, dcc
from components import ids
import pickle

def link(app):
    app.callback(
        Output(ids.SAVE_BUTTON, 'n_clicks'),
        Output('download-datahandler', 'data'),
        Input(ids.SAVE_BUTTON, 'n_clicks'),
        prevent_initial_call=True,
    )(pickle_datahandler)

def pickle_datahandler(value):
    from utils.data_state import data_handler
    print('PICKLING DATAHANDLER to datahandler.pkl')
    bytes = data_handler.save('datahandler.pkl', temporary=True)
    data = dcc.send_bytes(bytes, 'datahandler.pkl')
    return value, data