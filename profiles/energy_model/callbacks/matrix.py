import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.matrix import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Comparison Matrix'
        }, 'figure'),

        Output({
            'type': 'energy_model-matrix-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-matrix-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-matrix-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-matrix-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-matrix-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-matrix-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'Power System Models',
            'viz': 'Comparison Matrix'
        }, 'figure'),

        State({
            'type': 'energy_model-matrix-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_matrix(_p_type, _scenarios, _aggregate, _region, _download, _canvas, _data):
        #print('updating matrix plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-matrix-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-matrix-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Comparison Matrix'].to_csv,
                                             "matrix.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-matrix-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['Power System Models']['Comparison Matrix'],
                                   _scenarios[idx], _aggregate[idx], _region[idx])

        return _canvas, [dash.no_update for _ in _data]
