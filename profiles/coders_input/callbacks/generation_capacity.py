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
        Input({
                           'type': 'coders_input-gencap-aggregate-switch',
            'index': MATCH
        }, 'checked')
    )
    def update_plot(aggregate):
        from main import data_handler
        print("gen cap callback", aggregate)
        df = data_handler.processed_data['CODERS Input']['Capacity'].copy()

        return render_plot(df, aggregate)
