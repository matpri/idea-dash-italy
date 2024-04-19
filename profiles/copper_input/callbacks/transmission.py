import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_input.visualization_scripts.transmission import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'transmission'
        }, 'figure'),

        Output({
            'type': 'copper_input-transmission-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'copper_input-transmission-plot-select',
            'index': ALL
        }, 'value'),

        Input({
            'type': 'copper_input-transmission-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-transmission-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper_input-transmission-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_input',
            'viz': 'transmission'}, 'figure'),
        State({
            'type': 'copper_input-transmission-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_transmission(_p_type, _scenarios, _years, _download,
                            _canvas, _data):
        print('updating transmission plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'copper_input-transmission-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper_input-transmission-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER Output']['Capacity'].to_csv,
                                             "transmission.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper_input-transmission-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['COPPER Input']['Transmission'],
                                   _years[idx], _scenarios[idx])
        return _canvas, [dash.no_update for _ in _data]
