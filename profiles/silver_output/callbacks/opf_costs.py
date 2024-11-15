import dash
from dash import Output, Input, State, ALL, dcc

from profiles.silver_output.visualization_scripts.opf_costs import render_plot

from components import ids
def link(app):
    @app.callback(
        Output({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'opf_costs'
        }, 'figure'),
        Output({
            'type': 'silver-opf_costs-download',
            'index': ALL
        }, 'data'),
        Input({
            'type': 'silver-opf_costs-scenario-multi-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-opf_costs-time_step-select',
            'index': ALL
        }, 'value'),
        Input({
            'type': 'silver-opf_costs-download-button',
            'index': ALL
        }, 'n_clicks'),
        State({
            'type': ids.FIGURE,
            'index': ALL,
            'profile': 'silver_output',
            'viz': 'opf_costs'
        }, 'figure'),
        State({
            'type': 'silver-opf_costs-download',
            'index': ALL
        }, 'data'),
        prevent_initial_call=True
    )
    def update_opf_costs(_scenarios,_tstep, _download, _canvas, _data):
        print('updating opf_costs plot')
        from main import data_handler
        ctx = dash.callback_context
        trigger_id = eval(ctx.triggered[0]['prop_id'].split('.')[0])

        if 'silver-opf_costs-download-button' in trigger_id['type']:
            idx = 0
            for i, id in enumerate(ctx.inputs_list[0]):
                if ((id['id']['index'] == trigger_id['index']) and
                        (id['id']['type'] == 'silver-opf_costs-download-button')):
                    idx = i
                    break
            _data[idx] = dcc.send_data_frame(data_handler.processed_data['SILVER']['OPF Costs'].to_csv, "opf_costs.csv")
            return _canvas, _data

        idx = 0
        for i, id in enumerate(ctx.inputs_list[0]):
            if ((id['id']['index'] == trigger_id['index']) and
                    (id['id']['type'] == 'silver-opf_costs-plot-select')):
                idx = i
                break

        _canvas[idx] = render_plot(data_handler.processed_data['SILVER']['OPF Costs'],
                                   _scenarios[idx], time_size=_tstep[idx])


        return _canvas, [dash.no_update for _ in _data]
