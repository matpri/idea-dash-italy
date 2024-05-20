import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from profiles.coders_input.visualization_scripts.generation_capacity import render_plot


def link(app):
    print("gen cap link")
    @app.callback(
        Output({
            'type': 'figure',
            'index': MATCH,
            'profile': 'coders_input',
            'viz': 'gencap'
        }, 'figure'),
        Output({
            'type': 'coders_input-gencap-download',
            'index': MATCH
        }, 'data'),
        Input({
                           'type': 'coders_input-gencap-aggregate-switch',
            'index': MATCH
        }, 'checked'),
        Input({
            'type': 'coders_input-gencap-download-button',
            'index': MATCH
        }, 'n_clicks'),
        prevent_initial_call=True
    )
    def update_plot(aggregate, n_clicks):
        from main import data_handler
        print("gen cap callback", aggregate)
        df = data_handler.processed_data['CODERS Input']['Capacity'].copy()

        ctx = dash.callback_context
        if ctx.triggered:
            prop_id = ctx.triggered[0]['prop_id']
            if 'demand-download-button' in prop_id:
                print('downloading')
                return dash.no_update, dcc.send_data_frame(df.to_csv, "capacity.csv", index=False)
        return render_plot(df, aggregate), dash.no_update
