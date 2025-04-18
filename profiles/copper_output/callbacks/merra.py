import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from profiles.copper_output.visualization_scripts.merra import vre_plot
from components import ids


def link(app):
    #print("gen cap link")
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': MATCH,
            'profile': 'COPPER',
            'viz': 'VRE Capacity'
        }, 'figure'),
        Output({
            'type': 'copper_output-vre-download',
            'index': MATCH
        }, 'data'),
        Input({
                           'type': 'copper_output-vre-variable-dropdown',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'copper_output-vre-year-dropdown',
            'index': MATCH
        }, 'value'),
        Input({
            'type': 'copper_output-vre-download-button',
            'index': MATCH
        }, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_plot(variable, year, n_clicks):
        from main import data_handler
        #print("gen cap callback", variable)
        df = data_handler.processed_data['COPPER']['VRE Capacity'].copy()

        ctx = dash.callback_context
        if ctx.triggered:
            prop_id = ctx.triggered[0]['prop_id']
            if 'vre-download-button' in prop_id:
                #print('downloading')
                return dash.no_update, dcc.send_data_frame(df.to_csv, "vre.csv", index=False)
        return vre_plot(df, variable, year), dash.no_update
