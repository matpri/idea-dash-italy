import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.comparison import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'comparison'
        }, 'figure'),

        Output({
            'type': 'energy_model-comparison-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-comparison-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-comparison-scenario_a-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-comparison-scenario_b-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-comparison-aggregate-switch',
            'index': ALL
        }, 'checked'),
        Input({
            'type': 'energy_model-comparison-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-comparison-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'comparison'
        }, 'figure'),

        State({
            'type': 'energy_model-comparison-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_comparison(_p_type, _scenario_a, _scenario_b, _aggregate, _region, _download, _canvas, _data):
        #print('updating comparison plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-comparison-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-comparison-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Comparison Matrix'].to_csv,
                                             "comparison.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-comparison-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['Power System Models']['Comparison Matrix'],
                                      _scenario_a[idx], _scenario_b[idx], _aggregate[idx], _region[idx])

        return _canvas, [dash.no_update for _ in _data]
