import dash
from dash import Output, Input, State, ALL, dcc

from profiles.silver_output.visualization_scripts.map_plots import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'map_plots'
        }, 'figure'),
        Output({
            'type': 'silver-map_plots-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'silver-map_plots-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-scenario-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-time_step-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-map_plots-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'map_plots'
        }, 'figure'),
        State({
            'type': 'silver-map_plots-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_map_plots(_p_type, _scenario, _ts,  _download, _canvas, _data):
        print('updating map_plots plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'silver-map_plots-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-map_plots-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['SILVER Output']['Map Plots'].to_csv, "map_plots.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'silver-map_plots-plot-select')):
                idx = i
                break

        print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['SILVER Output']['Map Plots'], _scenario[idx], time_size=_ts[idx])

        return _canvas, [dash.no_update for _ in _data]
