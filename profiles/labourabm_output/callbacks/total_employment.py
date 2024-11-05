import dash
from dash import Output, Input, State, ALL, dcc

from profiles.labourabm_output.visualization_scripts.total_employment import render_plot


def link(app):
    @app.callback(
        Output({
            'type': 'figure',
            'index': ALL,
            'profile': 'labourabm_output',
            'viz': 'total_employment'
        }, 'figure'),
        Output({
            'type': 'labourabm-total_employment-region-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'labourabm-total_employment-region-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'labourabm-total_employment-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'labourabm-total_employment-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_employment-occupation-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_employment-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_employment-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': 'figure',
            'index': ALL,
            'profile': 'labourabm_output',
            'viz': 'total_employment'
        }, 'figure'),
        State({
            'type': 'labourabm-total_employment-region-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'labourabm-total_employment-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_total_employment(_scenarios, _occupations, _region, _download, _canvas, _regions, _data):
        #print('updating total_employment plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'labourabm-total_employment-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'labourabm-total_employment-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['LabourABM']['Total Employment'].to_csv,
                                             "total_employment.csv")
            return _canvas, _region, _regions, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'labourabm-total_employment-plot-select')):
                idx = i
                break

        if 'labourabm-total_employment-scenario-multi-select' in trigger_id['type']:
            data = data_handler.processed_data['LabourABM']['Total Employment']
            _regions[idx] = data[data['scenario'].isin(_scenarios[idx])]['region'].unique().tolist()
            if len(_regions[idx]) == 0:
                _region[idx] = ''
            else:
                _region[idx] = _regions[idx][0]

        _canvas[idx] = render_plot(data_handler.processed_data['LabourABM']['Total Employment'], _scenarios[idx], _occupations[idx], _region[idx])

        return _canvas, _region, _regions, [dash.no_update for _ in _data]
