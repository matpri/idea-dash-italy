import dash
from dash import Output, Input, State, ALL, MATCH, dcc

from profiles.coders_input.visualization_scripts.demand import render_plot

from components import ids

def link(app):
    #print('linking demand')

    @app.callback(
        Output({
            'type': 'coders_input-demand-download',
            'index': MATCH
        }, 'data'),
        Input({
            'type': 'coders_input-demand-download-button',
            'index': MATCH
        }, 'n_clicks'),
        prevent_initial_call=True
    )
    def download_data(n_clicks):
        from main import data_handler
        df = data_handler.processed_data['CODERS Input']['Demand']
        return dcc.send_data_frame(df.to_csv, "demand.csv", index=False)
