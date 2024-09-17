import dash
from dash import Output, Input, State, ALL, dcc

from profiles.energy_model.visualization_scripts.heatmap import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'heatmap'
        }, 'figure'),

        Output({
            'type': 'energy_model-heatmap-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'energy_model-heatmap-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-heatmap-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-heatmap-year-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'energy_model-heatmap-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'energy_model',
            'viz': 'heatmap'
        }, 'figure'),

        State({
            'type': 'energy_model-heatmap-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_heatmap(_p_type, _scenarios, _year, _download, _canvas, _data):
        #print('updating heatmap plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'energy_model-heatmap-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'energy_model-heatmap-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['Power System Models']['Heatmap'].to_csv,
                                             "heatmap.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'energy_model-heatmap-plot-select')):
                idx = i
                break

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['Power System Models']['Heatmap'],
                                   _scenarios[idx], _year[idx])

        return _canvas, [dash.no_update for _ in _data]
