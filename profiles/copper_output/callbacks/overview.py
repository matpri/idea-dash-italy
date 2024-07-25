import dash
from dash import Output, Input, State, ALL, dcc

from profiles.copper_output.visualization_scripts.overview import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'overview'
        }, 'figure'),

        Output({
            'type': 'copper-overview-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'copper-overview-plot-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'copper-overview-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'copper_output',
            'viz': 'overview'
        }, 'figure'),

        State({
            'type': 'copper-overview-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_overview(_p_type, _download, _canvas, _data):
        #print('updating overview plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'copper-overview-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'copper-overview-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['COPPER Output']['Overview'].to_csv,
                                             "overview.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'copper-overview-plot-select')):
                idx = i
                break

        #print('idx:', idx, 'plot type:', _p_type[idx])

        _canvas[idx] = render_plot(_p_type[idx], data_handler.processed_data['COPPER Output']['Overview'])

        return _canvas, [dash.no_update for _ in _data]
