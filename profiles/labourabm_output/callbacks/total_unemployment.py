import dash
from dash import Output, Input, State, ALL, dcc

from profiles.labourabm_output.visualization_scripts.total_unemployment import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'labourabm_output',
            'viz': 'total_unemployment'
        }, 'figure'),

        Output({
            'type': 'labourabm-total_unemployment-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'labourabm-total_unemployment-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_unemployment-occupation-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_unemployment-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'labourabm_output',
            'viz': 'total_unemployment'
        }, 'figure'),

        State({
            'type': 'labourabm-total_unemployment-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_total_unemployment(_scenarios, _occupations, _download, _canvas, _data):
        #print('updating total_unemployment plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'labourabm-total_unemployment-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'labourabm-total_unemployment-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['LabourABM Output']['Total Unemployment'].to_csv,
                                             "total_unemployment.csv")
            return _canvas, _data,

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'labourabm-total_unemployment-plot-select')):
                idx = i
                break



        _canvas[idx] = render_plot(data_handler.processed_data['LabourABM Output']['Total Unemployment'], _scenarios[idx], _occupations[idx])

        return _canvas, [dash.no_update for _ in _data]
