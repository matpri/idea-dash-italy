import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.inputs import render_plot
from components import ids


def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'inputs'
        }, 'figure'),

        Output({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'copper-inputs-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-inputs-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'inputs'
        }, 'figure'),

        State({
            'type': 'copper-inputs-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_inputs(_p_type, _download, _canvas, _data):
        #print('updating inputs plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'copper-inputs-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-inputs-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER']['Inputs'].to_csv,
                                             "inputs.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-inputs-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['COPPER']['Inputs'])

        return _canvas, [dash.no_update for _ in _data]
