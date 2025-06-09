import dash
from dash import Output, Input, State, ALL, dcc

from profiles.labourabm_output.visualization_scripts.total_demand import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'LabourABM',
            'viz': 'Total Demand'
        }, 'figure'),
        Output({
            'type': 'labourabm-total_demand-region-select',
            'index': ALL
        }, 'value'),
        Output({
            'type': 'labourabm-total_demand-region-select',
            'index': ALL
        }, 'data'),
        Output({
            'type': 'labourabm-total_demand-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'labourabm-total_demand-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_demand-occupation-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_demand-region-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'labourabm-total_demand-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'LabourABM',
            'viz': 'Total Demand'
        }, 'figure'),
        State({
            'type': 'labourabm-total_demand-region-select',
            'index': ALL
        }, 'data'),
        State({
            'type': 'labourabm-total_demand-download',
            'index': ALL
        }, 'data'),

        prevent_initial_call=True
    )
    def update_total_demand(_scenarios, _occupations, _region, _download, _canvas, _regions, _data):
        #print('updating total_demand plot')
        from utils.data_state import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'labourabm-total_demand-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'labourabm-total_demand-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['LabourABM']['Total Demand'].to_csv,
                                             "total_demand.csv")
            return _canvas, _region, _regions, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'labourabm-total_demand-plot-select')):
                idx = i
                break

        if 'labourabm-total_demand-scenario-multi-select' in trigger_id['type']:
            data = data_handler.processed_data['LabourABM']['Total Demand']
            _regions[idx] = data[data['scenario'].isin(_scenarios[idx])]['region'].unique().tolist()
            if len(_regions[idx]) == 0:
                _region[idx] = ''
            else:
                _region[idx] = _regions[idx][0]

        _canvas[idx] = render_plot(data_handler.processed_data['LabourABM']['Total Demand'], _scenarios[idx], _occupations[idx], _region[idx])

        return _canvas, _region, _regions, [dash.no_update for _ in _data]
