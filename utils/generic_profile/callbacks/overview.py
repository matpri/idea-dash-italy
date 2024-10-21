import dash
from dash import Output, Input, State, ALL, dcc, MATCH

from utils.generic_profile.visualization_scripts.overview import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'model': MATCH,
            'name': 'overview'
        }, 'figure'),
        Output({
            'type': 'overview-download',
            'index': ALL,
            'model': MATCH,
        }, 'data'),
        Input({
            'type': 'overview-plot-select',
            'index': ALL,
            'model': MATCH,
        }, 'value'),
        Input({
            'type': 'overview-download-button',
            'index': ALL,
            'model': MATCH,
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'model': MATCH,
            'name': 'overview'
        }, 'figure'),
        State({
            'type': 'overview-download',
            'index': ALL,
            'model': MATCH,
        }, 'data'),
        prevent_initial_call=True
    )
    def update_gencap_cost(_p_type, _download, _canvas, _data):
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])
        model = trigger_id['model']
        name = 'Overview'
        print(f'updating {name}, {model} plot')

        if 'generic-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'generic-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(
                data_handler.processed_data[model][name].to_csv, f"{name}.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'generic-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])
        _canvas[idx] = render_plot(_p_type[idx],
                                   data_handler.processed_data[model][name]
                                   )

        return _canvas, [dash.no_update for _ in
                         _data],
